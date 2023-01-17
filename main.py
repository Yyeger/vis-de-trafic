import time
import json
import sys
import os
import codecs
import interface

regex = ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B','C','D','E','F', '1','2','3','4','5','6','7','8','9','0']
#chars possible pour un valeur hexadecimal

starttime = time.time()  #le timer commence
times = []
array = []
offsets = []
fichier = 'trames.txt'
if len(sys.argv) == 2:
    fichier = sys.argv[1] #j'utilise le fichier ecrit en ligne de comande pour lire les trames
file =  open(fichier, 'r')
line = []
trames = 0
for x in file:
    temp = x.split(' ') #suprimer les espaces

    temp[len(temp) - 1] = temp[len(temp) - 1].strip('\n') #supprimer le dernier character d'une ligne "\n"

    if temp[0] == '': #ne considerer pas les lignes vides
        continue
        
    offsets.append(int(temp[0],16))
   
    if temp[0] == "0000":   #no repetition
        offsets = []
        trames += 1
        if trames != 1:
            array.append(line) #je stocke la trame entiere
            times.append(round(float((time.time() - starttime))*10000.0,9)) #je stoke le temps de lecture de la trame
            line = []
            
 
    if len(offsets) > 1: #control offsets
        if offsets[len(offsets)-1] < offsets[len(offsets)-2]:
            print("error in offsets")
        
    del temp[0] #je supprime le char au debut de la ligne de le quelle j'ai pas besoin
    del temp[0]
    del temp[0]
    for elem in temp:
        if len(elem) != 2:
            print(elem, "error in length") #control length
        if elem[0] not in regex or elem[1] not in regex:
            print("error in regex")  #control regex
            
    line +=  temp
    
array.append(line) #je stocke la derniere trame
times.append(round(float((time.time() - starttime))*10000.0,9))



def HexToDec(liste):

    if len(liste) == 6:  #pour les adress MAC j'utilise les deux points
        dec = ""
        for x in liste:
            dec += x + ":"
        return dec[:len(dec)-1] 
        
    dec = ""
    for x in liste:
        dec += str(int(x, 16)) + "."

    return dec[:len(dec)-1]  

def HexSumtoDec(liste):
    tot = ""
    for x in liste:
        tot += x

    return HexToDec([tot])

def HexToType(protocol):
    #du valeur hexadecimal au protocol!
    if int(protocol, 16) == 1: #type
        return "ICMP"
    elif int(protocol, 16) == 6:
        return "TCP"
    elif int(protocol, 16) == 17:
        return "UDP"
    else:
       return "inconnue"


#function pour des creeres des listes avec les valeurs de chaque trame:
def DestAddIP():
    liste = []
    for i in range(trames):
        liste.append(HexToDec(array[i][30:34]))
    return liste

def SrcAddIP():
    liste = []
    for i in range(trames):
        liste.append(HexToDec(array[i][26:30]))
    return liste

def DestAddMAC():
    liste = []
    for i in range(trames):
        liste.append(HexToDec(array[i][0:6]))
    return liste

def SrcAddMAC():
    liste = []
    for i in range(trames):
        liste.append(HexToDec(array[i][6:12]))
    return liste

def SrcAddMAC():
    liste = []
    for i in range(trames):
        if type()[i] == "UDP" or type()[i] == "TCP":
            liste.append(HexSumtoDec(array[i][34:36]))
        else:
            liste.append(0)
    return liste


#seulement les trames UDP et TCP ont le numero de port
def DestPort():
    liste = []
    for i in range(trames):
        if type()[i] == "UDP" or type()[i] == "TCP":
            liste.append(HexSumtoDec(array[i][36:38]))
        else:
            liste.append(0)
    return liste

def SrcPort():
    liste = []
    for i in range(trames):
        if type()[i] == "UDP" or type()[i] == "TCP":
            liste.append(HexSumtoDec(array[i][38:40]))
        else:
            liste.append(0)
    return liste

