#!/home/edilson/anaconda3/bin/python3.8
import zmq
import sys
import json
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
port = sys.argv[1]
socket.bind(f"tcp://*:{port}")
#address proxy 
server_info = {}

def send_info_proxy(address):
    context_proxy = zmq.Context()
    socket_proxy = context_proxy.socket(zmq.REQ)
    socket_proxy.connect(f"tcp://{address}")
    socket_proxy.send_multipart([json.dumps(server_info).encode('utf-8')])
    response_proxy = socket_proxy.recv_multipart()
    print(response_proxy)


def get_args():
    address_proxy = sys.argv[2]
    files_folder = sys.argv[3]
    if not os.path.isdir(files_folder):
        os.mkdir(files_folder)
    server_info['files_folder'] = files_folder
    server_info['port'] = port
    server_info['address'] = 'localhost'
    server_info['command'] = 'server_on'
    send_info_proxy(address_proxy)
    
    return


def upload(request):
    filename = request.get('filename').decode('utf-8')
    bytes_to_save = request.get('bytes')
    files_folder = server_info.get('files_folder')
    with open(f"{files_folder}/{filename}", "wb") as f:
        f.write(bytes_to_save)
    socket.send_multipart([json.dumps({'file_saved': True}).encode('utf-8')])

        
def download(request):
    filename = request.get('filename').decode('utf-8')
    files_folder = server_info.get('files_folder')
    with open(f"{files_folder}/{filename}",'rb') as f:
        download_bytes =  f.read()
    socket.send_multipart([download_bytes])

def decide_commands(request):
    command = request.get('command')
    if command == b'upload':
        upload(request)
    elif command == b'download':
        download(request)
    return
  
    command = args[0]
def main():
    print(f"server is running on port : {port}")
    while True:
        request = socket.recv_multipart()
        files = {
            'filename': request[0],
            'command': request[1]
        }
        if len(request) > 2:
            files['bytes'] = request[2]
        decide_commands(files)


if __name__ == '__main__':
    get_args()
    main()
    