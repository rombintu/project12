import json
import pandas as pd

from loguru import logger as log


def DEBAG(mess):
    log.debug(mess)

def get_data():

    url = "https://apps.timwhitlock.info/emoji/tables/unicode"

    bytes_utf_8_smiles = []
    data = pd.read_html(url)
    for table in data:
        bytes_utf_8_smiles.append(table['Bytes (UTF-8)'])

    # DEBAG(bytes_utf_8_smiles)
    with open('codec_smiles.py', 'w') as f:
        buff = 'smile_dict = ['
        for el in bytes_utf_8_smiles:
            for el2 in el:
                buff += 'b"' + str(el2) + '", \n'
            
        f.write(buff + ']')

get_data()