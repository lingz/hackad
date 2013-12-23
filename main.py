import os.path
from live_stylus import ConvStylus

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [(r'/', IndexHandler), (r'/hack72', Hack72Handler), 
        (r'/nyuad_hackathon_results', NYUADHackathonResultsHandler),
        (r'/nyuad_hackathon', NYUADHackathonHandler)]
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    static_path = os.path.join(os.path.dirname(__file__), "static")
    conn = pymongo.Connection("localhost", 27017)
    self.db = conn["hackad"]
    tornado.web.Application.__init__(self, handlers, template_path=template_path, static_path=static_path, debug=True)

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")
  def post(self):
    name = self.get_argument("name")
    net_id = self.get_argument("net_id")
    coll = self.application.db.members
    sign_up_doc = coll.find_one({"net_id":net_id})
    if sign_up_doc:
      self.write({"status":418,"reason":"NetID already recorded"})
      return
    sign_up_doc = {"name": name, "net_id": net_id}
    coll.insert(sign_up_doc)
    self.write({"status":200})


class Hack72Handler(tornado.web.RequestHandler):
  def get(self):
    # coll = self.application.db.members
    # sign_up_doc = coll.find_one({"net_id":net_id})
    members = self.application.db.members
    forms = self.application.db.forms
    hack72 = forms.find_one({"name": "hack72_2013f"})
    if not hack72:
      names = []
    else:
      net_ids = hack72["data"]
      names = map(lambda member: member["name"], members.find({"net_id": {"$in": net_ids}}))

    self.render("hack72.html", names=names)

  def post(self):
    members = self.application.db.members
    forms = self.application.db.forms
    net_id = self.get_argument("net_id")
    sign_up_doc = members.find_one({"net_id":net_id})
    hack72 = forms.find_one({"name": "hack72_2013f"})

    if not sign_up_doc:
      self.write({"status":401, "reason":"NetID %s not registered as a member" % net_id})
      return
    if not hack72:
      forms.insert({"name": "hack72_2013f", "data": [net_id]})
    elif net_id in hack72["data"]:
      self.write({"status":418, "reason":"NetID %s already registered" % net_id})
      return
    forms.update({"_id": hack72["_id"]},{"$addToSet":{"data":net_id}})
    self.write({"status": 200, "name": sign_up_doc["name"]})
  
  def initialize(self):
    pass

class NYUADHackathonHandler(tornado.web.RequestHandler):
  def get(self):
    # coll = self.application.db.members
    # sign_up_doc = coll.find_one({"net_id":net_id})
    members = self.application.db.members
    forms = self.application.db.forms
    hackathon = forms.find_one({"name": "nyuad_hackathon_2014s"})
    if not hackathon:
      names = []
    else:
      net_ids = map(lambda datum: datum["net_id"], hackathon["data"])
      names = map(lambda member: member["name"], members.find({"net_id": {"$in": net_ids}}))

    self.render("hackathon.html", names=names)

  def post(self):
    members = self.application.db.members
    forms = self.application.db.forms
    net_id = self.get_argument("net_id")
    major = self.get_argument("major")
    year = self.get_argument("year")
    sign_up_doc = members.find_one({"net_id":net_id})
    hackathon = forms.find_one({"name": "nyuad_hackathon_2014s"})
    datum = {
      "net_id": net_id,
      "major": major,
      "year": year
    }
    if not sign_up_doc:
      self.write({"status":401, "reason":"NetID %s not registered as a member" % net_id})
      return
    if not hackathon:
      forms.insert({"name": "nyuad_hackathon_2014s", "data": [datum]})
      hackathon = forms.find_one({"name": "nyuad_hackathon_2014s"})
    elif net_id in map(lambda datum: datum["net_id"], hackathon["data"]):
      self.write({"status":418, "reason":"NetID %s already registered" % net_id})
      return
    forms.update({"_id": hackathon["_id"]},{"$addToSet":{"data":datum}})
    self.write({"status": 200, "name": sign_up_doc["name"]})

  def initialize(self):
    pass

class NYUADHackathonResultsHandler(tornado.web.RequestHandler):
  def get(self):
    # coll = self.application.db.members
    # sign_up_doc = coll.find_one({"net_id":net_id})
    members = self.application.db.members
    forms = self.application.db.forms
    hackathon = forms.find_one({"name": "nyuad_hackathon_2014s"})
    if not hackathon:
      names = []
    else:
      for entry in hackathon["data"]:
        entry["name"] = members.find_one({"net_id": entry["net_id"]})["name"]
    print hackathon["data"][0]["name"]

    self.render("hackathon_results.html", hackers=hackathon["data"])

if __name__ == '__main__':
  ConvStylus(os.path.join(os.path.dirname(__file__), "static/css/"))
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
