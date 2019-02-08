#!/usr/bin/python

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@ieee.org'

# Library Imports

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree
from threading import Thread
import re
import time

# Global Variables

data = time.strftime('%Y%m%d', time.localtime())


def ListaRouters(arquivo):

    router_dict = {}

    # Arquivo de Inventario #
    # nome_arquivo="routers"

    routers = open(arquivo, "r")

    for line in routers:

        ### Hardcoded port information!
        router_dict[line.rstrip()] = '22'

    return router_dict


def AcessaRouter(dispositivo, porta):

    lista_comandos_cli = [
        "show pfe statistics error",
        "show pfe statistics exceptions",
        "show tnp address"
    ]

    print("--------------------------------------------------------------")

    dev = Device(host=dispositivo, port=porta, user="user", password="P@sSW0rd")

    try:
        dev.open()
        dev.timeout = 600  # 10 minute timeout!

        print(" - Getting health check data from router {}".format(dispositivo) + " on: " + time.strftime('%d/%m/%Y', time.localtime()))
        print("--------------------------------------------------------------")

            nome = "/path/to/your/directory/" + dispositivo + "_health_check.txt"

            saida = open(nome, "w+")

            for cli_comando in lista_comandos_cli:
                print(" ---- Comando CLI: {}".format(cli_comando))
                saida.write("\n " + cli_comando + "\n")
                output = dev.cli(cli_comando, warning=False).encode('utf8')
                saida.write(output)

            dict_comandos_rpc = {
                dev.rpc.get_resource_monitor_summary_fpc_information({'format': 'text'}): 'get_resource_monitor_summary_fpc_information',
                dev.rpc.get_software_information({'format': 'text'}): 'get_software_information',
                dev.rpc.get_interface_information({'format': 'text'}, terse=True): 'get_interface_information (terse)',
                dev.rpc.get_bgp_summary_information({'format': 'text'}): 'get_bgp_summary_information',
                dev.rpc.get_bgp_group_information({'format': 'text'}): 'get_bgp_group_information',
                dev.rpc.get_ldp_session_information({'format': 'text'}): 'get_ldp_session_information',
                dev.rpc.get_lldp_neighbors_information({'format': 'text'}): 'get_lldp_neighbors_information',
                dev.rpc.get_route_summary_information({'format': 'text'}): 'get_route_summary_information',
                dev.rpc.get_isis_adjancency_information({'format': 'text'}): 'get_isis_adjacency_information',
                dev.rpc.get_ospf_neighbor_information({'format': 'text'}): 'get_ospf_neighbor_information',
                dev.rpc.get_pfe_statistics({'format': 'text'}): 'get_pfe_statistics',
                dev.rpc.get_system_alarm_information({'format': 'text'}): 'get_system_alarm_information',
                dev.rpc.get_alarm_information({'format': 'text'}): 'get_alarm_information',
                dev.rpc.get_power_usage_information({'format': 'text'}): 'get_power_usage_information',
                dev.rpc.get_system_core_dumps({'format': 'text'}): 'get_system_core_dumps',
                dev.rpc.get_route_engine_information({'format': 'text'}): 'get_route_engine_information',
                dev.rpc.get_firmware_information({'format': 'text'}): 'get_firmware_information',
                dev.rpc.get_craft_information({'format': 'text'}): 'get_craft_information',
                dev.rpc.get_fpc_information({'format': 'text'}): 'get_fpc_information',
                dev.rpc.get_pic_information({'format': 'text'}): 'get_pic_information',
                dev.rpc.get_fm_state_information({'format': 'text'}): 'get_fm_state_information',
                dev.rpc.get_fm_plane_state_information({'format': 'text'}): 'get_fm_plane_state_information',
                dev.rpc.get_fm_plane_location_information({'format': 'text'}): 'get_fm_plane_location_information',
                dev.rpc.get_fm_fpc_state_information({'format': 'text'}): 'get_fm_fpc_state_information',
                dev.rpc.get_chassis_inventory({'format': 'text'}): 'get_chassis_inventory',
                dev.rpc.get_environment_information({'format': 'text'}): 'get_environment_information',
                dev.rpc.get_environment_fpc_information({'format': 'text'}): 'get_environment_fpc_information',
                dev.rpc.get_environment_pem_information({'format': 'text'}): 'get_environment_pem_information',
                dev.rpc.get_environment_re_information({'format': 'text'}): 'get_environment_re_information',
                dev.rpc.get_database_replication_summary_information({'format': 'text'}): 'get_database_replication_summary_information',
                dev.rpc.get_subscriber_management_detail_information({'format': 'text'}): 'get_subscriber_management_detail_information',
                dev.rpc.get_subscribers_summary({'format': 'text'}): 'get_subscribers_summary',
                dev.rpc.get_license_summary_information({'format': 'text'}): 'get_license_summary_information'
            }

            for rpc_comando, comando_nome in dict_comandos_rpc.items():
                print(" ---- Comando RPC: {}".format(comando_nome))
                output = etree.tostring(rpc_comando)
                saida.write("\n " + comando_nome + "\n")
                saida.write(output)

            saida.close()

            dev.close()

        else:
            dev.close()

    except ConnectError as err:
        print(" ---- UNABLE TO ACCESS ROUTER {}. Error:  {} ---- ".format(dispositivo, err))
        dev.close()


if __name__ == '__main__':

    print("-----------------------------------------------------------------------")
    print("          Starting Juniper routers health check collection             ")
    print("                        Date:  " + time.strftime('%d/%m/%Y', time.localtime()))
    print("-----------------------------------------------------------------------")

    dict_completo = ListaRouters("routers")

    threads = []

    for roteador, porta in dict_completo.items():
        t = Thread(target=AcessaRouter(roteador, porta))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("------------------------------ END ------------------------------------")
