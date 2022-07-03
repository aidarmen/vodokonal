import requests
import pandas as pd
import json
from variables_global import filename_modem_type_and_num,filename_contract_num,filename_sn, filename_volume,filename_final_send,directory ,filename_json_response,login_our,password_our
from pathlib import Path
import os
import re

# только ХВС
# в коментариях  на уровне квартир: сектор; номер договора/лицевой счет
# модем тим и модем



# Path("data").mkdir(parents=True, exist_ok=True)



def collect_all(s,header):
  '''get list of all sectors,street, houses , flats and volumes. save to final_send.xlsx'''


  r = s.get('http://37.77.128.174:11111/api/v0.1/Core/MeasurePoints', headers=header)
  y = json.loads(r.text)

  df_serial_num = pd.read_excel(filename_sn)
  df_volume = pd.read_excel(filename_volume)

  df_modem_type_and_num = pd.read_excel(filename_modem_type_and_num)
  df_contracts = pd.read_excel(filename_contract_num)


  kvartira_nums=[]
  sector_id_kvartira = []
  # sector_id=[]
  consumer=[]
  adress=[]
  serialNumber=[]
  measurePointId=[]
  modem_type=[]
  modem = []
  street_id=[]
  house_num=[]
  kvartira=[]
  volume = []
  last_datetime = []
  contract_list = []
  water_measurement = []
  responsibleName = []
  responsiblePhone = []
  serviceNumber = []

  for row in y['measurePoints']:

    try:
      address_name,  street, house =  row['address'].split(';')
    except:
      address_name,  street, house  = "","",""

    if street == '':
      continue


    consumer_name = row['fullTitle'].split(' - ')[0].strip()
    kvartir_full_name = row['fullTitle'].split(' - ')[1].strip()

    kvartira_name = kvartir_full_name
    mid = row['counterId']

    try:
      kvartira_num = re.findall('\\d+', kvartir_full_name)[0]
    except:
      kvartira_num = ''

    try:
      serviceNum = row['serviceNumber']
    except:
      serviceNum =''


    # dont use this adress and equipment with this model
    # if row['title'] == 'Теплоснабжение' \
    #         or 'Малдагалиева стр. 26.1' in row['fullTitle'] \
    #         or row['title'] == 'Отопление' \
    #         or row['title'] == 'Отопение':
    #  # or consumer_name != 'Аксай 5-й микрорайон, 3Г К1'\
    #           or 'ХВС' not in row['title']  \
    if 'ХВС' not in row['title'].upper() and 'ГВС' not in row['title'].upper():
      continue

    # if address_name == 'Аксай 5-й микрорайон, 3Г К1':
    #   continue



    if 'кв' in kvartira_name.lower():
      sid_kvartira = '2'
    else:
      sid_kvartira = '0'

    # try:
    #   sid_kvartira = row['comment'].split(';')[0].strip()
    # except:
    #   sid_kvartira= ''



    # try:
    #   contract_id = df_contracts.loc[df_contracts['node_id'] == row['nodeId'], 'contract_num'].values[0]
    # except:
    #   contract_id = ''

    try:
      contract_id =  row['comment'].split(';')[0].strip()
    except:
      contract_id = ''

    try:
      rname = df_contracts.loc[df_contracts['node_id'] == row['nodeId'], 'responsibleName'].values[0]
    except:
      rname = ''

    try:
      rphone = df_contracts.loc[df_contracts['node_id'] == row['nodeId'], 'responsiblePhone'].values[0]
    except:
      rphone = ''


    try:
      sn = df_serial_num.loc[df_serial_num['measurePointId'] == row['counterId'], 'serialNumber'].values[0]
    except:
      sn = None

    try:
      vol = df_volume.loc[df_volume['measurePointId'] == row['id'], 'volume'].values[0]
    except:
      vol = None

    try:
      ldt =  df_volume.loc[df_volume['measurePointId'] == row['id'], 'last_datetime'].values[0]
    except:
      ldt = None

    try:
      modem_type_name = \
      df_modem_type_and_num.loc[df_modem_type_and_num['node_id'] == row['nodeId'], 'modem_type'].values[0]
    except:
      modem_type_name = None


    try:
      modem_num = str(df_modem_type_and_num.loc[df_modem_type_and_num['node_id'] == row['nodeId'], 'modem_num'].values[0])
    except:
      modem_num = None

    # if name is too big, oracle doesnt accept
    if len(kvartira_name) >20:
      kvartira_name = kvartira_name[:20]


    # if volume is empty or null
    if str(vol)=='nan' :
      continue

    # if sid_kvartira is wrong
    if sid_kvartira not in ['0','1','2' ]:
      continue

    # if sid_kvartira  == '0':
    #   acc_id = contract_id

    # round volume
    vol = round(vol, 3)
    serviceNumber.append(serviceNum)
    kvartira_nums.append(kvartira_num)
    sector_id_kvartira.append(sid_kvartira)
    water_measurement.append( row['title'])
    contract_list.append(contract_id)
    # sector_id.append(sec)
    consumer.append(consumer_name)
    adress.append(address_name)
    serialNumber.append(sn)
    measurePointId.append(mid)
    modem.append(modem_num)
    modem_type.append(modem_type_name)
    street_id.append(street)
    house_num.append(house)
    kvartira.append(kvartira_name)
    volume.append(vol)
    last_datetime.append(ldt)

    responsibleName.append(rname)
    responsiblePhone.append(rphone)



  df = pd.DataFrame({
    'kvartira_nums': kvartira_nums,
    'serviceNumber':serviceNumber,
    'sector_id_kvartira':sector_id_kvartira,
    'contract_list':contract_list,
    # 'sector_id': sector_id,
    'consumer': consumer,
    'adress': adress,
    'serialNumber': serialNumber,
    'measurePointId': measurePointId,
    'modem_type': modem_type,
    'modem':modem,
    'water_measurement':water_measurement,
    'street_id': street_id,
    'house_num': house_num,
    'kvartira': kvartira,
    'volume':volume,
    'last_datetime':last_datetime,
    'responsibleName':responsibleName,
    'responsiblePhone':responsiblePhone
  })

  df.to_excel(filename_final_send,index=False)







