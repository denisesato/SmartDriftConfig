from tabulate import tabulate
from tkinter import filedialog
import pandas as pd
import pm4py
import os
import numpy as np

def gera_teste_log():
    diretorio = 'C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\dataset2'
    print('&&&&&&&')
    for nome_log_geral in os.listdir(diretorio):
        try:
            caminho = os.path.join(diretorio, nome_log_geral)
            print(caminho)
            logG = pm4py.read_xes(caminho)
        except TypeError:
            print('log com erro')

if __name__ == '__main__':
    gera_teste_log()
    print('teste log')
