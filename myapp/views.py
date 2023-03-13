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
            if counterfail == 2:
                links.append(link(networkId, model, lastReportedAt, interface, status, ip))
            #print("Interface==>"+interface+", Status==>"+status+", IP==>"+ip)
    #ctx = {"uno":"uno"}
    return links

# Create your views here.
def hello(request):
    MERAKI_API_KEY="008189248694c721d9b440a15aa2333208e42206"
    ORG_NAME="OXXO 4.0 Sureste"
    organization_id = '618119048856602390'
    NETWORK_NAME="10OAX50FI4 - OXXO Guadalupe"
    #dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
    dashboard = meraki.DashboardAPI(MERAKI_API_KEY, suppress_logging=True)
    response = dashboard.organizations.getOrganizationUplinksStatuses(organization_id, total_pages='all')
    print(response)

    #Integration with servicenow
    # Create client object
    servicenowURL = 'https://dev113692.service-now.com/api/now/table/incident'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "short_description": "Ticket creado desde Python: Uplink Interface WAN1 - 10.236.129.90: Status Failed",
        "caller_id": "Eduardo Triana",
        "impact": 1,
        "urgency": 2
    }
    res = requests.post(servicenowURL, auth=('admin', '6z$mL%8JrpEV'), headers=headers, data=json.dumps(payload)) 
    print(res.text)
    return render(request, 'index.html')
    '''
    meraki-api="008189248694c721d9b440a15aa2333208e42206"
    API_ENDPOINT="https://tet-pov-rtp1.cpoc.co/"
    api_key="a8799f024bac433d83ebc09805aa794c"
    api_secret="4ba57794fc0322f48f339395801138ab234336b4"
    #restclient = RestClient(API_ENDPOINT,credentials_file='api_credentials.json',verify=False)
    restclient = RestClient(API_ENDPOINT, api_key=api_key, api_secret=api_secret, verify=False)
    resp = restclient.get('/app_scopes')

    for scope in resp.json():
	    print(scope["id"], scope["name"])
    return HttpResponse("<h2><center>System Status</center></h2><br><br><p>%s</p>" % scope)
    '''
def users(request):
    MERAKI_API_KEY="008189248694c721d9b440a15aa2333208e42206"
    ORG_NAME="OXXO 4.0 Sureste"
    organization_id = '618119048856602390'
    NETWORK_NAME="10OAX50FI4 - OXXO Guadalupe"

    #dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
    dashboard = meraki.DashboardAPI(MERAKI_API_KEY, suppress_logging=True)
    orgs = dashboard.organizations.getOrganizations()
    pprint(orgs)


    API_ENDPOINT = "https://tet-pov-rtp1.cpoc.co/"
    api_key = "79d3fec8ae1140008020f1b01aa0e082"
    api_secret = "49d8fcd6c058af147fc9ac369ea5f3e005a23d4b"
    #API_ENDPOINT="https://tet-pov-rtp1.cpoc.co/"
    #api_key="a8799f024bac433d83ebc09805aa794c"
    #api_secret="4ba57794fc0322f48f339395801138ab234336b4"
    restclient = RestClient(API_ENDPOINT, api_key=api_key, api_secret=api_secret, verify=False)

    for entry in orgs:
        if entry['name'] == ORG_NAME:
            organization_id = entry["id"]
    print(organization_id)

    resp = restclient.get('/users')
    to_print = "<center>"
    for user in resp.json():
        to_print += user["email"]
        to_print += "<br>"
    to_print += "</center>"
    return HttpResponse("<h2><center>Users</center></h2><br><br><p>%s</p>" % to_print)

    