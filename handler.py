#event handler
'''
Handler Code:
0 = attack
1 = discard
2 = trash
3 = gain card
4 = gain province
5 = gain victory card
'''
class Handler:
    def __init__(self):
        self.subscribers = []

    def notify(self, event):
        for subscriber in self.subscribers:
            subscriber(event, self)