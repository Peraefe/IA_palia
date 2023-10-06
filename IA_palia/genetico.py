from numpy.random import choice
import numpy as np
from crops import *
from percent import *
from matrepr import mprint
from copy import deepcopy
from math import sqrt
import matplotlib.pyplot as plt

plots = int(input("Quantos espaços de terra (plots) deseja? (Dê um número quadrado! Ex: 9 (para plot 3x3))"))
dias = int(input("Quantos dias deseja?"))
#cromossomo = [['' for i in range(plots)]for j in range(dias)]
tam_pop = int(input("Qual o tamanho da população desejado?"))
populacao = [[['' for i in range(plots)]for j in range(dias)] for k in range(tam_pop)]
geracoes = int(input("Quantas gerações deseja?"))
cruzamentos = int(input("Quantos cruzamentos por geração?"))
porcMutacao = int(input("Quantos porcento de mutação deseja?"))
mutacao = (porcMutacao/100)


def StartPopulacao():        
    for individuo in populacao:
        contDias = 0
        for plotPorDia in (individuo):
            for plot in range(plots):
                if plotPorDia[plot] == '':
                    crop = (choice(crops))
                    if (contDias + (crop['time'])<dias):
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
                    individuo[dia][campo] = f'{individuo[dia][campo][0:5]} {quantidadeColhida}{individuo[dia][campo][5:(len(individuo[dia][campo]))]}'
                campo+=1 
            dia+=1
        
    return populacao

def VizinhosQualidade(individuo,dia,campo):
    dimensao_campo = int(sqrt(len(individuo[dia])))
    matriz = [['' for a in range(dimensao_campo)]for b in range(dimensao_campo)]
    vizinhos = ['' for c in range(4)]
    cont = 0
    x = 0
    y = 0
    for m in range(dimensao_campo):
        for n in range(dimensao_campo):
            if cont == campo:
                x = m
                y = n
            cont += 1
            try:
                matriz[m][n] = deepcopy(individuo[dia][n])
            except:
                matriz[m][n] = ''
    for g in range(4):
        if g == 0:
            w = -1
            z = 0
        elif g == 1:
            w = 0
            z = -1
        elif g == 2:
            w = 0
            z = 1
        elif g == 3:
            w = 1
            z = 0
        try:
            vizinhos[g]=matriz[x+w][y+z]
        except:
            vizinhos[g]=''
    if (vizinhos[0]).find('corn')!= -1 or (vizinhos[1]).find('corn')!= -1 or (vizinhos[2]).find('corn')!= -1 or (vizinhos[3]).find('corn')!= -1:
        return True
    if (vizinhos[0]).find('cotton')!= -1 or (vizinhos[1]).find('cotton')!= -1 or (vizinhos[2]).find('cotton')!= -1 or (vizinhos[3]).find('cotton')!= -1:
        return True
    return False

def VizinhosQuantidade(individuo,dia,campo):
    dimensao_campo = int(sqrt(len(individuo[dia])))
    matriz = [['' for a in range(dimensao_campo)]for b in range(dimensao_campo)]
    vizinhos = ['' for c in range(4)]
    cont = 0
    x = 0
    y = 0
    for m in range(dimensao_campo):
        for n in range(dimensao_campo):
            if cont == campo:
                x = m
                y = n
            cont += 1
            try:
                matriz[m][n] = deepcopy(individuo[dia][n])
            except:
                matriz[m][n] = ''
    for g in range(4):
        if g == 0:
            w = -1
            z = 0
        elif g == 1:
            w = 0
            z = -1
        elif g == 2:
            w = 0
            z = 1
        elif g == 3:
            w = 1
            z = 0
        try:
            vizinhos[g]=matriz[x+w][y+z]
        except:
            vizinhos[g]=''
    if (vizinhos[0]).find('rice')!= -1 or (vizinhos[1]).find('rice')!= -1 or (vizinhos[2]).find('rice')!= -1 or (vizinhos[3]).find('rice')!= -1:
        return True
    if (vizinhos[0]).find('wheat')!= -1 or (vizinhos[1]).find('wheat')!= -1 or (vizinhos[2]).find('wheat')!= -1 or (vizinhos[3]).find('wheat')!= -1:
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
                    #print("Aqui:",plot)
                    price = [crop['price'] for crop in crops if crop['nome']==plot[10:len(plot)]][0]  
                    quantidadeColhida = float(plot[6:9])
                    producePrice = price*quantidadeColhida
                    fitness[contFitness] += producePrice
                campo+=1 
            dia+=1
        contFitness += 1            
    return fitness

