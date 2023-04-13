from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from tetpyclient import RestClient
import os
from pprint import pprint
import meraki
import pysnow
import requests
import json
from django.template import Template, Context

# Create your models here.


class Device(models.Model):
    def __init__(self, mac, name, productType, serial, status):
        self.mac = mac
        self.name = name
        self.productType = productType
        self.serial = serial
        self.status = status

    def getDevices(self):
        print("GET DEVICEEEEEES")
        devices = []
        MERAKI_API_KEY="1ba6895780ac12d8c108e641367fcf4c7a9ffc17"
        organization_id = '618119048856602329'      
        dashboard = meraki.DashboardAPI(MERAKI_API_KEY, output_log=False, print_console=False)
        response = dashboard.organizations.getOrganizationDevicesAvailabilities(organization_id, total_pages='all')
        for device in response:
            mac = device ["mac"]
            name = device ["name"]
            productType = device ["productType"]
            serial = device ["serial"]
            status = device ["status"]
            devices.append(device(mac, name, productType, serial, status))
        return devices