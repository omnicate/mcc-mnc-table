import pandas as pd

def mcc_mnc_to_operators():
    """
    Gets data from mcc-mnc.net and constructs a map of maps MCC -> MNC -> Operator(name, TADIG), in Kotlin format.
    Excludes MCC/MNC pairs that don't have a TADIG.
    """
    url = 'https://s3.amazonaws.com/mcc-mnc.net/mcc-mnc.csv'
    csv = pd.read_csv(url, sep=';', dtype={ 'MCC': str, 'MNC': str }).groupby('MCC')
    mcc_list = {}
    for mcc, group in csv:
        mcc_list[mcc] = []
        for _, item in group.iterrows():
            if pd.notnull(item['TADIG']):
                mcc_list[mcc].append(
                    { 'MNC': item['MNC'], 'TADIG': item['TADIG'], 'name': str(item['Operator']).replace('"', '\\"') }
                )
    for mcc in mcc_list:
        if len(mcc_list[mcc]) == 0:
            continue
        print('"{mcc}" to mapOf('.format(mcc=mcc))
        for mnc in mcc_list[mcc]:
            print('    "{}" to Operator("{}", "{}"),'.format(mnc['MNC'], mnc['name'], mnc['TADIG']))
        print('),')

mcc_mnc_to_operators()
