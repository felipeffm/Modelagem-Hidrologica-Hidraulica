# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""
#importacao de pacotes utilizados ao longo do codigo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print('As formulas e dados foram retirados da fonte : http://yang.sdsu.edu/textbookhydrologyp275.html')


########DADOS

#Vazao de inflow medida na forma de array
Inflow = np.array([352, 587, 1353,2725, 4408.5, 5987, 6704, 6951, 6839, 6207, 5246, 4560, 3861, 3007, 2357.5, 1779, 1405, 1123, 952.5, 730, 605, 514, 422, 352, 352, 352])

#Pesos
C0= 0.1304
C1= 0.3044
C2= 0.5652

#duracao de tempo das medicoes
dt = 1

#O numero de medicoes e justamente a quantidade de vazoes medidas.
numero_vazoes_medidas = len(Inflow)
#criacao de uma tabela chamada "df" para armazenar os dados
df = pd.DataFrame()
#criacao da coluna inflow na tabela
df['Inflow'] = Inflow
#mostrar os dados de entrada
print('Os dados de Inflow sao')
print(df['Inflow'])

########FUNCOES UTEIS

#Calculo de C1, C2, C3 e C4 e os retorna em um array
#def Cs_Kunge(dt,K,X):
#    aux1 = dt/K 
#    aux2 = 1-X
#    C1 = (aux1 + 2*X) / (aux1 + 2*aux2)
#    C2 = (aux1 - 2*X) / (aux1 + 2*aux2)
#    C3 = (2*aux2 - aux1) / (aux1 + 2*aux2)
#    C4 = 2*aux1 / (aux1 + (2*aux2))
#    return [C1,C2,C3,C4]
#funcao que calcula minimos quadrados de duas series de dados(X, Y), no formato de array do pacote numpy

def MMQ(X,Y):
    #Calcular a e b dos minimos quadrados
    #.dot e o produto matricial da algebra linear
    denominador  = X.dot(X) - X.mean() * X.sum()
    a = (X.dot(Y) - Y.mean()*X.sum() ) / denominador
    b = (Y.mean() * X.dot(X) - X.mean()*X.dot(Y) ) / denominador

    #calcular o previsao de Y
    Yprev = a*X +b

    # calcular R²
    d1 = Y - Yprev
    d2 = Y - Y.mean()
    r2 = 1 - d1.dot(d1) / d2.dot(d2)
    return(r2,a)


#Funcao que calcula Outflow baseada no Inflow
def Inflow_gera_Outflow(Inflow, df):
    #Loop por cada valor de medicao
    #Antes de iniciar o barramento o Outflow 'e igual ao Inflow
    Outflow_I = Inflow[0]
    #Outflow sera um array com todos os valores de Outflow
    Outflow = np.array([Outflow_I])

    for delta_t in range(numero_vazoes_medidas - 1):
        Outflow_II = ( Inflow[delta_t  + 1] )*C0 + ( Inflow[delta_t] ) * C1 + C2 * Outflow_I
        Outflow = np.append(Outflow, Outflow_II)
        Outflow_I = Outflow_II
    #Criacao da coluna Outflow na tabela df, que 'e um dataframe do pacote pandas
    df['Outflow'] = Outflow
    print('Os dados de Outflow sao')
    print(df['Outflow'])


#Funcao que plota grafico Inflow vs Outflow
def grafico_Inflow_Outflow(Inflow,Outflow,dt):
    #descobrir numero de vazoes medidas de outra forma
    medidas = df.shape[0]
    #dimensionar eixo X
    t = np.arange(0, medidas*dt, dt)
    #nomear os eixos
    plt.xlabel('Outflow')
    plt.ylabel('Inflow')
    #coloca grade
    plt.grid(True)
    #plota
    plt.plot(t, Inflow, Outflow)
    #mostra
    plt.show()


