import numpy as np
import pandas as pd  
import plotly.express as px 
import streamlit as st  
import os

import lib.all_sales as all_sales
import lib.monthly_sales as monthly_sales
import lib.weekly_price as weekly_price
import lib.monthly_revenue as monthly_revenue

# Configura Streamlit
st.set_page_config(
    page_title="Dashboard - Projeto ADA",
    page_icon="✅",
    layout="wide",
)

# Cria pasta dataset, caso não exista
if not os.path.isdir("dataset"):
    os.mkdir('dataset')

# Carrega Dados
df_all_sales = all_sales.load_data_all_sales()

def load_dados(df_all_sales):
    df_monthly_sales = monthly_sales.load_data_monthly_sales(df_all_sales)
    df_weekly_price = weekly_price.load_data_weekly_price(df_all_sales)
    df_monthly_revenue = monthly_revenue.load_data_monthly_revenue(df_all_sales, df_weekly_price)
    df_monthly_revenue = df_monthly_revenue.sort_values(by=['month_year'], ascending=True, na_position='first')
    return df_monthly_sales, df_weekly_price, df_monthly_revenue

# Carrega Primeira Semana
if df_all_sales.shape[0] == 0:
    st.title(f"Quitanda vazia")
    if st.button('Carregar Primeira Semana'):
        df_all_sales = all_sales.load_one_week(r'http://localhost:3000/api/ep1')
        df_monthly_sales, df_weekly_price, df_monthly_revenue = load_dados(df_all_sales)    


