"""
DH MITM -- Starter Code

Connect to the DH exchange server and act as a transparent proxy.
Your job: modify the messages to perform a man-in-the-middle attack
and recover the encrypted secret.

    python starter.py [host] [port]
"""

import hashlib
import json
import socket
import sys
import secrets


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HOST = sys.argv[1] if len(sys.argv) > 1 else "111.88.147.123"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9000


def _derive_key(p, shared: int) -> bytes:
    key_bytes = (p.bit_length() + 7) // 8  
    return hashlib.sha256(shared.to_bytes(key_bytes, "big")).digest()


def connect():
    sock = socket.create_connection((HOST, PORT), timeout=30)
    buf = b""

    def recv():
        nonlocal buf
        while b"\n" not in buf:
            chunk = sock.recv(4096)
            if not chunk:
                raise ConnectionError
            buf += chunk
        idx = buf.index(b"\n")
        line, buf = buf[:idx], buf[idx + 1 :]
        msg = json.loads(line)
        print(f"<-- {msg}")
        return msg

    def send(obj):
        print(f"--> {obj}")
        sock.sendall(json.dumps(obj).encode() + b"\n")

    return recv, send


def main():
    recv, send = connect()

    msg = recv()
    p = int(msg["message"]["p"], 16)
    g = int(msg["message"]["g"], 16)
    A = int(msg["message"]["A"], 16)
    
    #evil 
    e = secrets.randbelow(p - 2) + 1
    E = pow(g, e, p)
    print(E)
    msg["message"]["A"] = hex(E)
    send({"to": "bob", "message": msg["message"]})

    msg = recv()
    B = int(msg["message"]["B"], 16)
    msg["message"]["B"] = hex(E)
    send({"to": "alice", "message": msg["message"]})

    msg = recv()
       

    iv = bytes.fromhex(msg["message"]["iv"])
    ct = bytes.fromhex(msg["message"]["ciphertext"])

    keyA = _derive_key(p, pow(A, e, p))
    dec = Cipher(algorithms.AES(keyA), modes.CFB(iv)).decryptor()
    pt = (dec.update(ct) + dec.finalize()).decode(errors="replace")
    print(pt)
    #keyB = _derive_key(p, pow(B, e, p))
    #enc = Cipher(algorithms.AES(keyB), modes.CFB(iv)).encryptor()
    #ct = enc.update() + enc.finalize()
    send({"to": "bob", "message": msg["message"]})

    result = recv()
    print(f"\nResult: {result['status']}")


if __name__ == "__main__":
    main()
