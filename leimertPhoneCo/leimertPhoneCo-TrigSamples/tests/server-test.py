def handler(addr, tags, stuff, source):
    print("Received message on address:", addr)
    print("Tags:", tags)
    print("Data:", stuff)
    print("Source:", source)

# Create an OSC server
server = pyOSC3.OSCServer(('127.0.0.1', 58110))  # Listen on the specified IP and port

# Register a handler for the desired address
server.addMsgHandler("/nowPlaying", handler)

# Start the server
server.serve_forever()

print("running")