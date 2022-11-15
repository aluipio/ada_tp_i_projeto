import pandas as pd
import numpy as np
import os.path

# By: Anderson Miranda

def monthly_revenue(df_all_sales_raw, df_weekly_price):
    
    # Isola o conteudo desejado
    columns = ['n_week', 'prod_0', 'prod_1', 'prod_2', 'prod_3', 'prod_4', 'prod_5', 
            'prod_6', 'prod_7', 'prod_8', 'prod_9', 'prod_10', 'prod_11', 'prod_12',
            'prod_13', 'prod_14', 'prod_15']
    df_all_sales_sliced = df_all_sales_raw[columns]

    # Total de vendes por produtos, por semana
    df_sum_weekly = df_all_sales_sliced.groupby('n_week').agg('sum')
    
    # Total por semana = Preco x Volume -> com duas casas decimais round(2)
    df_monthly_revenue_week = (df_sum_weekly * df_weekly_price).round(2)
    df_monthly_revenue_week['n_week'] = df_monthly_revenue_week.index
    df_monthly_revenue_week.reset_index(drop=True, inplace=True)

    # Dados das Semanas
    df_date_weeks = df_all_sales_raw[['n_week','week_year','month_year']].drop_duplicates(subset='n_week', keep='first')
    df_date_weeks.reset_index(drop=True, inplace=True)

    # Salva Montante por semana
    #df_monthly_revenue_week.merge(df_date_weeks, how='outer', on='n_week')
    df_monthly_revenue_week = pd.merge(df_monthly_revenue_week, df_date_weeks, how="outer", on='n_week')
    df_monthly_revenue_week.to_csv('dataset/monthly_revenue_week.csv')

    # Calcula e Salva Montante por Mês, por Produto
    df_monthly_revenue_month = df_monthly_revenue_week.groupby(['month_year']).agg('sum')
    df_monthly_revenue_month.drop('n_week', axis=1, inplace=True)
    df_monthly_revenue_month['Total'] = df_monthly_revenue_month.sum(axis = 1)
    df_monthly_revenue_month = df_monthly_revenue_month.round(2)
    df_monthly_revenue_month['month_year'] = df_monthly_revenue_month.index
    df_monthly_revenue_month['month'] = df_monthly_revenue_month.index.map(lambda x: x[5:])
    df_monthly_revenue_month['year'] = df_monthly_revenue_month.index.map(lambda x: x[0:4])
    df_monthly_revenue_month.to_csv('dataset/monthly_revenue_month.csv', index=False)
    df_monthly_revenue_month.reset_index(drop=True, inplace=True)

    return df_monthly_revenue_week, df_monthly_revenue_month


def load_data_monthly_revenue(df_all_sales, df_weekly_price):
    # if os.path.isfile(r'dataset\monthly_revenue.csv'):
    #     return pd.read_csv(r'dataset\monthly_revenue.csv')
    # else:
    #     df_monthly_revenue_week, df_monthly_revenue_month = monthly_revenue(df_all_sales, df_weekly_price)
    #     return df_monthly_revenue_month
    df_monthly_revenue_week, df_monthly_revenue_month = monthly_revenue(df_all_sales, df_weekly_price)
    return df_monthly_revenue_month