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

print("\n----------------------------------------------------------") 

count = 1

for item in rtr_list:
    r = item.run(
        task=networking.napalm_get,
        getters=['facts']
    )

    for k,v in r.items():
        print("{:2d}  Device: {} | Model: {:7s} | OS: {:10s}".format(count,k,r[k].result["facts"]["model"],r[k].result["facts"]["os_version"]))
        count+=1

print("\n----------------------------------------------------------") 
