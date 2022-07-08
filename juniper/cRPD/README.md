# cRPD
Examples for creating a six-container lab running Juniper's cRPD.

## Directory structure:
```
├── cRPD
│   ├── Mass_cRPD_sr_isis_configuration.yaml
│   ├── SR_MPLS_over_ISIS.j2
│   ├── ansible.cfg
│   ├── cRPD.list
│   ├── cRPD_inventory_data.yaml
│   ├── cRPD_router_configuration.py
│   ├── cRPD_routing_data.yaml
│   ├── cRPD_string_removal.yaml
│   ├── desce_cRPD_3Clos.sh
│   ├── get_container_info.yaml
│   ├── host_vars/
│   ├── network_state/
│   └── sobe_cRPD_3Clos.sh
```
## Bash scripts:
- ```sobe_cRPD_3Clos.sh```: creates the lab, while defining internal networks and interfaces.
- ```desce_cRPD_3Clos.sh```: destroys the lab, while deleting internal networks and interfaces.

## Ansible Playbooks
- ```cRPD_inventory_data.yaml```: Ansible playbook for collecting general data about the devices.
- ```cRPD_routing_data.yaml```: Ansible playbook for obtaining routing information from the devices.
- ```cRPD_string_removal.yaml```: Playbook crafted for removing those pesky "," charactes Ansible adds to generated files.
- ```get_container_info.yaml```: Simple playbook for getting Docker-level info on the containers.
- ```Mass_cRPD_sr_isis_configuration.yaml```: Playbook for configuring SR-MPLS on the devices.

## Python Scripts:
- ```cRPD_router_configuration.py```: Extracts device configuration.

## Data files:
- ```ansible.cfg```: General Ansible config file
- ```cRPD.list```: Ansible inventory
- ```SR_MPLS_over_ISIS.j2```: jinja2 template for configuring SR-MPLS (called by ```Mass_cRPD_sr_isis_configuration.yaml```)

## Other data:
- ```host_vars/```: Individual input files used for configuring SR-MPLS (called by ```Mass_cRPD_sr_isis_configuration.yaml```)
- ```network_state/```: Device collected info
