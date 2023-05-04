import socket
import threading
IP ='0.0.0.0'
PORT = 9998

def main():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT)) #1 przekazujemy IP i adres na ktorym chcemy aby serwer sluchal
        server.listen(5) #2 mowimy serwerowi aby zacza sluchac z maksymalna iloscia oczekujacych polaczen w kolejce ustawiona na5
        print(f'[*] Listenieng on {IP}:{PORT}')
        while True:
            client, address = server.accept() #3 Metoda accept() zwraca krotkę, która zawiera dwa elementy: obiekt client i krotkę address.
            # print(f'len address: {len(address)}')
            # print(f'client: {client}')
            # print(f'address:{address}\n')
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            clientHandler = threading.Thread(target=handleClient, args=(client,)) #tworzymy nowy obiekt watku wskazujacy na funkcje handleClient i przekazanym socketem klienta 
            clientHandler.start() #4 uruchamiamy watek do obslugi polaczenia klienta 
            
def handleClient(clientSocket): #5 funkcja handle client wykonuje recv
    with clientSocket as sock:
        request = sock.recv(1024)
        print(f'[*] Recived: {request.decode("utf-8")}') #robimy decoding bo otrzymujemy wiadomosc binarna 
        sock.send(b'ACK')
if __name__=='__main__':
    main()