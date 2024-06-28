from django.shortcuts import render
from django.http import HttpResponse
from tetpyclient import RestClient
import os
from pprint import pprint
import meraki
import pysnow
import requests
from requests.auth import HTTPBasicAuth
#from dnac_config import DNAC_IP, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
import json
from django.template import Template, Context
#from acitoolkit.acitoolkit import Tenant, Session
#import appdynamics
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#python manage.py runserver 3000
#source venv/bin/activate
#user: ctriana@plannet.mx
#password: 7D702c4d80$
#instance: https://dev113692.service-now.com

#username: admin
#Current password: 6z$mL%8JrpEV

#git clone --branch [branch_name] --single-branch [remote-url]

#def BASE(request):
#    return render(request, 'base.html', {"id":getAppd()})
def BASE(request):
    return render(request, 'base.html')

def TIENDAS(request):
    return render(request, 'tiendas.html', {"links":getLinks()})

def BOTONPANICO(request):
    return render(request, 'botonpanico.html')

def SEGURIDAD(request):
    return render(request, 'seguridad.html')

#def SERVICIOS_ELECTRONICOS(request):
#    return render(request, 'servicios_electronicos.html', {"id":getAppd()})

def SERVICIOS_ELECTRONICOS(request):
    return render(request, 'servicios_electronicos.html')

def CEDIS(request):
    #return render(request, 'cedis.html')
    return render(request, 'cedis.html', {"DNACDevices":getDNACDevices()})

def BACK_OFFICE(request):
    return render(request, 'back_office.html')

def OTROS(request):
    return render(request, 'otros.html')

#def SERVICIOS_FINANCIEROS(request):
#    return render(request, 'servicios_financieros.html', {"id":getAppd()})

def SERVICIOS_FINANCIEROS(request):
    return render(request, 'servicios_financieros.html')

def TAE(request):
    return render(request, 'tae.html')

def SERVICIOS_NO_FINANCIEROS(request):
    return render(request, 'servicios_no_financieros.html')

#def CORRESPONSALIAS(request):
#    return render(request, 'corresponsalias.html', {"id":getAppd()})
def CORRESPONSALIAS(request):
    return render(request, 'corresponsalias.html')

def ENVIOS(request):
    return render(request, 'envios.html')

def REMESAS(request):
    return render(request, 'remesas.html')

def PAGO_TDC(request):
    return render(request, 'pago_tdc.html')

def AUTENTICACION_DE_CAJEROS(request):
    return render(request, 'autenticacion_de_cajeros.html')

def SPIN(request):
    return render(request, 'spin.html')

def OXXO_PREMIA(request):
    return render(request, 'oxxo_premia.html')

def RETIROS(request):
    return render(request, 'retiros.html')

def RETIROS_SIN_TARJETA(request):
    return render(request, 'retiros_sin_tarjeta.html')

def INTERNET(request):
    return render(request, 'internet.html')

def APLICACIONES(request):
    return render(request, 'aplicaciones.html')

def RED(request):
    #print("ACIIIIIIIII")
    #getACI()
    return render(request, 'red.html')

class link:
    def __init__(self, network, model, lastReportedAt, interface, status, ip):
        self.network = network
        self.model = model
        self.lastReportedAt = lastReportedAt
        self.interface = interface
        self.status = status
        self.ip = ip

class dev:
    def __init__(self, hostname, managementIpAddress, reachabilityStatus, serialNumber, platformId, softwareVersion, role, upTime, location, locationName):
        self.hostname = hostname
        self.managementIpAddress = managementIpAddress
        self.reachabilityStatus = reachabilityStatus
        self.serialNumber = serialNumber
        self.platformId = platformId
        self.softwareVersion = softwareVersion
        self.role = role
        self.upTime = upTime
        self.location = location
        self.locationName = locationName

'''
def getAppd():
    id = 0
    credentials = {
    "Account": "asteroids202304160747452",
    "Username": "asteroids202304160747452@asteroids202304160747452",
    "Password": "sf6u3pmvx8j7"
    }

    applicationsUrl = "https://" + credentials["Account"] + ".saas.appdynamics.com/controller/rest/applications?output=JSON"
    response = requests.get(applicationsUrl, auth=(credentials["Username"], credentials["Password"]))

    if(response.text != "[]"):
        id = 1
    return id
'''
    
