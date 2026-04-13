import socket
import sys
from datetime import datetime

class PortScanner:
    """
    A simple port scanner that checks for open ports on a target host.
    Only use on authorized targets: localhost or scanme.nmap.org
    """
    
    def __init__(self, target):
        """Initialize scanner with target host"""
        self.target = target
        self.open_ports = []
        
    def scan_port(self, port):
        """
        Attempts to connect to a specific port on the target.
        Returns True if port is open, False otherwise.
        """
        try:
            # Create TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set timeout to avoid hanging on closed ports
            sock.settimeout(0.5)
            
            # Attempt connection
            result = sock.connect_ex((self.target, port))
            
            # Close socket
            sock.close()
            
            # Return True if connection successful (port is open)
            return result == 0
            
        except socket.gaierror:
            print(f"[!] Hostname could not be resolved: {self.target}")
            return False
        except socket.error as e:
            print(f"[!] Could not connect to port {port}: {e}")
            return False
            
    def scan_range(self, start_port, end_port):
        """
        Scans a range of ports on the target host.
        Displays open ports as they are found.
        """
        print(f"\n[*] Starting scan of {self.target}")
        print(f"[*] Scanning ports {start_port} to {end_port}")
        print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Scan each port in the range
        for port in range(start_port, end_port + 1):
            if self.scan_port(port):
                self.open_ports.append(port)
                print(f"[+] Port {port}: OPEN")
            else:
                print(f"[-] Port {port}: CLOSED", end='\r')
        
        print("\n")
        print(f"[*] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Found {len(self.open_ports)} open ports")
        
        if self.open_ports:
            print(f"[*] Open ports: {', '.join(map(str, self.open_ports))}")
        else:
            print("[*] No open ports found in specified range")
            
        return self.open_ports

def main():
    """Main function to run the port scanner"""
    print("=" * 60)
    print("SIMPLE PORT SCANNER")
    print("=" * 60)
    print("\nAUTHORIZED TARGETS ONLY:")
    print("  - localhost (127.0.0.1)")
    print("  - scanme.nmap.org")
    print("\nScanning unauthorized targets is illegal!")
    print("=" * 60)
    
    # Get target from user
    target = input("\nEnter target host (127.0.0.1 or scanme.nmap.org): ").strip()
    
    # Validate target
    if target not in ['127.0.0.1', 'localhost', 'scanme.nmap.org']:
        print("[!] Error: Only localhost and scanme.nmap.org are authorized targets")
        sys.exit(1)
    
    # Get port range from user
    try:
        start_port = int(input("Enter starting port number: "))
        end_port = int(input("Enter ending port number: "))
        
        # Validate port range
        if start_port < 1 or end_port > 65535:
            print("[!] Error: Port numbers must be between 1 and 65535")
            sys.exit(1)
            
        if start_port > end_port:
            print("[!] Error: Starting port must be less than or equal to ending port")
            sys.exit(1)
            
    except ValueError:
        print("[!] Error: Port numbers must be integers")
        sys.exit(1)
    
    # Create scanner and run scan
    try:
        scanner = PortScanner(target)
        scanner.scan_range(start_port, end_port)
    except KeyboardInterrupt:
        print("\n\n[*] Scan interrupted by user")
    except Exception as e:
        print(f"\n[!] Error during scan: {e}")

if __name__ == "__main__":
    main()