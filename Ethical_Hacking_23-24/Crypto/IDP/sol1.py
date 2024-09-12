import pwn
from Crypto.Util.number import long_to_bytes

HOST = "cyberchallenge.disi.unitn.it"
PORT = 50303

if pwn.args['REMOTE']:
    r = pwn.remote(host=HOST, port=PORT)
else:
    r = pwn.process(['python3', 'challenge.py'])


def encrypt(msg:int) -> int:
    """ 
    Function that sends a msg to the server for encrytion
    
    @param msg (int): msg to encrypt
    @return ciphertext to integer 
    """
    r.recvuntil(b' Check if a password is correct')
    r.sendlineafter(b'> ', '1'.encode())
    r.recvuntil(b'Choose a username')
    r.sendlineafter(b'> ', long_to_bytes(msg))
    r.recvuntil(b': ')
    c = r.recvline(keepends=False)
    return int(c)

def decrypt(token):
    """ 
    Function that sends a ciphertext to the server for decryption
    
    @param token (int): token to decrypt
    @return plaintext to int
    
    """
    r.recvuntil(b' Check if a password is correct')
    r.sendlineafter(b'> ', '2'.encode())
    r.recvuntil(b'Insert the password')
    r.sendlineafter(b'> ', str(token).encode())
    r.recvuntil(b': ')
    plaintext = r.recvline(keepends=False)
    return int(plaintext)
    
    
### ecrypted flag 
r.recvuntil(b': ')
enc_flag = int(r.recvline(keepends=False).strip())

message = encrypt(2)

token = enc_flag * message 

dec_flag = decrypt(token) // 2

print(long_to_bytes(dec_flag).decode())