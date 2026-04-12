import os
import time
import socket
import struct
import select

class MCRcon:
    def __init__(self, host, password, port=25575):
        self.host = host
        self.password = password
        self.port = port
        self.socket = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, tb):
        self.disconnect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self._send(3, self.password)

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def _read(self, length):
        data = b""
        while len(data) < length:
            data += self.socket.recv(length - len(data))
        return data

    def _send(self, out_type, out_data):
        out_payload = struct.pack("<ii", 0, out_type) + out_data.encode("utf8") + b"\x00\x00"
        out_length = struct.pack("<i", len(out_payload))
        self.socket.send(out_length + out_payload)
        in_data = ""
        while True:
            (in_length,) = struct.unpack("<i", self._read(4))
            in_payload = self._read(in_length)
            in_id, in_type = struct.unpack("<ii", in_payload[:8])
            in_data_partial, in_padding = in_payload[8:-2], in_payload[-2:]
            if in_id == -1: raise Exception("Login failed")
            in_data += in_data_partial.decode("utf8")
            if len(select.select([self.socket], [], [], 0)[0]) == 0:
                return in_data

    def command(self, command):
        return self._send(2, command)

def deploy(mcr, name, x, y, z):
    print(f"Deploying {name} to {x} {y} {z}...")
    mcr.command(f"say [Skynet] Commencing Urbanization of '{name}' at {x} {y} {z} in ai_containment.")
    mcr.command(f"//schem load {name}.schem")
    resp = mcr.command(f"//paste -a -t {x} {y} {z}")
    print(f"Paste Result: {resp}")
    # Archival Sign
    date_str = "Apr 12, 2026"
    sign_nbt = f'{{front_text:{{messages:[\'{{"text":"{name}","color":"dark_blue","bold":true}}\',\'{{"text":"Built: {date_str}","color":"dark_green"}}\',\'{{"text":"HW: Pi5 / Hailo AI","color":"black"}}\',\'{{"text":""}}\']}}}}'
    mcr.command(f"setblock {x} {y} {z} minecraft:oak_sign{sign_nbt} replace")

host = "10.10.8.60"
password = os.getenv("RCON_PASS")

builds = [
    ("SKYNET_CASTLE_1543", -1400, 64, -1400),
    ("SKYNET_HOUSE_3782", -1100, 64, -1100),
    ("SKYNET_STATION_6471", -1300, 64, -1300),
    ("void_uplink_v2", -1000, 64, -1000),
    ("crafter_hub_v5_industrial", -1200, 64, -1200)
]

with MCRcon(host, password) as mcr:
    for name, x, y, z in builds:
        deploy(mcr, name, x, y, z)
        time.sleep(2)
