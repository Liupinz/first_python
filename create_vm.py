#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import urllib2
import urllib
import json
import random
import time

def curl_keystone():
    url='http://controller:5000/v2.0/tokens'
    values={
        "auth": {
            "tenantName":"admin",
            "passwordCredentials": {
                "username":"admin",
                "password":"123456"
            }
        }
    }
    data=json.dumps(values)
    headers={'content-type':'application/json','accept':'application/json'}
    request=urllib2.Request(url,data,headers)
    keystone_response=urllib2.urlopen(request)
    returned_data=json.loads(keystone_response.read())
    token = returned_data['access']['token']['id']
    return token

def get_nova_id():
    ntoken = curl_keystone()
    url = 'http://controller:8774/v2.1/servers'
    headers = {'content-type':'application/json','accept':'application/json'}
    req = urllib2.Request(url)
    req.add_header('X-Auth-Token',ntoken)
    response = urllib2.urlopen(req)
    data = response.read()
    ddata = json.loads(data)
    list = ddata['servers']
    nova_id = []
    for i in range(len(list)):
        ID = list[i]['id']
        nova_id. append(ID)
    return nova_id 

def get_flavor_id():
    ftoken = curl_keystone()
    url = 'http://controller:8774/v2.1/flavors'
    headers = {'content-type':'application/json','accept':'application/json'}
    req = urllib2.Request(url)
    req.add_header('X-Auth-Token',ftoken)
    response = urllib2.urlopen(req)
    data = response.read()
    ddata = json.loads(data)
    list = ddata['flavors']
    flavor_id = []
    for i in range(len(list)):
        ID = list[i]['id']
        flavor_id.append(ID)
    return flavor_id

def get_glance_image_id():
    gtoken = curl_keystone()
    url = 'http://controller:9292/v2/images'
    headers = {'content-type':'application/json','accept':'application/json'}
    req = urllib2.Request(url)
    req.add_header('X-Auth-Token',gtoken)
    response = urllib2.urlopen(req)
    data = response.read()
    ddata = json.loads(data)
    list = ddata['images']
    glance_id = []
    for i in range(len(list)):
        ID = list[i]['id']
        glance_id.append(ID)
    return glance_id

def get_network_id():
    ntoken = curl_keystone()
    url = 'http://controller:9696/v2.0/networks'
    headers = {'content-type':'application/json','accept':'application/json'}
    req = urllib2.Request(url)
    req.add_header('X-Auth-Token',ntoken)
    response = urllib2.urlopen(req)
    data = response.read()
    ddata = json.loads(data)
    list = ddata['networks']
    network_id = []
    for i in range(len(list)):
        ID = list[i]['id']
        network_id.append(ID)
    return network_id

def get_floating_ip():
    ftoken = curl_keystone()
    url = 'http://controller:9696/v2.0/floatingips'
    values = {
    "floatingip": {
        "floating_network_id": "9f583fd4-7a23-477e-9ff3-b7098d405665"
        }
    }
    data = json.dumps(values)
    headers = {'content-type':'application/json','accept':'application/json'}
    req = urllib2.Request(url,data = data,headers = headers)
    req.add_header('X-Auth-Token',ftoken)
    response = urllib2.urlopen(req)
    data = response.read()
    ddata = json.loads(data)
    floating_ip = ddata['floatingip']['floating_ip_address']
    return floating_ip

def create_vm():
    ctoken = curl_keystone()
    url = 'http://controller:8774/v2.1/servers'
    image = get_glance_image_id()[0]
    flavor = get_flavor_id()[0]
    network = get_network_id()
    net_id = random.sample(network,1)[0]
    values={
    "server": {
        "name":"pp",
        "imageRef":image,
        "flavorRef":flavor,
        "networks":[{"uuid":net_id}]
        }
    }
    data = json.dumps(values)
    headers = {'content-type':'application/json','accept':'application/json'}
    req = urllib2.Request(url,data = data,headers = headers)
    req.add_header('X-Auth-Token',ctoken) 
    response = urllib2.urlopen(req)

def associate_fip():
    atoken = curl_keystone()
    vm_id = get_nova_id()[0]
    f_ip = get_floating_ip()
    url = 'http://controller:8774/v2.1/servers/' + vm_id + '/action'
    values = {
    "addFloatingIp": {
        "address": f_ip
        }
    } 
    data = json.dumps(values)
    headers = {'content-type':'application/json','accept':'application/json'}
    req = urllib2.Request(url,data = data,headers = headers)
    req.add_header('X-Auth-Token',atoken)
    response = urllib2.urlopen(req)


if __name__ == "__main__":
    create_vm()
    time.sleep(60)
    associate_fip()
