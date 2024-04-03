import socket

HOST = (socket.gethostname(), 1000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)
print("Client conected to", HOST)


while True:
    message = input("Введите скрипты для запуска в формате: [script1 {arg1 arg2}, script2]: ")
    if message == "q":
        break
    client.send(message.encode('utf-8'))

client.close()
