from numpy.random import choice
import numpy as np
from crops import *
from percent import *
from matrepr import mprint

plots = int(input("Quantos plots (espaços de terra) deseja?"))
dias = int(input("Quantos dias deseja?"))
#cromossomo = [['' for i in range(plots)]for j in range(dias)]
tam_pop = int(input("Qual o tamanho da população desejado?"))
populacao = [[['' for i in range(plots)]for j in range(dias)] for k in range(tam_pop)]
geracoes = int(input("Quantas gerações deseja?"))
cruzamentos = int(input("Quantos cruzamentos por geração?"))
porcMutacao = int(input("Quantos porcento de mutação deseja?"))
mutacao = (porcMutacao/100)

#print(f'choice(crops)[id]: {(choice(crops))["id"]}')

def StartPopulacao():        
    for individuo in populacao:
        contDias = 0
        for plotPorDia in (individuo):
            #print(f'plotPorDia: {plotPorDia}')
            for plot in range(plots):
                #print("plotAtual: ", {plotPorDia[plot]})
                if plotPorDia[plot] == '':
                    crop = (choice(crops))
                    #print(f'crop: {crop["nome"]}')
                    if (contDias + (crop['time'])<31):
                        for dia in range(crop['time']):
                            if crop['nome'] == 'tomato':
                                if (dia == 9) or (dia == 3) or (dia == 5) or (dia == 7):
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
    for individuo in populacao:
        dia = 0
        for plotPorDia in individuo:
            campo = 0
            for plot in plotPorDia:
                quantidadeColhida = 0
                if individuo[dia][campo][0:5]=='colhe':
                    if VizinhosQuantidade(individuo,dia,campo) and VizinhosQualidade(individuo,dia,campo):
                        quantidadeColhida = choice(bothBonus)
                        #print("both")     
                    elif VizinhosQuantidade(individuo,dia,campo):
                        quantidadeColhida = choice(quantityBonus)
                        #print("quantidade")      
                    elif VizinhosQualidade(individuo,dia,campo):
                        quantidadeColhida = choice(qualityBonus)
                        #print("qualidade")  
                    else:
                        quantidadeColhida = choice(noBonus)
                        #print("nenhum"
                    individuo[dia][campo] = f'{individuo[dia][campo][0:5][0:5]} {quantidadeColhida}{individuo[dia][campo][5:(len(individuo[dia][campo]))]}'
                    #print("producePrice:",producePrice)
                #print(f'individuo[{dia}][{campo}]: {individuo[dia][campo]}')
                campo+=1 
            #print("dia:",dia)
            dia+=1
    #Printando cada indivíduo:
    #mprint(individuo,max_rows=None,max_cols=None)
        
    return populacao

def VizinhosQualidade(individuo,dia,campo):
    vizinhos = ['']*4
    for i in range(4):
        if i==0:
            x=-1
            y=0
        elif i==1:
            x=0
            y=-1
        elif i==2:
            x=0
            y=1
        elif i==3:
            x=1
            y=0
        try:
            vizinhos[i]=individuo[dia+x][campo+y]
            if vizinhos[i]!='':
                if vizinhos[i][0:5]=='colhe':
                    vizinhos[i]=vizinhos[i][10:(len(vizinhos[i]))] 
        except IndexError:
            vizinhos[i]=''
    if 'corn' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3]}:
        return True
    if 'cotton' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3]}:
        return True
    
    return False

def VizinhosQuantidade(individuo,dia,campo):
    vizinhos = ['']*4
    for i in range(4):
        if i==0:
            x=-1
            y=0
        elif i==1:
            x=0
            y=-1
        elif i==2:
            x=0
            y=1
        elif i==3:
            x=1
            y=0
        try:
            vizinhos[i]=individuo[dia+x][campo+y]
        except IndexError:
            vizinhos[i]=''
    if 'rice' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3]}:
        return True
    if 'wheat' in {vizinhos[0],vizinhos[1],vizinhos[2],vizinhos[3]}:
        return True
    return False
        
        
        
