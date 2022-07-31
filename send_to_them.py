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




def send_devices_w_volume():

    df_collected= pd.read_excel(filename_final_send)
    df_collected["id_modem_registered_modem"] = ''
    df_collected["message_modem"] = ''
    df_collected["id_modem_registered_volume"] = ''
    df_collected["message_volume"] = ''
    df_collected["message_volume_send"] = ''

    for index, row in df_collected.iterrows():

        logging.debug("[SENDING] "
                      "account_id:{account_id},"
                      "sector_id_kvartira:{sector_id_kvartira},"
                      "serialNumber:{serialNumber},"
                      "modem:{modem},"
                      "modem_type:{modem_type},"
                      "house_num:{house_num}"
                      "kvartira:{kvartira}".format(
            account_id=row['contract_list'],
            sector_id_kvartira=row['sector_id_kvartira'],
            serialNumber=row['serialNumber'],
            modem=row['modem'],
            modem_type=row['modem_type'],
            house_num=row['house_num'],
            kvartira=row['kvartira']
        ))

        single_modem_obj = {
            'account_id':  row['contract_list'],
            'organization_id': 131,
            'sector_id': row['sector_id_kvartira'],
            'consumer': row['consumer'],
            'adress': row['adress'],
            'serialNumber': row['serialNumber'],
            'modem': row['modem'],
            'modem_type': row['modem_type'],
            'street_id': row['street_id'],
            'house_num': row['house_num'],
            'kvartira': row['kvartira'],
            'person': row['responsibleName'],
            'phone': row['responsiblePhone']}

        # try:
        id_modem_registered_modem, message_modem = stype_14(single_modem_obj=single_modem_obj )
        # tm = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        # 2021-10-29T00:00:00

        df_collected.at[index, 'id_modem_registered_modem'] = id_modem_registered_modem
        df_collected.at[index, 'message_modem'] = message_modem

        ldt = row['last_datetime'].replace("T", " ")
        last_datetime = datetime.datetime.strptime(ldt, '%Y-%m-%d %H:%M:%S')
        tm = last_datetime.strftime("%d.%m.%Y %H:%M:%S")

        id_modem_registered_volume, message_volume = stype_15(
            id_register_to_modem=id_modem_registered_modem,
            NPok=row['volume'],
            DtDate=tm)



        df_collected.at[index, 'id_modem_registered_volume'] = id_modem_registered_volume
        df_collected.at[index, 'message_volume'] = message_volume

        if message_volume.isnumeric():
            df_collected.at[index, 'message_volume_send'] = 1
        else:
            df_collected.at[index, 'message_volume_send'] = 0


    dt_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    path = os.path.join(directory, 'datasend_{0}.xlsx'.format(dt_string))

    df_collected.to_excel(path,index=False)
        # except Exception as e:
        #     row["success"] = 0
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
# single_modem_obj = {'sector_id':"2", 'serialNumber':"19_3078056", 'modem':"353656102027010"}
# id = stype_17(single_modem_obj =single_modem_obj )
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