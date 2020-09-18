#!/home/edilson/anaconda3/bin/python3.8
import zmq
import sys
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
port = sys.argv[1]
socket.bind(f"tcp://*:{port}")

def upload(request):
    filename = request.get('filename').decode('utf-8')
    bytes_to_save = request.get('bytes')
    with open(f"files/{filename}", "wb") as f:
        f.write(bytes_to_save)
    socket.send_multipart([json.dumps({'file_saved': True}).encode('utf-8')])

        
def download(request):
    filename = request.get('filename').decode('utf-8')
    with open(f"files/{filename}",'rb') as f:
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
    
    main()
    