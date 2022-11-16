import pandas as pd



def monthly_sales(df_all_sales):

    # criando df somente com produtos e o mês
    month_and_product = df_all_sales.loc[:, 'month_year':]

    # somando o numero de transações por mês
    sum_of_month = month_and_product.groupby(['month_year']).sum()

    # salvando o csv
    sum_of_month.to_csv('dataset/monthly_sales.csv', index=True, sep=',')

    return sum_of_month


def load_data_monthly_sales(df_all_sales):

    return monthly_sales(df_all_sales)