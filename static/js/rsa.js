
var socket = io('http://localhost:3000/');

// $("#form_user").submit(function(){

// 	var user = {
// 		"username": this.username,
// 		"priv_key": this.priv_key,
// 		"pub_key": this.pub_key,
// 	}
// 	console.log(user);
// 	socket.emit("new_user", user);

// });

$("#send").on("click", function(){
		var user = {
		"username": "this.username",
		"priv_key": "this.priv_key",
		"pub_key": "this.pub_key",
	}
	console.log(user);
	// socket.emit("new_user", user);
});