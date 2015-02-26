
var socket = io('http://localhost:3000/');

$("#send").on("click", function(){
		var user = {
			"id": 0,
		"username": $("#username").val(),
		"priv_key": $("#priv_key").val(),
		"pub_key": $("#pub_key").val(),
	}
	$("#username, #priv_key, #pub_key").val('');
	console.log(user);
	socket.emit("new_user", user);
});

socket.on("connected_users", function(data){
	$("a").detach();
	$.each(data, function(u, users){
		$(".list-group").append("<a data-toggle=\"modal\" data-target=\"#conversation\" class=\"list-group-item\">" + u.username + "</a>");
	});
});

//"<li class=\"list-group-item\">" + u.username + "</li>"