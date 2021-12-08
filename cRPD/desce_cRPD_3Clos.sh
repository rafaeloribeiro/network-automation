#!/usr/bin/env bash
#
# Script para desligamento dos containers docker:
# e redes associadas
#   <rafael.ribeiro@ieee.org>
#

# Desassociação de redes:

printf "\n%s\n\n" "Desconectando os containers de cada rede:"
docker network disconnect brd_leaf01_spine01 cRPD-leaf01
docker network disconnect brd_leaf01_spine01 cRPD-spine01

docker network disconnect brd_leaf01_spine02 cRPD-leaf01
docker network disconnect brd_leaf01_spine02 cRPD-spine02

docker network disconnect brd_leaf02_spine01 cRPD-leaf02
docker network disconnect brd_leaf02_spine01 cRPD-spine01

docker network disconnect brd_leaf02_spine02 cRPD-leaf02
docker network disconnect brd_leaf02_spine02 cRPD-spine02

docker network disconnect brd_leaf03_spine01 cRPD-leaf03
docker network disconnect brd_leaf03_spine01 cRPD-spine01

docker network disconnect brd_leaf03_spine02 cRPD-leaf03
docker network disconnect brd_leaf04_spine01 cRPD-spine01

docker network disconnect brd_leaf04_spine01 cRPD-leaf04
docker network disconnect brd_leaf03_spine02 cRPD-spine02

docker network disconnect brd_leaf04_spine02 cRPD-leaf04
docker network disconnect brd_leaf04_spine02 cRPD-spine02

# Containers:

printf "\n%s\n\n" "Parando os containers:"
for i in `docker ps | grep cRPD- | awk '{print $1}'`; do docker stop $i ; done

# Redes:

printf "\n%s\n\n" "Removendo as redes:"
for i in `docker network ls | grep brd_ | awk '{print $1}'`; do docker network rm $i ; done

# Confirmando:

printf "\n%s\n\n" "Checando se há containers rodando:"
docker ps

printf "\n%s\n\n" "Checando remoção das redes:"
docker network ls

printf "\n%s\n\n" "Checando remoção das redes - Inspeção:"
for i in `docker network ls | grep brd_ | awk '{print $2}'`; do docker network inspect $i | egrep "brd_|cRPD-leaf|cRPD-spine" ; done

printf "\n%s\n" "Fim!"
exit 2
