from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
import random
import math

host = "127.0.0.1"



class Registry(Thread):
    def __init__(self, port, m):
        self.port = port
        self.nodes = {}
        self.m = m
        self.rang = int((math.pow(2, m)) - 1)

        Thread.__init__(self)

    def register(self, port):
        random.seed(0)

        if len(self.nodes) == self.rang + 1:
            return False, 'Chord is full'

        if port in self.nodes:
            return False, 'Port already exists'

        node_id = random.randint(0, self.rang)

        while node_id in self.nodes:
            node_id = random.randint(0, self.rang)

        self.nodes[node_id] = port
        return node_id, str(len(self.nodes))

    def deregister(self, node_id):
        if node_id not in self.nodes:
            return False, f'Node {node_id} not found'

        else:
            del self.nodes[node_id]
            for node in self.nodes:
                node.finger_table = self.populate_finger_table(node.id)
            return True, f'Node {node_id} deleted'

    def get_chord_info(self):
        return str(self.nodes)

    def populate_finger_table(self, node):

        if node not in self.nodes:
            return False, f'Node {node} not found'
        f_table = {}
        for i in range(1, self.m + 1):
            temp = node
            first = math.pow(2, self.m)
            second = node + math.pow(2, i - 1)
            for nodekey in self.nodes.keys():
                if nodekey > second:
                    min = nodekey - second
                    if min < first:
                        first, temp = min, nodekey
            f_table[str(i)] = temp
        return f_table




    def run(self):
        server = SimpleXMLRPCServer((host, self.port), logRequests=False)

        server.register_function(self.register)
        server.register_function(self.deregister)
        server.register_function(self.populate_finger_table)
        server.register_function(self.get_chord_info)

        server.serve_forever()