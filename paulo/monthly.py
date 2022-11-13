import pandas as pd
import numpy as np

# desafio -> somar o volume mensal
# cada transação tem varios produtos e um volume para cada produto
# é necessário, portanto, somar o volume de cada transação para que se tenha o volume mensal


def monthly(df):
    # criando df somente com produtos e o mês
    month_and_product = df.loc[:, 'month_year':'prod_15']

    # somando o numero de transações por mês
    sum_of_month = month_and_product.groupby(['month_year']).sum()

    return sum_of_month

# abrindo e salvando como um dataframe
df = pd.read_csv(r'dados\all_sales.csv')

# passa a função
data = monthly(df)

# print(data)

# salvando o csv
data.to_csv('dados\monthly.csv', index=True, sep=',')


