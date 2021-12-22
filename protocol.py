#   Ex. 2.7 template - protocol
import os


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    dataparts = data.split()
    if len(dataparts) == 0:
        return False
    if dataparts[0] not in ["TAKE_SCREENSHOT", "SEND_PHOTO", "DIR", "DELETE", "COPY", "EXECUTE", "EXIT"]:
        return False
    if dataparts[0] in ["DELETE", "EXECUTE"]:
        if os.path.isfile(dataparts[1]):
            return True
        else:
            return False
    if dataparts[0] == "COPY":
        if os.path.isfile(dataparts[1]) and os.path.isfile(dataparts[2]):
            return True
        else:
            return False
    if dataparts[0] == "DIR":
        if os.path.isdir(dataparts[1]):
            return True
        else:
            return False
    return True


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    length = str(len(data))
    filledlength = length.zfill(2)
    rdata = f"{str(filledlength)}{data}"
    return rdata.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    data = my_socket.recv(LENGTH_FIELD_SIZE)
    if not data:
        return False, "Error"
    length = int(data.decode())
    data = my_socket.recv(length)
    if not data:
        return False, "Error"
    return True, data.decode()
