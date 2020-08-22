import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style


def startup():
    folder = sys.argv[1]
    if not os.path.exists(folder):
        os.mkdir(folder)
    stored = []
    my_deque = deque()
    return folder, stored, my_deque


def process_and_write(inp: str,
                      folder: str,
                      stored: list,
                      my_deque: deque):
    '''
    Process the given inp URL and write the processed text into the appropriate
    file in folder, store the URL without the .com part in stored and my_deque
    '''
    processed = inp[0:inp.rfind('.')]

    ofile = f'{folder}\\{processed}.txt'
    with open(ofile, 'w') as f:
        if inp[:8] != "https://":
            r = requests.get("https://" + inp)
        elif inp[:8] == "https://":
            r = requests.get(inp)

        soup = BeautifulSoup(r.content, 'html.parser')
        filtered = soup.find_all(['p', 'a', 'title', 'ul', 'ol', 'li'])
        content = ''
        for item in filtered:
            if item.name == 'a':
                content += Fore.BLUE + item.text + '\n' + Style.RESET_ALL
            else:
                content += item.text + '\n'
        f.write(content)

    stored.append(processed)
    print(content)
    my_deque.append(content)

    return stored, my_deque


def open_stored(inp, folder, my_deque):
    with open(f'{folder}\\{inp}.txt') as f:
        doc = f.read()
        print(doc)
        my_deque.append(doc)
    return my_deque


def back_page(my_deque):
    if len(my_deque) > 0:
        my_deque.pop()
        x = my_deque.pop()
        print(x)
        my_deque.append(x)
    return my_deque


def main():
    f, st, dq = startup()
    inp = input()

    while inp != 'exit':
        if inp.find('.') != -1:  # if . is found in input
            st, dq = process_and_write(inp, f, st, dq)
        elif inp in st:
            dq = open_stored(inp, f, dq)
        elif inp == "back":
            dq = back_page(dq)
        else:
            print("Error: input a valid URL")
        inp = input()

init()
main()
