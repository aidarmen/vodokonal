from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml
import requests





def stype_20( stype='20'):
    global url, headers, username, password
    text = """
   <?xml version="1.0" ?>
<root>
</root>
    """

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
    print(response.status_code)



    print(beauty_print_xml(response.content))

