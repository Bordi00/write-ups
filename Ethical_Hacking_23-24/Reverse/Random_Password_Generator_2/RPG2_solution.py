from ctypes import CDLL
import pwn

port = 50150
host = "cyberchallenge.disi.unitn.it"

r = pwn.remote(host=host, port=port)
r.sendlineafter(b': ', "ciao".encode())
r.recvuntil(b': ')
p = r.recvline(keepends=False).decode()

libc = CDLL("libc.so.6")
for i in range(1, 32769):
    libc.srand(i)
    #print(i)
    password = ''.join([chr(libc.rand() % 0x5e + ord('!')) for _ in range(16)])   

    if p == password:
        print("found:" + password)
        break


password = ''.join([chr(libc.rand() % 0x5e + ord('!')) for _ in range(16)])
r.sendlineafter(b': ', password.encode())

r.recvline(keepends=False)
print(r.recvline(keepends=False))
