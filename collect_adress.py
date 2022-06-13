from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml
import requests
import xml.etree.ElementTree as ET


from decode_to_base64 import decode_to_base64
from variables_global import *
from beauty_print_xml import beauty_print_xml
import requests
import re
import pandas as pd


def get_house( stype='13',sector_id=1,street_id = 1):
    global url, headers, username, password
    text = """
    <?xml version="1.0"?>
    <root>
    <Service SectorId = "{sector_id}" type="xsd:int" UlId = "{street_id}"/>
    </root>
    """.format(sector_id =sector_id ,street_id=street_id )

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

    x = re.findall('\"(.*)\"', xml)


    if len(x[3:]) == 0:
        return True

    for i in x[3:]:
        yield i



def collect_adress( stype='12',sector_id=1,package_id = 1, df=  pd.DataFrame()):
    global url, headers, username, password
    text = """
    <?xml version="1.0"?>
    <root>
    <Service SectorId = "{sector_id}" type="xsd:int" PackageId = "{package_id}"/>
    </root>
    """.format(sector_id =sector_id ,package_id=package_id )

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





    x = re.findall('\"(.*)\"', xml)
    # print(sector_id, package_id)
    # print(xml)

    sector_id_list = []
    street_id_list = []
    street_name_list = []
    house_list = []

    if len(x[3:]) ==0:
        return True , None

    for i in x[3:]:

        # if len(i)==0:
        #     return True

        li = i.split('" Name="')

        # if len(li)==0:
        #     return True

        street_id = li[0]
        street_name = li[1]

        # print(sector_id,package_id,street_id,street_name)

        for house in get_house( sector_id=sector_id, street_id=street_id):
            sector_id_list.append(str(sector_id))
            street_id_list.append(str(street_id))
            street_name_list.append(str(street_name))
            house_list.append(str(house))

    df = pd.DataFrame({
        'sector_id': sector_id_list,
        'street_id': street_id_list,
        'street_name': street_name_list,
        'house': house_list
    })

    return False, df
           # sector_id_list,street_id_list,street_name_list,house_list





