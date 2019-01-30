# coding:utf-8
"""
use the script as follows:
python upload_image.py controller_ip image_path image_name
"""
import requests
import json
import sys

class UploadImage(object):
    """upload a openstack image"""
    def __init__(self, controller_ip, image_path, image_name):
        self.ip = controller_ip
        self.imagepath = image_path
        self.imagename = image_name

    def get_token(self):
        """get keystone token"""
        keystone_url = "http://" + self.ip + ":5000/v2.0/tokens"
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
        r_data = r.json()
        self.token = r_data['access']['token']['id']

    def create_images(self):
        """get image id"""
        ci_url = "http://" + self.ip + ":9292/v2/images"
        ci_data = {
            "container_format": "bare",
            "disk_format": "raw",
            "name": self.imagename
        }
        r = requests.post(url=ci_url, data=json.dumps(ci_data), headers={"X-Auth-Token": self.token})
        r_data = r.json()
        self.id = r_data['id']

    def upload_image(self):
        """upload binary image data"""
        ui_url = "http://" + self.ip + ":9292/v2/images/" + self.id + "/file"
        headers = {'content-type': 'application/octet-stream', "X-Auth-Token": self.token}
        with open(self.imagepath, 'rb') as infile:
            r = requests.put(url=ui_url, data=infile, headers=headers)

    def import_image(self):
        """import an image"""
        ii_url = "http://" + self.ip + ":9292/v2/images/" + self.id + "/import"
        ii_data = {
            "method": {
                "name": "glance-direct"
            }
        }
        headers = {'content-type': 'application/json', 'accept': 'application/json', "X-Auth-Token": self.token}
        r = requests.post(url=ii_url, data=json.dumps(ii_data), headers=headers)


if __name__ == '__main__':
    ip = sys.argv[1]
    imagepath = sys.argv[2]
    imagename = sys.argv[3]
    up = UploadImage(ip=ip, imagepath=imagepath, imagename=imagename)
    up.get_token()
    up.create_images()
    up.upload_image()
    up.import_image()

