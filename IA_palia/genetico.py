from numpy.random import choice
import numpy as np
from crops import *
from percent import *
from matrepr import mdisplay, mprint

plots,dias = (9, 30)
cromossomo = [[None for i in range(plots)]for j in range(dias)]
populacao = [cromossomo for i in range(10)]
#print(f'Cromossomo: \n{np.matrix(cromossomo)}')
#print(f'População: \n{np.array(populacao)}')
geracoes = 5
mutacao = 0.01

#print(f'choice(crops)[id]: {(choice(crops))["id"]}')

#for individuo in populacao:
#    #print(f'individuo: {individuo}')
#    for plotPorDia in cromossomo:
#        individuo[plotPorDia]=int((choice(crops))["id"])
def start_populacao():        
    for individuo in populacao:
        cont_dias = 0
        for plotPorDia in (individuo):
            #print(f'plotPorDia: {plotPorDia}')
            for plot in range(plots):
                #print("plotAtual: ", {plotPorDia[plot]})
                if plotPorDia[plot] == None:
                    crop = (choice(crops))
                    #print(f'crop: {crop["nome"]}')
                    if (cont_dias + (crop['time'])<31):
                        for dia in range(crop['time']):
                            #print("dia:",dia)
                            #print("cont_dias:", cont_dias)
                            individuo[(cont_dias + dia)][plot] = crop['nome']
                    else:
                        break                
                        
                    #individuo[plotPorDia]=int((choice(crops))["id"])
                else:
                    continue 
            cont_dias += 1
            
        #mprint(individuo)
        

        
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