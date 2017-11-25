#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

try:
    METHOD = sys.argv[1].upper()
    LOGIN_RECEIVER = sys.argv[2].split('@')[0]
    IP_SERVER = sys.argv[2].split('@')[-1].split(':')[0]
    PORT = int(sys.argv[2].split(':')[-1])

except IndexError:
    print ("Usage: python3 client.py method receiver@IP:SIPport")
    raise SystemExit

# Dirección IP del servidor.


# Contenido que vamos a enviar
LINE = METHOD + ' sip:' + LOGIN_RECEIVER + '@' + IP_SERVER + ' SIP/2.0'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP_SERVER, PORT))

    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    expected = ('SIP/2.0 100 Trying\r\n\r\n'
            'SIP/2.0 180 Ring\r\n\r\n'
            'SIP/2.0 200 OK\r\n\r\n')
    if data == expected:
        METHOD = 'ACK'
        LINE = METHOD + ' sip:' + LOGIN_RECEIVER + '@' + IP_SERVER + ' SIP/2.0'
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n\r\n')
    print('Recibido -- ', data.decode('utf-8'))
    print("Terminando socket...")
    # my_socket.close()

print("Fin.")
