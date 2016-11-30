from jukio import app
from flask import json, request
from subprocess import check_output
import mpdaddsimilar, mpd, os


mpd_status = {
    "autoplay": False,
    "consume": 0,
    "random": 0,
    "single": 0,
    "track": ""
}

def mpd_connect():
    mpc = mpd.MPDClient()
    mpd_host = ""
    mpd_port = 0

    # Guess default values
    try:
        mpd_host = os.environ["MPD_HOST"]
    except KeyError:
        mpd_host = "localhost"

    try:
        mpd_port = int(os.environ["MPD_PORT"])
    except KeyError:
        mpd_portT = 6600

    mpc.connect(mpd_host, mpd_port)

    return mpc

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/status')
def status():
    mpc = mpd_connect()
    status = mpc.status()
    now_playing = mpc.playlistinfo(status["song"])
    mpc.close()
    mpc.disconnect()

    mpd_status = status + now_playing

    out = check_output(["autoplay.py", "radio"])
    mpd_status["autoplay"] = True if out.strip() == "Radio Mode : Enabled" else False

    out = check_output(["autoplay.py", "trigger"])
    mpd_status["quantity"] = out.split(" : ")[1]

    return json.jsonify(mpd_status)

@app.route('/controls', methods=['POST'])
def controls():
    req = request.get_json()

    print(req)

    if req.get("consume") is not None:
        mpc = mpd_connect()
        mpc.consume(req["consume"])
        mpd_status["consume"] = mpc.status()["consume"]
        mpc.close()
        mpc.disconnect()

    if req.get("random") is not None:
        mpc = mpd_connect()
        mpc.random(req["random"])
        mpd_status["random"] = mpc.status()["random"]
        mpc.close()
        mpc.disconnect()
        mpd_status["random"] = req["random"]

    if req.get("repeat") is not None:
        mpc = mpd_connect()
        mpc.repeat(req["repeat"])
        mpd_status["repeat"] = mpc.status()["repeat"]
        mpc.close()
        mpc.disconnect()
        mpd_status["repeat"] = req["repeat"]

    if req.get("single") is not None:
        mpc = mpd_connect()
        mpc.single(req["single"])
        mpd_status["single"] = mpc.status()["single"]
        mpc.close()
        mpc.disconnect()
        mpd_status["single"] = req["single"]

    print(mpd_status)

    return json.jsonify(mpd_status)

@app.route('/autoplay', methods=['POST'])
def playmore():
    if req.get("autoplay") is not None:
        exe = ["autoplay.py", "radio"]
        exe.append("on" if req["autoplay"] else "off")
        out = check_output(exe)
        if out.strip() == "Radio Mode : Enabled":
            mpd_status["autoplay"] = True
        elif out.strip() == "Radio Mode : Disabled":
            mpd_status["autoplay"] = False

    if req.get("quantity") is not None:
        exe = ["autoplay.py", "trigger", req["quantity"]]
        out = check_output(exe)
        how_many = out.split(" : ")[1]
        mpd_status["quantity"] = how_many

    return json.jsonify({"status": True})

@app.route('/playmore', methods=['POST'])
def playmore():
    req = request.get_json()
    if req.get("quantity") is not None:
        mpdaddsimilar.mpd_connect()
        added = mpdaddsimilar.add_similar_tracks("c", req["quantity"], True)
        return json.jsonify({"added": added})

@app.route('/playtop', methods=['POST'])
def playmore():
    req = request.get_json()
    if req.get("quantity") is not None:
        mpdaddsimilar.mpd_connect()
        added = mpdaddsimilar.add_top_tracks("c", req["quantity"], True)
        return json.jsonify({"added": added})