def type(): #donnez le type a partir de valuer hexa de la trame ethernet
    liste = []
    for i in range(trames):
        if array[i][12:14][0]+array[i][12:14][1] == "0806":
            liste.append("ARP")
        elif array[i][12:14][0]+array[i][12:14][1] == "8035":
            liste.append("RARP")
        elif array[i][12:14][0]+array[i][12:14][1] == "0800":
            liste.append(HexToType(array[i][23]))
        else:
            liste.append("inconnue")

    return liste

def commentaire(): #return un liste avec le comment a afficher pour chaque trame dans l'interface graphique
    liste = []
    for i in range(trames):
        if type()[i] == "ICMP":
            liste.append("type: " + HexSumtoDec(array[i][34]) + ", code: " + HexSumtoDec(array[i][35]))
        elif type()[i] == "ARP" or type()[i] == "RARP": 
            liste.append("Who has " + HexToDec(array[i][32:38])+"? Tells "+HexToDec(array[i][22:28]))
        elif type()[i] == "UDP":
            port = "DNS"
            if DestPort()[i] == 67 or SrcPort()[i] == 67 or DestPort()[i] == 68 or SrcPort()[i] == 68:
                port = "DHCP"
            if DestPort()[i] == 123 or SrcPort()[i] == 123:
                port = "NTP"
            liste.append("port reservé:" + port)
        elif type()[i] == "TCP":
            if tcp(i)["Source Port"]=="80" or tcp(i)["Destination Port"] == "80": #pour les messages HTTP
                liste.append("Method: " + http(i)["Method"] + ", URI: " +  http(i)["URI"] + ", Version: " + http(i)["Version"])
            else:
                port = ""
                if DestPort()[i] == 21 or SrcPort()[i] == 21:
                    port = "[FTP] "
                synackfin = ""
                if tcp(i)["SYN"] == 1:
                    synackfin += "[SYN] "
                if tcp(i)["ACK"] == 1:
                    synackfin += "[ACK] "
                if tcp(i)["FIN"] == 1:
                    synackfin += "[FIN] "            
                liste.append(port + synackfin + "Seq=" + HexSumtoDec(array[i][38:42])+ ", Ack="+ HexSumtoDec(array[i][42:46]))
        else:
            liste.append("inconnue")
    return liste






#fonctions qui return un dictionaire avec l'analyse de tous l'entete du paquet:
def ethernet(i):
    return {
            "DestMAC": HexToDec(array[i][0:6]), 
            "SrcMAC" : HexToDec(array[i][6:12]),
            "type" : type()[i],
            #"data" : array[i][14:]
            }

def ip(i):
    return {
            "Version" : array[i][14][0],
            "IHL" : array[i][14][1],
            "TOS" : array[i][15],
            "Total Length" : HexSumtoDec(array[i][16:18]),
            "Identification" : HexSumtoDec(array[i][18:20]),
            "Flags" : str(bin(int(array[i][20], 16)).zfill(8)[0:3]),
            "Fragment Offset" : str(bin(int(array[i][20], 16))[3:]) + str(bin(int(array[i][21], 16))),
            "TTL:" : HexSumtoDec(array[i][22]),
            "Protocol": HexSumtoDec(array[i][23]),
            "Header Checksum" : array[i][24] + array[i][25],
            "SrcIP" : SrcAddIP()[i],
            "DestIP" : DestAddIP()[i],
            #"data" : array[i][34:]
        }

def icmp(i):
    return {
            "type": HexSumtoDec(array[i][34]), 
            "code" : HexSumtoDec(array[i][35]),
            "Checksum" : HexSumtoDec(array[i][36:38]),
            }

