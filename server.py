#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion\r\n\r\n")
        methods = ['INVITE', 'ACK', 'BYE']
        line = self.rfile.read().decode('utf-8').split() #probar sin decode
        if len(line) != 3: #miramos si la peticion tiene la forma correcta
            self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')
        elif line[0] not in methods:
            self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
        else:
            if line[0] == 'INVITE':
                expected = ('SIP/2.0 100 Trying\r\n\r\n'
                            'SIP/2.0 180 Ringing\r\n\r\n'
                            'SIP/2.0 200 OK\r\n\r\n')
                self.wfile.write(bytes(expected, 'utf-8'))
            elif line[0] == 'ACK':
                os.system('./mp32rtp -i 127.0.0.1 -p 23032 < ' +
                                audio_file)
            elif line[0] == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        serv = socketserver.UDPServer((sys.argv[1],
                                       int(sys.argv[2])), EchoHandler)
        audio_file = sys.argv[3]
        if not os.path.isfile(audio_file):
            print ("This file does not exist: ' + audio_file")
            raise SystemExit
        print("Listening...")
    except IndexError:
        print ("Usage: python3 server.py IP port audio_file")
        raise SystemExit
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nFinalizado servidor")
