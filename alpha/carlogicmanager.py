from twisted.internet import reactor, protocol


class Manager(protocol.Protocol):

    def connectionMade(self):
        print("Connected to client!")

    def dataReceived(self, data):
        print("Received: {}".format(data))
        # Echo
        self.transport.write(data)

    def connectionLost(self, reason):
        print("Connection lost for reason: {}".format(reason))

def main():
    factory = protocol.ServerFactory()
    factory.protocol = Manager
    reactor.listenTCP(9998,factory)
    reactor.run()

if __name__ == '__main__':
    main()
