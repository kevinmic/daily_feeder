from os import system

def printer(header, lines):
    #system('clear')
    print(header)
    print('-------')
    for line in lines:
        print(line)
