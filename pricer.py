import pandas as pd
import numpy as np

processed_stock = "./storage/Processed Stock Summary.csv"
final_price_list = "./storage/final_price_list.csv"

processed_stock_json = "./public/Processed Stock Summary.json"
final_price_list_json = "./public/final_price_list.json"
stock_with_price_list_json = "./public/stock_with_price_list.json"

headers_processed_stock = ['items','code','under','quantity','extra']
headers_raw_stock = ["items", "code", "under", "quantity",'extra']
headers_mask_stock = ["items", "code", "under", "quantity",'extra']

# def csv2df(loc, headers=None):
#     if headers:
#         return pd.read_csv(loc, names=headers,encoding="utf-16le")
#     else:
#         return pd.read_csv(loc,encoding="utf-16le")

def csv2df(loc, headers=None, encoding='utf-16le'):
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
        return pd.read_csv(loc, encoding=encoding, names=headers)
    else:
        return pd.read_csv(loc, encoding=encoding)

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
    processed_stock_df = processed_stock_df[processed_stock_df.quantity != 0]
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



def saveAsJSON(df, loc):
    df.to_json(loc, orient='records')



processed_stock_df = get_processed_df()
final_price_list_df = get_final_price_list_df()
stock_with_price_df = get_stock_with_price_list_df(final_price_list_df, processed_stock_df)
# generating JSON for stock with price list

saveAsJSON(processed_stock_df, processed_stock_json)
saveAsJSON(final_price_list_df, final_price_list_json)
saveAsJSON(stock_with_price_df, stock_with_price_list_json)
