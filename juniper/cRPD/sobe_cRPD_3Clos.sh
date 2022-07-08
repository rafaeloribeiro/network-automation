#!/usr/bin/env bash
#
# Script para subida dos containers docker:
# e redes associadas
#   <rafael.ribeiro@ieee.org>
#

# Redes:

printf "\n%s\n\n" "Criando Redes de gerência e ponto-a-ponto:"
docker network create --driver bridge brd_mgmt_crpd --subnet 192.168.255.0/24 --gateway=192.168.255.1 --ipv6 --subnet 2001:db8:c0a8:ff::/64 --gateway=2001:db8:c0a8:ff::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf01_spine01 --internal --subnet 10.0.11.0/24 --gateway=10.0.11.1 --ipv6 --subnet 2001:db8:a0:b::/64  --gateway 2001:db8:a0:b::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf01_spine02 --internal --subnet 10.0.12.0/24 --gateway=10.0.12.1 --ipv6 --subnet 2001:db8:a0:c::/64  --gateway 2001:db8:a0:c::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf02_spine01 --internal --subnet 10.0.21.0/24 --gateway=10.0.21.1 --ipv6 --subnet 2001:db8:a0:15::/64 --gateway 2001:db8:a0:15::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf02_spine02 --internal --subnet 10.0.22.0/24 --gateway=10.0.22.1 --ipv6 --subnet 2001:db8:a0:16::/64 --gateway 2001:db8:a0:16::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf03_spine01 --internal --subnet 10.0.31.0/24 --gateway=10.0.31.1 --ipv6 --subnet 2001:db8:a0:1f::/64 --gateway 2001:db8:a0:1f::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf03_spine02 --internal --subnet 10.0.32.0/24 --gateway=10.0.32.1 --ipv6 --subnet 2001:db8:a0:20::/64 --gateway 2001:db8:a0:20::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf04_spine01 --internal --subnet 10.0.41.0/24 --gateway=10.0.41.1 --ipv6 --subnet 2001:db8:a0:29::/64 --gateway 2001:db8:a0:29::1 --attachable && sleep 2
#docker network create --driver bridge brd_leaf04_spine02 --internal --subnet 10.0.42.0/24 --gateway=10.0.42.1 --ipv6 --subnet 2001:db8:a0:2a::/64 --gateway 2001:db8:a0:2a::1 --attachable && sleep 2

# /29 test:
docker network create --driver bridge brd_leaf01_spine01 --internal --subnet 10.0.11.0/29 --gateway=10.0.11.1 --ipv6 --subnet 2001:db8:a0:b::/64  --gateway 2001:db8:a0:b::1 --attachable && sleep 2
docker network create --driver bridge brd_leaf01_spine02 --internal --subnet 10.0.12.0/29 --gateway=10.0.12.1 --ipv6 --subnet 2001:db8:a0:c::/64  --gateway 2001:db8:a0:c::1 --attachable && sleep 2
docker network create --driver bridge brd_leaf02_spine01 --internal --subnet 10.0.21.0/29 --gateway=10.0.21.1 --ipv6 --subnet 2001:db8:a0:15::/64 --gateway 2001:db8:a0:15::1 --attachable && sleep 2
docker network create --driver bridge brd_leaf02_spine02 --internal --subnet 10.0.22.0/29 --gateway=10.0.22.1 --ipv6 --subnet 2001:db8:a0:16::/64 --gateway 2001:db8:a0:16::1 --attachable && sleep 2
docker network create --driver bridge brd_leaf03_spine01 --internal --subnet 10.0.31.0/29 --gateway=10.0.31.1 --ipv6 --subnet 2001:db8:a0:1f::/64 --gateway 2001:db8:a0:1f::1 --attachable && sleep 2
docker network create --driver bridge brd_leaf03_spine02 --internal --subnet 10.0.32.0/29 --gateway=10.0.32.1 --ipv6 --subnet 2001:db8:a0:20::/64 --gateway 2001:db8:a0:20::1 --attachable && sleep 2
docker network create --driver bridge brd_leaf04_spine01 --internal --subnet 10.0.41.0/29 --gateway=10.0.41.1 --ipv6 --subnet 2001:db8:a0:29::/64 --gateway 2001:db8:a0:29::1 --attachable && sleep 2
docker network create --driver bridge brd_leaf04_spine02 --internal --subnet 10.0.42.0/29 --gateway=10.0.42.1 --ipv6 --subnet 2001:db8:a0:2a::/64 --gateway 2001:db8:a0:2a::1 --attachable && sleep 2

# Containers:

