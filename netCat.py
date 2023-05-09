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
    #1 tworzymy command line interface za pomoca argparse
    parser = argparse.ArgumentParser( 
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        #2 wypisujemy guide dla usera jak uzywac naszego programu 
        epilog = textwrap.dedent('''Example:        
                                 netcat.py -t 192.168.1.108 -p 5555 -l -c                       # command shell
                                 netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt            # upload file
                                 netcat.py -t 192.168.1.108 -p 5555 -l =e=\"cat /etc/passwd\"   # execute command 
                                 echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135               # echo txt to server port 135
                                 netcat.py -t 192.168.1.108 -p 5555                             # connect to server
                                 '''))
    #3 dodajemy 6 argumentow ktore beda sterowac naszym programem
    parser.add_argument('-c', '--command', action='store_true', help='command_shell') #interactive shell
    parser.add_argument('-e','--execute',help='execute secified command')   #wykonuje jedna specificzna komende 
    parser.add_argument('-p', '--listen', action='store_true', help='listen')   #wskazuje ze bedzie urzywany listener 
    parser.add_argument('-p', '--port', type=int, default=9001, help='specified port')  #port do komunikacji 
    parser.add_argument('-t', '--target', default='192.168.1.1', help='specified IP')   #target ip
    parser.add_argument('-u', '--upload', help='upload file') #nazwa pliku do uploadu
    #-c -e -u wspolpracuja z -l (tylko w trybie listen)
    #-t -p wystarcza aby wskazac cel poalczenia 
    
    args = parser.parse_args()
    if args.listen: #4 kiedy korzystamy z opcji listenera tworzymy okiekt netCat z pustym bufferem 
        buffer = ''
    else:           # kiedy korzystamy z send do buffera idzie stdin
        buffer = sys.stdin.read()    
    nc = NetCat(args, buffer.encode())
    nc.run()
    
    
class NetCat:
# w Pythonie  __init__ to konstruktor klasy self jest koniecznie wymagane aby obiekt mog sie odwolac do parametrow    
    def __init__(self, args, buffer=None):  #1 inicjalizacja obiektu netcat wraz z argumentami z CLI i bufferem
        self.args = args #argumenty z lini polecen przekazywane do netCata
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #2 tworzymy obiekt socket
              
    def run(self):
        if self.args.listen:
            self.listen()   #3 jezeli nasluchujemy wywoluje metode listen
        else:
            self.send() #4 kiedy wysylamy dane wywola metode send
            
    def send(self):#1
        self.socket.connect((self.args.target, self.args.port)) # podwojne nawiasy poniewaz metoda connect wymaga przekazania tupli z adresem IP i portem a owa jest definiowana przez nawiasy okr
        if self.buffer:
            self.socket.send(self,buffer)
        try: #2
            while True: #3
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break   #4
                    if response: 
                        print(response)
                        buffer = input('> ')
                        buffer+= '\n'
                        self.socket.send(buffer.encode()) #5
        except KeyboardInterrupt: #6
            print('User terminated.')
            self.socket.close()
            sys.exit()
