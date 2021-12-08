#!/usr/bin/env python3

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@br.routzgroup.com'

#### Library Imports ####

from jnpr.junos import Device
from lxml import etree
import colorama
import pprint
import os
import re
import sys
import time

#### Global Variables ####

data = time.strftime('%Y%m%d', time.localtime()) 

def AcessaRouter(dispositivo):

    dev = Device(host=dispositivo, port="22", user="root", password="Juniper123")

    try:
        dev.open()

        print(" - Coletando configuracoes do ativo {} na data de: ".format(dispositivo) + time.strftime('%d/%m/%Y', time.localtime()))

        resultado = dev.rpc.get_config(options={'format':'text'})

        sci_output = etree.tostring(resultado,encoding='utf8')

        nome = "network_state/" + dispositivo + "_show_configuration.txt"

        saida = open(nome,"w+")
        saida.write(f"{sci_output}")
        saida.close()

        resultado_set = dev.rpc.get_config(options={'format':'set'})

        sci_output_set = etree.tostring(resultado_set,encoding='utf8')

        nome_set = "network_state/" + dispositivo + "_show_configuration_display_set.txt"

        saida_set = open(nome_set,"w+")
        saida_set.write(f"{sci_output_set}")
        saida_set.close()

        dev.close()

    except Exception as exc:
        print(" ----- " + colorama.Fore.RED + "ERRO: NAO FOI POSSIVEL ACESSAR O ATIVO {} {}".format(dispositivo,exc) + colorama.Style.RESET_ALL + "----- ")

if __name__ == '__main__':

    print("-----------------------------------------------------------------------")
    print("    cRPD: Iniciando coleta de configuracoes dos roteadores Juniper     ")
    print("-----------------------------------------------------------------------")

    lista = [
        "cRPD-leaf01",
        "cRPD-leaf02",
        "cRPD-leaf03",
        "cRPD-leaf04",
        "cRPD-spine01",
        "cRPD-spine02"
            ]

    for roteador in lista: 
        AcessaRouter(roteador)

    print("------------------------------- FIM -----------------------------------\n")

