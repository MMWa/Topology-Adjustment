class NodeRecordEntry:
    def __init__(self, node, value):
        self.node = node
        self.value = value

class NodeRecord:
    def __init__(self):
        self.record_list =[]

    def update(self, record):
        idx, exist = self.isMember(record)
        print(idx)
        if exist:
            self.record_list[idx] = record
        else:
            self.record_list.append(record)

    def isMember(self, record):
        for idx, item in enumerate(self.record_list):
            if item.node == record.node:
                return idx, True
        return None, False

if __name__ == "__main__":

    hello ="asda"

    test1 = NodeRecordEntry("213", 3)
    test2 = NodeRecordEntry("2133", 4)
    test3 = NodeRecordEntry(hello, 1)

    aba = NodeRecord()
    aba.update(test1)
    aba.update(test2)
    aba.update(test3)
    print(aba)

    test3 = NodeRecordEntry(hello, 6)
    aba.update(test3)
    print(aba)

    test2 = NodeRecordEntry("2133", 7)
    aba.update(test2)
    print(aba)