def CalculaFitness(populacao): 
    fitness = [0 for i in range(len(populacao))]
    contFitness = 0
    for individuo in populacao:
        dia = 0
        for plotPorDia in individuo:
            campo = 0
            for plot in plotPorDia:
                producePrice = 0
                if individuo[dia][campo][0:5]=='colhe':
                    price = [crop['price'] for crop in crops if crop['nome']==plot[10:len(plot)]][0]  
                    quantidadeColhida = float(plot[6:9])
                    producePrice = price*quantidadeColhida
                    fitness[contFitness] += producePrice
                #print(f'individuo[dia][campo]: {individuo[dia][campo-1]}')
                campo+=1 
            dia+=1
        contFitness += 1            
    return fitness

def Cruzamento(populacao, fitness,cruzamentos):
    filhos = ['']*cruzamentos
    paisPossiveis = ['']*(int((len(fitness))/2))
    aux = fitness.copy()
    #print("aux:",aux)
    for i in range(len(paisPossiveis)):
        index_max = np.argmax(aux)
        aux[index_max] = 0
        paisPossiveis[i] = index_max
        #print(f'paisPossiveis: {paisPossiveis}')
        #print("aux:",aux)
    for j in range(cruzamentos):
        aux2 = paisPossiveis.copy()
        #print("aux2:",aux2)        
        escolha1 = choice(aux2)
        aux2.pop(aux2.index(escolha1))
        escolha2 = choice(aux2)
        #print("aux2:",aux2)   
        pai1 = populacao[escolha1].copy()
        pai2 = populacao[escolha2].copy()
        pai2Tratado = pai2[15:30].copy()
        #mprint(pai2Tratado,max_rows=None,max_cols=None)
        for i in range(int(len(pai2Tratado[0]))):
            #print("Antes:")
            #mprint(pai2Tratado,max_rows=None,max_cols=None)
            #print("i",i)
            if pai2Tratado[0][i] != '':
                if pai2Tratado[0][i].find('tomato')!= -1:
                    cont = 0
                    #print("pai2Tratado[cont][i]",pai2Tratado[cont][i])
                    while pai2Tratado[cont][i] == 'tomato':
                        #print('cont',cont)
                        cont+=1
                    if cont>1:
                        continue
                    else:
                        cont2 = 0
                        #mprint(pai2Tratado,max_rows=None,max_cols=None)
                        while pai2Tratado[cont2][i].find('tomato') != -1:
                            #print("pai2Tratado[cont2][i]",pai2Tratado[cont2][i])
                            pai2Tratado[cont2][i] = ''
                            #print("cont2:",cont2)
                            if cont2 == 6:
                                break
                            cont2+=1
                elif pai2Tratado[0][i][0:5] == 'colhe':
                    pai2Tratado[0][i] = ''
                else:
                    contDias = 1
                    #mprint(pai2Tratado,max_rows=None,max_cols=None)
                    #print("i:",i)
                    while pai2Tratado[contDias][i][0:5] != 'colhe':
                        #print("contDias:",contDias)
                        contDias += 1
                        if contDias>13:
                            break
                    if contDias<14:
                        #print("cont",contDias)
                        cropNome = pai2Tratado[contDias][i][10:(len(pai2Tratado[contDias][i]))]
                        #print("nome:",cropNome)
                        tempoCrescimento = [crop['time'] for crop in crops if crop['nome']==cropNome][0]
                        #print("var:",tempoCrescimento)
                        #print("tempo:",tempoCrescimento)
                        #print("contDias:",contDias)
                        if tempoCrescimento>(contDias+1):
                            for k in range(contDias+1):
                                pai2Tratado[k][i] = '' 
            #print("paitratado")
            #mprint(pai2Tratado,max_rows=None,max_cols=None)       
        filho = pai1[0:15] + pai2Tratado
        filhos[j]=(filho)
        #mprint(filho)
    filhos=Mutacao(filhos)
    return filhos
    
