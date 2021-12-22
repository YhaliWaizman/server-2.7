import socket
import protocol
import glob
import os
import shutil
import subprocess
import pyautogui


IP = "localhost"
# The path + filename where the screenshot at the server should be saved
PHOTO_PATH = "C:\\Users\\cyberclass\\Desktop\\VSCodePythonYhali\\screen.jpg"


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    boolval = protocol.check_cmd(cmd)
    # Then make sure the params are valid
    dataparts = cmd.split()
    # (6)
    if boolval:
        return True, dataparts[0], dataparts[1:]
    else:
        return False, None, None


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    # (7)
    if command == "DIR":
        response = glob.glob(params[0] + "*")
        response.join("\n")
        response = response.encode()
    elif command == "DELETE":
        response = ("Deleting " + params[0]).encode()
        os.remove(params[0])
    elif command == "COPY":
        response = ("Copying " + params[0] + " to " + params[1]).encode()
        shutil.copy(params[0], params[1])
    elif command == "EXECUTE":
        response = ("Executing " + params[0]).encode()
        subprocess.call(params[0], shell=True)
    elif command == "EXIT":
        response = "Exiting".encode()
    elif command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        response = "Screenshot saved".encode()
    elif command == "SEND_PHOTO":
        response = os.path.getsize(PHOTO_PATH)
    else:
        response = "Bad command or parameters".encode()

    return response


def main():
    # open socket with client

    MyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    MyServer.bind((IP, 11111))
    MyServer.listen()
    print("Server is running...")
    client_socket, address = MyServer.accept()
    print("Connection from: ", address)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # add length field using "create_msg"
                packet = protocol.create_msg(response)
                # send to client
                client_socket.send(packet)
                if command == 'SEND_FILE':
                    # Send the data itself to the client
                    with open(PHOTO_PATH, 'rb') as f:
                        packet = f.read(response)
                        client_socket.send(packet)
                    # (9)
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    main()
