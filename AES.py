
# Fortunately, we don’t need to implement AES from scratch
# to do so We have to first install "pycrypto" library
# -- pip install pycrypto


# pycrypto is a collection of both secure hash functions (such as SHA256 and RIPEMD160), and various encryption
# algorithms (AES, DES, RSA, etc.).
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# As of PyCrypto 2.1.0, PyCrypto provides an easy-to-use random number generator
from Crypto import Random
import base64

# taking key from user and hashing it (can generate random key also )
# hash key can be 16 bytes or 24 bytes or 32 bytes long
key = input("Enter your secret key: ")
# print(key)
hash_key = SHA256.new(key.encode()).digest()
print("Hashedn key for your secret key:")
print(hash_key)
len_hash_key = len(hash_key)
# print(len_hash_key)

# taking block size to be implemented in AES
block_size = input("Enter the block-size in bytes: ")
block_size = int(block_size)
print(block_size)


# Writing padding and unpadding functions
# padding: as AES algorithm works in blocks of ciphers,our message gets divides into blocks of ciphers which
# can be 128 or 192 or 256 bits long, we want our message in multiples of this numbers.thats why we padd our msg.
# unpadding can be used in time of decryption and padding in time of encryption
# example: lets take string "I love cats" len-11 after padding "I love cats ----" len-16
# padding character used here '-'


def padding(msg, blocks_size):
    padding_bytes_len = blocks_size - len(msg) % blocks_size
# The chr() method returns a character (a string) from an integer (unicode)
# we are generating padding char using padding_bytes_len
# we can also use any padding char as explained in above example such as -,= etc
    padded_char = chr(padding_bytes_len)
    padding_string = padding_bytes_len*padded_char
    padded_res = msg+padding_string
    return padded_res


def unpadding(msg):
    last_char = msg[len(msg) - 1:]
# The ord() function returns the number representing the unicode code of a character.
# as we added unicode code of character to make it padded we are removing same
    unpadded_bytes_len = ord(last_char)
    unpadded_res = msg[:-unpadded_bytes_len]
    return unpadded_res

# chr(3)=\x03
# so we adding 3 characters while padding
# while unpadding ord(\x03)=3
# so we removing 3 characters


# Encrypting Function
# Two modes of AES in pycryoto module
# using CBC mode (Cipher Blocker Chaining)
def encryption(message):
    # padding entered message
    message = padding(message, block_size)
    # generating a new random initialization_vector with the size of an AES block
    initialize_vector = Random.new()
    initialize_vector = initialize_vector.read(block_size)
    # creating AES cipher with our hash-key,in mode CBC and initialized vector
    cipher = AES.new(hash_key, AES.MODE_CBC, initialize_vector)
    # envoking encrypt function from generated cipher
    encrypted_text = cipher.encrypt(message.encode())
    # placing encrypted_text after initialization_vector and
    # converting back from bits to readable characters.
    return base64.b64encode(initialize_vector+encrypted_text)

# Decryption Function


def decryption(message):
    # converting message from characters to bits
    message = base64.b64decode(message)
    # extracting our intialization vector which will be first block_size bits of message
    initialize_vector = message[:block_size]
    # creating new cipher with our hash_key,in mode CBC and extracted intialized vector
    cipher = AES.new(hash_key, AES.MODE_CBC, initialize_vector)
    # envoking decrypt function from new cipher and decoding it into text
    plain_text = cipher.decrypt(message[block_size:]).decode("utf-8")
    # finally unpadding plain_text and returning
    return unpadding(plain_text)


# Testing algorithm
# asking for the message to test
input_text = input("Enter your msg to test algorithm: ")
cipher_text = encryption(input_text)
print("Encrypted_text is: ")
print(cipher_text)
decrypted_text = decryption(cipher_text)
print("Decrypted_text is: ")
print(decrypted_text)


# Sample input output

# Enter your secret key: Hello
# Enter the block-size in bytes: 16
# Enter your msg to test algorithm: I love cats
# Encrypted_text is: b'UyRjiGtZsA3Gc7C1M0RCakZVIIFlAfnNTa8h32+uuJA='
# Decrypted_text is: I love cats

# Enter your secret key: qazxswedcplmnko
# Enter the block-size in bytes: 16
# Enter your msg to test algorithm: I love cats
# Encrypted_text is:b'IkUR6G3s9e9E5p+aA6X2/kfJdlWTuytJhg49SjmideU='
# Decrypted_text is: I love cats

# Enter your secret key: qazxswedcplmnko
# Enter the block-size in bytes: 16
# Enter your msg to test algorithm: I love AES-algo
# Encrypted_text is:b'ZlFl33jqCtpb9v9YwfNFoZZfjJaRct6NgbMJ8ECY0ek='
# Decrypted_text is: I love AES-algo
