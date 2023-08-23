import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

processed_stock = "./storage/Processed Stock Summary.csv"
final_price_list = "./storage/final_price_list.csv"
tyre_pricelist = "./storage/MRF PRICE LIST.csv"
reorder_csv = "./storage/ReorderPurc.csv"
status_csv = "./status.csv"
statusmrf_csv = "./status_mrf.csv"

processed_stock_json = "./public/Processed Stock Summary.json"
final_price_list_json = "./public/final_price_list.json"
stock_with_price_list_json = "./public/stock_with_price_list.json"
tyre_price_list_json = "./public/tyre_price_list.json"
reorder_json = "./public/reorderpurc.json"
status_json = "./public/status.json"

headers_status = ['item','updatedon']
headers_processed_stock = ['items','code','under','quantity','extra']
headers_raw_stock = ["items", "code", "under", "quantity",'extra']
headers_mask_stock = ["items", "code", "under", "quantity",'extra']
headers_reorder_stock = ["code", "items", "reorderlevel", "quantity",'netquantity',"purchaseprice", "gstprice", "gstrate", "lastpurchasedate",'reorderquantity','extra']

# def csv2df(loc, headers=None):
#     if headers:
#         return pd.read_csv(loc, names=headers,encoding="utf-16le")
#     else:
#         return pd.read_csv(loc,encoding="utf-16le")

old_status_file = status_json
headers_old_status = ["param","value"]
old_status_df = pd.DataFrame(columns=headers_old_status)
try:
    old_status_df = pd.read_json(old_status_file)
    print(old_status_df)
except:
    pass


current_status_file = status_csv
headers_current_status = ["param","value"]
current_status_df = pd.DataFrame(columns=headers_current_status)
try:
    current_status_df = pd.read_csv(current_status_file, names=headers_current_status)
    print(current_status_df)
except:
    pass

mrf_status_file = statusmrf_csv
headers_current_status = ["param","value"]
current_status_df = pd.DataFrame(columns=headers_current_status)
try:
    mrf_status_df = pd.read_csv(mrf_status_file, names=headers_current_status)
    print(mrf_status_df)
except:
    pass


def get_value(df,colname,itemname):
    time = df.loc[df[colname] == itemname]
    if(not time.empty):
        return time['value'].values[0]
    else:
        return ""













def csv2df(loc, headers=None, encoding='utf-16le', dtype = None):
    # Read in the file
    # with open(loc, 'r') as file :
    #     filedata = file.read()
    # Replace the target string
    # filedata = filedata.replace('\00', '')
    # filedata = filedata.replace(",\n", '')
    # Write the file out again
    # with open(loc, 'w', encoding='utf-16le') as file:
    #     file.write(filedata)
    if headers:
        return pd.read_csv(loc, encoding=encoding, names=headers, dtype=dtype)
    else:
        return pd.read_csv(loc, encoding=encoding,dtype=dtype)

def assignPrice(pricelist_df, processed_stock_df):
    priced_tally_df = pd.merge(processed_stock_df, pricelist_df, on='items', how='left')
    print(priced_tally_df)
    priced_tally_df['priced'] = priced_tally_df['retail_price'].notna()
    priced_tally_df.loc[priced_tally_df['priced'] == False, 'priced'] = CONST_NO_MATCH
    priced_tally_df.loc[priced_tally_df['priced'] == True, 'priced'] = CONST_MRF_MATCH
    return priced_tally_df

def clean_df(df, columnname):
    df.dropna(subset=[columnname], inplace=True)


def get_processed_df():
    processed_stock_df = csv2df(processed_stock,headers_processed_stock)
    processed_stock_df = processed_stock_df.iloc[1:]
    # processed_stock_df = processed_stock_df[processed_stock_df.quantity != 0]
    clean_df(processed_stock_df, 'items')
    return processed_stock_df


def get_final_price_list_df():
    final_price_list_df = csv2df(final_price_list, encoding='utf-8')
    final_price_list_df.drop(columns=['under'], inplace=True)
    clean_df(final_price_list_df, 'items')
    return final_price_list_df

