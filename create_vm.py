#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import urllib2
import urllib
import json
import random

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

def create_vm():
    ctoken = curl_keystone()
    url = 'http://controller:8774/v2.1/servers'
    image = get_glance_image_id()[0]
    flavor = get_flavor_id()[0]
    network = get_network_id()
    net_id = random.sample(network,1)[0]
    values={
    "server": {
        "name":"python",
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

if __name__ == "__main__":
    create_vm()
   # print (curl_keystone()) 
