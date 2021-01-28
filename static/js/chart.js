
let chart = {
    init: function(){

        chart.apiGet("/get-historical/"+"5m/", (response) => {
            chart.preFill(response);
        })
    },
    preFill(data) {
      console.log(data);
      candleSeries.setData(data)
    },
    apiGet: function (url, callback){
        fetch(url, {
            method: "GET",
            credentials: "same-origin"
        })
            .then(response => response.json())
            .then(json_response => callback(json_response));
    }
}


let chartLight = LightweightCharts.createChart(document.getElementById('chartbox'), {
	width: 1500,
  	height: 750,
	layout: {
		backgroundColor: 'white',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	priceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
		secondsVisible: false,
	},
});


let candleSeries = chartLight.addCandlestickSeries({
	upColor: '#00ff00',
	downColor: '#ff0000',
	borderDownColor: 'rgba(255, 144, 0, 1)',
	borderUpColor: 'rgba(255, 144, 0, 1)',
	wickDownColor: 'rgba(255, 144, 0, 1)',
	wickUpColor: 'rgba(255, 144, 0, 1)',
});


chart.init();