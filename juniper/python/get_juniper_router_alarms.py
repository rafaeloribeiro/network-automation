#!/usr/bin/python

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@ieee.org'

#### Library Imports ####

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree
from threading import Thread
import colorama
import pprint
import os
import re
import sys
import time
import multiprocessing as mp

#### Global Variables ####

data = time.strftime('%Y%m%d', time.localtime()) 

#### nome_arquivo="routers"

def ListaRouters(arquivo):

    router_dict = {}

    #### Arquivo de Inventario ####

    routers=open(arquivo,"r")

    for line in routers:

        ### Hardcoded port value: 22
        router_dict[line.rstrip()]='22'

    return router_dict

def AcessaRouter(dispositivo,porta):

    dev = Device(host=dispositivo, port=porta, user="user", password="P@sSW0rd")

    try:
        dev.open()

        print(" - Getting alarms from the device {} on: ".format(dispositivo) + time.strftime('%d/%m/%Y', time.localtime()))

        resultado_chassis = dev.rpc.get_alarm_information({'format':'text'})
        resultado_system = dev.rpc.get_system_alarm_information({'format':'text'})

        sca_output = etree.tostring(resultado_chassis,encoding='utf8', pretty_print=True)
        ssa_output = etree.tostring(resultado_system,encoding='utf8', pretty_print=True)

        nome = "/path/to/your/directory/routers_show_chassis_system_alarms.txt"

        saida = open(nome,"a+")

        # Somente serao inseridos em arquivo os roteadores com alarmes!

        if "No alarms currently active" in sca_output and "No alarms currently active" in ssa_output:
            print("   ---> " + colorama.Fore.GREEN + "No alarms found on device {}.".format(dispositivo) + colorama.Style.RESET_ALL + " --- ")

        else:
            print("   ---> " + colorama.Fore.RED + "Alarms were found on device {}.".format(dispositivo) + colorama.Style.RESET_ALL + " <--- ")
            print("   ---> " + colorama.Fore.RED + "Please check router_show_chassis_system_alarms.txt file" + colorama.Style.RESET_ALL + " <--- ")
            saida.write(dispositivo)
            saida.write("\n --- show chassis alarms: ----\n" + sca_output)
            saida.write(" --- show system alarms:  ----\n" + ssa_output)
            saida.close()

        dev.close()

    except ConnectError as err:
        dev.close()
        print(" ------- " + colorama.Fore.RED + "UNABLE TO ACCESS DEVICE {}. Error: {} ".format(dispositivo,err) + colorama.Style.RESET_ALL + "------- ")

if __name__ == '__main__':

    print("-----------------------------------------------------------------------")
    print("              Starting Juniper routers alarm collection                ")
    print("                        Date:  " + time.strftime('%d/%m/%Y', time.localtime()))
    print("-----------------------------------------------------------------------")

    lista = ListaRouters("routers")

    threads=[]

    for roteador,porta in lista.items(): 
        t=Thread(target=AcessaRouter(roteador, porta))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("------------------------------- END -----------------------------------\n")