#Funcao que acha o Save, dado um Inflow e um Outflow
def Inflow_e_Outflow_geram_Save (dt, Inflow, Outflow, df):
    #S 'e o Save e comeca vazio porque antes desse momento Inflow era igual a Outflow
    S = np.array([0.0])
    #S1 e o primeiro elemento de S
    S1 = S[0]
    #descobrir numero de vazoes medidas
    medidas = df.shape[0]
    #Loop por todas as linhas da tabela df
    for instante in range(1, medidas):
        S2 = S1 + (dt/2) * (Inflow[instante-1] +  Inflow[instante] - Outflow[instante-1] - Outflow[instante])
        S1 = S2
        S = np.append(S, S2)
    df['Save'] = S
    print('Os dados de Save sao')
    print(df['Save'])


#Funcao que acha pesos para todos os Xs entre 0 e 0.5 e retorna o melhor X (duas casas decimais) e seus respectivos pesos.
def Encontra_melhor_X(Inflow, Outflow, Save):
    #valores possiveis de x
    Possiveis_X = np.arange(0.000001,.5,.01)
    #declaracao de variavel com valor impossivel
    r2_anterior = 0.0
    #numero de vazoes medidas
    medidas = df.shape[0]
    #Nesse loop ao inves de trabalhar com objeto dataframe vou trabalhar com listas.
    #O loop acha o melhor valor de X depois de calcular todos os pesos para todos os X.
    for X in Possiveis_X:
        #Zerar variavel q vai receber todos os pesos a cada vez que troca o X
        Weighted_Flow = [0.0]
        #A primeira linha nao tem pesos, entao nao comecamos de range(0,medidas)
        for instante in range(1,medidas):
            W = X*Inflow[instante] + (1 - X)* Outflow[instante]
            Weighted_Flow.append(W)
        #Precisei transformar em array para aplicar minha funcao de minimos quadrados
        Weighted_Flow = np.array(Weighted_Flow)
        #a funcao MMQ retorna dois valores, de coeficiente angular e R2.
        result = MMQ(Weighted_Flow[1:], Save[1:])
        #O primeiro valor e R2
        r2 = result[0]
        #O segundo valor e o coeficiente angular
        a=result[1]
        #O loop abaixo vai guardar as informacoes do melhor R2
        if float(r2) > r2_anterior and r2_anterior != "":
            #O coeficiente angular e igual a K
            K = a
            melhor_X = X
            r2_anterior = r2
            Potencial_Weighted_Flow = Weighted_Flow
    #descoberto o melhor X vamos colocar ele na tabela
    nome_coluna = 'Flow_Weight'
    df[nome_coluna] = Potencial_Weighted_Flow
    print('O melhor X tem o valor de ' + str(melhor_X)[:5])
    print('K vale  ' + str(K)[:5])
    return melhor_X


def grafico_Weight_Save(Flow_Weight,Save):
   #nomear os eixos
    plt.xlabel('Save')
    plt.ylabel('Flow_Weight')
    #coloca grade
    plt.grid(True)
    #plota
    plt.scatter(Flow_Weight, Save)
    #mostra
    plt.show()
    
def Cs_Muskingung(dt,K,X):
    aux1 = dt/K 
    aux2 = 1-X
    C1 = (aux1 + 2*X) / (aux1 + 2*aux2)
    C2 = (aux1 - 2*X) / (aux1 + 2*aux2)
    C3 = (2*aux2 - aux1) / (aux1 + 2*aux2)
    C4 = 2*aux1 / (aux1 + (2*aux2))
    return [C1,C2,C3,C4]


########EXECUCAO DAS FUNCOES

Inflow_gera_Outflow(Inflow, df)

grafico_Inflow_Outflow(df['Inflow'],df['Outflow'],dt)

Inflow_e_Outflow_geram_Save (dt, df['Inflow'],df['Outflow'], df)

Encontra_melhor_X(df['Inflow'],df['Outflow'],df['Save'])

grafico_Weight_Save(df['Flow_Weight'],df['Save'])