else: 

    df_monthly_sales, df_weekly_price, df_monthly_revenue = load_dados(df_all_sales)

    
  
    with st.sidebar: # Carrega SideBar

        st.title(f"Quitanda BR")

        if st.button('Carregar Semana'):
            df_all_sales = all_sales.load_one_week(r'http://localhost:3000/api/ep1')
            df_monthly_sales, df_weekly_price, df_monthly_revenue = load_dados(df_all_sales)
        
        if st.button('Carregar 05 Semanas'):
            df_all_sales = all_sales.load_one_month(r'http://localhost:3000/api/ep1')
            df_monthly_sales, df_weekly_price, df_monthly_revenue = load_dados(df_all_sales)
        
        if st.button('Carregar 01 Ano'):
            df_all_sales = all_sales.load_one_year(r'http://localhost:3000/api/ep1')
            df_monthly_sales, df_weekly_price, df_monthly_revenue = load_dados(df_all_sales)
            
        st.title(f"Home")

        with st.spinner("Loading..."):
            rd_view = st.radio("Visualização:", ('Geral', 'Produtos', 'DataFrame'))

    # Rotulo de Produtos e Preços 

    PRODUTOS_LABEL = [["prod_0","Banana","Unidade",0.2],
    ["prod_1","Melão","Unidade",0.5],
    ["prod_2","Mamão","Unidade",3],
    ["prod_3","Ovo","Unidade",0.6],
    ["prod_4","Melância","Unidade",8],
    ["prod_5","Atemoia","Unidade",5],
    ["prod_6","Laranja","Unidade",10],
    ["prod_7","Abacaxi","Unidade",10], 
    ["prod_8","Arroz","Quilograma",4.5],
    ["prod_9","Milho","Quilograma",3.5],
    ["prod_10","Soja","Quilograma",5],
    ["prod_11","Farinha","Quilograma",4],
    ["prod_12","Uva","Quilograma",8],
    ["prod_13","Tomate","Quilograma",8],
    ["prod_14","Batata","Quilograma",8],
    ["prod_15","Cebola","Quilograma",8],
    ["prod_16","Graviola","Quilograma",8],
    ["prod_17","Maça","Quilograma",8],
    ["prod_18","Feijão","Quilograma",8],
    ["prod_19","Feijão","Quilograma",8],
    ["prod_20","Feijão","Quilograma",8]]

    df_produtos = pd.DataFrame(PRODUTOS_LABEL, columns=['id','name','medida','preco'])
    df_produtos = df_produtos.sort_values(by='name', ascending=True, na_position='first')

    # Aba Produtos

    if rd_view == 'Produtos':

        st.title("Análise de Produtos")
        
        # Seleciona o Produto desejado
        sb_produto = st.selectbox("Selecione o produto:", df_produtos['name'].values)

        # creating a single-element container
        produtos_placeholder_1 = st.empty()
        with produtos_placeholder_1.container():

            produto = df_produtos[df_produtos['name'] == sb_produto].values[0]

            preco_atual = df_weekly_price[produto[0]].iloc[-1]
            preco_anterior = df_weekly_price[produto[0]].iloc[-2]

            col1, col2, col3 = st.columns(3)
            col1.metric("Produto", produto[1])
            col2.metric("Medida", produto[2])
            col3.metric("Preço Atual", f"R$ {(preco_atual).round(2)}",(preco_atual-preco_anterior).round(2), "inverse")

        if produto[0] in list(df_monthly_revenue.columns):
            
            produtos_placeholder_2 = st.empty()
            with produtos_placeholder_2.container():

                # create two columns for charts
                produtos_fig_col1, produtos_fig_col2 = st.columns(2)
                with produtos_fig_col1:
                    st.markdown("### Volume total por ano")

                    # Cria DF temporário
                    df_monthly_sales_temp = df_monthly_sales.copy()
                    df_monthly_sales_temp['year'] = df_monthly_sales_temp.index.map(lambda x: x[0:4])
                    df_temp = df_monthly_sales_temp.groupby('year').agg('sum')

                    # Gráfico 01
                    fig = px.bar(data_frame=df_temp[produto[0]], color=df_temp[produto[0]].index)
                    fig.update_layout(
                        yaxis_title=produto[2],
                        xaxis_title="Anos",
                        showlegend=False
                    )
                    st.write(fig)

                    # Print DF
                    # st.markdown("##### DF - Volume por ANO ")
                    # st.dataframe(df_temp[produto[0]])
                    
                with produtos_fig_col2:
                    st.markdown("### Montante negociado mês")

                    # Filtra o Produtos
                    _filter = produto[0]

                    if _filter in list(df_monthly_revenue.columns):
                        fig3 = px.line(data_frame=df_monthly_revenue, x="month", y=_filter, color='year', markers=True)
                        fig3.update_layout(
                            xaxis=dict(
                                showline=True,
                                showgrid=False,
                                showticklabels=True,
                                linecolor='rgb(204, 204, 204)',
                                linewidth=2,
                                ticks='outside',
                                tickfont=dict(
                                    family='Arial',
                                    size=12,
                                    color='rgb(82, 82, 82)',
                                ),
                            ),
                            yaxis=dict(
                                showgrid=True,
                                zeroline=False,
                                showline=False,
                                showticklabels=True,
                            ),
                            yaxis_title="Montante (R$)",
                            xaxis_title="Meses"
                        )
                        # st.write(fig3)
                        st.plotly_chart(fig3, use_container_width=True)

                    # st.markdown("##### DF - Volume por ANO ")
                    # st.dataframe(df_monthly_revenue)
            
            produtos_placeholder_3 = st.empty()
            with produtos_placeholder_3.container():
                st.markdown("### Comportamento de preço")

                # Dados das Semanas
                df_date_weeks = df_all_sales[['n_week','week_year','month_year']].drop_duplicates(subset='n_week', keep='first')
                df_date_weeks.reset_index(drop=True, inplace=True)

                # Tabela temporária de preço
                df_temp_price = pd.merge(df_weekly_price, df_date_weeks, how="outer", on='n_week')

                fig_produto = px.line(data_frame=df_temp_price, y=produto[0], x='month_year', markers=True)
                fig_produto.update_layout(
                    autosize=True,
                    xaxis=dict(
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        ),
                    ),
                    yaxis=dict(
                        showgrid=True,
                        zeroline=False,
                        showline=False,
                        showticklabels=True,
                    ),
                    yaxis_title=f"Preço da {produto[1]}",
                    xaxis_title="Tempo"
                )
                st.plotly_chart(fig_produto, use_container_width=True)
                
                st.markdown("### Montante vendido")
                df_temp_produto = df_monthly_revenue[['month_year', produto[0]]]
                df_temp_produto.set_index('month_year', inplace=True)

                fig_produto = px.line(data_frame=df_monthly_revenue, y=produto[0], x='month_year', markers=True)
                fig_produto.update_layout(
                    autosize=True,
                    xaxis=dict(
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        ),
                    ),
                    yaxis=dict(
                        showgrid=True,
                        zeroline=False,
                        showline=False,
                        showticklabels=True,
                    ),
                    yaxis_title="Montante (R$)",
                    xaxis_title="Tempo"
                )
                st.plotly_chart(fig_produto, use_container_width=True)

    ###########################################################################
    #####  Aba DataFrame
    ###########################################################################

    elif rd_view == 'DataFrame':

        st.title("Dados de projeto")
        
        menu = ["Transações","Consolidados Mensais","Preços Semanais","Montante Operado"]
        sb_df = st.selectbox("Selecione o DataFrame", menu)
        
        if menu.index(sb_df) == 1:
            st.markdown("### Consolidados mensais")
            st.dataframe(df_monthly_sales)
        elif menu.index(sb_df) == 2:
            st.markdown("### Preços Semanais")
            st.dataframe(df_weekly_price)
        elif menu.index(sb_df) == 3:
            st.markdown("### Montantes Operados")
            st.dataframe(df_monthly_revenue)
        else:
            st.markdown("### Transações realizadas")
            st.dataframe(df_all_sales)
  
    #  Aba Principal

    else:

        # dashboard title
        st.title("Dashboard - Projeto ADA - Geral")
        
        # creating a single-element container
        placeholder = st.empty()

        # Retorna quantidade de Vendas
        sells = df_all_sales.shape[0]

        # Total de meses
        meses = df_monthly_revenue.shape[0]

        # Retorna Montante Total de Vendas
        balance = np.sum(df_monthly_revenue['Total'])

        balance_total = np.sum(df_monthly_revenue['Total'])

        def moeda(x):
            return str(round(x,2)).replace('.', ',')

        with placeholder.container():

            # create three columns
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label = "Total de Vendas ⏳",
                value = round(sells),
            )
            
            kpi2.metric(
                label = "Ciclos",
                value = df_all_sales['n_week'].value_counts().count(),
            )

            kpi3.metric(
                label="Mês Atual",
                value= df_all_sales['month_year'].iloc[-1]
            )

            kpi4.metric(
                label="Balanço Total R＄",
                value=f"R$ {moeda(balance)} "
            )

            # create two columns for charts
            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                # Grágico 1
                st.markdown("### Volume total por produto")
                df_temp_by_produto = df_monthly_revenue.iloc[:,0:8].sum().to_frame()
                fig = px.bar(df_temp_by_produto, color=df_temp_by_produto.index, orientation='h')
                fig.update_layout(
                    xaxis_title="Unidades",
                    yaxis_title="Produtos",
                    showlegend=False
                )    
                st.write(fig)

                # Grágico 3
                st.markdown("### Volume total por ano")     
                df_all_sales['date'] = pd.to_datetime(df_all_sales['date'])
                df_temp_by_ano = df_all_sales['date'].dt.year.value_counts()
                fig2 = px.bar(data_frame=df_temp_by_ano, color=df_temp_by_ano.index)
                fig2.update_layout(
                    yaxis_title="Volume (kg + unidade)",
                    xaxis_title="Anos",
                    showlegend=False
                )       
                        
                st.write(fig2)
                
            with fig_col2:
                # Grágico 2
                st.markdown("### Volume total (kg) por produto")
                df_temp_by_produto = df_monthly_revenue.iloc[:,8:16].sum().to_frame()
                fig = px.bar(df_temp_by_produto, color=df_temp_by_produto.index, orientation='h')
                fig.update_layout(
                    xaxis_title="Peso (kg)",
                    yaxis_title="Produtos",
                    showlegend=False
                )    
                st.write(fig)
            
                # Grágico 4
                st.markdown("### Volume total por mês")

                # Prepara DataFrame
                df_monthly_sales_temp = df_monthly_sales.copy()
                df_monthly_sales_temp['total'] = df_monthly_sales_temp.sum(axis=1)
                df_monthly_sales_temp['month'] =  df_monthly_sales_temp.index.map(lambda x: x[5:])
                df_monthly_sales_temp['year'] =  df_monthly_sales_temp.index.map(lambda x: x[0:4])

                fig3 = px.line(data_frame=df_monthly_sales_temp, x="month", y='total', color='year', markers=True)
                fig3.update_layout(
                    xaxis=dict(
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        ),
                    ),
                    yaxis=dict(
                        showgrid=True,
                        zeroline=False,
                        showline=False,
                        showticklabels=True,
                    ),
                    yaxis_title="(kg + unidade)",
                    xaxis_title="Meses"
                )
                # st.write(fig3)
                st.plotly_chart(fig3, use_container_width=True)

            st.markdown("### DATAFRAME - Montante Operado ")
            st.dataframe(df_monthly_revenue.iloc[:,0:17])
            st.markdown("##### *Arquivo: monthly_revenue_month.csv*")