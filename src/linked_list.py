class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListHelp:
    def __init__(self):
        self.head = None

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def dequeue(self):
        if not self.head:
            return None
        current = self.head
        self.head = self.head.next
        return current.data

    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next