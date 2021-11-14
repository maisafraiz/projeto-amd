# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import numpy as np

st.write('# Introdução')

st.write('O objetivo do nosso projeto é entender quais são os fatores que influenciam os jovens e a educação brasileira. Utilizando os dados do INEP (Instituto Nacional de Estudos e Pesquisas Educacionais), podemos coletar o município, uf, média de alunos por turma, a taxa de reprovação, a taxa de abandono, a situação socio-econômica e diversas outras informações sobre o Ensino Médio de milhares de escolas ao redor do país e usar isso pra nos ajudar a compreender o que está por trás de uma educação de sucesso (ou não).')

st.write('# Conheça os nossos dados')

df_escola_em = pd.read_pickle('df_escola_em.pkl')

head = st.number_input("Selecione quantas linhas você deseja:", 1, 50)
st.dataframe(df_escola_em.head(head))

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
    
