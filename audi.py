import os 
import threading
import re
#---------------------------------------#
def buscador (varto,contenido):
    resultado=re.search(varto,contenido)
    return resultado.start(), resultado.end()
#---------------------------------------#
def search(ip_adress):
    response=os.popen(f"ping -c 1 {ip_adress}").read()#DIRECCION IP PRIVADA
    response_mac=os.popen(f"arp -a {ip_adress}").read()#DIRECCION MAC SIN DESGLOSAR
    desglo_mac= response_mac[118:138] #DIRECCION MAC
    if "Tiempos aproximados de ida y vuelta en milisegundos" in response:
        print(f" ------------------------\n Se encontro en: {ip_adress} \n Direccion MAC: {desglo_mac} \n ------------------------ ")
#---------------------------------------#
def pass_wifi(varto):
    try:
        search_pass=os.popen("netsh wlan show profile").read()
        user_wifi=search_pass[buscador(varto,search_pass)[0]:buscador(varto,search_pass)[1]]
        pass_wifi=os.popen(f"netsh wlan show profile name={user_wifi} key=clear").read()
        bonus=pass_wifi[buscador("Contenido de la clave  :",pass_wifi)[0]:buscador(" de costos",pass_wifi)[0]-15]
        return user_wifi , pass_wifi, bonus
    except:ValueError
#-----------------MENU DE BUSQUEDA----------------------#
print("------------------------\nConectados en Red Wifi = 1")
print("------------------------\nContraseñas guardadas de Wifi= 2")
print("------------------------\nConectar a una red Wifi= 3")
print("------------------------\nInformacion red Wifi= 4\n------------------------")
#-------------------------------------------------------#
try:
    var=int(input(": "))
    #---------------CONDICIONALES------------------------#
    if var == 1:
        for ip in range(1,254):
            ipv4=os.popen("ipconfig").read()
            current_ip=(ipv4[buscador("IPv4. . . . . . . . . . . . . . :",ipv4)[1]:buscador(" de subred",ipv4)[0]-13]+str(ip))
        #----------------MULTIHILOS-----------------------#
            run=threading.Thread(target=search, args=(current_ip,))#Se envia como parametro la funcion y luego el parametro de la funcion
            run.start()
    #---------------------------------------#
    if var == 2:
        try:
            conten=os.popen("netsh wlan show profile").read()
            print(f'{conten[buscador("Perfiles de usuario",conten)[0]:-1]}-------------------')
            user_wifi= input("Escoja el usuario: ")
            print(f"------------------------\nUsuario: {pass_wifi(user_wifi)[0]}\n{pass_wifi(user_wifi)[2]}\n------------------------")
        except:print("NOMBRE DE RED INCORRECTO")
    #---------------------------------------#
    if var == 3:
        try:
            print(os.popen("netsh wlan show networks mode=bssid").read())
            nom_red=input("Nombre de red: ")
            os.popen(f"netsh wlan connect name={nom_red}")
        except ValueError:print("Try again...")
    #---------------------------------------#
    if var == 4:
        try:
            print(os.popen("netsh wlan show profile").read())
            nom_red=input("Nombre de red: ")
            print(os.popen(f"netsh wlan show profile {nom_red} key=clear").read())
        except ValueError:print("Try again...")
    #---------------------------------------#
except ValueError: print("Oops!  That was no valid number.  Try again...")