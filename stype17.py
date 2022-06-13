from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml,get_value_from_param
import requests
import re





def stype_17( stype='17',
              sector_id="",
              serialNumber="",
              modem=""
              ):


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
        sector_id=sector_id,
        serialNumber=serialNumber,
        modem=modem
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
    # print(xml)
#     xml = """
#     <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#   <soap:Body>
#     <IntegrationMeteringResponse xmlns="http://tempuri.org/">
#       <IntegrationMeteringResult><?xml version="1.0"?>
# <root>
#   <ActList Status_Id="3" Status_Name="Принято в систему АСИЦРА" Message="470335"/>
# </root>
# </IntegrationMeteringResult>
#     </IntegrationMeteringResponse>
#   </soap:Body>
# </soap:Envelope>
#     """


    # print(measurePointId)
    id_modem_registered = get_value_from_param(xml, 'Id')


    return id_modem_registered


