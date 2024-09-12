import pwn
from Crypto.Util.number import bytes_to_long, long_to_bytes, GCD

HOST = "cyberchallenge.disi.unitn.it"
PORT = None # TODO: change port

e = 65537

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

# messages
ct1 = encrypt(2)
ct2 = encrypt(4)
ct3 = encrypt(8)
ct4 = encrypt(64)

# values
val1 = (ct1**2) - ct2 
val2 = (ct3**2) - ct4

modulus = GCD(val1, val2)

# retrieve flag
token = (enc_flag * (2**e)) % modulus
decrypted_flag = decrypt(token) // 2
print(long_to_bytes(decrypted_flag).decode())

