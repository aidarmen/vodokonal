from get_from_us import take_data_from_our_data
from send_to_them import send_devices_w_volume
from variables_global import filename_logger,directory
import logging
import os
filename_logger = os.path.join(directory, filename_logger)

logging.basicConfig(filename=filename_logger, level=logging.DEBUG,
                    format="%(asctime)s:%(name)s:%(message)s")

# start here

mistake = False

#take our data
try:
    logging.debug("[RUN] take_data_from_our_data()")
    take_data_from_our_data(get_volume = True,get_sn=True,collect= True)

except Exception as e:
    mistake = True
    logging.debug("[ERROR] in take_data_from_our_data")
    logging.debug( e)


    # send to them
# if not mistake:
#     logging.debug("[RUN] send_devices_w_volume()")
#     send_devices_w_volume()
# else:
#     logging.debug("[ERROR] send_devices_w_volume()")
