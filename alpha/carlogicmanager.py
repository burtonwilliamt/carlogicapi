from twisted.internet import reactor, protocol


class Manager(protocol.Protocol):

    def connectionMade(self):
        print("Connected to client!")

    def dataReceived(self, data):
        print("Received: {}".format(data))
        #self.transport.write(data)


def main():
    factory = protocol.ServerFactory()
    factory.protocol = Manager
    reactor.listenTCP(9998,factory)
    reactor.run()

if __name__ == '__main__':
    main()
