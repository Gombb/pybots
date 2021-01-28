
let chart = {
	dataCache: [],
    init: function(){

        chart.apiGet("/get-historical/"+"5m/", (response) => {
            chart.preFill(response);
        })
    },
    preFill(data) {
      chart.dataCache = data;
      candleSeries.setData(data);
    },
	plotOHLC: function (data) {
		let ohlcTable = document.querySelector("#ohlcTable");
		let dataHTML = `<tbody>
						<tr>
							<td>${data.open}</td>
							<td>${data.high}</td>
							<td>${data.low}</td>
							<td>${data.close}</td>
						</tr>
					</tbody>`;
		if (ohlcTable.children.length !== 1) ohlcTable.children[1].remove();
		ohlcTable.firstElementChild.insertAdjacentHTML("afterend", dataHTML);
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
	width: 700,
  	height: 350,
	layout: {
		backgroundColor: 'white',
		textColor: 'rgba(0, 0, 0, 0.75)',
		font_family: 'Calibri',
	},
	grid: {
		vertLines: {
            color: 'rgba(0, 0, 0, 0.5)',
            style: 1,
            visible: false,
        },
        horzLines: {
            color: 'rgba(0, 0, 0, 0.5)',
            style: 1,
            visible: false,
        },
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	priceScale: {
		borderColor: 'rgba(0, 0, 0, 0.5)',
	},
	timeScale: {
		borderColor: 'rgba(0, 0, 0, 0.5)',
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
chartLight.subscribeCrosshairMove(param => {
	if (param.time) {
		chart.plotOHLC(param.seriesPrices.get(candleSeries))
	}
  })

let binanceSocket = new WebSocket("wss://fstream.binance.com/ws/linkusdt@kline_5m");

binanceSocket.onmessage = function (event) {
	let message = JSON.parse(event.data);

	let candlestick = message.k;


	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}
