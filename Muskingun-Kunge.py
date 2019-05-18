#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:14:43 2019

@author: fm_pc
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("As formulas e dados de referencia sao do arquivo Exc_MsK_e_Msk-Cunge_24-04-2019.pdf")


########DADOS 
#comprimento do subtrecho, equivalente a 1/3 do trecho total de 18km
dx = 6000

#celeridade em m/s
c = 2

#largura da base do canal
B = 25.3

#inclinacao
So = 0.001

#fluxo lateral
q = 0 

#Vazao de inflow e tempo na forma de lista de lista.
df =  x = [[0,10],[1,12],[2,18],[3,28.5],[4,50],[5,78],[6,107],[7,134.5],[8,147],[9,150],[10,146],[11,129],[12,105],[13,78],[14,59],[15,45],[16,33],[17,24],[18,17],[19,12],[20,10]]

#dafaframe com vazao e tempo
df = pd.DataFrame(df, columns =["Time(hr)","Flow(m3/s)"] )


#vazao de pico em m3/s
Qpico = 150


########FUNCOES UTEIS

#Calculo de K
def K(dx,c):
    K = dx/c
    return K

#Calculo de X:
def X(Qpico,B,So,c,dx):
    return (1-(Qpico/(B*So*c*dx)))*0.5

#testa valor de dt
def teste_dt(dt,tp):
    if dt/tp<0.2:
        return "Diminua o dt"
    else:
        return"dt ta razoavel."

#garante a inexistencia de vazoes negativas
def teste_vazoes_negativas(dx,dt,cm,X,K):
    if (dx/dt <= cm/2*X) and (dx/dt >= cm/2*(1-X)):
        return "O dominio das variaveis e valido"
    else:
        return "O dominio das variaveis nao e valido"
        if dt/K<2*X:
            return" distancia entre secoes e muito grande ou intervalo de tempo e pequeno"
        elif dt/K > 2*(1-X):
            return "intervalo de tempo muito grande."
        
#Calculo de mi
def mi(Qpico, B, So):
    return Qpico/2*B*So

#Calculo de celeridade
def celeridade(dQ,dA):
    return dQ/dA





#Calcula vazao prevista como a multiplicacao entre os vetores de vazao e Cs
#O vetor Vazoes tera vazoes, nessa ordem: Q_n_j ; Q_n+1_j ; Q n_j+1; q
#df e a tabela com os valores e o tamanho do trecho igual ao tamanho do canal
def vazao_prevista(Vazoes, Cs, Inflow,df, tamanho_canal,q):
    trechos = []
    #cria colunas com o nome de cada trecho
    for trecho in range(1,int(tamanho_canal/dx)+1):
        df[str(trecho)]=np.nan
        trechos.append(str(trecho))
    #considera a vazao no tempo zero igual a zero.
    for linha in range(len(df['Flow(m3/s)'])) :
        if linha == 0:
            for coluna in trechos:
                df[coluna][linha] = df['Flow(m3/s)'][linha]
    #calcula a vazao para momentos posteriores ao instante inicial
        else:
            print(linha)
            for coluna in trechos:
                #A coluna Flow interage diretamente com a vazao antes do trecho
                coluna = int(coluna)
                if coluna == 1:
                    Q_n_j = df['Flow(m3/s)'][linha-1]
                    Q_n_mais1_j = df['Flow(m3/s)'][linha]
                    Q_n_j_mais1 = df[str(coluna)][linha-1]
                    
                    
                #A vazao das outras colunas so dependem daquelas calculadas anteriormente
                else: 
                    Q_n_j = df[str(coluna-1)][linha-1]
                    Q_n_mais1_j= df[str(coluna-1)][linha]
                    Q_n_j_mais1 = df[str(coluna)][linha-1]
                    
               
                Vazoes = []
                Vazoes.append(Q_n_j)
                Vazoes.append(Q_n_mais1_j)
                Vazoes.append(Q_n_j_mais1)
                Vazoes.append(q)
                Vazoes = np.array(Vazoes)
                Q_n_mais1_j_mais1 = Vazoes.dot(Cs)
                df[str(coluna)][linha] =  Q_n_mais1_j_mais1
            
    
def Vazao_por_Manning(n,A,R,So):
    return (1.49 * A * (R**(2/3)) * (So**(1/2)) ) /n
    

#Exemplo 3
K = K(dx,c)
X = X(Qpico,B,So,c,dx)
tp = K
dt = 3600
teste_dt(dt,tp)
tamanho_canal = 18000


cm = 5/3
mi = mi(Qpico, B, So)
Cs = np.array(Cs(dt,K,X))

#Exemplo4
#largura da base do canal
B = 25.3

#inclinacao
So = 0.001

#fluxo lateral
q = 0 

Qpico = 150

n = 0.029

