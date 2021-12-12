# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import numpy as np
import plotly.express as px

st.title('Trabalho de AMD')

st.header('Introdução')

st.write('O objetivo do nosso projeto é entender quais são os fatores que influenciam os jovens e a educação brasileira. Utilizando os dados do INEP (Instituto Nacional de Estudos e Pesquisas Educacionais), podemos coletar o município, uf, média de alunos por turma, a taxa de reprovação, a taxa de abandono, a situação socio-econômica e diversas outras informações sobre o Ensino Médio de milhares de escolas ao redor do país e usar isso pra nos ajudar a compreender o que está por trás de uma educação de sucesso (ou não).')

st.header('Conheça os nossos dados')

visualizar = st.radio('Escolha as colunas',['Todas', 'Selecionar colunas'])

df_escola_em = pd.read_pickle('df_escola_em.pkl')

df_escola_em.rename(columns={'id_escola': 'ID Escola', 'taxa_aprovacao_em': 'Taxa de Aprovação', 'taxa_reprovacao_em': 'Taxa de Reprovação', 'taxa_abandono_em':'Taxa de Abandono', 'ano': 'Ano', 'rede': 'Rede', 'localizacao': 'Localização', 'atu_em': 'Média de Alunos por Turma', 'had_em': 'Média de Horas-Aula Diária', 'tdi_em':'Taxa de Distorção Idade-Série', 'dsu_em':'Porcentual de Docentes com Curso Superior', 'regiao':'Região'}, inplace = True)

if visualizar == "Selecionar colunas":
    colunas = st.multiselect("Selecione as colunas", ['ID Escola', 'Taxa de Aprovação','Taxa de Reprovação', 'Taxa de Abandono', 'Ano', 'Rede', 'Localização', 'Média de Alunos por Turma','Média de Horas-Aula Diária','Taxa de Distorção Idade-Série', 'Porcentual de Docentes com Curso Superior', 'Região'])
else:
    colunas = ['Taxa de Aprovação','Taxa de Reprovação', 'Taxa de Abandono', 'Ano', 'Rede', 'Localização', 'Média de Alunos por Turma','Média de Horas-Aula Diária','Taxa de Distorção Idade-Série', 'Porcentual de Docentes com Curso Superior', 'Região']

head = st.number_input("Digite quantas linhas você deseja:", 1, 100)

st.dataframe(df_escola_em.head(head)[colunas])

option = st.radio(
     'Escolha uma visualização',
     ('Correlação das colunas', 'Média de aprovações por rede e localização', 'Média de reprovações por rede e localização', 'Média da taxa de abandono por rede e localização', 'Média de abandono ao longo do tempo'))

df_escola_em_dummies = pd.read_pickle('df_escola_em_dummies.pkl')
df_escola_em_dummies.rename(columns={'taxa_aprovacao_em': 'Taxa de Aprovação', 'taxa_reprovacao_em': 'Taxa de Reprovação', 'taxa_abandono_em':'Taxa de Abandono', 'ano': 'Ano', 'rede_estadual': 'Rede Estadual', 'rede_federal': 'Rede Federal','rede_municipal': 'Rede Municipal','rede_privada': 'Rede Privada', 'localizacao_rural': 'Rural', 'localizacao_urbana': 'Urbana','atu_em': 'Média de Alunos por Turma', 'had_em': 'Média de Horas-Aula Diária', 'tdi_em':'Taxa de Distorção Idade-Série', 'dsu_em':'Porcentual de Docentes com Curso Superior', 'regiao_Centro-Oeste':'Região Centro-Oeste', 'regiao_Nordeste':'Região Nordeste', 'regiao_Sudeste':'Região Sudeste', 'regiao_Sul':'Região Sul'}, inplace = True)


corr = df_escola_em_dummies.corr()


fig = sns.set(rc={'figure.figsize':(10, 10)})

if option == 'Correlação das colunas':
    ax = sns.heatmap(corr, 
                    vmin=-1, vmax=1, center=0, 
                    cmap=sns.diverging_palette(20, 220, n=200), 
                    square=True)
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=65,
        horizontalalignment='right');
    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.set_option('deprecation.showPyplotGlobalUse', False)
elif option == 'Média de aprovações por rede e localização':
    media_aprovacao = df_escola_em[['Taxa de Aprovação', 'Rede', 'Localização']].groupby(['Rede', 'Localização'], as_index=False).mean()
    sns.catplot(
        x = 'Rede',
        y = 'Taxa de Aprovação',
        hue = 'Localização',
        kind = 'bar',
        data = media_aprovacao
    );
    st.pyplot(fig)
elif option == 'Média de reprovações por rede e localização':
    media_reprovacao = df_escola_em[['Taxa de Reprovação', 'Rede', 'Localização']].groupby(['Rede', 'Localização'], as_index=False).mean()
    sns.catplot(
        x = 'Rede',
        y = 'Taxa de Reprovação',
        hue = 'Localização',
        kind = 'bar',
        data = media_reprovacao
    );
    st.pyplot(fig)
elif option == 'Média da taxa de abandono por rede e localização':
    media_abandono = df_escola_em[['Taxa de Abandono', 'Rede', 'Localização']].groupby(['Rede', 'Localização'], as_index=False).mean()
    sns.catplot(
        x = 'Rede',
        y = 'Taxa de Abandono',
        hue = 'Localização',
        kind = 'bar',
        data = media_abandono
    );    
    st.pyplot(fig)
    
    #Não to conseguindo fazer esse rodar!!
elif option == 'Média de abandono ao longo do tempo':
    media_abandono2 = df_escola_em[['Taxa de Abandono', 'Rede', 'Localização', 'Ano']].groupby(['Ano', 'Rede', 'Localização'], as_index=False).mean()
    media_abandono2["Ano"] = media_abandono2["Ano"].astype('str')
    # rede = st.selectbox(
    #  'Escolha a rede',
    #  ('Estadual', 'Federal', 'Municipal', 'Privada'))
    localizacao = st.selectbox('Escolha a localização', ('Rural', 'Urbana'))
    media_abandono2 = media_abandono2.loc[(media_abandono2['Localização'] == localizacao.lower())]
    # fig = sns.set(rc={'figure.figsize':(5,5)})

    # rel = sns.relplot(x=media_abandono2['Ano'], y=media_abandono2["Taxa de Abandono"],
    #                col=media_abandono2["Rede"], row=media_abandono2["Localização"], height=3,
    #                estimator=None, data=media_abandono2, kind = "line");
    # rel.set(xticks=[])
    fig = px.line(media_abandono2, x="Ano", y="Taxa de Abandono", color='Rede', template = 'simple_white'
)
    st.plotly_chart(fig)
