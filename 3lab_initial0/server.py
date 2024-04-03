#!/usr/bin/python3

import socket
import asyncio
import threading

          
class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self, is_async=True):
        if is_async:
            asyncio.run(self._async_start())
        else:
            self._thread_start()

    async def _async_start(self):
        #server = await asyncio.start_server(
            #handle_client, self._host, self._port)
        #addr = server.sockets[0].getsockname()
        #print(f'Сервер запущен на {addr}')
        #async with server:
            #await server.serve_forever()
        pass

    def _thread_start(self):
        #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_socket.bind((self._host, self._port))
        #server_socket.listen(1)
        #print(f"Сервер запущен и слушает на {self._host}:{self._port}")
        #try:
            #while True:
                #client_sock, address = server_socket.accept()
                #print(f"Принято соединение от {address}")
                #client_handler = threading.Thread(
                    #target=handle_client,
                    #args=(client_sock,)  # Передаем сокет клиента в поток
                #)
                #client_handler.start()
        #finally:
            #server_socket.close()
        pass