#meraki
def getLinks():
    links = []
    #oldmerakiapi='008189248694c721d9b440a15aa2333208e42206'
    #oldmerakiorg='618119048856602390'
    
    #MERAKI_API_KEY="73c7b2be0214ee988232e52ea8411934daffbc79"
    #organization_id = '618119048856602329'

    #MERAKI_API_KEY='1ba6895780ac12d8c108e641367fcf4c7a9ffc17'
    #MERAKI_API_KEY='73c7b2be0214ee988232e52ea8411934daffbc79'
    #organization_id = '618119048856602329'      
    organization_id = '618119048856601703'
    MERAKI_API_KEY = '6d48e1ba8174111ead5caeca9c2a531959c4bac4'

    dashboard = meraki.DashboardAPI(MERAKI_API_KEY, output_log=False, print_console=False)
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

#DNAC************************************************************************************************************************

def getDNACDevices():
    
    DNACdevices = []
    DNAC_IP = "sandboxdnac.cisco.com" #Reemplazar esta variable por la IP original del DNAC
    DNAC_PORT = 443 
    DNAC_USER = "devnetuser" #Reemplazar esta variable por el usuario original del DNAC
    DNAC_PASSWORD = "Cisco123!" #Reemplazar esta variable por password original del DNAC

    token = get_auth_token() # Get Token
    url = "https://"+DNAC_IP+"/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr, verify=False)  # Make the Get Request
    device_list = resp.json()
    #print(device_list)
    #print_device_list(device_list)
    for device in device_list['response']:
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        for (serialNumber, platformId) in serialPlatformList:
            hostname = device['hostname']
            managementIpAddress = device['managementIpAddress']
            reachabilityStatus = device['reachabilityStatus']
            #serialNumber = serialNumber
            #platformID = platformID
            softwareVersion = device['softwareVersion']
            role = device['role']
            upTime = "N/A" if device['upTime'] is None else device['upTime']
            location = device['location']
            locationName = device['locationName']
        DNACdevices.append(dev(hostname, managementIpAddress, reachabilityStatus, serialNumber, platformId, softwareVersion, role, upTime, location, locationName))
    return DNACdevices

def print_device_list(device_json):
    print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
          format("hostname", "mgmt IP", "serial","platformId", "SW Version", "role", "Uptime"))
    for device in device_json['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        for (serialNumber, platformId) in serialPlatformList:
            print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(device['hostname'],
                         device['managementIpAddress'],
                         serialNumber,
                         platformId,
                         device['softwareVersion'],
                         device['role'], uptime))

def get_auth_token():
    DNAC_IP = "sandboxdnac.cisco.com" #Reemplazar esta variable por la IP original del DNAC
    DNAC_PORT = 443 
    DNAC_USER = "devnetuser" #Reemplazar esta variable por el usuario original del DNAC
    DNAC_PASSWORD = "Cisco123!" #Reemplazar esta variable por password original del DNAC
    
    url = 'https://'+DNAC_IP+'/dna/system/api/v1/auth/token'       # Endpoint URL
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token 
    return token    # Create a return statement for the Token
#DNAC************************************************************************************************************************


#tetration
def getTetration():
    API_ENDPOINT = "https://tet-pov-rtp1.cpoc.co"
    restclient = RestClient(API_ENDPOINT, credentials_file='api_credentials.json', verify=False)
    #Followed by API calls, for example API to retrieve list of agents.
    #API can be passed /openapi/v1/sensores or just /sensors.
    resp = restclient.get('sensors')
    print(resp)
    
#aci
def getACI():
    base_url = 'https://198.18.153.144/api/'
    # create credentials structure
    name_pwd = {'aaaUser': {'attributes': {'name': 'admin', 'pwd': 'C1sco123!'}}}
    json_credentials = json.dumps(name_pwd)
    # log in to API
    login_url = base_url + 'aaaLogin.json'
    post_response = requests.post(login_url, data=json_credentials)
    # get token from login response structure
    auth = json.loads(post_response.text)
    login_attributes = auth['imdata'][0]['aaaLogin']['attributes']
    auth_token = login_attributes['token']
    # create cookie array from token
    cookies = {}
    cookies['APIC-Cookie'] = auth_token
    # read a sensor, incorporating token in request
    sensor_url = base_url + 'mo/topology/pod-1/node-1/sys/ch/bslot/board/sensor-3.json'
    get_response = requests.get(sensor_url, cookies=cookies, verify=False)
    # display sensor data structure
    print(get_response.json())