from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml,get_value_from_param
import requests
import re
from stype17 import stype_17


def isNaN(num):
    return num != num


def stype_14( stype='14', single_modem_obj={}):


    global url, headers, username, password



    if single_modem_obj['account_id'] is None or isNaN(single_modem_obj['account_id']) :
        single_modem_obj['account_id']=''

    try:
        single_modem_obj['account_id'] = int(single_modem_obj['account_id'])
    except:
        single_modem_obj['account_id'] =''

    if single_modem_obj['person'] is None or isNaN(single_modem_obj['person']):
        single_modem_obj['person']=''

    if single_modem_obj['phone'] is None or isNaN(single_modem_obj['phone']):
        single_modem_obj['phone']=''



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
        organization_id = single_modem_obj['organization_id'],
        account_id =single_modem_obj['account_id'] ,
        sector_id=single_modem_obj['sector_id'],
        consumer= single_modem_obj['consumer'],
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




    status = get_value_from_param(xml, 'Status_Id')
    status_name = get_value_from_param(xml, 'Status_Name')
    message = get_value_from_param(xml, 'Message')



    if message.isnumeric():
        id_modem_registered=message

    if status == '3':
        # if device is new and was registered successfully
        # print(status)
        # print(status_name)
        # print(id_modem_registered)
        return id_modem_registered,message
    elif 'Уже существует в системе прибор учета' in message:
        # if device already registered get id_modem_registered

        id_modem_registered = stype_17(single_modem_obj=single_modem_obj)
        # print(id_modem_registered)

        return id_modem_registered,message
    else:
        return '',message


