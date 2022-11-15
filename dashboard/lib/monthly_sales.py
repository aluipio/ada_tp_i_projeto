import pandas as pd
import numpy as np
import os.path

# By: Paulo Sergio
# desafio -> somar o volume mensal
# cada transação tem varios produtos e um volume para cada produto
# é necessário, portanto, somar o volume de cada transação para que se tenha o volume mensal

def monthly_sales(df_all_sales):

    # criando df somente com produtos e o mês
    month_and_product = df_all_sales.loc[:, 'month_year':]

    # somando o numero de transações por mês
    sum_of_month = month_and_product.groupby(['month_year']).sum()

    # salvando o csv
    sum_of_month.to_csv('dataset/monthly_sales.csv', index=True, sep=',')

    return sum_of_month


def load_data_monthly_sales(df_all_sales):
    # if os.path.isfile(r'dataset\monthly_sales.csv'):
    #     return pd.read_csv(r'dataset\monthly_sales.csv')
    # else:
    #     df_monthly_sales = monthly_sales(df_all_sales)
    #     return df_monthly_sales
    return monthly_sales(df_all_sales)