printf "\n%s\n\n" "Subindo containers cRPD:"
docker run --rm --detach --name cRPD-leaf01 -h cRPD-leaf01 --net=brd_mgmt_crpd --privileged -v cRPD-leaf01-config:/config -v cRPD-leaf01-varlog:/var/log -it crpd:21.2R1.10
docker run --rm --detach --name cRPD-leaf02 -h cRPD-leaf02 --net=brd_mgmt_crpd --privileged -v cRPD-leaf02-config:/config -v cRPD-leaf02-varlog:/var/log -it crpd:21.2R1.10
docker run --rm --detach --name cRPD-leaf03 -h cRPD-leaf03 --net=brd_mgmt_crpd --privileged -v cRPD-leaf03-config:/config -v cRPD-leaf03-varlog:/var/log -it crpd:21.2R1.10
docker run --rm --detach --name cRPD-leaf04 -h cRPD-leaf04 --net=brd_mgmt_crpd --privileged -v cRPD-leaf04-config:/config -v cRPD-leaf04-varlog:/var/log -it crpd:21.2R1.10
docker run --rm --detach --name cRPD-spine01 -h cRPD-spine01 --net=brd_mgmt_crpd --privileged -v cRPD-spine01-config:/config -v cRPD-spine01-varlog:/var/log -it crpd:21.2R1.10
docker run --rm --detach --name cRPD-spine02 -h cRPD-spine02 --net=brd_mgmt_crpd --privileged -v cRPD-spine02-config:/config -v cRPD-spine02-varlog:/var/log -it crpd:21.2R1.10

# Criando as intefaces de loopback:
docker exec -it cRPD-leaf01  ip -4 addr add 172.30.60.1/32 dev lo
docker exec -it cRPD-leaf02  ip -4 addr add 172.30.60.2/32 dev lo
docker exec -it cRPD-leaf03  ip -4 addr add 172.30.60.3/32 dev lo
docker exec -it cRPD-leaf04  ip -4 addr add 172.30.60.4/32 dev lo
docker exec -it cRPD-spine01 ip -4 addr add 172.30.60.5/32 dev lo
docker exec -it cRPD-spine02 ip -4 addr add 172.30.60.6/32 dev lo
docker exec -d cRPD-leaf01  ifconfig lo inet6 add 2001:db8:ac1e:3c::1/128
docker exec -d cRPD-leaf02  ifconfig lo inet6 add 2001:db8:ac1e:3c::2/128
docker exec -d cRPD-leaf03  ifconfig lo inet6 add 2001:db8:ac1e:3c::3/128
docker exec -d cRPD-leaf04  ifconfig lo inet6 add 2001:db8:ac1e:3c::4/128
docker exec -d cRPD-spine01 ifconfig lo inet6 add 2001:db8:ac1e:3c::5/128
docker exec -d cRPD-spine02 ifconfig lo inet6 add 2001:db8:ac1e:3c::6/128

# Associação de redes:
#   o 'sleep 1' e porque a VM pode dar algum problema se nao esperarmos

printf "\n%s\n\n" "Associando redes ponto-a-ponto aos containers:"
docker network connect brd_leaf01_spine01 cRPD-leaf01  && sleep 1
docker network connect brd_leaf01_spine01 cRPD-spine01 && sleep 1

docker network connect brd_leaf01_spine02 cRPD-leaf01  && sleep 1
docker network connect brd_leaf01_spine02 cRPD-spine02 && sleep 1

docker network connect brd_leaf02_spine01 cRPD-leaf02  && sleep 1
docker network connect brd_leaf02_spine01 cRPD-spine01 && sleep 1

docker network connect brd_leaf02_spine02 cRPD-leaf02  && sleep 1
docker network connect brd_leaf02_spine02 cRPD-spine02 && sleep 1

docker network connect brd_leaf03_spine01 cRPD-leaf03  && sleep 1
docker network connect brd_leaf03_spine01 cRPD-spine01 && sleep 1

docker network connect brd_leaf03_spine02 cRPD-leaf03  && sleep 1
docker network connect brd_leaf04_spine01 cRPD-spine01 && sleep 1

docker network connect brd_leaf04_spine01 cRPD-leaf04  && sleep 1
docker network connect brd_leaf03_spine02 cRPD-spine02 && sleep 1

docker network connect brd_leaf04_spine02 cRPD-leaf04  && sleep 1
docker network connect brd_leaf04_spine02 cRPD-spine02 && sleep 1

# Confirmando:
printf "\n%s\n\n" "Checando criação dos containers:"
docker ps

printf "\n%s\n\n" "Checando criação das redes:"
docker network ls | grep brd_

printf "\n%s\n\n" "Inspecionando as redes - conferência de conexões"
for i in `docker network ls | grep brd_ | awk '{print $1}'`; do docker network inspect $i | egrep "brd_|cRPD-leaf|cRPD-spine" ; done

printf "\n%s\n" "Fim!"
exit 2
