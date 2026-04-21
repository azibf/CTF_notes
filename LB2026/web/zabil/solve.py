from pwn import *
import subprocess

# Run the command


conn = remote('93.77.183.219', 1338)

conn.recvuntil(b"hashcash -mb26 ")
h =  conn.recvuntil(b"\n")
print(h)
result = subprocess.run(['hashcash', '-mb26', h[:-1].decode()], capture_output=True, text=True)
conn.recv(1024)
conn.send(result.stdout.encode())

conn.interactive()
conn.close()