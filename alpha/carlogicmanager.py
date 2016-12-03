from twisted.internet import reactor, protocol



TraCIcommands = {
    'Receive' : 100,
    'Send' : 200,
    'GetSpeed': 301,
    'GetLane': 302
}

buffer_len = 1024

def requestSpeed(self, vehID):
    print("Requesting speed")
    buffer = ""
    buffer += chr(TraCIcommands['GetSpeed'])
    buffer += chr(vehID)
    self.transport.write(int(buffer))

def acceptMessage(self, data):
    command = data[0]
    if(command == TraCIcommands['GetSpeed']):
        speed = data[1]
        print("Our speed is: {}".format(speed))

class Manager(protocol.Protocol):

    def connectionMade(self):
        print("Connected to client!")
        requestSpeed(self, 0)

    def dataReceived(self, data):
        print("Data received")
        acceptMessage(self, data)
        requestSpeed(self, 0)

    def connectionLost(self, reason):
        print("Connection lost for reason: {}".format(reason))

def main():
    factory = protocol.ServerFactory()
    factory.protocol = Manager
    reactor.listenTCP(9998,factory)
    reactor.run()

if __name__ == '__main__':
    main()
