from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

host = "127.0.0.1"


def address(port):
    return str("http://" + host + ":" + str(port) + "/")


class Node(Thread):
    def __init__(self, port, registry_port):
        self.port = port
        self.registry_port = registry_port
        self.registry_proxy = xmlrpc.client.ServerProxy(address(registry_port))
        self.id = self.registry_proxy.register(self.port)

        Thread.__init__(self)

    def get_finger_table(self):
        return self.finger_table

    def quit(self):
        ret = self.registry_proxy.deregister(self.id)
        return ret

    def run(self):
        self.finger_table = self.registry_proxy.populate_finger_table(self.id[0])

        server = SimpleXMLRPCServer((host, self.port))

        server.register_function(self.get_finger_table)
        server.register_function(self.quit)

        server.serve_forever()