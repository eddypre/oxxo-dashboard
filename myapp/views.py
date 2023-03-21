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
import appdynamics

#service now:
#user: ctriana@plannet.mx
#password: 7D702c4d80$
#cloud--
#instance: https://dev113692.service-now.com
#username: admin
#Current password: 6z$mL%8JrpEV

#
#python manage.py runserver 3000
#source venv/bin/activate

def BASE(request):
    return render(request, 'base.html', {"links":getLinks()})

def SEGURIDAD(request):
    return render(request, 'seguridad.html')

def INTERNET(request):
    return render(request, 'internet.html')

def APLICACIONES(request):
    return render(request, 'aplicaciones.html')

def RED(request):
    return render(request, 'red.html')

class link:
    def __init__(self, network, model, lastReportedAt, interface, status, ip):
        self.network = network
        self.model = model
        self.lastReportedAt = lastReportedAt
        self.interface = interface
        self.status = status
        self.ip = ip

def getLinks():
    links = []
    #oldmerakiapi='008189248694c721d9b440a15aa2333208e42206'
    #oldmerakiorg='618119048856602390'
    
    #MERAKI_API_KEY="73c7b2be0214ee988232e52ea8411934daffbc79"
    #organization_id = '618119048856602329'

    MERAKI_API_KEY="1ba6895780ac12d8c108e641367fcf4c7a9ffc17"
    organization_id = '618119048856602329'      

    dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
    response = dashboard.organizations.getOrganizationUplinksStatuses(organization_id, total_pages='all')

    for network in response:
        counterfail=0
        uplinks = network ["uplinks"]
        networkId = network["networkId"]
        model = network["model"]
        lastReportedAt = "None"
        if network["lastReportedAt"] != None:
            lastReportedAt = network["lastReportedAt"]
        #print("\nNetwork==>"+networkId+", Model==>"+model+", lastReportedAt==>"+ lastReportedAt)
        for uplink in uplinks:
            interface = "None"
            status = "None"
            ip = "None"
            if uplink["interface"] != None:
                interface = uplink["interface"]
            if uplink["status"] != None:
                status = uplink["status"]
            if uplink["ip"] != None:
                ip = uplink["ip"]
            if uplink["status"] != "active":
                counterfail = counterfail+1
            #if counterfail == 2:
            links.append(link(networkId, model, lastReportedAt, interface, status, ip))
            #print("Interface==>"+interface+", Status==>"+status+", IP==>"+ip)
    #ctx = {"uno":"uno"}
    return links