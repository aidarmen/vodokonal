from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml,get_value_from_param
import requests
import re
from stype18 import stype_18




def stype_17( stype='17',single_modem_obj={} ):

    global url, headers, username, password

    text = """
 <?xml version="1.0" ?>
<root>
 <Service
 SectorId = "{sector_id}"
 SerialNumber = "{serialNumber}"
 Modem = "{modem}"
 />
</root>
    """.format(
        sector_id=single_modem_obj['sector_id'],
        serialNumber=single_modem_obj['serialNumber'],
        modem=single_modem_obj['modem']
    )



    decoded = decode_to_base64(text)

    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
    <IntegrationMetering xmlns="http://tempuri.org/">
    <username type="xs:string">{username}</username>
    <password type="xs:string">{password}</password>
    <stype type="xs:string">{stype}</stype>
    <bytes type="xs:string">{decoded}</bytes>
    </IntegrationMetering>
    </soap:Body>
    </soap:Envelope>""".format(username = username ,password= password,decoded= decoded,stype=stype )


    response = requests.post(url,data=body,headers=headers)
    xml = beauty_print_xml(response.content)



    id_modem_registered = get_value_from_param(xml, 'Id')

    if "AccountId"  not in xml:
        AccountId = ''
    else:
        AccountId = get_value_from_param(xml, 'AccountId')

    single_modem_obj['id_modem_registered'] = id_modem_registered



    if AccountId !=single_modem_obj['account_id']:
        stype_18( single_modem_obj=single_modem_obj )

    return id_modem_registered


