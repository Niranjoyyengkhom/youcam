import os
import time
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def start_stream(stream_key):
    # Start the video stream with the given stream key
    command = "raspivid -o - -t 0 -n -w 720 -h 480 -fps 25 -b 2000000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/" + stream_key
    video_stream = os.popen(command)
    print("Stream started successfully.")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/start_stream', methods=['POST'])
def start():
    stream_key = request.form['stream_key']
    start_stream(stream_key)
    return jsonify({'message': 'Stream started successfully.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
