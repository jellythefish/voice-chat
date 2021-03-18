# Voice Chat

## About
This is a CLI application which provides communication for users via voice chat.

Features:
+ Chat with more than 2 users at the same time.
+ Sending voice data only if the signal is higher than certain RMS (the silence is not being transferred). 
+ The indication of speaking user in the console output.
+ Connection to certain voice chat **rooms**.

Server and clients support connection via UDP sockets. Server receives data from clients and broadcasts it to all other
clients in a voice chat room.

Application is based on [Python Voice Chat](https://github.com/domage/soa-curriculum-2021/tree/main/examples/sockets-voice-chat).

## Setup

### Server 

Server does not require any specific dependencies and it can be run natively as a python script:
```bash
python3 server-udp.py
```
or via Docker Container (The [Docker](https://www.docker.com/products/docker-desktop) itself should already be installed in host OS):
```bash
docker pull jellythefish/voice-chat
docker run --rm -i -p 8000:3000/udp jellythefish/voice-chat
```

Also, it is possible to build Docker image from Dockerfile. In the root project folder run:
```bash
docker build . --no-cache -t voice-chat
```

### Client
A client-side needs a PyAudio package as the main dependency for capturing and playing sound data.

```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python-pyaudio
pip install -r requirements.txt  # PyAudio==0.2.11
```

Then, it should be run natively as a python script:
```bash
python3 client-udp.py
```

## Usage

### Server

While running docker container with server you need to specify port 3000 or other in stdin corresponding to 
forwarding port in **docker run*...* command.
```cmd
C:\Users\Slava\Desktop\voice-chat>docker run --rm -i -p 8000:3000/udp jellythefish/voice-chat
Enter port number to run on --> 3000
Running on IP: 172.17.0.2
Running on port: 3000
```
Then, to connect to the server you should use the ip address of the host machine in a local network, **not the one which is provided in the console output
of the server!**.

For example, in local network host machine with ip 192.168.1.18 receives connections on port 8000 and forwards it to 
the destination 127.17.0.2:3000 which is docker container with the server.

In case of running server natively as a .py script without docker just use ip and port from the console output of a server.

### Client
Run client natively with:
```bash
python3 client-udp.py
```
When running the client in stdin you specify:
+ Client name
+ Local network host IP address
+ External port
+ Room number (integer from 0 to 255)
```bash
C:\Users\Slava\Desktop\voice-chat>python client-udp.py
Enter the name of the client --> test
Enter IP address of server --> 192.168.1.18
Enter target port of server --> 8000
Enter the id of room  --> 0
Connected to server to room 0 successfully!
Users online in room 0 : "test" (172.17.0.1:57873)
```

At this step you should be good to go and talk and hear other participants in a voice chat room.

To disconnect from voice chat room just stop the execution of client-udp.py:
Ctrl+C in Unix or Ctrl+Break in Windows.

### Command Line Interface

After the client is connected to the server it receives the list of current users in a room:
```bash
# Client's stdout
Connected to server to room 0 successfully!
Users online in room 0 : "test" (172.17.0.1:53498), "test2" (172.17.0.1:35170)
```
When a user leaves voice chat room all other users receives information about it:
```bash
# Client's stdout
User "test" (172.17.0.1:53498) has left voice chat, room 0.
Users online in room 0 : "test2" (172.17.0.1:35170)
```
When the certain user is talking any other user in a room receives information about it:
```bash
# Client's stdout
User with id 2 is talking (room 0)
```
For a simplification only id of a user is showed, because it is fetched from the header of UDP datagram. None of the
users stores the mapping from id to username, only server does this. Transferring the username in the header of a datapacket
is not that simple, because it requires certain constraints on the length of username and protocol. Storing specified
mapping from id to username on a client is also an overhead.

Server itself also supports stdout as some kind of log:
```bash
# Server's stdout
C:\Users\Slava\Desktop\voice-chat>docker run --rm -i -p 8000:3000/udp jellythefish/voice-chat
Enter port number to run on --> 3000
Running on IP: 172.17.0.2
Running on port: 3000
User "test" (172.17.0.1:57873) has joined voice chat, room 0.
Users online in room 0 : "test" (172.17.0.1:57873)
User "test" (172.17.0.1:49216) has joined voice chat, room 0.
Users online in room 0 : "test" (172.17.0.1:57873), "test" (172.17.0.1:49216)
User "test" (172.17.0.1:57873) has left voice chat, room 0.
Users online in room 0 : "test" (172.17.0.1:49216)
User "test" (172.17.0.1:49216) has left voice chat, room 0.
Users online in room 0 : 0
User "test" (172.17.0.1:53498) has joined voice chat, room 0.
Users online in room 0 : "test" (172.17.0.1:53498)
User "test2" (172.17.0.1:35170) has joined voice chat, room 0.
Users online in room 0 : "test" (172.17.0.1:53498), "test2" (172.17.0.1:35170)
User "test" (172.17.0.1:53498) has left voice chat, room 0.
Users online in room 0 : "test2" (172.17.0.1:35170)
User "test3" (172.17.0.1:33244) has joined voice chat, room 0.
Users online in room 0 : "test2" (172.17.0.1:35170), "test3" (172.17.0.1:33244)
User "test3" (172.17.0.1:33244) has left voice chat, room 0.
Users online in room 0 : "test2" (172.17.0.1:35170)
User "test54" (172.17.0.1:39427) has joined voice chat, room 42.
Users online in room 42 : "test54" (172.17.0.1:39427)
```
