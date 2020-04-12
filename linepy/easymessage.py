# -*- coding: utf-8 -*-

# EasyMessage by PASUNX(UNION)
# Release date: 4/27/2019

class EasyMessage:

    def __init__(self, client):
        # require LINE Object
        self.client = client

    def c(self, to, message=None): # create
        # require group/room/chat ID
        self.msg = message if message is not None else ''
        self.to = to

    def a(self, text): # add
        # require text
        if self.msg == '':
            self.msg += f"{text}"
        else:
            self.msg += f"\n{text}"

    def s(self): # send
        if 'to' not in dir(self):
            raise ValueError("missing object")
        if 'msg' not in dir(self):
            raise ValueError("missing message")
        self.client.sendMessage(self.to, self.msg)

if __name__ == '__main__':
    # Simple

    class SimpleLINE():
        def sendMessage(self, to, message):
            print(f"{message}")

    client = SimpleLINE()
    group = {"id": "1234", "members": ["A", "B", "C"]}
    msg = EasyMessage(client)

    msg.c(group["id"], "Members of this group:")
    for no, member in enumerate(group["members"]):
        msg.a(f"{no}. {member}")
    msg.s()
