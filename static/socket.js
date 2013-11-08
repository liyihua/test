$(document).ready(function() {

	$("#connect").click(function() {
		connect();
	});

	function connect() {
		//var host="ws://localhost:801"
		var ws = new WebSocket("ws://ddmg1.csail.mit.edu:8000/websocket");
		ws.onopen = function() {

			ws.send('1377195857.18');
			//alert("send message");
		};

		ws.onmessage = function(msg) {
			//var dataFromServer = JSON.parse(msg.data);
			//alert("receive an message" + msg.data);
			addData(msg.data.split(","));
		};

		ws.onclose = function() {
			alert("socket closed");
			//message('<p class="event">Socket Status: ' + socket.readyState + ' (Closed)');
		}
	}

});
