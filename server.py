import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket tipo interger

server.bind((host, port)) # para pasar los datos de conexion
server.listen()
print(f"Server running on {host}:{port}")

clients = [] #almacenamos las conexiones de los clientes/usuarios
usernames = [] # almacenamos los datos (nombres) de los clientes

def broadcast(message, _client): # esta funcion envia el mensaje a todos los clientes
    for client in clients:
        if client != _client:
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024) # 1024 bytes el peso maximo del mensaje que el servidor puede recibir
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"Chatbot: {username} disconnected".encode('utf-8')) #sistema de codificacion encode, este mensaje no puede ser enviado como un dato str entonces loconvertimos a bytes
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"Chatbot: {username} joined the chat!".encode('utf-8')
        broadcast(message, client)
        client.send("connected to server".encode('utf-8'))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()

          