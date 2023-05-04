import argparse #sluzy do parsowania argumentow wiersza polecen 
import socket  #interface do komunikacji sieciowej w pythonie (np tworzenie socektow)
import shlex    #analiza skladniowa ciagow znakow podobnyhc do wiersza polecen  - konwersja ciagow znakow na liste argumentow
import subprocess #ta bliblioteka podprocesow. zawiera interfejs tworzenia procesow, dajacych wiele sposobow na interakcje z programami klienckimi
import sys  #zapewnia dostep do zmiennych wykorzystywanych przez interpreter i funkcji wykorzystywanch przez interpreter
import textwrap #funkcje do formatowania tekstu (np. zwijanie i wycinanie) 
import threading #wsparcie dla wielowatkowosci.  Pozwala na tworzenie i zarządzanie wątkami, które są niezależnymi sekwencjami wykonywania w obrębie jednego procesu. 

def execute (cmd): # cmd jest poleceniem do wykoania 
    cmd = cmd.strip() #usuwa biale znaki z poczatku i konca argumentu cmd 
    if not cmd: #jezli zostal pusty ciag znakow return 
        return 
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT) #check_output - runs a command on the local operationg system and returns output 
    return output.decode()

                                #uwaga chatGPT napisal ponizsze 
#output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT): Ta linia wykonuje podane polecenie cmd jako proces systemowy. 
# Najpierw używa shlex.split(cmd) do podzielenia ciągu znaków cmd na listę argumentów w sposób podobny do powłoki systemowej. 
# Następnie subprocess.check_output uruchamia ten proces, pobierając wynik z jego standardowego wyjścia. 
# stderr=subprocess.STDOUT oznacza, że standardowe wyjście i błędy zostaną połączone w jednym strumieniu. Wynik jest przypisywany do zmiennej output.
# return output.decode(): Ta instrukcja zwraca wynik wykonania polecenia jako ciąg znaków. output.decode() dekoduje wynik jako tekst, ponieważ check_output zwraca bajty.

if __name__ == '__main__':
    parser = argparse.ArgumentParser( #1
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        #2
        epilog = textwrap.dedent('''Example:        
                                 netcat.py -t 192.168.1.108 -p 5555 -l -c                       # command shell
                                 netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt            # upload file
                                 netcat.py -t 192.168.1.108 -p 5555 -l =e=\"cat /etc/passwd\"   # execute command 
                                 echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135               # echo txt to server port 135
                                 netcat.py -t 192.168.1.108 -p 5555                             # connect to server
                                 '''))
    
    parser.add_argument('-c', '--command', action='store_true', help='command_shell') #3
    parser.add_argument('-e','--execute',help='execute secified command')
    parser.add_argument('-p', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=9001, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.1', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    
    args = parser.parse_args()
    if args.listen: #4
        buffer = ''
    else:
        buffer = sys.stdin.read()    
    nc = NetCat(args, buffer.encode())
    nc.run()
    
    
class NetCat:
    def __init__(self, args, buffer=None):  #1
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #2
        
    def run(self):
        if self.args.listen:
            self.listen()   #3
        else:
            self.send() #4