def getSerialNumber(s,header):
  '''get all serial numbers from measure points and save to serialNumber.xlsx'''
  r = s.get('http://37.77.128.174:11111/api/v1/Core/Equipment', headers=header)
  y = json.loads(r.text)
  measurePointId =[]
  serialNumber =[]

  for row in y['list']:
    measurePointId.append(row['id'])
    serialNumber.append(row['serialNumber'])

  df = pd.DataFrame({
    'measurePointId':measurePointId,
      'serialNumber':serialNumber
  })

  df.to_excel(filename_sn)

def get_volume_from_measure_points(s,header):
  '''get volume_from_measure_points'''
  r = s.get('http://37.77.128.174:11111/api/v1/Data/MeasurePoints/Totals/Last', headers=header)
  y = json.loads(r.text)
  measurePointId = []
  volume = []
  last_datetime = []


  dicts = r.json()
  measure_point_id = ""
  v_in = 0
  date_time = None
  for key in dicts:
    measure_point_id = key
    v_in = ''


    if dicts[key] and dicts[key]['values']:
      date_time = dicts[key]['dateTime']

      for item in dicts[key]['values']:
          if item['dataParameter'] == 'V_in':
            v_in = item['value']
            # print(v_in)
            break

      date_time = date_time.split(".",1)[0]
      measurePointId.append(key)
      volume.append( v_in)
      last_datetime.append(date_time)


  df = pd.DataFrame({
    'measurePointId': measurePointId,
    'volume': volume,
    'last_datetime':last_datetime
  })

  df.to_excel(filename_volume,index=False)




def get_modem_sn(s,header):
  r = s.get('http://37.77.128.174:11111/api/v1/Core/Equipment', headers=header)
  dicts = r.json()

  node_id = []
  measurePointId = []
  modem_type = []
  modem_num = []





  for key in dicts['list']:
    mid = key['id']
    for key2 in key['pollSettings']['connections']:
      # for key3 in key2['pollSettings']:
      if key2['commDevice'] is not None and key2['commDeviceModel'] is not None:
        ni = ''



        mn = key2['commDevice']['serialNumber']
        mt = key2['commDeviceModel']['title']

        for key3 in dicts['nodeEquipment']:
          if key3['equipmentId'] == mid:
            ni = key3['nodeId']
            break

        node_id.append(ni)
        # print(mid,mn,mt)
        measurePointId.append(mid)
        modem_num.append(mn)
        modem_type.append(mt)


  df = pd.DataFrame({
    'measurePointId':measurePointId,
    'modem_num': modem_num,
    'modem_type': modem_type,
    'node_id':node_id
  })

  df.to_excel(filename_modem_type_and_num)


