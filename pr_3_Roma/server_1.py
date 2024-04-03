import os
import json
from datetime import datetime
import socket
import subprocess


# создаем сокет сервера
HOST = (socket.gethostname(), 1000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(HOST)
server_socket.listen()
print("Server ready")

programs = {"dir", "echo 1"}


# функция для загрузки файла
def load_program_data():
    if os.path.exists("program_data.json"):
        with open("program_data.json", "r") as json_file:
            return json.load(json_file)
    else:
        return []


def run_programs(programs):
    program_data = load_program_data()  # добавляю программы, вызванные во время предыдущих запусков кода
    if program_data:
        for i in program_data:
            programs.add(i["program"])
    client_socket, addr = server_socket.accept()  # подключаюсь к клиенту
    print(f"Подключение установлено с {addr[0]}:{addr[1]}")
    new_programs = set()
    request = ''
    while True:  # обрабатываю сообщение(любой длины) от клиента
        data = client_socket.recv(1).decode('utf-8')
        if not data:
            break
        request += data
    if request:  # добавляю программы клиента к списку всех программ
        print("DATA FROM CLIENT:\n", request, "\n")
        for program in request.split(","):
            new_programs.add(program)
        client_socket.close()
        programs.update(new_programs)
    print(programs)

    for program in programs:
            print(program)
            # Создаем папку с именем программы, если она еще не существует
            if not os.path.exists(program):
                os.makedirs(program)

            # Получаем текущую дату и время
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y %m %d %H %M %S")

            # Создаем имя файла в формате "ГГГГ ММ ДД ЧЧ ММ СС"
            output_file_name = f"{formatted_datetime}.txt"

            # Создаем файл для вывода
            output_file = os.path.join(program, output_file_name)

            # Запускаем программу и записываем её вывод в файл
            with open(output_file, "w") as f:
                process = subprocess.run(program, shell=True, capture_output=True, text=True)
                output = process.stdout.encode('cp1251').decode('cp866')
                print(output)
                f.write(output)

            # Добавляем информацию о программе, папке и файле в список
            program_data.append({
                "program": program,
                "folder": program,
                "file": output_file
            })

    # Сохраняем информацию в файл JSON
    with open("program_data.json", "w") as json_file:
        json.dump(program_data, json_file, indent=4)


# Пример вызова функции с передачей списка программ
run_programs(programs)
