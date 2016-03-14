import zmq
context = zmq.Context()
print("Connecting to hello world server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
for request in range(1):
    print("Sending request %s" % request)
    socket.send("1 led 1 1")
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))
