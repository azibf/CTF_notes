                """
DH MITM -- Diffie-Hellman Man-in-the-Middle CTF Challenge

TCP server simulating Alice and Bob performing a naive (unauthenticated)
Diffie-Hellman key exchange.  The connected client sits on the wire --
every message passes through them.

Protocol (newline-delimited JSON):

  S->C  {"from":"alice","to":"bob",  "message":{"type":"public_key","p":"0x...","g":"0x2","A":"0x..."}}
  C->S  {"to":"bob",                 "message":{"type":"public_key","p":"0x...","g":"0x2","A":"0x..."}}
  S->C  {"from":"bob",  "to":"alice","message":{"type":"public_key","B":"0x..."}}
  C->S  {"to":"alice",               "message":{"type":"public_key","B":"0x..."}}
  S->C  {"from":"alice","to":"bob",  "message":{"type":"encrypted","iv":"...","ciphertext":"..."}}
  C->S  {"to":"bob",                 "message":{"type":"encrypted","iv":"...","ciphertext":"..."}}
  S->C  {"type":"result","status":"ok"|"error"}
"""

import hashlib
import json
import os
import secrets
import socket
import threading

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# RFC 3526 Group 14 -- 2048-bit MODP prime
P = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF",
    16,
)
G = 2
KEY_BYTES = (P.bit_length() + 7) // 8  # 256

FLAG = os.environ.get("FLAG", "LB{sike_i_lied}")
PORT = int(os.environ.get("PORT", "9000"))


def _derive_key(shared: int) -> bytes:
    return hashlib.sha256(shared.to_bytes(KEY_BYTES, "big")).digest()


def handle(conn: socket.socket):
    def send(obj):
        conn.sendall(json.dumps(obj).encode() + b"\n")

    def recv():
        buf = b""
        while b"\n" not in buf:
            chunk = conn.recv(4096)
            if not chunk:
                raise ConnectionError
            buf += chunk
        return json.loads(buf[: buf.index(b"\n")])

    try:
        conn.settimeout(30.0)

        a = secrets.randbelow(P - 2) + 1
        b = secrets.randbelow(P - 2) + 1
        A = pow(G, a, P)
        B = pow(G, b, P)

        # Alice -> Bob: params + public key
        send({
            "from": "alice", "to": "bob",
            "message": {"type": "public_key",
                        "p": hex(P), "g": hex(G), "A": hex(A)},
        })
        fwd = recv()
        A_for_bob = int(fwd["message"]["A"], 16)

        # Bob -> Alice: public key
        send({
            "from": "bob", "to": "alice",
            "message": {"type": "public_key", "B": hex(B)},
        })
        fwd = recv()
        B_for_alice = int(fwd["message"]["B"], 16)

        # shared secrets (each side sees the MITM-supplied value)
        alice_shared = pow(B_for_alice, a, P)
        bob_shared = pow(A_for_bob, b, P)

        # Alice encrypts the flag
        alice_key = _derive_key(alice_shared)
        iv = secrets.token_bytes(16)
        enc = Cipher(algorithms.AES(alice_key), modes.CFB(iv)).encryptor()
        ct = enc.update(FLAG.encode()) + enc.finalize()

        send({
            "from": "alice", "to": "bob",
            "message": {"type": "encrypted",
                        "iv": iv.hex(), "ciphertext": ct.hex()},
        })
        fwd = recv()

        # Bob decrypts
        bob_key = _derive_key(bob_shared)
        fwd_iv = bytes.fromhex(fwd["message"]["iv"])
        fwd_ct = bytes.fromhex(fwd["message"]["ciphertext"])
        dec = Cipher(algorithms.AES(bob_key), modes.CFB(fwd_iv)).decryptor()
        pt = (dec.update(fwd_ct) + dec.finalize()).decode(errors="replace")

        if pt == FLAG:
            send({"type": "result", "status": "ok"})
        else:
            send({"type": "result", "status": "error"})

    except (ConnectionError, socket.timeout, json.JSONDecodeError,
            KeyError, ValueError):
        pass
    finally:
        conn.close()


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(8)
    print(f"DH-MITM listening on :{PORT}", flush=True)
    while True:
        conn, _ = srv.accept()
        threading.Thread(target=handle, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    main()
