from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml,get_value_from_param
import requests
import logging




def stype_15( stype='15', id_register_to_modem='', NPok = '1', DtDate = '20.04.2022 23:00:00'):
    global url, headers, username, password
    text = """
        <?xml version="1.0"?>
        <root>
        <Service
        Id = "{id_register_to_modem}" 
        NPok = "{NPok}" 
        DtDate = "{DtDate}" 
         />
        </root>
    """.format(id_register_to_modem =id_register_to_modem ,NPok=NPok, DtDate=DtDate )

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

    # print(decoded)
    response = requests.post(url,data=body,headers=headers)

    xml = beauty_print_xml(response.content)

    status = get_value_from_param(xml, 'Status_Id')
    # status_name = get_value_from_param(xml, 'Status_Name')
    # id_modem_registered = get_value_from_param(xml, 'Message')

    message = get_value_from_param(xml, 'Message')
    if message.isnumeric():
        id_modem_registered=message
    else:
        id_modem_registered = ''

    if status != '3':
        logging.debug("[ERROR] wrong status")

    return id_modem_registered, message

