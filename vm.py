#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
Here is the function of this python script:
get token.
get a list of virtual machines and shutdown.
take a snapshot of the powered-off virtual machine.
"""


import requests
import json

def get_token():
    keystone_url = 'http://controller:5000/v2.0/tokens'
    keystone_data = {
        "auth": {
            "tenantName": "admin",
            "passwordCredentials": {
                "username": "admin",
                "password": "123456"
            }
        }
    }
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    r = requests.post(url=keystone_url, data=json.dumps(keystone_data), headers=headers)
    returned_data = r.json()
    token = returned_data['access']['token']['id']
    return token

def vm():
    vm_token = get_token()
    vm_url = 'http://controller:8774/v2.1/servers/detail'
    vm_data = {
        "os-stop": None
    }
    r = requests.get(url=vm_url, headers={'X-Auth-Token':vm_token})
    returned_data = r.json()
    returned_data = returned_data['servers']
    for i in range(0, len(returned_data)):
        message = returned_data[i]
        vm = {}
        vm['id'] = message['id']
        vm['name'] = message['name']
        vm['status'] = message['status']
        if vm['status'] == 'ACTIVE':
            url = 'http://controller:8774/v2.1/servers/' + vm['id'] + '/action'
            vm_r = requests.post(url=url, data=json.dumps(vm_data), headers={'X-Auth-Token':vm_token})
        else:
            snapshot ={
                "createImage": {
                    "name": vm['name'],
                    "metadata": {}
                }
            }

            url = 'http://controller:8774/v2.1/servers/' + vm['id'] + '/action'
            snapshot_r = requests.post(url=url, data=json.dumps(snapshot), headers={'X-Auth-Token':vm_token})

if __name__ == "__main__":
    vm()
