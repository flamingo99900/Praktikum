import os
import json
import xml.etree.ElementTree as ET
import socket
from datetime import datetime


def get_processes_info():
    process = []
    for line in os.popen('tasklist').readlines()[3:]:
        split_line = line.split()
        if len(split_line) >= 5:
            process.append({
                'Name': split_line[0],
                'PID': split_line[1],
                'Session Name': split_line[2],
                'Session#': split_line[3],
                'Memory Usage': split_line[4]
            })
    return process


def save_to_json(process, filename):
    with open(filename, 'w') as f:
        json.dump(process, f, indent=4)
    print(f"Сохранено в JSON файл: {filename}")


def save_to_xml(process, filename):
    root = ET.Element('processes')
    for process1 in process:
        proc_elem = ET.SubElement(root, 'process')
        for key, value in process1.items():
            ET.SubElement(proc_elem, key).text = value
    tree = ET.ElementTree(root)
    tree.write(filename)
    print(f"Сохранено в XML файл: {filename}")


def handle_client_connection(conn, addr):
    with conn:
        print('Подключен клиент:', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode()
            if command == 'update':
                process = get_processes_info()
                format_choice = input("Выберите формат сохранения (json/xml): ").lower()
                now = datetime.now()
                folder_name = now.strftime("%d-%m-%Y")
                filename = now.strftime("%H-%M-%S")
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                if format_choice == 'json':
                    save_to_json(process, f"{folder_name}/{filename}.json")
                elif format_choice == 'xml':
                    save_to_xml(process, f"{folder_name}/{filename}.xml")
                else:
                    print("Неправильный формат выбран.")
                conn.send(f'Сохранено в файл: {filename}.{format_choice}'.encode())
                break

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 4444

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Сервер запущен и ожидает подключения...')
        conn, addr = s.accept()
        with conn:
            handle_client_connection(conn, addr)