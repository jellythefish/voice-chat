#!/bin/sh

# dev
docker run --rm -it -p 8000:3000/udp jellythefish/voice-chat /bin/bash

# prod
docker run --rm -i -p 8000:3000/udp jellythefish/voice-chat