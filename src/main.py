#!/usr/bin/env python3
from socket import *
import os
import sys
import struct
import time
import select
import binascii

# Constants
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

# The checksum function calculates the checksum of the packet.
def checksum(data):
    """
    Compute the Internet Checksum of the supplied data.
    The checksum is computed as the 16-bit one's complement of the one's complement sum of all 16-bit words.
    """
    csum = 0
    countTo = (len(data) // 2) * 2
    count = 0
    while count < countTo:
        # Combine two bytes into one 16-bit number
        thisVal = data[count+1] * 256 + data[count]
        csum += thisVal
        csum = csum & 0xffffffff  # Keep it 32-bit
        count += 2
    if countTo < len(data):
        csum += data[len(data)-1]
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum += (csum >> 16)
    answer = ~csum & 0xffff
    # Swap bytes (for little endian)
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# The build_packet() function constructs an ICMP Echo Request packet.
def build_packet():
    """
    Build an ICMP Echo Request packet.
    Create a header with a dummy checksum, then calculate the correct checksum
    and rebuild the header before returning the complete packet.
    """
    myChecksum = 0
    pid = os.getpid() & 0xFFFF  # Use process ID as identifier
    # Create a dummy header with a zero checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, pid, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the header and data.
    myChecksum = checksum(header + data)
    # Convert checksum to network byte order.
    myChecksum = htons(myChecksum)
    # Rebuild the header with the correct checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, pid, 1)
    packet = header + data
    return packet

# The get_route() function sends the ICMP echo requests with increasing TTL values.
def get_route(hostname):
    """
    Trace the route to the specified hostname by sending ICMP echo requests with increasing TTL values.
    """
    destAddr = gethostbyname(hostname)
    print("Traceroute to %s (%s), %d hops max:" % (hostname, destAddr, MAX_HOPS))
    
    for ttl in range(1, MAX_HOPS + 1):
        for tries in range(TRIES):
            try:
                # Fill in start: Create a raw socket using ICMP.
                mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
                # Fill in end

                # Set the TTL for the socket.
                mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
                mySocket.settimeout(TIMEOUT)
                packet = build_packet()
                mySocket.sendto(packet, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], TIMEOUT)
                howLongInSelect = time.time() - startedSelect
                if whatReady[0] == []:  # Timeout
                    print("  %d    *        *        *    Request timed out." % ttl)
                    continue

                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                
            except timeout:
                # If a timeout occurs, try again for this TTL.
                continue
            else:
                # Fill in start: Extract the ICMP type from the received packet.
                # The IP header is 20 bytes, so the ICMP header starts at byte 20.
                icmpHeader = recvPacket[20:28]
                icmp_type, code, recvChecksum, pID, sequence = struct.unpack("bbHHh", icmpHeader)
                types = icmp_type
                # Fill in end

                if types == 11:  # Time Exceeded (TTL expired in transit)
                    bytes_in_double = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes_in_double])[0]
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - t) * 1000, addr[0]))
                elif types == 3:  # Destination Unreachable
                    bytes_in_double = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes_in_double])[0]
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - t) * 1000, addr[0]))
                elif types == 0:  # Echo Reply (destination reached)
                    bytes_in_double = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes_in_double])[0]
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - timeSent) * 1000, addr[0]))
                    return  # Destination reached; stop traceroute.
                else:
                    print("error: unexpected ICMP type %d" % types)
                    break
            finally:
                mySocket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <hostname>")
        sys.exit(1)
    get_route(sys.argv[1])
