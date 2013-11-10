$(document).ready(function() {
	//alert("here");
	var options = {
		xaxis : {
			mode : "time",
			timeformat : "%y/%m/%d",
			minTickSize : [1, "day"]

		}
		
	};
	var heatIndexOption = {
		xaxis : {
			mode : "time",
			timeformat : "%m/%d,%H:%M",
			minTickSize : [5, "minute"]
		},
		yaxis : {
			autoscaleMargin : 0.2,
			tickDecimals : 1
		},
		grid:{
			markings: [ { yaxis: { from: 91, to: 91 } ,color:"rgb(255,225,0)"},{ yaxis: { from:80, to: 80 } ,color:"rgb(188,239,79)"}]
		}
	};
	var options2 = {
		xaxes : [{
			mode : "time",
			timeformat : "%m/%d,%H:%M",
			tickSize : [1, "minute"]
		}],
		yaxes : [{
			tickDecimals : 1,
			autoscaleMargin : 0.15
		}, {
			position : "right",
			alignTicksWithAxis : true,
			tickDecimals : 1,
			autoscaleMargin : 0.15
		}]
	};

	var d1 = [];
	var d3 = [];
	var heatIndexData = [];

	var plot = $.plot("#data_container", [{
		data : d1,
		points : {
			show : true
		},
		lines : {
			show : true
		},
		label : "temperatur data for wheelchair1"
	}, {
		data : d3,
		yaxis : 2,
		points : {
			show : true
		},
		lines : {
			show : true
		},
		label : "humidity data for wheelchair1"
	}], options2);
    var empty=[];
	var heatIndexPlot = $.plot("#heatIndex_container", [{
		data : heatIndexData,
		color : "rgb(255,137,0)",
			threshold : [{
				below : 91,
				color : "rgb(255,225,0)"
			}, {
				below : 80,
				color : "rgb(188,239,79)"
			}],
		lines : {
			show : true
		},
		label : "Extreme Caution"
	},{label:"Caution",color:"rgb(255,225,0)",data:empty},{label:"Normal",color:"rgb(188,239,79)",data:empty}], heatIndexOption);
	//alert("here");
	var yaxisLabel = $("<div class='axisLabel yaxisLeftLabel'></div>").text("Temperature (F)").appendTo($('#data_container'));
	var yaxisLabel2 = $("<div class='axisLabel yaxisLabel'></div>").text("Humidity").appendTo($('#data_container'));
	var yaxisLabel3 = $("<div class='axisLabel yaxisLeftLabel'></div>").text("(Hour)").appendTo($('#placeholder'));
	var totalPoints = 22;

	function getHeatIndexSeriesObj() {
		return [{
			data : heatIndexData,
			color : "rgb(255,137,0)",
			threshold : [{
				below : 91,
				color : "rgb(255,225,0)"
			}, {
				below : 80,
				color : "rgb(188,239,79)"
			}],
			lines : {
				show : true
			},
			label : "Extreme Caution"
		}, {data:[],label:"Caution",color:"rgb(255,225,0)"},{label:"Normal",color:"rgb(188,239,79)",data:empty}];
	}

	function getSeriesObj() {
		return [{
			data : d1,
			points : {
				show : true
			},
			lines : {
				show : true
			},
			label : "temperatur data for wheelchair1"
		}, {
			data : d3,
			yaxis : 2,
			points : {
				show : true
			},
			lines : {
				show : true
			},
			label : "humidity data for wheelchair1"
		}];
	}

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
			color : 3,
			lines : {
				show : true
			},
			label : "humidity data for wheelchair1"
		}];
	}

   function getDiffInMin(start, end){
   	  return Math.floor((end-start)/60);
   }
   function updateCaption(time, indexValue){
   	  console.log(time);
      var current;
      var rangeList=["Normal (<80)", "Caution (80-91)", "Extreme Caution (91-102)", "Danger (>102)"];
   	   if (indexValue<80){
   	   	   current=0;
   	   }
   	   else if (indexValue<91){
   	   	   current=1;
   	   }
   	   else if (indexValue<102){
   	   	current=2;
   	   }
   	   if (start==null){
   	   	start=time;
   	   	$('#range').html(rangeList[current]);
   	   	$("#duration").html(" 0 ");
   	   }
   	   if (current!=previous){
   	   	   //update range and time
   	   	   $('#range').html(rangeList[current]);
   	   	   $("#duration").html(getDiffInMin(start,time));
   	   	   previous=current;
   	   	   start=time;  	   	   
   	   }
   	   else{
   	   	 $("#duration").html(getDiffInMin(start,time));
   	   }
   }
   var previous=0
   var start=null;
	//newData is array. first one[time,newTem]
	var timezone_diff = 18000000;
	function addData(newData) {

		if (d1.length > totalPoints) {
			d1 = d1.slice(1);
		}
		if (d3.length > totalPoints) {
			d3 = d3.slice(1);
		}
		var temp = toF(parseFloat(newData[1])).toFixed(1);
		var hum = parseFloat(newData[2]).toFixed(1);
        var time=parseFloat(newData[0]);
		d1.push([time * 1000 - timezone_diff, temp]);
		d3.push([time * 1000 - timezone_diff, hum]);
		var index = heatIndex(temp, hum);
		heatIndexData.push([time* 1000 - timezone_diff, index]);
		updateCaption(time,index);
		if (d1.length >= 3) {
			plot.setData(getSeriesObj());
			heatIndexPlot.setData(getHeatIndexSeriesObj());
			//plot.setData(getTemSeriesObj());
			//hum_plot.setData(getHumSeriesObj());
			//alert("here");
			plot.setupGrid();
			heatIndexPlot.setupGrid();
			//hum_plot.setupGrid();
			plot.draw();
			heatIndexPlot.draw();
			//hum_plot.draw();
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

	function toF(c) {
		return c * 9 / 5 + 32;
	};

	function heatIndex(temp, hum) {
		var c1 = -42.379;
		var c2 = 2.04901523;
		var c3 = 10.14333127;
		var c4 = -0.22475541;
		var c5 = -0.00683783;
		var c6 = -0.05481717;
		var c7 = 0.00122874;
		var c8 = 0.00085282;
		var c9 = -0.00000199;
		var T = parseFloat(temp);
		var R = parseFloat(hum);
		var HI = c1 + c2 * T + c3 * R + c4 * T * R + c5 * T * T + c6 * R * R + c7 * T * T * R + c8 * T * R * R + c9 * T * T * R * R;
		return HI;

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
			console.log("socket closed");
			//message('<p class="event">Socket Status: ' + socket.readyState + ' (Closed)');
		}
	}

});