def Mutacao(filhos):
    for filho in filhos:
        porcentagem = [0 for i in range(1000)]
        for i in range(int(mutacao*1000)):
            porcentagem[i]=1
        #print("filho antes de mutado:") 
        #mprint(filho,max_rows=None,max_cols=None)
        if choice(porcentagem)==1 or choice(porcentagem)==0:
            cropMutado = choice(crops)
            lugarMutacao = [(np.random.randint(30,size=1))[0],(np.random.randint(9,size=1))[0]]
            #print("lugar:",lugarMutacao)
            #print("cropMutado:",cropMutado)
            if filho[lugarMutacao[0]][lugarMutacao[1]] != '':
                if (30-lugarMutacao[0]<cropMutado['time']):
                    if  cropMutado['nome'] != 'tomato':
                        for i in range(lugarMutacao[0],30):
                            #print("i",i)
                            filho[i][lugarMutacao[1]] = ''
                    elif 30-lugarMutacao[0] > 3:
                        dia = 0
                        for i in range(lugarMutacao[0],30):
                            if (dia == 9) or (dia == 3) or (dia == 5) or (dia == 7):
                                filho[i][lugarMutacao[1]] = (f'colhe {cropMutado["nome"]}')
                                if VizinhosQuantidade(filho,i,lugarMutacao[1]) and VizinhosQualidade(filho,i,lugarMutacao[1]):
                                    quantidadeColhida = choice(bothBonus)
                                    #print("both")     
                                elif VizinhosQuantidade(filho,i,lugarMutacao[1]):
                                    quantidadeColhida = choice(quantityBonus)
                                    #print("quantidade")      
                                elif VizinhosQualidade(filho,i,lugarMutacao[1]):
                                    quantidadeColhida = choice(qualityBonus)
                                    #print("qualidade")  
                                else:
                                    quantidadeColhida = choice(noBonus)
                                    #print("nenhum"
                                filho[i][lugarMutacao[1]] = (f'{filho[i][lugarMutacao[1]][0:5]} {quantidadeColhida}{filho[i][lugarMutacao[1]][5:(len(filho[i][lugarMutacao[1]]))]}')
                            #print("aquio:",filho[i][lugarMutacao[1]])
                            else:
                                filho[i][lugarMutacao[1]] = cropMutado["nome"]
                            dia += 1
                else:
                    for i in range(cropMutado['time']):
                        if i == (cropMutado['time']-1):
                            aux ='colhe '+cropMutado['nome']
                            #print("assim:", aux)
                            filho[lugarMutacao[0]+i][lugarMutacao[1]] = aux
                            #print("Aqui2:",filho[lugarMutacao[0]+i][lugarMutacao[1]])
                            if VizinhosQuantidade(filho,lugarMutacao[0]+i,lugarMutacao[1]) and VizinhosQualidade(filho,lugarMutacao[0]+i,lugarMutacao[1]):
                                quantidadeColhida = choice(bothBonus)
                                #print("both")     
                            elif VizinhosQuantidade(filho,lugarMutacao[0]+i,lugarMutacao[1]):
                                quantidadeColhida = choice(quantityBonus)
                                #print("quantidade")      
                            elif VizinhosQualidade(filho,lugarMutacao[0]+i,lugarMutacao[1]):
                                quantidadeColhida = choice(qualityBonus)
                                #print("qualidade")  
                            else:
                                quantidadeColhida = choice(noBonus)
                                #print("nenhum"
                            filho[lugarMutacao[0]+i][lugarMutacao[1]] = f'{filho[lugarMutacao[0]+i][lugarMutacao[1]][0:5]} {quantidadeColhida}{filho[lugarMutacao[0]+i][lugarMutacao[1]][5:(len(filho[lugarMutacao[0]+i][lugarMutacao[1]]))]}'
                        else:
                            filho[lugarMutacao[0]+i][lugarMutacao[1]] = cropMutado["nome"]
                    if (lugarMutacao[0]+cropMutado['time']-1)<30:
                        #print("valor:",(lugarMutacao[0]+cropMutado['time']-1))
                        if filho[lugarMutacao[0]][lugarMutacao[1]].find('tomato') != -1:
                            cont = 1
                            while filho[cont][lugarMutacao[1]] == 'tomato':
                                cont+=1
                            if cont>4:
                                continue
                            else:
                                cont = 0
                                while filho[cont][lugarMutacao[1]].find('tomato') != -1:
                                    filho[cont][lugarMutacao[1]] = ''
                                    cont+=1
                        if filho[lugarMutacao[0]+cropMutado['time']-1][lugarMutacao[1]] != '':
                            i=0
                            #print("aksjdka:")
                            #mprint(filho,max_rows=None,max_cols=None)
                            if filho[lugarMutacao[0]+cropMutado['time']-1][lugarMutacao[1]][0:5] == 'colhe':
                                filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]]=''
                            else:
                                while(filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]][0:5]!='colhe'):
                                    filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]]=''
                                    i+=1
                                    #print("i",i)
                                    print("alterado:")
                                    print(filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]])
                                filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]]=''
            #print("filho mutado:") 
            #mprint(filho,max_rows=None,max_cols=None)
    return filhos
            
