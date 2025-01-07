import socket

# Create a raw socket and bind it to the public interface
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
sniffer.bind(("192.168.29.2", 0))  # Replace with your IP address

# Include the IP headers in the captured packets
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# Enable promiscuous mode
sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# Receive packets in an infinite loop
while True:
    # print(f"Packet from {addr}:")
    packet = sniffer.recvfrom(65565)
    print(packet)