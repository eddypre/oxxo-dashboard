'''
#!/usr/bin/python
 
from SOAPpy  import SOAPProxy
import sys
 
def createincident (params_dict ):
    # instance to send to
    instance = 'demo'
 
    # username/password
    username = 'itil'
    password = 'itil'
 
    # proxy - NOTE: ALWAYS use https://INSTANCE.service-now.com, not https://www.service-now.com/INSTANCE for web services URL from now on!
    proxy  = 'https://%s:%s@%s.service-now.com/incident.do?SOAP' %  (username , password , instance )
    namespace  = 'http://www.service-now.com/'
    server  = SOAPProxy (proxy , namespace )

    # uncomment these for LOTS of debugging output #server.config.dumpHeadersIn = 1 #server.config.dumpHeadersOut = 1 #server.config.dumpSOAPOut = 1 #server.config.dumpSOAPIn = 1
 
    response  = server. insert (impact = int (params_dict [ 'impact' ] ) , urgency = int (params_dict [ 'urgency' ] ) , priority = int (params_dict [ 'priority' ] ) , category =params_dict [ 'category' ] , location =params_dict [ 'location' ] , caller_id =params_dict [ 'user' ] , assignment_group =params_dict [ 'assignment_group' ] , assigned_to =params_dict [ 'assigned_to' ] , short_description =params_dict [ 'short_description' ] , comments =params_dict [ 'comments' ] )
    return response
 
values  = { 'impact':  '1' , 'urgency':  '1' , 'priority':  '1' , 'category':  'High' , 'location':  'San Diego' , 'user':  'fred.luddy@yourcompany.com' , 'assignment_group':  'Technical Support' , 'assigned_to':  'David Loo' , 'short_description':  'An incident created using python, SOAPpy, and web services.' , 'comments':  'This a test making an incident with python.\n Isn \' t life wonderful?' } 
new_incident_sysid =createincident (values )
 
print "Returned sysid: "+ repr (new_incident_sysid )
'''