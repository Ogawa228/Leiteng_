import socket
import struct


class RCONPacket(object):
    def __init__(self, ReqID=0, S1=0, ServerData=255, RecvData=255):
        self.RequestId = ReqID
        self.String1 = S1
        self.String2 = ""
        self.ServerData = ServerData
        self.RecvData = RecvData

    def OutputAsBytes(self):
        PacketSize = 4 + 4 + len(self.String1) + 1 + len(self.String2) + 1
        ByteArray = bytearray(struct.pack("<I", PacketSize))
        ByteArray += bytearray(struct.pack("<I", self.RequestId))
        ByteArray += bytearray(struct.pack("<I", self.ServerData))
        ByteArray += bytearray(self.String1.encode())
        ByteArray += b'\x00'
        ByteArray += bytearray(self.String2.encode())
        ByteArray += b'\x00'
        return ByteArray


class RconConnection(object):
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.password = password
        self.authenticated = False
        self.connect()
        if not self.authenticated:
            self.close()
            print("Failed to authenticate with server.")

    # do not call
    def connect(self):
        self.socket.connect((self.ip, self.port))
        self.auth()

    # do not call
    def auth(self):
        AuthPacket = RCONPacket(1, self.password, 3)
        self.socket.send(AuthPacket.OutputAsBytes())
        self.socket.recv(1024)
        response = self.socket.recv(1024)
        val = struct.unpack('<i', response[4:8])[0]
        if val > 0:
            self.authenticated = True

    def command(self, command):
        if self.authenticated:
            packet = RCONPacket(2, command, 2)
            self.socket.send(packet.OutputAsBytes())
            run = True
            text = ""
            while run:
                response = self.socket.recv(4100)
                numChars = struct.unpack('<I', response[:4])[0]
                text += response[12:-2].decode()
                if numChars < 4096:
                    run = False
            return text
        else:
            print("Command '" + command + "' failed because of authentication errors.")
            return ""

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    print(",".join(["0", "1", "2"]))
