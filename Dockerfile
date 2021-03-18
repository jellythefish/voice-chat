FROM python

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y portaudio19-dev python-pyaudio
RUN pip install -r requirements.txt

EXPOSE 3000/udp

CMD ["python3", "-u", "server-udp.py"]