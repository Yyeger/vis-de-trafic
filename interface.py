from dataclasses import dataclass
from tkinter import *
from tkinter import ttk
from turtle import width

# Window
window = Tk()
window.geometry("1900x700")
window.title("Flow Graph - Project ")
window.resizable(False,False)
protocol_selected  = StringVar()
ip_selected = StringVar()

# Canvas parameters
cnv_main=Canvas(window, width=1400, height=500, bg="snow")
cnv_time= Canvas(window,width=120,height=500,bg = "snow")
cnv_comment= Canvas(window,width=370,height=500,bg = "snow")
cnv_filtrer= Canvas(window,width=2000,height=900,bg = "snow")
cnv_comment.create_text(70,10,text="Comment")
cnv_time.create_text(30,25,text="Time")
list_protocol = []
list_srcI = []
list_dstI = []
list_srcM = []
list_dstM = []
list_srcP = []
list_dstP = []
list_times = []
list_ip = []
list_comment = []
nb_ip = 0

def affichePort(i,dico_ip,srciP,dstiP,srcPort,dstPort,p):
    '''
        Affiche les ports dans l'interface , pour la trame 'i'. Les conditions sont ici pour des petits détails d'ajustement dans la fenêtre...
                                                                                                                                            '''
    if(srcPort[i]!= 0):
                if(dico_ip[srciP[i]][0] < dico_ip[dstiP[i]][0]): ## src ---> dst
                    if(int(srcPort[i]) < 1000 ):
                        cnv_main.create_text(dico_ip[srciP[i]][0]-15,p,text=srcPort[i],font =('Times',10))
                    else : 
                        cnv_main.create_text(dico_ip[srciP[i]][0]-25,p,text=srcPort[i],font =('Times',10))
                    if(int(dstPort[i]) < 1000 ):
                        cnv_main.create_text(dico_ip[dstiP[i]][0]+15,p,text=dstPort[i],font =('Times',10))
                    else : 
                        cnv_main.create_text(dico_ip[dstiP[i]][0]+25,p,text=dstPort[i],font =('Times',10))
                else :  ### dst <---- src 
                    if(int(srcPort[i]) < 1000 ):
                        cnv_main.create_text(dico_ip[srciP[i]][0]+15,p,text=srcPort[i],font =('Times',10))
                    else : 
                        cnv_main.create_text(dico_ip[srciP[i]][0]+25,p,text=srcPort[i],font =('Times',10))
                    if(int(dstPort[i]) < 1000 ):
                        cnv_main.create_text(dico_ip[dstiP[i]][0]-15,p,text=dstPort[i],font =('Times',10))
                    else : 
                        cnv_main.create_text(dico_ip[dstiP[i]][0]-25,p,text=dstPort[i],font = ('Times',10))
def v_scroll(*args):
    global cnv_main,cnv_comment,cnv_time
    cnv_main.yview(*args)
    cnv_time.yview(*args)
    cnv_comment.yview(*args)

def  init(srciP,dstiP,protocol,destMac,srcMac,srcPort,dstPort,times,comment):

    '''
        Initialise l'interface , en mettant les adresses iP,Mac , les ports , le temps ainsi que les commentaires.
                                                                                                            '''
    global list_ip,nb_ip
    x=100
    p = 70
    dico_ip = {}
    b=0
    p_x = 50 
    p_y = 80
    t = nb_ip*170
    for i in range(0,len(srciP)):
        
            if(srciP[i] not in list_ip):
                if(b%2 == 0):
                    cnv_main.create_text(x,10,text=srciP[i],font =('Times',10))
                    y = 15
                else :
                    cnv_main.create_text(x,20,text=srciP[i],font =('Times',10))
                    y = 25
                list_ip.append(srciP[i])
                dico_ip[srciP[i]] = [x,y]
                x+=150
                b+=1
            if(dstiP[i] not in list_ip):
                if(b%2 != 0):
                    cnv_main.create_text(x,25,text=dstiP[i],font =('Times',10))
                    y= 25
                else :
                    cnv_main.create_text(x,15,text=dstiP[i],font =('Times',10))
                    y = 15
                list_ip.append(dstiP[i])
                dico_ip[dstiP[i]] = [x,y]
                x+=150
                b+=1
            if(protocol[i] == "ARP"):
                cnv_main.create_rectangle(1, p_x, t, p_y, fill='misty rose',outline='')
            elif (protocol[i]== "ICMP"):
                cnv_main.create_rectangle(1, p_x, t, p_y, fill='light cyan',outline='')
            elif (protocol[i]== "TCP"):
                 cnv_main.create_rectangle(1, p_x, t, p_y, fill='#F0F0FF',outline='')
            elif (protocol[i]== "UDP"):
                 cnv_main.create_rectangle(1, p_x, t, p_y, fill='#999999',outline='')
            cnv_main.create_line(dico_ip[srciP[i]][0], p, dico_ip[dstiP[i]][0], p, arrow=LAST)
            affichePort(i,dico_ip,srciP,dstiP,srcPort,dstPort,p)
            cnv_comment.create_text(100,p-5,text=comment[i],font=('Times',9))
            cnv_time.create_text(50,p-5,text=times[i],font = ('Times',10))
            p+=30
            p_x+=30
            p_y+=30 
    x = 100
    for i in range(0 , len(list_ip)):
        cnv_main.create_line(x, 50,x, p_y-32, dash=(4,4))
        x+=150
    list_ip = []
    nb_ip = 0