def get_contract(s,header):
  r = s.get(
    'http://37.77.128.174:11111/api/v1/Core/Nodes?getSuppliers=true',
    headers=header)

  dicts = r.json()

  house_title = []
  node_id = []
  contract_num = []
  responsibleName = []
  responsiblePhone = []

  for key in dicts['nodes']:
    title = key['title']
    id = key['id']
    cn = ''
    rname = key['responsibleName']
    rphone = key['responsiblePhone']

    for key2 in dicts['nodeSuppliers']:
      house_title.append(title)
      node_id.append(id)
      responsibleName.append(rname)
      responsiblePhone.append(rphone)

      if key2['nodeId'] == id:
        cn =key2['contractNumber']
      contract_num.append(cn)

  df = pd.DataFrame({
    'title': house_title,
    'node_id': node_id,
    'contract_num': contract_num,
    'responsibleName':responsibleName,
    'responsiblePhone':responsiblePhone
  })

  df.to_excel(filename_contract_num)


def take_data_from_our_data(get_volume = True,get_sn=True,collect= True, create_dir = True):

  with requests.Session() as s:
    payload = {
      "login": login_our,
      "password": password_our,
      "application": "string"
    }

    r = s.post('http://37.77.128.174:11111/api/v1/Login', json =payload)
    token = r.json()['token']
    # print("token:", token)
    header = {"Authorization": 'Bearer {}'.format(token)}


    # # Возвращает список оборудования.
    # r = s.get('http://37.77.128.174:11111/api/v1/Core/Equipment',headers=header)



    # # Возвращает список оборудования.
    # r = s.get('http://37.77.128.174:11111/api/v1/Core/Equipment/1', headers=header)


    # # Возвращает последние интеграторы по всем доступным точкам учёта.
    # r = s.get('http://37.77.128.174:11111/api/v1/Data/MeasurePoints/Totals/Last',headers=header)


    # # Возвращает последнее потребление по всем доступным точкам учёта.
    # r = s.get('http://37.77.128.174:11111/api/v1/Data/MeasurePoints/Consumption/Last',headers=header)

    # # Возвращает последнее потребление по точке учёта.
    # r = s.get('http://37.77.128.174:11111/api/v1/Data/MeasurePoints/3/Consumption/Last',headers=header)

    # # Возвращает последние интеграторы по точке учёта.
    # r = s.get('http://37.77.128.174:11111/api/v1/Data/MeasurePoints/5033/Totals/Last', headers=header)

    # # Возвращает последние интеграторы по всем доступным точкам учёта.
    # r = s.get('http://37.77.128.174:11111/api/v1/Data/MeasurePoints/Totals/Last', headers=header)


    # # Возвращает список точек учёта.
    # r = s.get('http://37.77.128.174:11111/api/v0.1/Core/MeasurePoints',headers=header)


    # # Возвращает точку учёта с указанным идентификатором.
    # r = s.get('http://37.77.128.174:11111/api/v0.1/Core/MeasurePoints/5033',headers=header)



    if not os.path.exists(directory):
      os.makedirs(directory)

    # if not os.path.exists(directory_allow):
    #   os.makedirs(directory_allow)


    if get_volume:
      get_volume_from_measure_points(s,header)

    if get_sn:
      getSerialNumber(s,header)
      get_modem_sn(s, header)
      get_contract(s, header)

    if collect:
      collect_all(s,header)

    # to see content of json response
    with open(filename_json_response, 'wb') as fd:
      fd.write(r.content)

# #
with requests.Session() as s:
  payload = {
    "login": login_our,
    "password": password_our,
    "application": "string"
  }

  r = s.post('http://37.77.128.174:11111/api/v1/Login', json =payload)
  token = r.json()['token']
  # print("token:", token)
  header = {"Authorization": 'Bearer {}'.format(token)}
  # get_contract(s, header)
  # r = s.get('http://37.77.128.174:11111/api/v1/Core/MeasurePoints?getEquipment=true&getAttributes=true&getCustomers=true',headers=header)
  # r = s.get('http://37.77.128.174:11111/api/v1/Core/MeasurePoints', headers=header)

  # r = s.get('http://37.77.128.174:11111/api/v1/Data/MeasurePoints/Totals/Last', headers=header)
  # r = s.get('http://37.77.128.174:11111/api/v1/ServerInfo/Extra',headers=header)

  # r = s.get('http://37.77.128.174:11111/api/v1/Core/Nodes?getMeasurePoints=true&getServicemen=true&getServiceCompanies=true&getSignaling=true&getCustomers=true&getSuppliers=true&getAttributes=true', headers=header)
  # r = s.get('http://37.77.128.174:11111/api/v1/Core/Nodes?getMeasurePoints=true&getServicemen=true&getServiceCompanies=true&getSignaling=true&getCustomers=true&getSuppliers=true&getAttributes=true', headers=header)
  # r = s.get(
  #  'http://37.77.128.174:11111/api/v0.1/Core/MeasurePoints',
  #   headers=header)

  with open(filename_json_response, 'wb') as fd:
    fd.write(r.content)