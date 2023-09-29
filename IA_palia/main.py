from numpy.random import choice
from crops import *
from percent import *

cromossomo = [None]*9
populacao = [None]*10
geracoes = 5
mutacao = 0.01

for individuo in populacao:
    for i in range(0,len(cromossomo)):
        individuo[i]=(choice(crops))['id']