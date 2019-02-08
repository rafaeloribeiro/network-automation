#!/usr/bin/python

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rribeiro@juniper.net'

#### Library Imports ####

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree
from threading import Thread
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
    porta_base = 2200
    contador = 0

    #### Arquivo de Inventario ####

    routers=open(arquivo,"r")

    for line in routers:

        if "LAB" not in line:
            porta = porta_base + contador
        elif "RTEDLAB" in line:
            porta = 2280
        else:
            porta = 2281

        router_dict[line.rstrip()]=porta
        contador+=1

    return router_dict

def AcessaRouter(dispositivo,porta):

    print "--------------------------------------------------------------"

    #### Roteadores tem associacao com Tuneis SSH em portas crescentes, a partir de 2200 ####

    if "LAB" not in dispositivo:
        dev = Device(host="localhost", port=porta, user="F8042459", password="Quantum7!")
    elif "RTEDLAB01" in dispositivo:
        dev = Device(host="localhost", port=porta, user="03528759", password="Xuoqu9niengo")
    else:
        dev = Device(host="localhost", port=porta, user="timbbip", password="S3mfr0nt3ir4$")

    try:
        dev.open()

        print " Roteador: %s" % (dispositivo)
        
        if "master" in dev.facts["re_info"]['default']['1']:
            print " ###### ATENCAO! ERRO! RE1 e' a Master! para %s ###### " % dispositivo

        scre_output = dev.rpc.get_route_engine_information({'format':'text'})

        nome = "/home/rribeiro/TIM/network_state/" + dispositivo + "_show_chassis_routing_engine.txt"

        saida = open(nome,"w+")
        saida.write(etree.tostring(scre_output))
        saida.close()

        dev.close()

    except ConnectError as err:
        print " ---- ERRO: NAO FOI POSSIVEL ACESSAR O ATIVO %s %s---- " % (dispositivo,err)
        dev.close()

if __name__ == '__main__':

    print("-----------------------------------------------------------------------")
    print("   TIM: Iniciando coleta de informacoes de REs dos roteadores Juniper  ")
    print("-----------------------------------------------------------------------")

    lista = ListaRouters("routers")
   
    threads=[]

    for roteador,porta in lista.items(): 
        t=Thread(target=AcessaRouter(roteador, porta))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print "-------------------------- FIM -------------------------------\n"
