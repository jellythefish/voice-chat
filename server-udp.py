#!/usr/bin/python3

import socket
from protocol import DataType, Protocol
from collections import defaultdict


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())

        while 1:
            try:
                self.port = int(input('Enter port number to run on --> '))
                self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.s.settimeout(5)
                self.s.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that port")

        self.clients = {}
        self.clientCharId = {}
        self.rooms = defaultdict(list)
        self.client_room = {}
        self.receiveData()

    def receiveData(self):   
        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))
        
        while True:
            try:
                data, addr = self.s.recvfrom(1026)
                message = Protocol(datapacket=data)
                self.handleMessage(message, addr)
            except socket.timeout:
                pass

    def handleMessage(self, message, addr):
        if self.clients.get(addr, None) is None:
            try:
                if message.DataType != DataType.Handshake:
                    return

                name = message.data.decode(encoding='UTF-8')
                room = message.room

                self.clients[addr] = name
                self.clientCharId[addr] = len(self.clients)
                self.rooms[room].append(addr)
                self.client_room[addr] = room

                update_message = self.get_update_message(addr, room, "joined")
                users_message = self.get_online_users(room)
                notification = "".join(update_message + users_message)
                print(notification)

                ret = Protocol(dataType=DataType.Handshake, room=message.room, data="".join(users_message).encode(encoding='UTF-8'))
                ret_b = Protocol(dataType=DataType.Handshake, room=message.room, data=notification.encode(encoding='UTF-8'))
                self.s.sendto(ret.out(), addr)
                self.broadcast(addr, room, ret_b)
            except Exception as err:
                print(err)
            return

        elif message.DataType == DataType.ClientData:
            self.broadcast(addr, message.room, message)

        elif message.DataType == DataType.Terminate:
            room = message.room
            update_message = self.get_update_message(addr, room, "left")
            self.clients.pop(addr)
            self.clientCharId.pop(addr)
            self.rooms[room].remove(addr)
            self.client_room.pop(addr)
            users_message = self.get_online_users(room)
            notification = "".join(update_message + users_message)
            print(notification)
            message_ter = Protocol(dataType=DataType.Terminate, room=room, data=notification.encode("utf-8"))
            self.broadcast(addr, message.room, message_ter)

    def broadcast(self, sentFrom, room, data):
        if not data.head:
            data.head = self.clientCharId[sentFrom]
        for client in self.rooms[room]:
            if client[0] != sentFrom[0] or client[1] != sentFrom[1]:
                try:
                    self.s.sendto(data.out(), client)
                except Exception as err:
                    raise err

    def get_online_users(self, room):
        users = ["Users online in room %s : " % room]
        if len(self.rooms[room]) == 0:
            users.append("0")
        for client in self.rooms[room]:
            if len(users) > 1:
                users.append(", ")
            users.append("\"%s\" (%s:%s)" % (self.clients[client], client[0], client[1]))
        return users

    def get_update_message(self, addr, room, state):
        message_list = ["User \"%s\" (%s:%s) has %s voice chat, room %s.\n" % (self.clients[addr], addr[0], addr[1], state, room)]
        return message_list


server = Server()
