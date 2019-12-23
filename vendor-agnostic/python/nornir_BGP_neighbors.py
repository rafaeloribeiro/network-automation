#!/usr/local/bin/python3

__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@ieee.org'

# Library Imports
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking

nr = InitNornir(config_file="./nornir_config.yaml")

rtr_list = []
rtr_list.append(nr.filter(~F(site="SITE01") & ~F(groups__contains="BRAS")))
rtr_list.append(nr.filter(~F(site="SITE01") & F(groups__contains="BRAS"))) 
rtr_list.append(nr.filter(F(site="SITE02")))

print("\n-----------------------------------------")
print("\n          Gathering BGP neighbors")
print("\n-----------------------------------------")

count = 1

for item in rtr_list:
    r = item.run(
        task=networking.napalm_get,
        getters=['bgp_neighbors'] 
    )
    print_result(r)

print("\n ----------------- END  -----------------")
