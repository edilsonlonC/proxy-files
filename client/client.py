#!/home/edilson/anaconda3/bin/python3.8

import zmq
import json
import sys
from hashlib import sha256
from getpass import getpass
from utilities import string_response, get_newname
import os

files = {}
size = 1024 * 1024 * 10
proxy_address = ''

try:
    if sys.argv[1] == 'list' or sys.argv[1] == 'register':
        proxy_address = sys.argv[3]
    else :
        proxy_address = sys.argv[4]
except IndexError:
    print('Arguments are missing')

print(proxy_address)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{proxy_address}")


def upload(response_proxy, filename):
    servers_list = response_proxy.get("servers")
    parts_hash = response_proxy.get("hash_parts")
    file = open(filename, "rb")
    print("uploading file")
    sockets_created = {}
    for s in range(len(servers_list)):
        bytes_to_send = file.read(size)
        json_server = json.dumps(servers_list[s])
        socket = sockets_created.get(json_server)
        if socket:
            socket.send_multipart(
                [
                    parts_hash[s].encode("utf-8"),
                    files.get("command").encode("utf-8"),
                    bytes_to_send,
                ]
            )
            response = socket.recv_multipart()
        else:

            address = servers_list[s]["address"]
            port = servers_list[s]["port"]
            context_server = zmq.Context()
            socket_server = context_server.socket(zmq.REQ)
            socket_server.connect(f"tcp://{address}:{port}")
            sockets_created[json_server] = socket_server
            socket_server.send_multipart(
                [
                    parts_hash[s].encode("utf-8"),
                    files.get("command").encode("utf-8"),
                    bytes_to_send,
                ]
            )
            response = socket_server.recv_multipart()
    return


def filename_exist(filename):
    return os.path.isfile(filename)


def get_hash(files):
    filename = files.get("filename")
    hash_list = list()
    with open(filename, "rb") as f:
        m = sha256()
        _bytes = f.read(size)
        m.update(_bytes)
        hash_list.append(m.hexdigest())
        while _bytes:
            m = sha256()
            _bytes = f.read(size)
            m.update(_bytes)
            hash_list.append(m.hexdigest())
    return hash_list


def list_files(args):
    files["username"] = args[1]
    socket.send_multipart([json.dumps(files).encode("utf-8")])
    response = socket.recv_multipart()
    files_list = json.loads(response[0])
    if not isinstance(files_list, list):
        if files_list.get("unauthorized"):
            print("access denied")
            return

    if not files_list:
        print("you don't have files")
        return

    message = string_response(files_list)
    print(message)
    return


def get_servers_proxy(args):
    if len(args) < 3:
        print("arguments are misssed")
        return
    filename = args[1]
    files["filename"] = filename
    files["hash_parts"] = get_hash(files)
    try:
        file = open(f"{filename}", "rb")
        bytes_to_send = file.read()
        socket.send_multipart([json.dumps(files).encode("utf-8")])
        response = socket.recv_multipart()
        json_response = json.loads(response[0])
        if json_response.get("file_exist"):
            print(f"the file with name {filename} already exists")
            return
        elif json_response.get("unauthorized"):
            print("access dienied")
            return
        elif json_response.get("serversNotFound"):
            print("servers not found")
            return

        upload(json_response, filename)
    except FileNotFoundError:
        print(f"the file {filename} doesn't exist")


def register(args):
    files["username"] = args[1]
    socket.send_multipart([json.dumps(files).encode("utf-8")])
    response = socket.recv_multipart()
    json_response = json.loads(response[0])
    if json_response.get("user_saved"):
        print(f"the user f{files.get('username')} was created")
        return
    if json_response.get("user_exist"):
        print(f"the user {files.get('username')} already exists")
        return


def download(response, filename):
    hash_parts = response.get("hash_parts")
    servers = response.get("servers")
    command = response.get("command")
    if files.get("new_name"):
        filename = files.get("new_name")
    with open(filename, "ab") as f:
        sockets_created = {}
        print("downloading file")
        for s in range(len(servers)):
            json_server = json.dumps(servers[s])
            socket = sockets_created.get(json_server)
            if socket:
                socket.send_multipart(
                    [
                        hash_parts[s].encode("utf-8"),
                        files.get("command").encode("utf-8"),
                    ]
                )
                response = socket.recv_multipart()
                f.write(response[0])
            else:
                address = servers[s]["address"]
                port = servers[s]["port"]
                context_server = zmq.Context()
                socket_server = context_server.socket(zmq.REQ)
                socket_server.connect(f"tcp://{address}:{port}")
                sockets_created[json_server] = socket_server
                socket_server.send_multipart(
                    [
                        hash_parts[s].encode("utf-8"),
                        files.get("command").encode("utf-8"),
                    ]
                )
                response = socket_server.recv_multipart()
                f.write(response[0])


def proxy_download(args):
    files["filename"] = args[1]
    files["username"] = args[2]
    filename = files.get("filename")
    if filename_exist(filename):
        new_name = get_newname(filename, os.listdir())
        files["new_name"] = new_name
    socket.send_multipart([json.dumps(files).encode("utf-8")])
    response = socket.recv_multipart()
    json_response = json.loads(response[0])

    if json_response.get("FileNotFound"):
        print("file does not exist")
        return
    if json_response.get("unauthorized"):
        print("access denied")
        return
    download(json_response, files.get("filename"))


def decide_command():
    if len(sys.argv) <= 1:
        print("arguments are missing")
        return
    args = sys.argv[1:]
    command = args[0]
    files["password"] = getpass()
    files["command"] = command
    if command == "upload":
        files["username"] = args[2]
        get_servers_proxy(args)
    elif command == "register":
        register(args)
    elif command == "download":
        proxy_download(args)
    elif command == "list":
        list_files(args)
    else:
        print("the command doesn't exist")
        return


def main():
    decide_command()


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print('Arguments are missing')