def get_stock_with_price_list_df(final_price_list_df, processed_stock_df):
    merged = pd.merge(final_price_list_df, processed_stock_df, on='items', how='right',suffixes=('_pricelist', ''))
    merged.drop(columns=['code_pricelist'], inplace=True)
    return merged

# def updateStatus():
#     data = [['github_lastUpdated', datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%dT%H:%M:%S.%f")]]
#     status_df = pd.DataFrame(data, columns=['param', 'value'])
#     return status_df

def saveAsJSON(df, loc):
    df.to_json(loc, orient='records')

def getEmailTime():
    df = pd.read_csv(status_csv, names=["datetime"])
    emailTime = df.iloc[0]['datetime']
    data = [['github_lastUpdated', emailTime]]
    status_df = pd.DataFrame(data, columns=['param', 'value'])
    return status_df



def read_statusjson():
    pass


status_data=[]
# processing  processed data and stock with price data and final pricelist
try:    
    processed_stock_df = get_processed_df()
    final_price_list_df = get_final_price_list_df()
    if(len(processed_stock_df.index)>0 and len(final_price_list_df.index)>0):
        processed_stock_df.drop(['extra'], axis=1, inplace=True)    
        final_price_list_df.drop(['extra'], axis=1, inplace=True)
        stock_with_price_df = get_stock_with_price_list_df(final_price_list_df, processed_stock_df)
        # rename dataframes
        final_price_list_df.rename(columns = {'retail_price':'ret_prc','suggested_price':'sug_prc', 'wholesale_price':'wsale_prc'}, inplace = True)
        stock_with_price_df.rename(columns = {'quantity':'qty','retail_price':'ret_prc','suggested_price':'sug_prc', 'wholesale_price':'wsale_prc'}, inplace = True)
        # replace NaN for prices with 0
        final_price_list_df[["wsale_prc","sug_prc","ret_prc"]] = final_price_list_df[["wsale_prc","sug_prc","ret_prc"]].fillna(0)
        stock_with_price_df[["wsale_prc","sug_prc","ret_prc"]] = stock_with_price_df[["wsale_prc","sug_prc","ret_prc"]].fillna(0)
        stock_with_price_df[["priced"]] = stock_with_price_df[["priced"]].fillna("No Match")
        saveAsJSON(processed_stock_df, processed_stock_json)
        saveAsJSON(final_price_list_df, final_price_list_json)
        saveAsJSON(stock_with_price_df, stock_with_price_list_json)
        status_data.append({'param':'processed_data', 'value':get_value(current_status_df,'param','processed_data')})
    else:
        status_data.append({'param':'processed_data', 'value':get_value(old_status_df,'param','processed_data')})
except Exception as error:
    print("An error occurred:", error)
    status_data.append({'param':'processed_data', 'value':get_value(old_status_df,'param','processed_data')})


# processing tyre_pricelist
try:
    tyre_pricelist_df = csv2df(tyre_pricelist, encoding='utf-8')
    if(len(tyre_pricelist_df.index)>0):
        saveAsJSON(tyre_pricelist_df, tyre_price_list_json)
        status_data.append({'param':'pricelist_mrf', 'value':get_value(mrf_status_df,'param','pricelist_mrf')})
    else:
        status_data.append({'param':'pricelist_mrf', 'value':get_value(mrf_status_df,'param','pricelist_mrf')})
except:
    status_data.append({'param':'pricelist_mrf', 'value':get_value(mrf_status_df,'param','pricelist_mrf')})


# Processing Reorder and Purchase Data
try:
    reorder_df = csv2df(reorder_csv, headers=headers_reorder_stock, dtype={'code': str})
    if(len(reorder_df.index)>0):
        reorder_df.drop(['extra'], axis=1, inplace=True)
        saveAsJSON(reorder_df, reorder_json)
        status_data.append({'param':'reorder_data', 'value':get_value(current_status_df,'param','reorder_data')})
    else:
        status_data.append({'param':'reorder_data', 'value':get_value(old_status_df,'param','reorder_data')})
except:
    status_data.append({'param':'reorder_data', 'value':get_value(old_status_df,'param','reorder_data')})



# generating status
# status_df = getEmailTime()
status_df = pd.DataFrame.from_records(status_data)
saveAsJSON(status_df, status_json)





