$(document).ready(function() {
	var options = {
		xaxis : {
			mode : "time",
			timeformat : "%y/%m/%d",
			minTickSize : [1, "day"]

		}
	};

	var options2 = {
		xaxis : {
			mode : "time",
			timeformat : "%m/%d, %H:%M:%S",
		},
		yaxis : {
			position : "right",
			alignTicksWithAxis : true
		}
	};

	var d1 = [];
	var d3 = [];

	var plot = $.plot("#data_container", [{
		data : d1,
		points : {
			show : true
		},
		lines : {
			show : true
		},
		label : "temperatur data for wheelchair1"
	}], options2);

	var hum_plot = $.plot("#hum_container", [{
		data : d3,
		points : {
			show : true
		},
		lines : {
			show : true
		},
		color:3,
		label : "humidity data for wheelchair1"
	}], options2);

	//alert("here");
	var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text("Temperature (°C)").appendTo($('#data_container'));
	var yaxisLabel2 = $("<div class='axisLabel yaxisLabel'></div>").text("Humidity").appendTo($('#hum_container'));
	var yaxisLabel3 = $("<div class='axisLabel yaxisLeftLabel'></div>").text("(Hour)").appendTo($('#placeholder'));
	var totalPoints = 20;

	function getTemSeriesObj() {
		return [{
			data : d1,
			points : {
				show : true
			},
			lines : {
				show : true
			},
			label : "temperatur data for wheelchair1"
		}];
	}

	function getHumSeriesObj() {
		return [{
			data : d3,
			points : {
				show : true
			},
			color:3,
			lines : {
				show : true
			},
			label : "humidity data for wheelchair1"
		}];
	}

	//newData is array. first one[time,newTem]
	var timezone_diff=18000000;
	function addData(newData) {

		if (d1.length > totalPoints) {
			d1 = d1.slice(1);
		}
		if (d3.length > totalPoints) {
			d3 = d3.slice(1);
		}
		d1.push([parseFloat(newData[0]) * 1000-timezone_diff, parseFloat(newData[1])]);
		d3.push([parseFloat(newData[0]) * 1000-timezone_diff, parseFloat(newData[2])]);
		if (d1.length>=3){
		plot.setData(getTemSeriesObj());
		hum_plot.setData(getHumSeriesObj());
		//alert("here");
		plot.setupGrid();
		hum_plot.setupGrid();
		plot.draw();
		hum_plot.draw();
}
	}

	//bar with is 1/4 a day since showing only three
	var BAR_WIDTH = 6 * 60 * 60 * 1000;
	var DATE1 = convertDate(2013, 8, 23);

	var DATE2 = convertDate(2013, 8, 24);
	var DATE3 = convertDate(2013, 8, 25);
	var DATE4 = convertDate(2013, 8, 26);
	var DATE5 = convertDate(2013, 8, 27);
	//var DATE6=convertDate(2013,8,28);

	var d2 = [[DATE1, 1.1], [DATE3, 0.72], [DATE4, 0.6666], [DATE5, 0.72]];

	var d4 = [];
	for (var i = 0; i < 14; i += 0.1) {
		d4.push([i * 100000, Math.sqrt(i * 10)]);
	}
	var d6 = [[DATE1 + BAR_WIDTH, 0.283], [DATE2 + BAR_WIDTH, 0.3333], [DATE4 + BAR_WIDTH, 0.83333], [DATE5 + BAR_WIDTH, 0.2]];

	$.plot("#placeholder", [{
		data : d2,
		bars : {
			show : true,
			barWidth : BAR_WIDTH
		},
		label : "wheelchair1"
	}, {
		data : d6,
		bars : {
			show : true,
			barWidth : BAR_WIDTH
		},
		label : "wheelchair2"
	}], options);

	function convertDate(year, month, day) {

		var d = new Date(year, month, day);
		var zone = d.getTimezoneOffset();
		d.setFullYear(year, month, day);
		return d.getTime() - zone * 100000;
	};

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