def interface(srciP,dstiP,protocol,destMac,srcMac,srcPort,dstPort,times,comment):
  
    global nb_ip
    nb_ip = len(srciP)
    init(srciP,dstiP,protocol,destMac,srcMac,srcPort,dstPort,times,comment)

    '''
        Création de l'interface 
                            '''
    # Widgets
    scrollbarX = Scrollbar(window,orient="horizontal",width=50,  command=cnv_main.xview)
    scrollbarY = Scrollbar(window,orient="vertical",width=50,  command=v_scroll)

    protocol_cb = ttk.Combobox(cnv_filtrer, textvariable= protocol_selected)
    protocol_cb['values'] = ["All Flows","ICMP","ARP","TCP","UDP"]
    protocol_cb['state'] = 'readonly'
    protocol_cb.set("All Flows")

    ip_cb = ttk.Combobox(cnv_filtrer,textvariable=ip_selected)
    l_ip = ["All iP"]
    for i in range(len(srciP)):
        if srciP[i] not in l_ip:
            l_ip.append(srciP[i])
    ip_cb["values"] = l_ip
    ip_cb['state'] = 'readonly'
    ip_cb.set(l_ip[0])

   

    # Configure 

    cnv_main.configure(xscrollcommand=scrollbarX.set)
    cnv_main.configure(yscrollcommand=scrollbarY.set)
    cnv_main.configure(scrollregion=cnv_main.bbox("all"))
    cnv_time.configure(scrollregion=cnv_time.bbox("all"))
    cnv_comment.configure(scrollregion=cnv_comment.bbox("all"))

    # .pack()
    scrollbarY.pack(side=RIGHT,fill=Y)
    scrollbarX.pack(side=BOTTOM,fill=X)
    
    # .place() 
    cnv_main.place(x= 120,y = 0)
    cnv_time.place(x=0,y=0)
    cnv_comment.place(x=1500,y=0)
    cnv_filtrer.place(x=0,y=501)
    protocol_cb.place(x=1100,y=50)
    ip_cb.place(x=550,y=50)


    # Events 
    '''
        Associe les différentes boîtes à choix multiple à la fonction filtre
                                                                            '''
    protocol_cb.bind("<<ComboboxSelected>>",filtre)
    ip_cb.bind("<<ComboboxSelected>>",filtre)
    window.mainloop()

def filtre(event):
    '''
        Gère l'interface en la mettant à jour en fonction du filtre appliqué.
                                                                            '''
    global list_protocol ,list_srcI, list_dstI,list_srcM,list_dstM,list_srcP,list_dstP,list_times,list_comment,nb_ip
    cnv_main.delete(ALL)
    cnv_time.delete(ALL)
    cnv_comment.delete(ALL)
    cnv_comment.create_text(50,10,text="Comment")
    cnv_time.create_text(30,25,text="Time")
    l_protocol = []
    l_src = []
    l_dst = []
    l_srcM = []
    l_dstM = []
    l_srcP = []
    l_dstP = []
    l_times = []
    l_comment = []
    if(protocol_selected.get()=="All Flows" and ip_selected.get()=="All iP") : 
        nb_ip = len(list_srcI)
        init(list_srcI,list_dstI,list_protocol,list_dstM,list_srcM,list_srcP,list_dstP,list_times,list_comment)
    else :
        if(protocol_selected.get()=="All Flows") :
            for i in range(0,len(list_srcI)):
                if(ip_selected.get()==list_srcI[i]):
                    l_protocol.append(list_protocol[i])
                    l_src.append(list_srcI[i])
                    l_dst.append(list_dstI[i])
                    l_srcM.append(list_srcM[i])
                    l_dstM.append(list_dstM[i])
                    l_srcP.append(list_srcP[i])
                    l_dstP.append(list_dstP[i])
                    l_times.append(list_times[i])
                    l_comment.append(list_comment[i])
        elif(ip_selected.get()=="All iP"):
            for i in range(0,len(list_srcI)):
                if(protocol_selected.get()==list_protocol[i]):
                    l_protocol.append(list_protocol[i])
                    l_src.append(list_srcI[i])
                    l_dst.append(list_dstI[i])
                    l_srcM.append(list_srcM[i])
                    l_dstM.append(list_dstM[i])
                    l_srcP.append(list_srcP[i])
                    l_dstP.append(list_dstP[i])
                    l_times.append(list_times[i])
                    l_comment.append(list_comment[i])
        else :
            for i in range(0,len(list_srcI)):
                if(protocol_selected.get()==list_protocol[i] and ip_selected.get()==list_srcI[i]):
                    l_protocol.append(list_protocol[i])
                    l_src.append(list_srcI[i])
                    l_dst.append(list_dstI[i])
                    l_srcM.append(list_srcM[i])
                    l_dstM.append(list_dstM[i])
                    l_srcP.append(list_srcP[i])
                    l_dstP.append(list_dstP[i])
                    l_times.append(list_times[i])
                    l_comment.append(list_comment[i])
        nb_ip= len(l_src)+len(l_dst)
        init(l_src,l_dst,l_protocol,l_dstM,l_srcM,l_srcP,l_dstP,l_times,l_comment)

def start(srciP,dstiP,protocol,destMac,srcMac,srcPort,dstPort,times,comment):
    global list_protocol ,list_srcI, list_dstI,list_srcM,list_dstM,list_srcP,list_dstP,list_times,list_comment
    list_protocol = protocol        
    list_srcI = srciP
    list_dstI = dstiP
    list_srcM = srcMac
    list_dstM = destMac
    list_srcP = srcPort
    list_dstP = dstPort
    list_times = times
    list_comment = comment
    interface(srciP,dstiP,protocol,destMac,srcMac,srcPort,dstPort,times,comment)
