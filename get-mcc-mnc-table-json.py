# Get the Mobile Country Codes (MCC) and Mobile Network Codes (MNC) table
# from mcc-mnc.com and output it in JSON format.

import re
import urllib.request
import json
import pandas as pd
import string

def mcc_mnc_com():
    td_re = re.compile('<td>([^<]*)</td>'*6)
    with urllib.request.urlopen('http://mcc-mnc.com/') as f:
        html = f.read().decode('utf-8')

        mcc_mnc_list = []

        for line in html.replace('\n', '').replace('\r', '').replace('\t','').split('<tr>'):
            if '<td>' in line:
                td_search = td_re.search(line)
                if td_search:
                    current_item = {}
                    td_search = td_re.split(line)

                    current_item['mcc'] = td_search[1]
                    current_item['mnc'] = td_search[2]
                    current_item['iso'] = td_search[3]
                    current_item['country'] = td_search[4]
                    current_item['country_code'] = td_search[5]
                    current_item['network'] = td_search[6][0:-1]

                    mcc_mnc_list.append(current_item)

        j = json.dumps(mcc_mnc_list, indent=2)
        with open('mcc-mnc-table.json', 'w') as f:
            f.write(j)
        print(j)

def mcc_mnc_net_to_kotlin_map():
    url = 'https://s3.amazonaws.com/mcc-mnc.net/mcc-mnc.csv'
    csv = pd.read_csv(url, sep=';')
    mcc_mnc_list = []
    kotlin_format = "\"{mcc}\" to Country(\"{iso}\", \"{cc}\", \"{country}\"),"

    csv = csv.drop_duplicates(subset=['MCC', 'ISO']).sort_values('ISO')

    for _, item in csv.iterrows():
        if '/' in str(item['ISO']):
            for iso in str(item['ISO']).split('/'):
                mcc_mnc_list.append(kotlin_format.format(mcc=item['MCC'], iso=str(iso).upper(), cc='', country=item['Country']))
        else:
            mcc_mnc_list.append(kotlin_format.format(mcc=item['MCC'], iso=str(item['ISO']).upper(), cc='', country=item['Country']))

    print('\n'.join(mcc_mnc_list))

mcc_mnc_net_to_kotlin_map()