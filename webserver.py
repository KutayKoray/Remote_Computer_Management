from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3
import subprocess
from functools import wraps
import socket

app = Flask(__name__)

app.secret_key = 'zattirizortzort'
username = 'admin'
password = 'admin'

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

        data = request.data.decode('utf-8')
        
        if data == 'true':
            
            subprocess.Popen(['python3', '-c', 'import os; os.system("python3 socket_listener.py")'])

            return "Listener started from webserver."
        elif data == 'false':
            command = """
                import os
                import socket_listener

                close = socket_listener.Listener()
                close.close_connection()
                os.system("pkill -f socket_listener.py")
                """

            subprocess.Popen(['python3', '-c', command], 
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
            
            return "Listener already stopped."
            
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