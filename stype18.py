from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml,get_value_from_param
import requests
import re


def stype_18( stype='18', single_modem_obj={}):
    """Изменение привязки модема к прибору учета: stype=18:"""

    global url, headers, username, password


    text = """
 <?xml version="1.0" ?>
<root>
 <Service
 Id = "{id}"
 FirmaId = "{organization_id}"
 SectorId = "{sector_id}"
AccountId = "{account_id}"
Consumer = "{consumer}"
Adress = "{adress}"
Objects = "{house_num}"
Place = ""
SerialNumber = "{serialNumber}"
Modem = "{modem}"
ModemType = "{modem_type}"
UlId = "{street_id}"
Nd = "{house_num}"
Kv = "{kvartira}"
MountingId = "{organization_id}"
Person = "{person}"
Phone = "{phone}"
 />
</root>
    """.format(
        id=single_modem_obj['id_modem_registered'],
        organization_id = single_modem_obj['organization_id'],
        account_id =single_modem_obj['account_id'] ,
        sector_id=single_modem_obj['sector_id'],
        consumer=single_modem_obj[ 'consumer'],
        adress=single_modem_obj['adress'],
        serialNumber=single_modem_obj['serialNumber'],
        modem=single_modem_obj['modem'],
        modem_type=single_modem_obj['modem_type'],
        street_id=single_modem_obj['street_id'],
        house_num=single_modem_obj['house_num'],
        kvartira=single_modem_obj['kvartira'],
        person = single_modem_obj['person'],
        phone = single_modem_obj['phone']
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