def Cruzamento(populacao, fitness,cruzamentos):
    filhos = ['' for j in range(cruzamentos)]
    paisPossiveis = ['' for i in range(int(len(fitness)/2))]
    aux = CalculaFitness(populacao)
    for i in range(len(paisPossiveis)):
        index_max = np.argmax(aux)
        paisPossiveis[i] = index_max
        aux[index_max] = 0
    for j in range(cruzamentos):
        aux2 = deepcopy(paisPossiveis)        
        escolha1 = choice(aux2)
        aux2.pop(aux2.index(escolha1))
        escolha2 = choice(aux2)  
        pai1 = deepcopy(populacao[escolha1])
        pai2 = deepcopy(populacao[escolha2])
        pai2Tratado = (pai2[int(dias/2):dias])
        for i in range(int(len(pai2Tratado[0]))):
            if (pai1[int(dias/2)-1][i]).find('tomato')!=-1 and pai2Tratado[0][i].find('tomato')!=-1:
                contaReverso = 1
                while (pai1[contaReverso][i]).find('tomate') != -1:
                    contaReverso += 1
                contaDireto = 1
                while (pai2Tratado[contaDireto][i]).find('tomato') != -1:
                    contaDireto += 1
                if (contaDireto+contaReverso)<4:
                    for a in range(contaDireto):
                        pai2Tratado[a][i]=''
                else:
                    for a in range(contaDireto):
                        if (contaReverso+a)==3 or (contaReverso+a)==5 or (contaReverso+a)==7 or (contaReverso+a)==9 or (contaReverso+a)==13 or (contaReverso+a)==15 or (contaReverso+a)==17 or (contaReverso+a)==19:
                            pai2Tratado[a][i]='colhe tomato'
                            quantidadeColhida = 0
                            if VizinhosQuantidade(pai2Tratado,a,i) and VizinhosQualidade(pai2Tratado,a,i):
                                quantidadeColhida = choice(bothBonus)
                                #print("both")     
                            elif VizinhosQuantidade(pai2Tratado,a,i):
                                quantidadeColhida = choice(quantityBonus)
                                #print("quantidade")      
                            elif VizinhosQualidade(pai2Tratado,a,i):
                                quantidadeColhida = choice(qualityBonus)
                                #print("qualidade")  
                            else:
                                quantidadeColhida = choice(noBonus)
                                #print("nenhum"
                            pai2Tratado[a][i]=f'colhe {quantidadeColhida} tomato'
                        else:
                            pai2Tratado[a][i]='tomato'
            elif pai1[int(dias/2)-1][i] == pai2Tratado[0][i] and pai2Tratado[0][1][0:5]!='colhe' and pai2Tratado[0][1]!='':
                contaReverso = 1
                while pai1[contaReverso][i] == pai2Tratado[0][i]:
                    contaReverso += 1
                contaDireto = 1
                while pai2Tratado[contaDireto][i] == pai2Tratado[0][i]:
                    contaDireto += 1
                tempoCrescimento = [crop['time'] for  crop in crops if crop['nome']==pai2Tratado[0][1]][0]
                if (contaDireto+contaReverso)<tempoCrescimento:
                    for a in range(contaDireto):
                        pai2Tratado[a][i]=''
                else:
                    quantidadeColhida=0
                    if VizinhosQuantidade(pai2Tratado,((tempoCrescimento-contaReverso)-1),i) and VizinhosQualidade(pai2Tratado,((tempoCrescimento-contaReverso)-1),i):
                        quantidadeColhida = choice(bothBonus)
                        #print("both")     
                    elif VizinhosQuantidade(pai2Tratado,((tempoCrescimento-contaReverso)-1),i):
                        quantidadeColhida = choice(quantityBonus)
                        #print("quantidade")      
                    elif VizinhosQualidade(pai2Tratado,((tempoCrescimento-contaReverso)-1),i):
                        quantidadeColhida = choice(qualityBonus)
                        #print("qualidade")  
                    else:
                        quantidadeColhida = choice(noBonus)
                        #print("nenhum"
                    pai2Tratado[(tempoCrescimento-contaReverso)-1][i] = (f'colhe {quantidadeColhida} {pai2Tratado[0][1]}')
                    for a in range(((tempoCrescimento-contaReverso)),contaDireto):
                        pai2Tratado[a][i]=''
            else:
                if pai2Tratado[0][i].find('tomato')!= -1:
                    cont = 0
                    while pai2Tratado[cont][i] == 'tomato':
                        cont+=1
                    if cont>2:
                        continue
                    else:
                        cont2 = 0
                        while pai2Tratado[cont2][i].find('tomato') != -1:
                            pai2Tratado[cont2][i] = ''
                            if cont2 == 8:
                                break
                            cont2+=1
                elif pai2Tratado[0][i][0:5] == 'colhe':
                    pai2Tratado[0][i] = ''
                else:
                    contDias = 1
                    while pai2Tratado[contDias][i][0:5] != 'colhe':
                        contDias += 1
                        if contDias>(int(dias/2)-1):
                            break
                    if contDias<int(dias/2):
                        cropNome = pai2Tratado[contDias][i][10:(len(pai2Tratado[contDias][i]))]
                        tempoCrescimento = [crop['time'] for crop in crops if crop['nome']==cropNome][0]
                        if tempoCrescimento>(contDias+1):
                            for k in range(contDias+1):
                                pai2Tratado[k][i] = ''    
        filho = pai1[0:(int(len(pai1)/2))] + pai2Tratado
        filhos[j]=(filho)
    filhos=Mutacao(filhos)
    return filhos
    
