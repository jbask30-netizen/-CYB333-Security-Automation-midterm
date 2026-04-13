import socket
import sys

def start_client(host='127.0.0.1', port=5555):
    """
    Creates a client that connects to the server.
    The client sends messages to the server and receives responses.
    """
    # Create a TCP socket using IPv4
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set a timeout for connection attempts
    client_socket.settimeout(5)
    
    try:
        # Attempt to connect to the server
        print(f"[*] Attempting to connect to {host}:{port}...")
        client_socket.connect((host, port))
        print(f"[+] Successfully connected to server at {host}:{port}")
        
        # Remove timeout after successful connection
        client_socket.settimeout(None)
        
        # Send and receive messages
        while True:
            # Get user input
            message = input("\nEnter message to send (or 'quit' to exit): ")
            
            # Send message to server
            client_socket.send(message.encode('utf-8'))
            print(f"[+] Sent to server: {message}")
            
            # Receive response from server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"[+] Server response: {response}")
            
            # Exit if user types quit
            if message.lower() == 'quit':
                print("[*] Disconnecting from server...")
                break
                
    except socket.timeout:
        print("[!] Connection timeout - server may not be running")
    except ConnectionRefusedError:
        print("[!] Connection refused - server is not running or not accepting connections")
    except socket.error as e:
        print(f"[!] Socket error: {e}")
    except KeyboardInterrupt:
        print("\n[*] Client shutdown requested")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()
        print("[*] Client socket closed")

if __name__ == "__main__":
    start_client()