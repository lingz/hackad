$(function() {
	$("form").on("submit", function(e) {
		e.preventDefault();
		name = $("#name").val();
		net_id = $("#netid").val();
		$.post(window.location.href, {name: name, net_id: net_id}, function(data){
			if (data.status == 200) {
				$("form").html("<br /> <h2>Welcome to the revolution <span class='text-red'> "+ name + "</span>.</h2>");
			}
			else {
				$("form").html("<br /><h2>NetID <span class='text-red'> "+ net_id + "</span> already registered.</h2>");

			}
		});
		$("form").html("<br /><img src='/static/images/loader.gif'/><h3 class='text-center'>Talking to server...</h5>")
	}
	);

});

