from variables_global import *
from collect_adress import collect_adress
import pandas as pd
import os
import datetime
import logging


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

get_list_of_all_houses_from_them()
