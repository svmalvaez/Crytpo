var socket = io('http://localhost:3000/');
var id = 1;

$("#send").on("click", function(){
		var user = {
			"id": id,
		"username": $("#username").val(),
		"priv_key": $("#priv_key").val(),
		"pub_key": $("#pub_key").val(),
	}
	$("#username, #priv_key, #pub_key").val('');
	console.log(user);
	socket.emit("new_user", user);
	id ++;
});

socket.on("connected_users", function(data){
	$("a").detach();
	$.each(data, function(u, users){
		$(".list-group").append("<a data-toggle=\"modal\" data-target=\"#conversation\" class=\"list-group-item\" id=\""+ u +"\">" + users.username + "</a>");
	});
});


$("#send_message").on("click", function(){
	message = $("#message").val();


});