'''
Help on module csv2yaml:

NAME
    csv2yaml - This module converts a csv file containing network assets
into an Ansible-readable inventory

'''
__author__ = 'Rafael de Oliveira Ribeiro'
__email__ = 'rafael.ribeiro@ieee.org'

#### Library Imports ####

import os
import re
import time

#### Global Variables ####

data = time.strftime('%Y%m%d', time.localtime())

def touch(fname):
    '''

    Simple function to check if a file exists. If true, it will update
    the file's timestamp; otherwise, it will create it.

    '''

    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

#### file_name='hosts.csv'

def read_csv(file_name):
    '''
    This function will create a dictionary based on the input .csv file

    It is assumed that the CSV file will have the following structure:

        device,ipaddr,port,user,pw,group(optional)

    The output dictionary has the following structure:

        device_dict['device']= ['ipaddr','port','user','pw','group']

    If the device has no group assigned, this function will assume these
    two options:

      1) If the 'port' is equal to 23, the device will be inserted on the
         'all_telnet' group.
      2) Else, it will be added to an 'other' group. Mind you that these
         devices will not have their inventory collected by the either the
         ansible ad-hoc commands or the playbook destined for the
         telnet-accessible devices.

    '''

    device_dict = {}

    #### CSV file ####

    with open(file_name,'r') as devices:

        for line in devices:

            device_data_list = []

            if re.match(r'^\#',line):
                pass
            else:
                key = line.split(',')

                for column in key[1:]:

                    # This avoids listing the '\n' character found at the end
                    # of lines.
                    device_data_list.append(column.rsplit('\n')[0])

                # Checking for absent group information, on the last column.
                if device_data_list[-1] == '':
                    if device_data_list[1] == '23':
                        device_data_list[-1]='all_telnet'
                    else:
                        device_data_list[-1]='others'

                device_dict[key[0]]=device_data_list

    return device_dict

def create_group_dictionary(device_dict):
    '''
    This function creates a group dictionary, based on the device_dict that
    was created on the read_csv function.

    In other words, the devices will be arranged by the group that is on the
    'device_data_list' of each device entry.

    {'group01': {
        'device01': ['device01','ipaddr01','port01','user01','pw01'],
        'device02': ['device02','ipaddr02','port02','user02','pw02']
        },
     'group02': {
        'device03': ['device03','ipaddr03','port03','user03','pw03'],
        'device04': ['device04','ipaddr04','port04','user04','pw04']
        },
     ...
    }

      -- groups_dict['group'] will return a dictionary whose keys are the
         device names

    '''

    groups_dict = {}  # Return variable empty groups dictionary

    all_groups = []   # Empty group list

    for chave,valor in device_dict.items():

        temp_dict = {}  # Empty temporary dictionary
        temp_list = []  # Empty temporary list

        temp_list.append(chave)

        for item in valor:
            temp_list.append(item)

        temp_dict[chave] = temp_list

        # Inserting just the group name in this list.
        # It is the last column of the list object.
        all_groups.append(valor[-1])

    # Creating a list of all unique groups
    all_groups = list(dict.fromkeys(all_groups))

    # Iterating through the groups, creating the return dictionary
    for group in all_groups:

        inner_dict = {}   # Empty groups dictionary

        for abscissa,ordenada in device_dict.items():
            # Remember, the last column of the input dictionary's lists
            # contains the group.
            if ordenada[-1] == group:
                inner_dict[abscissa] = [abscissa,ordenada[:-1]]

        groups_dict[group] = inner_dict

    return groups_dict

def create_ansible_inventory(groups_dict):
    '''
    This function creates an Ansible Inventory, based on the 'groups_dict'
    that was created on the 'create_group_dictionary' function.

    A simple inventory template is as follows:

    [group01]
    device01 ansible_host=2001:db8:abcd::1:1 ansible_port=22
    device02 ansible_host=2001:db8:abcd::1:2 ansible_port=4000

    [group01:vars]
    ansible_user="group01_user"
    ansible_ssh_pass="group01_pass"

    ...

    [groupNN]
    deviceN1 ansible_host=2001:db8:ef01::1:1 ansible_port=2200
    deviceN2 ansible_host=2001:db8:ef01::1:2 ansible_port=2221

    [groupNN:vars]
    ansible_user="groupNN_user"
    ansible_ssh_pass="groupNN_pass"

    At first, it is assumed that the groups:vars will be the same.

    TODO: Check for individual access credentials and then create
          and save under the "host_vars" directory

    The output of this function is the inventory file itself, named as
    'inventory.list'

    '''

    file_name='inventory.list'
    touch(file_name)

    with open('inventory.list', 'w') as output_file_name:
        for groups,lists in groups_dict.items():

            # Printing group header info:

            group_header_string = "[" + str(groups) + "]\n"
            output_file_name.write(str(group_header_string))

            # Iterating through the 'lists' dictionary, so as to gather
            # every host from a particular group:

            for chave,valor in lists.items():
                host_string = chave + " ansible_host=" + valor[1][0] \
                  + " ansible_port=" + valor[1][1] +"\n"
                output_file_name.write(str(host_string))

            # We now go to the vars section.

            group_var_header_string = "\n[" + str(groups) + ":vars]\n"
            output_file_name.write(str(group_var_header_string))

            # Iterating again through the 'lists' dictionary, so as to
            # gather every host from a particular group:
            #    WIP: make it efficient: avoid this second lookup.
            #
            # CAVEAT: as this stands today, the last host information is
            # the one that will be sent to the final file!

            for chave,valor in lists.items():
                user_string = 'ansible_user="' + valor[1][2] + '"\n'
                if valor[1][1] == '23':
                    pass_string = 'ansible_password="' + valor[1][3] + '"\n'
                else:
                    pass_string = 'ansible_ssh_pass="' + valor[1][3] + '"\n'

            # Adding network_cli connection string
            conn_string = 'ansible_connection=network_cli' + '\n'

            # We're assuming all devices will be Juniper, running Junos.
            os_string = 'ansible_network_os=junos' + '\n\n'

            output_file_name.write(str(user_string))
            output_file_name.write(str(pass_string))
            output_file_name.write(str(conn_string))
            output_file_name.write(str(os_string))


if __name__ == '__main__':

    print('')
    print(' Extracting host information to be used as an Ansible Inventory '\
          .center(80, '*'))
    print('')
    print(' 1) Reading input CSV file')

    device_list = read_csv('hosts.csv')

    print(' 2) Creating group-oriented dictionary')

    group_list = create_group_dictionary(device_list)

    print(' 3) Creating the Inventory itself\n')

    create_ansible_inventory(group_list)

    print('>> File is ready for inspection at: inventory.list <<'\
          .center(80,'='))
    print('')
    print(' Exiting '.center(80, '*'))
    print('')
