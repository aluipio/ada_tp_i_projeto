import pandas as pd
import numpy as np
import requests
import json
import os.path

# By: Elenilson
# Edit: Anderson

def load_data_all_sales():
    path_all_sales = r'dataset/all_sales.csv'
    if os.path.isfile(path_all_sales):
        return pd.read_csv(path_all_sales)
    else:
        df_all_sales = pd.DataFrame(columns=['id', 'date', 'n_week', 'week_year', 'month_year']+[f'prod_{n}' for n in range(16)])
        df_all_sales.to_csv(path_all_sales, index=False)
        return df_all_sales
    

"""Faz as requisições na API até a data atual e transforma os dados recebidos para um dataset"""
def load_one_week(url_api: str = r'http://localhost:3000/api/ep1'):
    df_all_sales = load_data_all_sales()
    df_request = pd.DataFrame(requests.get(url_api).json())
    if 'date' in df_request.columns:
        if df_all_sales.shape[0] == 0:
            df_request['n_week'] = 1
        else:
            df_request['n_week'] = df_all_sales['n_week'].max() + 1
        df_request['date'] = pd.to_datetime(df_request['date'], unit='s')
        df_request['month_year'] = df_request['date'].dt.strftime('%Y-%m')
        df_request['week_year'] = df_request['date'].dt.strftime('%Y-%U')

        df_request = df_request.fillna(0)
        df_all_sales_new = pd.concat([df_all_sales, df_request])
        df_all_sales_new = df_all_sales_new.fillna(0)
        df_all_sales_new.to_csv(r'dataset/all_sales.csv', index=False)

        # Retorna df_all_sales
        return df_all_sales_new
    else:
        return df_all_sales

"""Faz as requisições na API até a data atual e transforma os dados recebidos para um dataset"""
def load_one_month(url_api: str = r'http://localhost:3000/api/ep1'):
    df_all_sales = load_data_all_sales()
    count = 1
    while count <= 5:
        df_all_sales = load_one_week(url_api)
        count += 1

    # Retorna df_all_sales
    return df_all_sales

"""Faz as requisições na API até a data atual e transforma os dados recebidos para um dataset"""
def load_one_year(url_api: str = r'http://localhost:3000/api/ep1'):
    df_all_sales = load_data_all_sales()
    count = 1
    while count <= 12:
        df_all_sales = load_one_month(url_api)
        count += 1

    # Retorna df_all_sales
    return df_all_sales