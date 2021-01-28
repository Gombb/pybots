from flask import Flask, render_template, request, redirect, session, jsonify
from flask_bcrypt import Bcrypt
import queries
import data_manager
import req_historical
import req_user_data
import bot
import os
import time
from datetime import datetime
app = Flask(__name__, template_folder="templates")
bcrypt = Bcrypt(app)
app.secret_key = b'\xe3\r\x8b<\xa1\xc4L2S\x9c\xc4\xbew\x03N\xf0'


@app.template_filter('datetime')
def datetime_from_timestamp(ts):
    ts /= 1000
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/chart")
def chart_page():
    return render_template("chart.html")


@app.route("/cache/<ele>/<side>/")
def get_cache_strat(ele, side):
    if ele == "strat":
        if side == "bull":
            result = data_manager.read_csv(data_manager.STRAT_BULL_PATH)
        if side == "bear":
            result = data_manager.read_csv(data_manager.STRAT_BEAR_PATH)
    return jsonify(result)


@app.route("/trade-history")
def trade_history():
    symbol_history = req_user_data.request_trading_stats("LINKUSDT")
    return render_template("history.html", historical_data=symbol_history)


@app.route("/get-historical/<timeframe>/")
def get_historical(timeframe):
    current_time = int(time.time() * 1000)
    unix_9days = 691200000
    if timeframe == "5m":
        time_int = unix_9days / 9
    else:
        time_int = unix_9days
    result = req_historical.get_historical_data(current_time - time_int, current_time, timeframe)
    json_like = []
    for ele in result:
        dict_temp = {"open": ele.open, "high": ele.high, "low": ele.low, "close": ele.close, "time": ele.openTime / 1000}
        json_like.append(dict_temp)
    return jsonify(json_like)


@app.route("/bot-control/<status>/")
def bot_control(status):
    if status == "on":
        bot.init()
    if status == "off":
        bot.shutdown()
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    password_input = request.form.get("inputPassword")
    if bcrypt.check_password_hash(queries.get_password_hash(), password_input):
        session["status"] = "logged in"
    return redirect("/")


if __name__ == '__main__':
    app.run()
