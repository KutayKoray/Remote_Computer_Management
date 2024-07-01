from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3
from functools import wraps
import socket
import json

def json_send(data, sock):
	if isinstance(data, bytes):
		data = data.decode("utf-8", errors="ignore")
	json_data = json.dumps(data)
	sock.send(json_data.encode("utf-8"))

def send_data_to_socket(data):
    try:
        # 192.168.1.62 adresine ve 8080 portuna bağlanın
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('192.168.1.15', 8080))
            data = "web:" + data
            #sock.sendall(data.encode('utf-8'))
            json_send(data, sock)
            response = sock.recv(1024)
            sock.close()
            print("Received from server:", response.decode('utf-8'))
            return response.decode('utf-8')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


app = Flask(__name__)

app.secret_key = 'zattirizortzort'
username = 'admin'
password = 'admin'


class mypid:
    pid = None
    @classmethod
    def set_pid(cls, pid):
        cls.pid = pid
    @classmethod
    def get_pid(cls):
        return cls.pid


users = {
    'admin': 'admin'
}

# Kullanıcı giriş işlemi
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_username = request.form.get("username")
        form_password = request.form.get("password") 

        if form_username in users and users[form_username] == form_password:
            session['logged_in'] = True
            return redirect(url_for('mainpage'))
        else:
            flash("Invalid credentials.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    if 'logged_in' not in session:
        return redirect(url_for('login'))   

    if request.method == 'POST': 
        data = request.get_json()
        
        if data and data.get('name') == 'command':
            command = data.get('message')
            response = send_data_to_socket(command)
            return response
        else:
            return "Unknown command."     

    return render_template('mainpage.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        col = int(request.form.get('delete'))
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM commands WHERE id = ?;''', (col,))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM commands''')
    rows = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', rows=rows)

@app.route('/attacks', methods=['GET', 'POST'])
def attacks():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    return render_template('attacks.html')



if __name__ == '__main__':
    app.run(debug=True, port=5555)