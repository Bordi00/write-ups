import pwn


BLOCK_SIZE = 16

host = "cyberchallenge.disi.unitn.it"
port = 50301


if pwn.args['REMOTE']:
    r = pwn.remote(host=host, port=port)
else:
    r = pwn.process(['python3', 'challenge.py'])
    

# sign up
r.recvuntil(b"Login with a token")
r.sendlineafter(b"> ", bytes("1".encode("utf-8")))

r.recvuntil(b"Choose a username")
r.sendlineafter(b"> ", bytes("bdmin?desc?I am a boss".encode("utf-8")))

r.recvuntil(b"Insert a description of yourself")
r.sendlineafter(b"> ", bytes("xxxxxxxxxx".encode("utf-8")))

r.recvuntil(b': ')
ciphertext = bytes.fromhex(r.recvline(keepends=False).decode("utf-8"))


# IV: xxxxxxxxxxxxxxxx
# block1: desc=xxxxxxxxxx&
# block2: user=bdmin?desc?
# block3: I am a boss\0x05\0x05\0x05\0x05\0x05

plaintext = b"user=bdmin?desc?" # Original string 
goal = b"user=admin&desc="  # Traget string

block1 = ciphertext[16:32]
iv = pwn.xor(block1, plaintext, goal)

new_token = iv + ciphertext[32:]

r.recvuntil(b"Login with a token")
r.sendlineafter(b"> ", bytes("2".encode("utf-8")))
r.recvuntil(b"Insert the token (hex)")
r.sendlineafter(b"> ", new_token.hex().encode())
flag = r.recvline(keepends=False).decode("utf-8")
print(flag)