def arp(i):
    return {
            "Hardware": "0x"+(array[i][14])+(array[i][15]), 
            "Protocol" : "0x"+(array[i][16])+(array[i][17]),
            "Hlen" : HexSumtoDec(array[i][18]),
            "Tlen" : HexSumtoDec(array[i][19]),
            "Operation" : "0x"+(array[i][20])+(array[i][21]),
            "Sender HA": HexToDec(array[i][22:28]),
            "Sender IA": HexToDec(array[i][28:32]),
            "Target HA": HexToDec(array[i][32:38]),
            "Target IA": HexToDec(array[i][38:42]),
            }

def udp(i):
    return {
            "Source Port": HexSumtoDec(array[i][34:36]), 
            "Destination Port" : HexSumtoDec(array[i][36:38]),
            "Length" : HexSumtoDec(array[i][38:40]),
            "Checksum" : HexSumtoDec(array[i][40:42]),
            #"data" : array[i][42:]
            }
            
def tcp(i):
    return {
            "Source Port": HexSumtoDec(array[i][34:36]), 
            "Destination Port" : HexSumtoDec(array[i][36:38]),
            "Sequence Number" : HexSumtoDec(array[i][38:42]),
            "Acknowledgment Number" : HexSumtoDec(array[i][42:46]),
            "Offset" : str(bin(int(array[i][46], 16))[:4]),
            "Reserved" : str(bin(int(array[i][46], 16))[4:]) + str(bin(int(array[i][47], 16))[:2]),
            "URG" : str(bin(int(array[i][47], 16))[1]),
            "ACK" : str(bin(int(array[i][47], 16))[2]),
            "PSH" : str(bin(int(array[i][47], 16))[3]),
            "RST" : str(bin(int(array[i][47], 16))[4]),
            "SYN" : str(bin(int(array[i][47], 16))[5]),
            "FIN" : str(bin(int(array[i][47], 16))[6]),
            "Window" : HexSumtoDec(array[i][48:50]),
            "Checksum" : HexSumtoDec(array[i][50:52]),
            "Urgent Pointer" : HexSumtoDec(array[i][52:54]),
            #"data" : array[i][54:]
            }

def http(i):

    entete = array[i][54:]
    word = ""
    values = []
    for elem in entete:
        if elem == '20' or elem == '0d' or elem == '0a':
            if word == "":
                continue
                
            values.append((codecs.decode(word,"hex")).decode('utf-8')) #de hexadecimal au ASCII
            
            word = ""
        else:
            word += elem

    dic = {
            "Method" : values[0],
            "URI" : values[1],
            "Version" : values[2],
            values[3] : values[4],
            values[5] : values[6]
            } 
        
    return dic

#pour la trame i preleve l'analise de chaque entete de tous le paquets de cette trame.
def trameTotal(i):
    res = {
        "Ethernet" : ethernet(i), 
    }

    if type()[i] == "ARP" or type()[i] == "RARP" :
            res["ARP"] = arp(i)
            return res
            
    res["IP"] = ip(i)

    if type()[i] == "ICMP":
        res["ICMP"] = icmp(i)
    elif type()[i] == "UDP":
        res["UDP"] = udp(i)
    elif type()[i] == "TCP":
        res["TCP"] = tcp(i)
        if tcp(i)["Source Port"]=="80" or tcp(i)["Destination Port"] == "80":
            #print("hola")
            res["HTTP"] = http(i)
    else:
        res["inconnue" : "Trame non riconnue!"]

    #print(DestPort()[i], SrcPort()[i])

    
 
    return res



#ecrit dans le fichier output.txt trameTotal() pour chaque trame
def output():
    if os.path.exists('output.txt'):
      os.remove('output.txt')

    for i in range(len(array)):
        print("Trame n°" + str(i+1), file=open('output.txt', 'a'))
        pretty = json.dumps(trameTotal(i), indent=4) #pour rendre plus simple la lecture
        print(pretty+"\n", file=open('output.txt', 'a'))


output()
interface.start(SrcAddIP(), DestAddIP(), type(),DestAddMAC(),SrcAddMAC(),DestPort(),SrcPort(),times,commentaire())



