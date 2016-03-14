from flask import Flask
from flask import render_template
import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process


app = Flask(__name__)

@app.route("/")
@app.route('/<name>')
def hello(name=None):
    context = zmq.Context()
    socket_sub1 = context.socket(zmq.SUB)
    socket_sub2 = context.socket(zmq.SUB)

    socket_sub1.connect("tcp://localhost:%s" % 5566)
    socket_sub2.connect("tcp://localhost:%s" % 5567)

    socket_sub1.setsockopt(zmq.SUBSCRIBE, "")
    socket_sub2.setsockopt(zmq.SUBSCRIBE, "")


    while True:
        json_data1 = socket_sub1.recv_json()
        json_data2 = socket_sub2.recv_json()
#    print('{0}'.format(json_data1))
#    print('{0}'.format(json_data2))

        return render_template('hello.html', json=json_data1)
#        return '{0}\n {1}\n'.format(json_data1, json_data2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
