import socket
import sys

def start_server(host='127.0.0.1', port=5555):
    """
    Creates a server that listens for incoming connections.
    The server receives messages from clients and sends responses back.
    """
    # Create a TCP socket using IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reuse of address to avoid "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind the socket to the specified host and port
        server_socket.bind((host, port))
        
        # Listen for incoming connections (max 5 queued connections)
        server_socket.listen(5)
        
        print(f"[*] Server listening on {host}:{port}")
        print("[*] Waiting for client connection...")
        
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"[+] Connection established with {client_address[0]}:{client_address[1]}")
        
        # Receive data from client
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                print("[-] Client disconnected")
                break
                
            message = data.decode('utf-8')
            print(f"[+] Received from client: {message}")
            
            # Send response back to client
            response = f"Server received: {message}"
            client_socket.send(response.encode('utf-8'))
            print(f"[+] Sent response to client: {response}")
            
            # Exit if client sends 'quit'
            if message.lower() == 'quit':
                print("[*] Client requested disconnect")
                break
        
        # Close connections
        client_socket.close()
        print("[*] Client connection closed")
        
    except KeyboardInterrupt:
        print("\n[*] Server shutdown requested")
    except socket.error as e:
        print(f"[!] Socket error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        server_socket.close()
        print("[*] Server socket closed")

if __name__ == "__main__":
    start_server()