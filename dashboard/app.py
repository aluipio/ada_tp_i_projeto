import numpy as np
import pandas as pd  
import plotly.express as px 
import streamlit as st  

# Configura Streamlit
st.set_page_config(
    page_title="Dashboard - Projeto ADA",
    page_icon="✅",
    layout="wide",
)


# Carrega SideBar
with st.sidebar:
    st.title("Quitanda BR")

    st.write("Home")

    with st.spinner("Loading..."):
        rd_view = st.radio("Visualização:", ('Geral', 'Produtos', 'DataFrame'))

###########################################################################
##### Carrega Dados
###########################################################################

DIR_DATA = 'dataset/'

df_all_sales = pd.read_csv(DIR_DATA + 'all_sales.csv')
df_monthly_sales = pd.read_csv(DIR_DATA + 'monthly_sales.csv')
df_weekly_price = pd.read_csv(DIR_DATA + 'weekly_price.csv')

df_monthly_revenue = pd.read_csv(DIR_DATA + 'monthly_revenue.csv', sep=";")
df_monthly_revenue['month'] = df_monthly_revenue['month_year'].map(lambda x: x[0:2])
df_monthly_revenue['year'] = df_monthly_revenue['month_year'].map(lambda x: x[3:])
df_monthly_revenue['month_year'] = df_monthly_revenue['month_year'].map(lambda x: x[3:]+"-"+x[0:2])
df_monthly_revenue = df_monthly_revenue.sort_values(by='month_year', ascending=True, na_position='first')

###########################################################################
##### Rotulo de Produtos e Preços 
###########################################################################

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

###########################################################################
#####  Aba Produtos
###########################################################################

if rd_view == 'Produtos':

    st.title("Análise de Produtos")
    
    sb_produto = st.selectbox("Selecione o projeto", df_produtos['name'].values)

    # creating a single-element container
    placeholder_2 = st.empty()

    with placeholder_2.container():

        produto = df_produtos[df_produtos['name'] == sb_produto].values[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Produto", produto[1])
        col2.metric("Medida", produto[2])
        col3.metric("Preço da Medida", "R$ " + str(round(produto[3],2)))

    if produto[0] in list(df_monthly_revenue.columns):
        
        st.markdown("### DataFrama - Montante Vendido ao longo do tempo")
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
            )
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

###########################################################################
#####  Aba Principal
###########################################################################

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
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Vendas ⏳",
            value=round(sells),
            delta=round(sells) - 10,
        )
        
        kpi2.metric(
            label="Meses",
            value=meses,
            delta=meses-1,
        )
        
        kpi3.metric(
            label="Balanço Total R＄",
            value=f"R$ {moeda(balance)} ",
            delta=-round(balance) * 100,
        )

        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### Volume por produto")
            
            df_temp = df_monthly_revenue.iloc[:,1:17].sum().to_frame()
            fig = px.bar(df_temp)
            st.write(fig)

            # df_temp = df_temp.transpose()
            # st.dataframe(df_temp)
            # st.markdown("### First Chart")
            # df_temp['Produto'] = list(df_temp.index)
            # df_temp.rename({'0':'Quantidade'}, inplace=True)
            # fig = px.pie(df_monthly_revenue, names='product', values='Total', title='Product balance')

            # sum_balance = np.sum(df_monthly_revenue['Total'])
            # df_monthly_revenue.loc[df_monthly_revenue['Total'] < 0.05 * sum_balance, 'product'] = 'Other' # Represent only large countries
            # fig = px.pie(df_monthly_revenue, names='product', values='Total', title='Product balance')
            # st.write(fig)
            
        with fig_col2:
            st.markdown("### Montante Vendido ao longo do ano")
            #   df_monthly_revenue.columns[1:16]
            sb_geral_produto = st.selectbox("Selecionar produto:", df_produtos['name'].values)
            _filter = df_produtos[df_produtos['name'] == sb_geral_produto].values[0][0]

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
                    )
                )
                # st.write(fig3)
                st.plotly_chart(fig3, use_container_width=True)

            # if _filter in list(df_monthly_revenue.columns):

            #     fig2 = px.line(data_frame=df_monthly_revenue, y=_filter, x='month_year', markers=True)

            #     fig2.update_layout(
            #         xaxis=dict(
            #             showline=True,
            #             showgrid=False,
            #             showticklabels=True,
            #             linecolor='rgb(204, 204, 204)',
            #             linewidth=2,
            #             ticks='outside',
            #             tickfont=dict(
            #                 family='Arial',
            #                 size=12,
            #                 color='rgb(82, 82, 82)',
            #             ),
            #         ),
            #         yaxis=dict(
            #             showgrid=True,
            #             zeroline=False,
            #             showline=False,
            #             showticklabels=True,
            #         )
            #     )
            #     st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df_monthly_revenue.iloc[:,0:17])