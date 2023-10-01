from numpy.random import choice
import numpy as np
from crops import *
from percent import *
from matrepr import mprint

plots,dias = (9, 30)
cromossomo = [[None for i in range(plots)]for j in range(dias)]
populacao = [cromossomo for i in range(10)]
#print(f'Cromossomo: \n{np.matrix(cromossomo)}')
#print(f'População: \n{np.array(populacao)}')
geracoes = 5
mutacao = 0.01

#print(f'choice(crops)[id]: {(choice(crops))["id"]}')

def StartPopulacao():        
    for individuo in populacao:
        contDias = 0
        for plotPorDia in (individuo):
            #print(f'plotPorDia: {plotPorDia}')
            for plot in range(plots):
                #print("plotAtual: ", {plotPorDia[plot]})
                if plotPorDia[plot] == None:
                    crop = (choice(crops))
                    #print(f'crop: {crop["nome"]}')
                    if (contDias + (crop['time'])<31):
                        for dia in range(crop['time']):
                            if crop['nome'] == 'tomato':
                                if (dia == 10) or (dia == 4) or (dia == 6) or (dia == 8):
                                    individuo[(contDias + dia)][plot] = (f'colhe {crop["nome"]}')
                                else:
                                    individuo[(contDias + dia)][plot] = crop["nome"]
                            else:
                                if dia == (crop['time']-1):
                                    individuo[(contDias + dia)][plot] = (f'colhe {crop["nome"]}')
                                else:
                                    individuo[(contDias + dia)][plot] = crop['nome']
                                #print("dia:",dia)
                                #print("contDias:", contDias)      
                    else:
                        break                
                else:
                    continue 
            contDias += 1
        
        #Printando cada indivíduo:
        #mprint(individuo)
        
    return populacao

def VizinhosQualidade(individuo,dia,campo):
    vizinhos = [None]*8
    for i in range(8):
        if i==0:
            x=-1
            y=-1
        elif i==1:
            x=-1
            y=0
        elif i==2:
            x=-1
            y=1
        elif i==3:
            x=0
            y=-1
        elif i==4:
            x=0
            y=1
        elif i==5:
            x=1
            y=-1
        elif i==6:
            x=1
            y=0
        elif i==7:
            x=1
            y=1
        try:
            vizinhos[i]=individuo[dia+x][campo+y]
        except IndexError:
            vizinhos[i]=None
    if 'corn' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3],vizinhos[4],vizinhos[5],vizinhos[6],vizinhos[7]}:
        return True
    if 'cotton' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3],vizinhos[4],vizinhos[5],vizinhos[6],vizinhos[7]}:
        return True
    return False

def VizinhosQuantidade(individuo,dia,campo):
    vizinhos = [None]*8
    for i in range(8):
        if i==0:
            x=-1
            y=-1
        elif i==1:
            x=-1
            y=0
        elif i==2:
            x=-1
            y=1
        elif i==3:
            x=0
            y=-1
        elif i==4:
            x=0
            y=1
        elif i==5:
            x=1
            y=-1
        elif i==6:
            x=1
            y=0
        elif i==7:
            x=1
            y=1
        try:
            vizinhos[i]=individuo[dia+x][campo+y]
        except IndexError:
            vizinhos[i]=None
    if 'rice' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3],vizinhos[4],vizinhos[5],vizinhos[6],vizinhos[7]}:
        return True
    if 'wheat' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3],vizinhos[4],vizinhos[5],vizinhos[6],vizinhos[7]}:
        return True
    return False
        
        
        
def CalculaFitness(populacao): 
    fitness = [0 for i in range(10)]
    contFitness = 0
    for individuo in populacao:
        dia = 0
        for plotPorDia in individuo:
            campo = 0
            for plot in plotPorDia:
                producePrice = 0
                if plot != None:
                    if plot[0:5]=='colhe':
                        crop = [crop['price'] for crop in crops if crop['nome']==plot[6:len(plot)]]  
                        crop = crop[0]
                        if VizinhosQuantidade(individuo,dia,campo) and VizinhosQualidade(individuo,dia,campo):
                            producePrice = crop*choice(bothBonus)
                            #print("both")     
                        elif VizinhosQuantidade(individuo,dia,campo):
                            producePrice = crop*choice(quantityBonus)
                            #print("quantidade")      
                        elif VizinhosQualidade(individuo,dia,campo):
                            producePrice = crop*choice(qualityBonus)
                            #print("qualidade")  
                        else:
                            producePrice = crop*choice(noBonus)
                            #print("nenhum")  
                        print("producePrice:",producePrice)
                        fitness[contFitness] += producePrice
                #print(f'individuo[dia][campo]: {individuo[dia][campo-1]}')
                campo+=1 
            dia+=1
        #for item in produce:
        #    if item == 'carrot':
        #        item == (crops[0]['price'])
        contFitness += 1            
    return fitness

#def Cruzamento:
    

StartPopulacao()

CalculaFitness(populacao)

print(crops[0]['price'])
        
#Algoritmo genético tem:

# 1-População formada por indivíduos

# 2-Cromossomos de cada indivíduo da população

# 3-Gerações

# 4-Cruzamentos

# 5-Mutação

# 6-Fitness

# Primeiro, escolhemos o tamanho da população, a quantidade de gerações e o valor de mutação
# Então, cada indivíduo(cromossomo) da população é gerado de forma aleatória
# Essa é a primeira geração, então é medido o fitness de cada indivíduo da população, e os 50% de melhor fitness participam do cruzamento
# O cruzamento seleciona indivíduos aleatoriamente e os cruza
# Os filhos são gerados com a primeira metade do cromossomo de um dos pais e a segunda metade do outro
# Ocorrem as mutações, onde é mudado aleatoriamente 1 parte do cromossomo de um dos filhos
# É calculado o fitness dos filhos 
# Os indivíduos com maior fitness repetem o processo enquanto houver gerações 