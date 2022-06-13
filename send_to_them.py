from stype12 import stype_12
from stype13 import stype_13
from stype14 import stype_14
from stype15 import stype_15
from stype16 import stype_16
from stype17 import stype_17
from stype19 import stype_19
from stype20 import stype_20
from variables_global import *
from collect_adress import collect_adress
import pandas as pd
import os
import datetime
import logging

filename_sparvochnik_adress = os.path.join(directory, filename_sparvochnik_adress)
filename_final_send = os.path.join(directory, filename_final_send)
#
#
def get_list_of_all_houses_from_them():
    df = pd.DataFrame({
    'sector_id': [],
    'street_id': [],
    'street_name': [],
    'house': []})

    sector_id_col =[]
    street_id_col=[]
    street_name_col=[]
    house_col=[]

    for sector_id in [0,1,2]:
        package_id = 1
        all_packages = False

        while not all_packages:

            all_packages, df_temp = collect_adress( sector_id=sector_id, package_id = package_id)


            # sector_id_col.extend(sector_id_list)
            # street_id_col.extend(street_id_list)
            # street_name_col.extend(street_name_list)
            # house_col.extend(house_list)


            df = pd.concat([df, df_temp], axis=0)
            package_id = package_id + 1




    # df = pd.DataFrame({
    #     'sector_id': sector_id_col,
    #     'street_id': street_id_col,
    #     'street_name': street_name_col,
    #     'house': house_col
    # })

    df.to_excel(filename_sparvochnik_adress)

# get_list_of_all_houses_from_them()


def send_devices_w_volume():

    df_collected= pd.read_excel(filename_final_send)

    for index, row in df_collected.iterrows():

        logging.debug("[SENDING] "
                      "account_id:{account_id},"
                      "sector_id_kvartira:{sector_id_kvartira},"
                      "serialNumber:{serialNumber},"
                      "modem:{modem},"
                      "modem_type:{modem_type},"
                      "house_num:{house_num}"
                      "kvartira:{kvartira}".format(
            account_id=row['account_id'],
            sector_id_kvartira=row['sector_id_kvartira'],
            serialNumber=row['serialNumber'],
            modem=row['modem'],
            modem_type=row['modem_type'],
            house_num=row['house_num'],
            kvartira=row['kvartira']
        ))
        # try:
        id_modem_registered = stype_14(
            organization_id="131",
            account_id=row['account_id'],
            sector_id=row['sector_id_kvartira'],
            consumer=row['consumer'],
            adress=row['adress'],
            serialNumber=row['serialNumber'],
            modem=row['modem'],
            modem_type=row['modem_type'],
            street_id=row['street_id'],
            house_num=row['house_num'],
            kvartira=row['kvartira'],
            person=row['responsibleName'],
            phone=row['responsiblePhone']

        )
        # tm = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        # 2021-10-29T00:00:00
        ldt = row['last_datetime'].replace("T", " ")
        last_datetime = datetime.datetime.strptime(ldt, '%Y-%m-%d %H:%M:%S')
        tm = last_datetime.strftime("%d.%m.%Y %H:%M:%S")
        # stype_15(id_register_to_modem=id_modem_registered, NPok=row['volume'], DtDate=tm)

        # except Exception as e:
        #     logging.debug("[ERROR] failed to send")
        #     logging.debug(e)




# # Справочника улиц:
# stype_12(sector_id=2,package_id = 2)

# # Справочник домов
# stype_13(sector_id=0,street_id = 360)

# ИП "Цыфлер" organization_id='131'
# # Передача регистрации привязки модема к прибору учета
# stype_14(
#               stype='14',
#               organization_id="131",
#               account_id="",
#               sector_id="0",
#               consumer="Аксай 5-й микрорайон, 3Г К1 ",
#               adress="Аксай 5-й микрорайон, 3Г К1",
#               serialNumber="1900218",
#               measurePointId="3709",
#               modem_type="ХВС общий",
#               street_id="2935",
#               house_num="3Г, корп.1 ",
#               kvartira="Аксай 5-й микрорайон, 3Г К1 "
# )


# # Передача показаний
# stype_15(id_register_to_modem = "470335", NPok='0.709999978542327')

# # Запрос актуальности привязки модема к прибору учета по(ID регистрации модема к ПУ)
# stype_16(id_register_to_modem = "466379")

#  Запрос актуальности привязка модема к приборe учета п
# id = stype_17(  sector_id="0", serialNumber="1900218", modem="353656102027010")
# print(id)

# # Запрос на получение адреса по лицевому счету
# stype_19( Account_Id='',Sector_Id='1')

# # Запрос на получение справочника монтажных организации
# stype_20()

#  &lt;ActList Status_Id="3" Status_Name="Принято в систему АСИЦРА" Message="466372"/&gt;

#  &lt;ActList Status_Id="3" Status_Name="Принято в систему АСИЦРА" Message="466373"/&gt;
# <ActList Status_Id="3" Status_Name="Принято в систему АСИЦРА" Message="466377"/>

#   <ActList Status_Id="3" Status_Name="Принято в систему АСИЦРА" Message="466378"/>
#   <ActList Status_Id="3" Status_Name="Принято в систему АСИЦРА" Message="466379"/>