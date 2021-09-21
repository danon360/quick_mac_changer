#!/usr/bin/env python
import codecs

from scapy.all import *

conf.checkIPaddr=False

# configuration
localiface = 'wlan0'
requestMAC = '7c:b0:c1:fe:30:da'
myhostname='kali'
localmac = '7c:b0:c1:fe:30:da'
#localmacraw = requestMAC.replace(':','').decode('hex')
localmacraw = codecs.decode(requestMAC.replace(':',''),'hex')

def change_mac(mac_addr):
    subprocess.call(["sudo", "ifconfig", localiface,
                     "down"])
    subprocess.call(["sudo", "ifconfig", localiface,
                     "hw", "ether", mac_addr])
    subprocess.call(["sudo", "ifconfig", localiface,
                     "up"])
def discover():
     # prepare DHCP DISCOVER
    dhcp_discover = Ether(src=localmac, dst='ff:ff:ff:ff:ff:ff')/IP(src='0.0.0.0', dst='255.255.255.255')/UDP(dport=67, sport=68)/BOOTP(chaddr=localmacraw,xid=RandInt())/DHCP(options=[('message-type', 'discover'), 'end'])
    print(dhcp_discover.display())

    # send discover, wait for reply
    dhcp_offer = srp1(dhcp_discover,iface=localiface, verbose=1)
    #print(dhcp_offer.display())
    
    return dhcp_offer

def request(offered_ip, server_ip, xid):
     dhcp_request = Ether(src=localmac, dst='ff:ff:ff:ff:ff:ff')/IP(src='0.0.0.0', dst='255.255.255.255')/UDP(dport=67, sport=68)/BOOTP(chaddr=localmacraw,xid=xid)/DHCP(options=[('message-type', 'request'),("server_id",server_ip),("requested_addr",offered_ip),("hostname", myhostname), 'end'])
     print(dhcp_request.display())
     
     # send request, wait for ack
     dhcp_ack = srp1(dhcp_request,iface=localiface)
     print(dhcp_ack.display())
     return dhcp_ack
 

if __name__ == "__main__":

    requestMAC = '7c:b0:c1:fe:30:db'
    localmac = '7c:b0:c1:fe:30:db'
    #change_mac(requestMAC)
    localmacraw = codecs.decode(requestMAC.replace(':',''),'hex')
    dhcp_offer = discover() 
    exit()
    # craft DHCP REQUEST from DHCP OFFER
    myip=dhcp_offer[BOOTP].yiaddr
    sip=dhcp_offer[BOOTP].siaddr
    xid=dhcp_offer[BOOTP].xid

    print(myip)
    print(sip)
    print(xid)

    dhcp_ack = request(myip, sip,xid)
