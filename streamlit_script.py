# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import numpy as np

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
    colunas = ['ID Escola', 'Taxa de Aprovação','Taxa de Reprovação', 'Taxa de Abandono', 'Ano', 'Rede', 'Localização', 'Média de Alunos por Turma','Média de Horas-Aula Diária','Taxa de Distorção Idade-Série', 'Porcentual de Docentes com Curso Superior', 'Região']

head = st.number_input("Digite quantas linhas você deseja:", 1, 100)

st.dataframe(df_escola_em.head(head)[colunas])

option = st.radio(
     'Escolha uma visualização',
     ('Correlação', 'Outra'))

df_escola_em_dummies = pd.read_pickle('df_escola_em_dummies.pkl')
corr = df_escola_em_dummies.corr()
fig = sns.set(rc={'figure.figsize':(13.7,10.27)})

ax = sns.heatmap(   corr, 
                    vmin=-1, vmax=1, center=0, 
                    cmap=sns.diverging_palette(20, 220, n=200), 
                    square=True
                )
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=65,
    horizontalalignment='right'
);

if option == 'Correlação':

    st.pyplot(fig)

    st.set_option('deprecation.showPyplotGlobalUse', False)
elif option == 'Outra':
    st.write('No processo de adicionar mais')
    
