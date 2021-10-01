from registry import Registry
import xmlrpc.client
from node import Node
a = 2

host = "127.0.0.1"


def address(port):
    return str("http://" + host + ":" + str(port) + "/")


if a == 3:
    print('hi')
    #len(sys.argv) != 4:
#     print("format as (python ./main.py <m> <first_port> <last_port>)")
#     exit(0)

else:

    try:
        # m = int(sys.argv[1])
        # first_port = int(sys.argv[2])
        # last_port = int(sys.argv[3])
        m, first_port, last_port = input().split(' ')
        m = int(m)
        first_port = int(first_port)
        last_port = int(last_port)

        reg = Registry(first_port - 1, m)
        reg.start()
        print(f'Registry and {m} nodes are created')

        nodes = []
        ports = range(first_port, last_port + 1)

        for port in ports:
            node = Node(port, first_port - 1)
            nodes.append(node)

        for node in nodes:
            node.start()


        registry = xmlrpc.client.ServerProxy(address(first_port - 1))

        while True:
            message = input()
            try:
                if 'register' in message:
                    command, port = message.split(' ')
                    port = int(port)
                    print(registry.register(port))
                    continue

                if 'deregister' in message:
                    command, port = message.split(' ')
                    port = int(port)
                    print(registry.deregister(port))
                    continue

                if 'get_chord_info' in message:
                    print(registry.get_chord_info())
                    continue

                if 'get_finger_table' in message:
                    command, port = message.split(' ')
                    node_xmlrpc = xmlrpc.client.ServerProxy(address(port))
                    print(node_xmlrpc.get_finger_table())
                    continue

                else:
                    print('Message not supported')

            except KeyboardInterrupt:
                print('Keyboard interrupt')
                exit(0)

            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
        exit(0)
