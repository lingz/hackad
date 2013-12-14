$(function() {
	$(document).on("submit", "form", function(e) {
		e.preventDefault();
		var netId = $("#net_id").val();
		var formHtml = $("form").html();
		$.post(window.location.href, {net_id: netId}, function(data){
			if (data.status == 200) {
				$("form").html("<br /> <h2>See you there <span class='text-red'> "+ data.name + "</span>.</h2>");
				$("ul").append("<li>" + data.name + "</li>");
			}
			else if (data.status == 401) {
				$("form").html(formHtml + "<br /><h2>NetID <span class='text-red'> "+ netId + "</span> has not" +
					" been <a href='" + window.location.origin + "'> registered </a> as a member.</h2><br/>");
			}
			else {
				$("form").html(formHtml + "<br /><h2>NetID <span class='text-red'> "+ netId + "</span> already registered.</h2><br />");

			}
		});
		$("form").html("<br /><img src='/static/images/loader.gif'/><h3 class='text-center'>Talking to server...</h5>");
	}
	);

});
