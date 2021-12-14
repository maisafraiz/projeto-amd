# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import numpy as np
import plotly.express as px

st.title('Escolas brasileiras - Ensino Médio')

st.header('Introdução')

st.write('O projeto a seguir, apresentado para a matéria de Aquisição e Manipulação de Dados, tem como objetivo investigar os fatores que influenciam o ensino médio brasileiro.')
st.write('Utilizando informações oficiais do governo, coletadas pelo INEP (Instituto Nacional de Estudos e Pesquisas Educacionais), podemos analisar dados como a região, a média de alunos por turma, o tipo de rede da escola, entre outros, e analisar como esses se relacionam com taxas que podem servir de métrica para o desempenho da escola, aqui consideradas a taxa de aprovação, de reprovação e de abandono.')
st.write('Estamos cientes dos muitos fatores socio-econômicos que estão envolvidos quando discutimos sobre a educação brasileira, porém nesse projeto buscaremos fazer análises que dependem apenas dos dados contidos na base do INEP.')

st.header('Conheça os nossos dados')

st.write('Para o leitor poder obter um pouco mais de familiaridade com os dados utilizados no projeto, segue abaixo uma tabela interativa do dataset que estaremos utilizando.')
st.write('É possível selecionar quais colunas você deseja visualizar e quantas linhas deseja ver (escolha um número entre 1 e 350586), possibilitando uma visualização sucinta de uma base de dados consideravelmente populada. Também é possível organizar o modo que a tabela é exibida ao clicar em cima dos labels de cada coluna.')


visualizar = st.radio('Você deseja selecionar as colunas ou visualizar todas?',['Exibir todas', 'Selecionar colunas'])

df_escola_em = pd.read_pickle('df_escola_em.pkl')

df_escola_em.rename(columns={'id_escola': 'ID Escola', 'taxa_aprovacao_em': 'Taxa de Aprovação', 'taxa_reprovacao_em': 'Taxa de Reprovação', 'taxa_abandono_em':'Taxa de Abandono', 'ano': 'Ano', 'rede': 'Rede', 'localizacao': 'Localização', 'atu_em': 'Média de Alunos por Turma', 'had_em': 'Média de Horas-Aula Diária', 'tdi_em':'Taxa de Distorção Idade-Série', 'dsu_em':'Porcentual de Docentes com Curso Superior', 'regiao':'Região'}, inplace = True)

if visualizar == "Selecionar colunas":
    colunas = st.multiselect("Selecione todas as colunas que deseja visualizar:", ['ID Escola', 'Taxa de Aprovação','Taxa de Reprovação', 'Taxa de Abandono', 'Ano', 'Rede', 'Localização', 'Média de Alunos por Turma','Média de Horas-Aula Diária','Taxa de Distorção Idade-Série', 'Porcentual de Docentes com Curso Superior', 'Região'])
else:
    colunas = ['ID Escola', 'Taxa de Aprovação','Taxa de Reprovação', 'Taxa de Abandono', 'Ano', 'Rede', 'Localização', 'Média de Alunos por Turma','Média de Horas-Aula Diária','Taxa de Distorção Idade-Série', 'Porcentual de Docentes com Curso Superior', 'Região']

head = st.number_input("Digite quantas linhas você deseja:", 1, 350586)

st.dataframe(df_escola_em.head(head)[colunas])

st.header('Visualizações')

st.write('Também temos disponíveis algumas visualizações sobre esses dados, que nos ajudam a observar melhor a correlação entre os fatores e as taxas métricas escolhidas.')
st.write(' Selecione abaixo a visualização que deseja exibir.')


option = st.selectbox(
     '',
     ('Correlação das colunas', 'Média de aprovações por rede e localização', 'Média de reprovações por rede e localização', 'Média da taxa de abandono por rede e localização', 'Média de taxa de abandono por região', 'Média de abandono ao longo do tempo'))

df_escola_em_dummies = pd.read_pickle('df_escola_em_dummies.pkl')
df_escola_em_dummies.rename(columns={'taxa_aprovacao_em': 'Taxa de Aprovação', 'taxa_reprovacao_em': 'Taxa de Reprovação', 'taxa_abandono_em':'Taxa de Abandono', 'ano': 'Ano', 'rede_estadual': 'Rede Estadual', 'rede_federal': 'Rede Federal','rede_municipal': 'Rede Municipal','rede_privada': 'Rede Privada', 'localizacao_rural': 'Rural', 'localizacao_urbana': 'Urbana','atu_em': 'Média de Alunos por Turma', 'had_em': 'Média de Horas-Aula Diária', 'tdi_em':'Taxa de Distorção Idade-Série', 'dsu_em':'Porcentual de Docentes com Curso Superior', 'regiao_Centro-Oeste':'Região Centro-Oeste', 'regiao_Nordeste':'Região Nordeste', 'regiao_Sudeste':'Região Sudeste', 'regiao_Sul':'Região Sul', 'regiao_Norte': 'Região Norte'}, inplace = True)


