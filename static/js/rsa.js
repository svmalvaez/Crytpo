var socket = io('http://localhost:3000/');
var passphrase = $("#passphrase").val()
var userRSAKey = cryptico.generateRSAKey(passphrase,1024);

$("#send").on("click", function(){
	var userPublicKey = cryptico.publicKeyString(userRSAKey);
	var user = {
		"username": $("#username").val(),
		"pub_key": userPublicKey,
	}
	$("#username, #passphrase").val('');
	console.log(user);
	socket.emit("new_user", user);
});

socket.on("connected_users", function(data){
	$("a").detach();
	$.each(data, function(u, users){
		$(".list-group").append("<a data-toggle=\"modal\" data-target=\"#conversation\" data-pub_key = \""+ 
			users.pub_key +"\" class=\"list-group-item\" id=\""+ u +"\">" + users.username + "</a>");
	});
});


$('#conversation').on('show.bs.modal', function(e) {

    //get data-pubkey attribute of the clicked element
    pub_key = $(e.relatedTarget).data('pub_key');
    $("#message").data("key",pub_key);
});

$("#send_message").on("click", function(){
	var RSAKey = cryptico.generateRSAKey("Prueba",1024)
	message = $("#message").data("key");
	message_result = cryptico.encrypt(message,pub_key, RSAKey);
	socket.emit("cypher_message", message_result);
});

socket.on("message", function(data){
	console.log(userRSAKey);
	var decrypt= cryptico.decrypt(data.cipher,userRSAKey);
	console.log(decrypt);
});