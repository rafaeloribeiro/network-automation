#!/usr/bin/python

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@ieee.org'

# Library Imports

from threading import Thread
import os
import paramiko
import socket
import sys
import time

# Global Variables

data = time.strftime('%Y%m%d', time.localtime())


def ListaServers(arquivo):

    server_dict = {}

    # Arquivo de Inventario #
    # nome_arquivo="servers"

    servers = open(arquivo, "r")

    for line in servers:

        ### Hardcoded port value: 22
        server_dict[line.rstrip()] = '22'

    return server_dict


def AcessaServer(dispositivo, porta):

    lista_comandos_cli_linux = [
        "df -h",
        "ps -ef --sort=-%mem | head -20",
        "free -m"
    ]


    dev = paramiko.SSHClient()
    dev.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:

        dev.connect(dispositivo,porta, username='user', password='P@sSW0rd', timeout=1, look_for_keys=False)

        print(" - Getting server {} health check information ".format(dispositivo) + " on: " + time.strftime('%d/%m/%Y', time.localtime()))

        nome = "/path/to/your/directory/" + dispositivo + "_health_check.txt"

        saida = open(nome, "w+")

        for cli_comando in lista_comandos_cli_linux:
            print(" ---- Comando CLI: {}".format(cli_comando))
            saida.write("\n " + cli_comando + "\n")
            (std_in, std_out, std_err) = dev.exec_command(cli_comando,timeout=120,bufsize=8192)
            saida.write(std_out.read())

        saida.close()

        dev.close()

    except Exception as err:
        print(" ---- UNABLE TO ACCESS SERVER {}. Error:  {} ---- ".format(dispositivo, err))
        dev.close()


if __name__ == '__main__':

    print("-----------------------------------------------------------------------")
    print("               Starting server health checks collection                ")
    print("                        Date:  " + time.strftime('%d/%m/%Y', time.localtime()))
    print("-----------------------------------------------------------------------")

    dict_completo = ListaServers("servers")

    threads = []

    for servidor, porta in dict_completo.items():
        t = Thread(target=AcessaServer(servidor, porta))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("------------------------------ FIM ------------------------------------")