corr = df_escola_em_dummies.corr()


fig = sns.set(rc={'figure.figsize':(10, 10)})

if option == 'Correlação das colunas':
    st.subheader('Correlação entre as colunas.')
    st.write('O gráfico a seguir, do estilo heatmap, nos permite observar como cada atributo influencia o outro de acordo com o nosso set de dados. Podemos perceber que em muitas duplas, a correlação não é muito forte, mas é interessante observar onde as cores estão mais fortes, e perceber que apesar que algumas relações são triviais (como a taxa de reprovação e a taxa de reprovação), outras têm maior valor analítico.')
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
elif option == 'Média de aprovações por rede e localização':
    st.subheader("Média de aprovações, filtrada por rede e localização.")
    st.write("Nesse histograma, é possível perceber que a taxa de aprovação não parece estar fortemente relacionada com esses dados. Apesar, por exemplo, de ser maior em escolas privadas do que municipais, a diferença não é muito significativa, e a localização ser rural ou urbana não parece ser de muita influência.")
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
    st.subheader("Média de reprovações, filtrada por rede e localização.")
    st.write('Nesse histograma., é possível perceber que, independentemente da rede, a taxa de reprovação é significativamente maior em escolas urbanas do que em escolas rurais. Podemos também perceber que, em geral, escolas privadas possuem menos reprovações, e escolas federais, mais. Escolas estaduais parecem ser as que a localização mais influencia na taxa.')
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
    st.subheader("Média de taxa de abandono, filtrada por rede e localização.")
    st.write('Nesse histograma, podemos perceber que escolas em localizações rurais são as que mais há abandono de alunos. Vale enfatizar que os nossos dados são apenas de alunos do ensino médio, onde há uma maior chance de alunos abandonarem a escola em busca de aumentar a renda familiar. Porém, não podemos afirmar que essa é a razão que escolas rurais têm maior taxa de abandono, pois como foi dito na introdução do projeto, os fatores sócio-econômicos não estão sendo avaliados por não estarem contidos na base de dados utilizada. Podemos também perceber que escolas privadas urbanas têm a menor taxa de abandono, enquanto escolas privadas rurais têm a quarta menor taxa. A maior média de taxa de abandono está nas escolas municipais rurais, atingindo quase 12%.')
    media_abandono = df_escola_em[['Taxa de Abandono', 'Rede', 'Localização']].groupby(['Rede', 'Localização'], as_index=False).mean()
    sns.catplot(
        x = 'Rede',
        y = 'Taxa de Abandono',
        hue = 'Localização',
        kind = 'bar',
        data = media_abandono
    );    
    st.pyplot(fig)
elif option == 'Média de abandono ao longo do tempo':
    st.subheader('Média de abandono nas escolas, de acordo com o ano.')
    st.write("Primeiramente, selecione a localização que deseja visualizar. O gráfico que aparecerá é interativo!")
    media_abandono2 = df_escola_em[['Taxa de Abandono', 'Rede', 'Localização', 'Ano']].groupby(['Ano', 'Rede', 'Localização'], as_index=False).mean()
    media_abandono2["Ano"] = media_abandono2["Ano"].astype('str')
    st.write('É possível perceber que, independetemente da localização, a taxa de abandono diminuiu com o passar dos anos. Que bom! As outras informações condizem com histograma mostrado na opção "Média da taxa de abandonos por rede e localização".')
    localizacao = st.selectbox('Escolha a localização', ('Rural', 'Urbana'))
        
    media_abandono2 = media_abandono2.loc[(media_abandono2['Localização'] == localizacao.lower())]

    fig = px.line(media_abandono2, x="Ano", y="Taxa de Abandono", color='Rede', template = 'simple_white'
)
    st.plotly_chart(fig)
else:
    st.subheader("Média de taxa de abandono, filtrada pela região.")
    st.write("Podemos perceber que há um grande efeito da região na porcentagem de alunos abandonando a escola durante o ensino médio, onde o Norte apresenta uma taxa muito maior que o Sudeste. Isso pode estar relacionado com fatores sócio-esconômicos, como o PIB de cada região.")
    media_abandono = df_escola_em[['Taxa de Abandono', 'Região']].groupby(['Região'], as_index=False).mean()
    sns.barplot(
        x = 'Região',
        y = 'Taxa de Abandono',
        data = media_abandono
    );
    st.pyplot(fig)
    
