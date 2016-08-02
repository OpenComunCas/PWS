import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    Se trata de un server TCP básico para recoger los datos enviados desde Arduino. 
    Hay que configurar el ESP para que acceda a la IP correcta
    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data

if __name__ == "__main__":
    HOST, PORT = "192.168.1.31", 5000

    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

