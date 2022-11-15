import pandas as pd
import math
import os.path

# By: Rafael

def weekly_price(df_all_sales):

    # Integração ao código
    df = df_all_sales

    # criando novo dataframe só com produtos e semanas
    only_week_product = df.loc[:,'prod_0':'prod_15']
    only_week_product.insert(16,'n_week',df['n_week'])
    
    # manipulando os dados: produtos de 0 a 7 são inteiros pois são comprados em unidades
    #                       produtos de 8 a 15 continuam float pois são comprados por kg
    only_week_product.loc[:,'prod_0':'prod_7'] = only_week_product.loc[:,'prod_0':'prod_7'].astype(int)
    #deixando apenas valores não negativos e trocando NaN por 0
    only_week_product = only_week_product[only_week_product>0].fillna(0)
    # agrupando por semanas, usar group_week.describe() para ver como ficou
    group_week = only_week_product.groupby('n_week')
    # criando DataFrame com a média de vendas dos produtos em cada semana
    mean_week = group_week.mean()

    #criando DataFrame para os preços
    prices = mean_week[mean_week==0].fillna(0)
    for lin in range(mean_week.shape[0]):
        for col in range(mean_week.shape[1]):
            # todo produto tem inicialmente um preço pré definido para as duas primeiras semanas
            if(lin <= 1):
                prices.iloc[lin,col] = 1

            # se houve venda na ultima semana
            elif((lin > 1) and (mean_week.iloc[lin-1,col] != 0)):
                # se a venda da penultima semana for igual a zero
                # define quem é fat pois se não, terá uma indeterminação na função 've\to\infty'
                if(mean_week.iloc[lin-2,col] == 0):
                    fat = 1
                else:
                # caso contrario, calcula normalmente
                    ve = (mean_week.iloc[lin-1,col]-mean_week.iloc[lin-2,col])/(mean_week.iloc[lin-2,col])
                    fat = 1/(1+math.exp(-ve))
                flog = 0.5 + fat
                prices.iloc[lin,col] = flog*prices.iloc[lin-1,col]

            # se não houve venda na ultima semana
            elif((lin > 1) and (mean_week.iloc[lin-1,col] == 0)):
                # se continuar não havendo venda do produto, o preço se mantem, pois de 've': M(t)-M(t-1) = 0,
                # considerando não variação na média de venda semanal
                if(mean_week.iloc[lin-2,col] == 0):
                    fat = 0.5
                else:
                # caso contrario, calcula normalmente
                    ve = (mean_week.iloc[lin-1,col]-mean_week.iloc[lin-2,col])/(mean_week.iloc[lin-2,col])
                    fat = 1/(1+math.exp(-ve))
                flog = 0.5 + fat
                prices.iloc[lin,col] = flog*prices.iloc[lin-1,col]

    # Editado por Anderson
    # Salvar dados
    prices.to_csv(r"dataset/weekly_price.csv")
    mean_week.to_csv(r"dataset/mean_sales.csv")       

    return prices


def load_data_weekly_price(df_all_sales):
    # if os.path.isfile(r'dataset\weekly_price.csv'):
    #     return pd.read_csv(r'dataset\weekly_price.csv')
    # else:
    #     weekly_prices, mean_week = weekly_price(df_all_sales)
    #     return weekly_prices
    return weekly_price(df_all_sales)