def Mutacao(filhos):
    for filho in filhos:
        porcentagem = [0 for i in range(1000)]
        for i in range(int(mutacao*1000)):
            porcentagem[i]=1
        if choice(porcentagem)==1:
            cropMutado = choice(crops)
            lugarMutacao = [(np.random.randint(dias,size=1))[0],(np.random.randint(plots,size=1))[0]]
            if filho[lugarMutacao[0]][lugarMutacao[1]] != '':
                if (dias-lugarMutacao[0]<cropMutado['time']):
                    if  cropMutado['nome'] != 'tomato':
                        for i in range(lugarMutacao[0],dias):
                            filho[i][lugarMutacao[1]] = ''
                    elif dias-lugarMutacao[0] > 3:
                        dia = 0
                        for i in range(lugarMutacao[0],dias):
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
                            else:
                                filho[i][lugarMutacao[1]] = cropMutado["nome"]
                            dia += 1
                else:
                    for i in range(cropMutado['time']):
                        if i == (cropMutado['time']-1):
                            aux ='colhe '+cropMutado['nome']
                            #print("assim:", aux)
                            filho[lugarMutacao[0]+i][lugarMutacao[1]] = aux
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
                    if (lugarMutacao[0]+cropMutado['time']-1)<dias:
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
                            if filho[lugarMutacao[0]+cropMutado['time']-1][lugarMutacao[1]][0:5] == 'colhe':
                                filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]]=''
                            else:
                                while(filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]][0:5]!='colhe'):
                                    filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]]=''
                                    i+=1
                                filho[lugarMutacao[0]+cropMutado['time']+i-1][lugarMutacao[1]]=''
    return filhos
            
def EscolheNovaPopulacao(populacao,filhos):
    antigaPopulacao = deepcopy(populacao)+deepcopy(filhos)
    novaPopulacao = [[['' for i in range(plots)] for j in range(dias)] for k in range((len(populacao)))]
    fitnessNovaPopulacao = [0 for i in range((len(populacao)))]
    aux = CalculaFitness(populacao)+CalculaFitness(filhos)
    for i in range(len(populacao)):
        index_max = np.argmax(aux)
        fitnessNovaPopulacao[i]=aux[index_max]
        novaPopulacao[i] = antigaPopulacao[index_max]
        aux[index_max] = 0
    return novaPopulacao,fitnessNovaPopulacao

