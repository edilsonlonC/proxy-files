from dotenv import load_dotenv

load_dotenv()
from database.database import database
import json


db = database()
import zmq

#!/home/edilson/anaconda3/bin/python3.8
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")


def check_file(filename, ext, username, password):
    file = db.files.find_one({"username": username, "filename": filename})
    return True if file else False


def save_file(request):
    username = request.get("username")
    password = request.get("password")
    filename = request.get("filename")
    hash_parts = request.get("hash_parts")
    servers = request.get("servers")
    name, ext = filename.rsplit(".", 1)
    if check_file(filename, ext, username, password):
        socket.send_multipart([json.dumps({"file_exist": True}).encode("utf-8")])
        return False
    # query = {'$and':[{'username': username} , { 'password':password}]}
    # values = {'$set':{name: {'hash_parts':hash_parts,'servers': servers,'ext':ext}}}
    # db.users.update_one(query,values)
    db.files.insert_one(
        {
            "filename": filename,
            "hash_parts": hash_parts,
            "servers": servers,
            "username": username,
        }
    )
    return True


def choose_server(request):
    hash_parts = request.get("hash_parts")
    number_servers = db.servers.count_documents({})
    servers = db.servers.find({}, {"address": 1, "port": 1, "_id": 0})
    print(number_servers)
    print(servers)
    if number_servers == 0:
        socket.send_multipart([json.dumps({"serversNotFound": True}).encode("utf-8")])
        return
    server_itr = 0
    server_list = list()
    for h in hash_parts:
        if server_itr >= number_servers:
            server_itr = 0
        server_list.append(servers[server_itr])
        server_itr = server_itr + 1

    request["servers"] = server_list
    if save_file(request):
        socket.send_multipart([json.dumps(request).encode("utf-8")])


def upload(request):
    choose_server(request)


def download(request):
    filename = request.get("filename")
    username = request.get("username")
    password = request.get("password")
    print(username, filename)
    # name,ext = filename.rsplit('.',1)
    # hash_and_servers =  db.users.find_one({'username': username,'password':password,f"{name}.ext":ext},{name:1,'_id':0})
    hash_and_servers = db.files.find_one(
        {"username": username, "filename": filename}, {"_id": 0}
    )  # TODO check if file exist en db
    if not hash_and_servers:
        socket.send_multipart([json.dumps({"FileNotFound": True}).encode("utf-8")])
        return
    hash_and_servers["command"] = request.get("command")
    socket.send_multipart([json.dumps(hash_and_servers).encode("utf-8")])


def user_exist(username, password):
    user = db.users.find_one({"username": username, "password": password})
    return True if user else False


def register(files):
    username = files.get("username")
    password = files.get("password")
    if user_exist(username, password):
        socket.send_multipart([json.dumps({"user_exist": True}).encode("utf-8")])
        return
    db.users.insert_one({"username": username, "password": password})
    socket.send_multipart([json.dumps({"user_saved": True}).encode("utf-8")])


def server_on(request):
    port = request.get("port")
    address = request.get("address")
    print(port, address)
    query = {"address": address, "port": port}
    server = db.servers.find_one(query)
    print(server)
    if not server:
        db.servers.insert_one(query)
    socket.send_multipart([json.dumps({"server_on": True}).encode("utf-8")])
    return


def server_off(request):
    port = request.get("port")
    address = request.get("address")
    delete_server = db.servers.delete_one({"address": address, "port": port})
    print(delete_server)
    socket.send_multipart([json.dumps({"server_off": True}).encode("utf-8")])
    print(port, address)
    return


def list_files(request):
    username = request.get("username")
    files = list(
        db.files.find(
            {"username": username},
            {"hash_parts": 0, "servers": 0, "_id": 0, "username": 0},
        )
    )
    print(files)
    socket.send_multipart([json.dumps(files).encode("utf-8")])
    return


def decide_command(request):
    username = request.get("username")
    password = request.get("password")
    if not user_exist(username, password):
        socket.send_multipart([json.dumps({"unauthorized": True}).encode("utf-8")])
        return
    command = request.get("command")
    if command == "upload":
        upload(request)
    elif command == "register":
        register(request)
    elif command == "download":
        download(request)
    elif command == "server_on":
        server_on(request)
    elif command == "list":
        list_files(request)
    elif command == "server_off":
        server_off(request)


def main():
    print("server is running on port 5556")
    while True:
        request = socket.recv_multipart()
        json_request = json.loads(request[0])
        decide_command(json_request)


if __name__ == "__main__":
    main()
