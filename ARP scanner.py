#In summary, the ARP scan starts by sending an ARP request asking about the MAC address associated with the IP address 192.168.2.1.
#The received packet is a response, providing the requested information—mapping the IP address 192.168.2.1 to the MAC address 40:c7:29:fd:6b:88.
#This process helps in discovering live hosts on the network and their corresponding MAC addresses.

#scapy: This refers to the scapy library, which is a powerful packet manipulation library for Python. It allows you to create, send, and capture network packets.
import scapy.all as scapy

def arp_scan(ip):
    #using the scapy library to create an ARP (Address Resolution Protocol) request packet.
    #pdst=ip: This is an argument passed to the ARP class constructor. It specifies the destination IP address for which the ARP request is being made.
    arp_request = scapy.ARP(pdst=ip)

    #using the scapy library to create an Ethernet frame with a specific destination MAC address.
    #In Ethernet, the broadcast address is represented by all ones in the MAC address field (ff:ff:ff:ff:ff:ff).
    #Sending a frame to the broadcast address means that it will be received by all devices on the local network.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    #/ (Slash Operator): In the context of Scapy, the slash operator (/) is used for combining two layers of a packet.
    #It essentially stacks the arp_request layer on top of the broadcast layer, creating a new packet that contains both layers.
    arp_request_broadcast = broadcast/arp_request

    #This line is using the scapy library to send ARP request packets and receive responses
    #srp: This is a function within scapy that stands for "send and receive in packet mode." It is used for sending packets and receiving their responses.

    #[0]: The scapy.srp function returns a tuple containing two elements: a list of sent packets and a list of received packets.
    #In this line, [0] is used to access the first element of the tuple, which is the list of answered packets. = answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    answered_list, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    # Access the list of sent and received ARP packets (answered_list)
    for sent_packet, received_packet in answered_list:
        # Access information about the sent packet
        # Sent packets asks who has 192.168.2.1 says tell 192.168.2.243 (me)
        print("Sent Packet:", sent_packet.summary())
        # Access information about the received packet
        print("Received Packet:", received_packet.summary())

    # Access the list of received ARP packets (client_list)
    # It extracts information about the live hosts (IP and MAC addresses) from the ARP reply packets and organizes this information into a list of dictionaries. 
    clients_list = []
    for element in answered_list:
        # Extract IP address (psrc) and MAC address (hwsrc) from the received ARP reply packet
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
         # Add the extracted information to the clients_list
        clients_list.append(client_dict)
    return clients_list

def print_results(results_list):
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

# Example usage
#The "/24" denotes the subnet mask, and it means that the first 24 bits of the IP address are used for the network portion, leaving the remaining 8 bits for host addresses.
#In practical terms, this means there are 2^8 (256) possible host addresses in this subnet.
#Note that Network Address: 192.168.1.0 and Broadcast Address: 192.168.1.255 are reserved
#Routers set 192.168.1.1 as the IP address
target_ip = "192.168.2.1/24"  # Replace with your target IP or IP range
scan_result = arp_scan(target_ip)
print_results(scan_result)