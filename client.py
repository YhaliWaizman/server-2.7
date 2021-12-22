import socket
import protocol


IP = "localhost"
# The path + filename where the copy of the screenshot at the client should be saved
SAVED_PHOTO_LOCATION = "C:\\Users\\cyberclass\\Desktop\\VSCodePythonYhali\\screen.jpg"


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    length = my_socket.recv(2)
    data = my_socket.recv(int(length))
    if cmd != "SEND_PHOTO":
        print(data.decode())
    # (10) treat SEND_PHOTO
    elif cmd == "SEND_PHOTO":
        # (9)
        with open(SAVED_PHOTO_LOCATION, "wb") as f:
            f.write(data)
        print("Photo saved to " + SAVED_PHOTO_LOCATION)


def main():
    # open socket with the server

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, 11111))

    # print instructions
    print('Welcome to remote computer application. Available commands are:')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