st.header('Modelo')

st.write('Usando o algoritmo supervisionado Random Forest, treinamos um modelo que busca, dadas as informações disponíveis sobre uma escola, prever a taxa de aprovação ou a taxa de abandono da mesma.')
st.write('Podemos testar esse modelo alimentando-o com informações de uma escola fictícia e observando taxa que nos é retornada.')
st.write('Primeiramente, devemos escolher uma taxa para prever.')
st.subheader("Taxa")

taxa = st.selectbox("Selecione a taxa", ["Taxa de Aprovação", "Taxa de Abandono"])

if taxa == 'Taxa de Aprovação':
    st.write('A acurácia final desse modelo foi de 56.1%. Isso pode ser justificado pela baixa correlação entre os dados.')
else:
    st.write('A acurácia final desse modelo foi de 52.96%. Isso pode ser justificado pela baixa correlação entre os dados.')


st.subheader("Dados")

st.write("Agora, digite os dados da escola.")

#Ano, Atu, Had, Tdi, Dsu, estadual, federal, municipal, privada, rural, urbana, centro oeste, nordeste, norte, sudeste, sul
ano_modelo = st.number_input("Digite o ano", step = 1)
atu_modelo = st.number_input("Digite a média de aluno por turma", step = 0.01)
had_modelo = st.number_input("Digite a média de horas-aula diárias", step = 0.01)
tdi_modelo = st.number_input('Digite a taxa de distorção idade-série', step = 0.01)
dsu_modelo = st.number_input('Digite o porcentual de docentes com curso superior', step = 0.01, help = "Se deseja 100%, digite 100, e não 1")
rede_modelo = st.selectbox("Escolha a rede", ["Estudual", "Federal", "Municipal", "Privada"])
localizacao_modelo = st.selectbox('Escolha a localização', ['Rural', 'Urbana'])
regiao_modelo = st.selectbox('Escolha a região', ['Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul'])

def normaliza(valor, coluna):
    valmin = df_escola_em[coluna].min()
    valmax = df_escola_em[coluna].max()
    normalizado = (valor - valmin)/(valmax - valmin)
    return normalizado


ano_vect = ano_modelo
atu_vect = normaliza(atu_modelo, 'Média de Alunos por Turma')
had_vect = normaliza(had_modelo, 'Média de Horas-Aula Diária')
tdi_vect = normaliza(tdi_modelo, 'Taxa de Distorção Idade-Série')
dsu_vect = dsu_modelo/100


estadual_vect, federal_vect, municipal_vect, privada_vect = 0, 0, 0, 0
if rede_modelo == "Estadual":
    estadual_vect = 1
elif rede_modelo == "Federal":
    federal_vect = 1
  
elif rede_modelo == "Municipal":
    municipal_vect = 1
else:
    privada_vect = 1
    
    
rural_vect, urbana_vect = 0, 0
if localizacao_modelo == "Rural":
    rural_vect = 1
else:
    urbana_vect = 1
    
centrooeste_vect, nordeste_vect, norte_vect, sudeste_vect, sul_vect = 0, 0, 0, 0, 0
if regiao_modelo == 'Centro-Oeste':
    centrooeste_vect = 1
elif regiao_modelo == 'Nordeste':
    nordeste_vect = 1
elif regiao_modelo == 'Norte':
    norte_vect = 1
elif regiao_modelo == 'Sudeste':
    sudeste_vect = 1
else:
    sul_vect = 1
    

vect = [ano_vect, atu_vect, had_vect, tdi_vect, dsu_vect, estadual_vect, 
        federal_vect, municipal_vect, privada_vect, rural_vect, urbana_vect, 
        centrooeste_vect, nordeste_vect, norte_vect, sudeste_vect, sul_vect] 
   
array = np.array(vect)
array = array.reshape(1, -1)


if taxa == 'Taxa de Aprovação':
    with open("models/model_aprovacao.pkl", 'rb') as file:  
        modelinho = pickle.load(file)
    resultado = modelinho.predict(array)
else:
    with open("models/model_abandono.pkl", 'rb') as file:  
        modelinho = pickle.load(file)
    resultado = modelinho.predict(array)


st.subheader("Resultado")

st.write(taxa, ": ", resultado)

terminado = st.checkbox("Marque aqui se oficialmente acabou o período e começou as férias.")

if terminado:
    st.write("Hurrayy!")
    st.balloons()


