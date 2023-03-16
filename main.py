from get_from_us import take_data_from_our_data
from send_to_them import send_devices_w_volume
from variables_global import filename_logger_info,directory,filename_logger_debug
import logging
import os
import datetime
from get_list_all_houses import get_list_of_all_houses_from_them



filename_logger_debug = os.path.join(directory, filename_logger_debug)
filename_logger_info = os.path.join(directory, filename_logger_info)


logging.basicConfig(filename=filename_logger_debug, level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")


logging.basicConfig(filename=filename_logger_info, level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
# start here

logging.getLogger("urllib3").setLevel(logging.WARNING)



mistake = False




#take our data
# try:
#     logging.debug("[RUN] take_data_from_our_data()")
#     take_data_from_our_data(get_volume = True,get_sn=True,collect= True)
#
# except Exception as e:
#     mistake = True
#     logging.debug("[ERROR] in take_data_from_our_data")
#     logging.debug( e)

# take_data_from_our_data(get_volume=True, get_sn=True, collect=True)

    # send to them
if not mistake:
    # get_list_of_all_houses_from_them()
    logging.debug("[RUN] send_devices_w_volume()")
    send_devices_w_volume()
else:
    logging.debug("[ERROR] send_devices_w_volume()")


# free memory
for name in dir():
    if not name.startswith('_'):
        del globals()[name]

for name in dir():
    if not name.startswith('_'):
        del locals()[name]

import gc
gc.collect()