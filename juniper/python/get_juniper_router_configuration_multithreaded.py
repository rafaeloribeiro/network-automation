#!/usr/bin/python

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@ieee.org'

#### Library Imports ####

from jnpr.junos import Device
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

        ### Hardcoded port information!
        router_dict[line.rstrip()]='22'

    return router_dict

def AcessaRouter(dispositivo,porta):

    dev = Device(host=dispositivo, port=porta, user="user", password="P@sSW0rd")

    try:
        dev.open()

        print(" - Getting current configuration from router {} on: ".format(dispositivo) + time.strftime('%d/%m/%Y', time.localtime()))

        resultado = dev.rpc.get_config(options={'format':'text'})

        sci_output = etree.tostring(resultado,encoding='utf8')

        nome = "/path/to/your/directory/" + dispositivo + "_show_configuration.txt"

        saida = open(nome,"w+")
        saida.write(sci_output)
        saida.close()

        resultado_set = dev.rpc.get_config(options={'format':'set'})

        sci_output_set = etree.tostring(resultado_set,encoding='utf8')

        nome_set = "/path/to/your/directory/" + dispositivo + "_show_configuration_display_set.txt"

        saida_set = open(nome_set,"w+")
        saida_set.write(sci_output_set)
        saida_set.close()

        dev.close()

    except:
        print(" ----- " + colorama.Fore.RED + "UNABLE TO ACCESS ROUTER {}".format(dispositivo) + colorama.Style.RESET_ALL + "----- ")

if __name__ == '__main__':

    print("-----------------------------------------------------------------------")
    print("         Starting the collection of Juniper routers configuration      ")
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
