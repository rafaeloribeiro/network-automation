#!/usr/bin/python3

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@ieee.org'

#### Library Imports ####

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree
import colorama
import csv
import time

#### Global Variables ####

data = time.strftime('%Y%m%d', time.localtime()) 

#### nome_arquivo="routers.txt"

def ListaRouters(arquivo):

    router_dict = {}

    #### Arquivo de Inventario ####

    with open(arquivo,"r") as input_file:
        # Formato arquivo:
        # ROTEADOR1;PORTA-SSH
        # ROTEADOR2;
        # (...)
        # ROTEADOR4;PORTA-SSH
        linereader = csv.reader(input_file, delimiter=';')
        for line in linereader:
            try:
                router_name = line[0]
                if line[1]:
                    router_port = line[1]
                    router_dict[router_name]=router_port
                else:
                    # Default porta 22 se não houver, mas exista o ";"
                    router_dict[router_name]="22"
            except:
                # Default porta 22 se não houver nada após o nome do roteador
                router_dict[router_name]="22"

    return router_dict

def AcessaRouter(dispositivo,porta,saida):

    #### AQUI ASSUME-SE QUE O USUARIO E SENHA SERAO OS MESMOS! ####

    dev = Device(host=dispositivo, port=porta, user="USUARIO", password="PASSWORD")

    try:
        dev.open(normalize=True)

        print(f' - Coletando inventario XML do roteador {dispositivo} na data de: ' + time.strftime('%d/%m/%Y', time.localtime()))

        resultado_inventory = dev.rpc.get_chassis_inventory()

        sch_output = etree.tostring(resultado_inventory, encoding='unicode',pretty_print=True)
        saida.write(f'{dev.user}@' + str(dispositivo) + '> show chassis hardware detail | display xml | no-more \n' + str(sch_output))
 
        dev.close()

    except ConnectError as err:
        dev.close()
        print(" ------- " + colorama.Fore.RED + "NAO FOI POSSIVEL ACESSAR O ATIVO {}. Erro: {} ".format(dispositivo,err) + colorama.Style.RESET_ALL + "------- ")

if __name__ == '__main__':

    print(f"---------------------------------------------------------------------------\n"
          f"|    Iniciando coleta de Inventario XML dos roteadores Juniper            |\n"
          f"|                        Data:  " + time.strftime('%d/%m/%Y', time.localtime())+ "                                |\n"
          f"---------------------------------------------------------------------------")
   
    dict_routers = ListaRouters("routers.txt")

    nome_out = "Router_XML_chassis_inventory.txt"

    saida = open(nome_out,"w+")

    for roteador,porta in dict_routers.items(): 
        AcessaRouter(roteador, porta, saida)

    saida.close()

    print(f"--------------------------------- FIM -------------------------------------\n")