def MostrarTabelaIndividuo(individuo,titulo):
    title_text = titulo
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'
    data = deepcopy(individuo)
    #data =['']+[(f'Campo: {plot+1}') for plot in plots]
    #for i in range(dias):
    #    data.append(f'Dia {i+1}:'+individuo[i])
    # Pop the headers from the data array
    column_headers = [(f'Campo: {plot+1}') for plot in range(plots)]
    row_headers = [f'Dia: {dia}' for dia in range(dias)]
    # Table data needs to be non-numeric text. Format the data
    # while I'm at it.
    cell_text = []
    for row in data:
        cell_text.append([f'{x}' for x in row])
    # Get some lists of color specs for row and column headers
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    # Create the figure. Setting a small pad on tight_layout
    # seems to better regulate white space. Sometimes experimenting
    # with an explicit figsize here can produce better outcome.
    plt.figure(linewidth=2,
            edgecolor=fig_border,
            facecolor=fig_background_color,
            tight_layout={'pad':0.5},
            #figsize=(5,3)
            )
    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                        rowLabels=row_headers,
                        rowColours=rcolors,
                        rowLoc='right',
                        colColours=ccolors,
                        colLabels=column_headers,
                        loc='center')
    # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    the_table.scale(1, 1)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(title_text)
    # Add footer
    footer_text = ''
    plt.figtext(0.95, 0.05,footer_text, horizontalalignment='right', size=6, weight='light')
    # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    plt.draw()
    # Create image. plt.savefig ignores figure edge and face colors, so map them.
    fig = plt.gcf()
    plt.savefig('pyplot-table-demo.png',
                #bbox='tight',
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                dpi=300
                )
    
def MostrarFitness(fitness,titulo):
    title_text = titulo
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'
    data = deepcopy(fitness)
    #data =['']+[(f'Campo: {plot+1}') for plot in plots]
    #for i in range(dias):
    #    data.append(f'Dia {i+1}:'+individuo[i])
    # Pop the headers from the data array
    column_headers = [(f'Individuo: {i+1}') for i in range(tam_pop)]
    row_headers = [f'Geração: {i+1}' for i in range(geracoes)]
    # Table data needs to be non-numeric text. Format the data
    # while I'm at it.
    cell_text = []
    for row in data:
        cell_text.append([f'{x}' for x in row])
    # Get some lists of color specs for row and column headers
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    # Create the figure. Setting a small pad on tight_layout
    # seems to better regulate white space. Sometimes experimenting
    # with an explicit figsize here can produce better outcome.
    plt.figure(linewidth=2,
            edgecolor=fig_border,
            facecolor=fig_background_color,
            tight_layout={'pad':0.5},
            #figsize=(5,3)
            )
    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                        rowLabels=row_headers,
                        rowColours=rcolors,
                        rowLoc='right',
                        colColours=ccolors,
                        colLabels=column_headers,
                        loc='center')
    # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    the_table.scale(1, 1)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(title_text)
    # Add footer
    footer_text = ''
    plt.figtext(0.95, 0.05,footer_text, horizontalalignment='right', size=6, weight='light')
    # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    plt.draw()
    # Create image. plt.savefig ignores figure edge and face colors, so map them.
    fig = plt.gcf()
    plt.savefig('pyplot-table-fitness.png',
                #bbox='tight',
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                dpi=300
                )
    
def main():
    populacao = StartPopulacao()
    
    matrizFitness =[]

    fitnessPopulacao = CalculaFitness(populacao)
    
    matrizFitness.append(deepcopy(fitnessPopulacao))
    
    print(f'Fitness Geração 1: {fitnessPopulacao}')
    

    for i in range(geracoes-1):

        filhos = Cruzamento(populacao,fitnessPopulacao,(cruzamentos))

        populacao,fitnessPopulacao = EscolheNovaPopulacao(populacao,filhos)
        
        matrizFitness.append(deepcopy(fitnessPopulacao))
        
        print(f'Fitness Geração {i+2}: {fitnessPopulacao}')
        
    print("Melhor Resultado:")
    mprint(populacao[0],max_rows=None,max_cols=None)
    MostrarTabelaIndividuo(populacao[0],'Melhor Indivíduo')
    MostrarFitness(matrizFitness,'Fitness por Gerações')
        
    
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