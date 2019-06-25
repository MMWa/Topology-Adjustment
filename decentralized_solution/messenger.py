class Message:
    def __init__(self, data, sender, target):
        self.target = target
        self.sender = sender
        self.path = [sender]
        self.data = data


class Messenger:
    def __init__(self, node_name):
        self.node_name = node_name
        self.in_queue = []
        self.out_queue = []

    def receive(self, message):
        self.in_queue.append(message)

    def process(self):
        for m in self.in_queue:
            m: Message

            if self.node_name == m.target:
                print("recived message from " + m.sender)
                print("Data: \33[91m" + m.data + "\33[0m")
            else:
                self.out_queue.append(m)
            self.in_queue.remove(m)
