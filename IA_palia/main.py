from numpy.random import choice
#from crops import *
#from percent import *
from genetico import *



plots,dias = int(input("Quantos plots (espaços de terra) deseja?")),int(input("Quantos dias deseja?"))
cromossomo = [None]*plots
tam_pop = int(input("Qual o tamanho da população desejado?"))
populacao = [None]*tam_pop
geracoes = int(input("Quantas gerações deseja?"))
cruzamentos = int(input("Quantos cruzamentos por geração?"))
porcMutacao = int(input("Quantos porcento de mutação deseja?"))
mutacao = (porcMutacao/100)


populacao = StartPopulacao()

fitnessPopulacao = CalculaFitness(populacao)
    
#print(f'Fitness 1: {fitnessPopulacao}')
#print(f'Fitness 2: {CalculaFitness(populacao)}')
#print(f'Fitness 3: {CalculaFitness(populacao)}')

for i in range(geracoes-1):

    filhos = Cruzamento(populacao,fitnessPopulacao,(cruzamentos))

    fitnessFilhos = CalculaFitness(filhos)

    #print("fitness2",fitnessFilhos)

    novaPopulacao,fitnessPopulacao = EscolheNovaPopulacao(populacao,filhos,fitnessPopulacao,fitnessFilhos)
    
    print(f'Fitness Geração {i+2}: {fitnessPopulacao}')

fitnessPopulacao = CalculaFitness(populacao)    
#print(f'Fitness populacao: {fitnessPopulacao}')  
fitnessPopulacao = CalculaFitness(novaPopulacao)
#print(f'Fitness novaPopulacao: {fitnessPopulacao}')