def EscolheNovaPopulacao(populacao,filhos,fitnessPopulacao,fitnessFilhos):
    antigaPopulacao = populacao+filhos
    novaPopulacao = [[['' for i in range(plots)] for j in range(dias)] for k in range((len(populacao)))]
    fitnessNovaPopulacao = [0 for i in range((len(populacao)))]
    #print("Fitnessfilhos",fitnessFilhos)
    aux = fitnessPopulacao.copy()+fitnessFilhos.copy()
    #print("fitnessNovaPopulacao:",aux)
    #print("Aux:",aux)
    for i in range(len(populacao)):
        index_max = np.argmax(aux)
        #print("Antiga:")
        #mprint(antigaPopulacao[index_max])
        fitnessNovaPopulacao[i]=aux[index_max]
        novaPopulacao[i] = antigaPopulacao[index_max]
        aux[index_max] = 0
        #print("Nova:")
        #mprint(novaPopulacao[i])
        #print(f'paisPossiveis: {paisPossiveis}')
    #print("fitnessNovaPopulacao:",fitnessNovaPopulacao)
    #teste = CalculaFitness(populacao)
    #teste2 = CalculaFitness(novaPopulacao)
    #print("Teste:",teste)
    #print("Teste2",teste2)
    #print("Nova:")
    #mprint(novaPopulacao[0],max_rows=None,max_cols=None)
    
    return novaPopulacao,fitnessNovaPopulacao
    
def main():
    populacao = StartPopulacao()

    fitnessPopulacao = CalculaFitness(populacao)
        
    novaPopulacao =[]
    
    print(f'Fitness Geração 1: {fitnessPopulacao}')

    for i in range(geracoes-1):

        filhos = Cruzamento(populacao,fitnessPopulacao,(cruzamentos))

        fitnessFilhos = CalculaFitness(filhos)

        #print("fitness2",fitnessFilhos)

        novaPopulacao,fitnessPopulacao = EscolheNovaPopulacao(populacao,filhos,fitnessPopulacao,fitnessFilhos)
        
        print(f'Fitness Geração {i+2}: {fitnessPopulacao}')
        print(f'Fitness2 Geração {i+2}: {CalculaFitness(novaPopulacao)}')
        

    #fitnessPopulacao = CalculaFitness(populacao)    
    #print(f'Fitness populacao: {fitnessPopulacao}')  
    #fitnessPopulacao = CalculaFitness(novaPopulacao)
    #print(f'Fitness novaPopulacao: {fitnessPopulacao}')


main()
 
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