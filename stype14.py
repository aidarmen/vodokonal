from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml,get_value_from_param
import requests
import re
from stype17 import stype_17





def stype_14( stype='14',
              organization_id="131",
              account_id="",
              sector_id="",
              consumer="",
              adress="",
              serialNumber="",
              modem="",
              modem_type="",
              street_id="",
              house_num="",
              kvartira="",
              person ="",
              phone =''
              ):


    global url, headers, username, password
    text = """
 <?xml version="1.0" ?>
<root>
 <Service
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
        organization_id = organization_id,
        account_id =account_id ,
        sector_id=sector_id,
        consumer= consumer,
        adress=adress,
        serialNumber=serialNumber,
        modem=modem,
        modem_type=modem_type,
        street_id=street_id,
        house_num=house_num,
        kvartira=kvartira,
        person = person,
        phone = phone
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


    status = get_value_from_param(xml, 'Status_Id')
    status_name = get_value_from_param(xml, 'Status_Name')
    id_modem_registered = get_value_from_param(xml, 'Message')



    if status == '3':
        # if device is new and was registered successfully
        # print(status)
        # print(status_name)
        # print(id_modem_registered)
        return id_modem_registered
    else:
        # if device already registered get id_modem_registered
        id_modem_registered = stype_17(sector_id=sector_id, serialNumber=serialNumber, modem=modem)
        # print(id_modem_registered)

        return id_modem_registered



