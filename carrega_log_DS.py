from tabulate import tabulate
from tkinter import filedialog
#pm4py
import pm4py
from numpy import log2 as log
from pm4py.objects.log.util import dataframe_utils
#from pm4py.objects.log.util import func as functools
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.petri_net import visualizer as pn_vis
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.objects.petri_net.importer import importer as pnml_importer

#Leitura de arquivos
import os
import glob

#metricas
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator

#internos
#import arquivos_csv
from pathlib import Path

#Outros
import pandas as pd
import random
import numpy as np


def log_completo(df, dfm):
    print("Selecione o arquivo de Log principal/completo .............")
    #caminho_log = filedialog.askopenfilenames(title='ESCOLHA O LOG PRINCIPAL',
    #                                          initialdir='C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\') #casa
    #caminho_log = filedialog.askopenfilenames(title='ESCOLHA O LOG PRINCIPAL',
    #                                          initialdir='C:\\sheila\\FMP\\log_geral\\') #PUC
    #caminho_log = filedialog.askopenfilenames()
    caminho_log = filedialog.askopenfilenames(title='ESCOLHA O LOG PRINCIPAL',
                                              initialdir='C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\') # casa

#teste
    print("*** Cria padrão de nome de pasta para armazenar os resultados ***")

    caminhox=caminho_log[0]
    tam = len(caminhox)
    nome_semraiz = (caminhox[2:tam])
    nome_arquivo_log = os.path.basename(nome_semraiz)
    #nome_arquivo_log = 'pasta_'+nome_arquivo_log
    chars = '.,'
    #res_nome_arquivo_log = nome_arquivo_log.translate(str.maketrans('', '', chars))
    res_nome_arquivo_log = nome_arquivo_log.translate(str.maketrans('', '', chars))
    res_nome_arquivo_log = 'pasta_'+ res_nome_arquivo_log
    print(nome_arquivo_log,'   ',res_nome_arquivo_log)
#teste
    logG = pm4py.read_xes(caminho_log[0])
    #pm4py.write_xes(logG, 'C:/Users/Sheila Freitas/pythonProject/FMP/testexes.xes')

    #Denise
    #variant = xes_importer.Variants.ITERPARSE
    #parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    #eventlogG = xes_importer.apply(caminho_log[0], variant=variant, parameters=parameters)
    #logG = pm4py.convert_to_dataframe(eventlogG)
    #

    nomeG=caminho_log[0]

    print(tabulate(logG.head(3), headers='keys', tablefmt='simple_grid'))

    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(logG)
    start_activities = pm4py.get_start_activities(logG)
    end_activities = pm4py.get_end_activities(logG)
    print(tabulate(logG.head(), headers='keys', tablefmt='simple_grid'))

    fitnessG = replay_fitness_evaluator.apply(
        logG,
        net,
        initial_marking,
        final_marking,
        variant=replay_fitness_evaluator.Variants.TOKEN_BASED
    )
    fitg = np.round((fitnessG['log_fitness']),2)

    prec_tokG = precision_evaluator.apply(
        logG,
        net,
        initial_marking,
        final_marking,
        variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    prec_tokG = np.round(prec_tokG, 2)

    genG = generalization_evaluator.apply(
        logG,
        net,
        initial_marking,
        final_marking)
    genG = np.round(genG, 2)

    simpG = simplicity_evaluator.apply(net)
    simpG = np.round(simpG, 2)

    df.loc[0] = [nomeG, fitnessG['log_fitness'], prec_tokG, genG, simpG]
    dfm.loc[0] = [nomeG, fitnessG['log_fitness'], prec_tokG, genG, simpG]

    metricas_ger = [fitg, prec_tokG, genG, simpG]
    return(df.round(2), dfm.round(2), res_nome_arquivo_log,nomeG,metricas_ger, nome_arquivo_log)


def sub_log(df, dfm, npasta_csv, nome_arq_log):
    lista_sublog = []
    lista_modelos = []
    media_des_padrao_submod = []

    print("Selecione os SUBLOGS no formato *.XES ......................:")
    #arquivos = filedialog.askopenfilenames() #aquivos é do tipo tuple
    #arquivos = filedialog.askopenfilenames(title='ESCOLHA OS SUBLOGS',
    #                                       initialdir= 'C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\s_cb5k\\sublogs\\') #casa

    #arquivos = filedialog.askopenfilenames(title='ESCOLHA OS SUBLOGS *.XES',
    #                                       initialdir='C:\\sheila\\FMP\\log_geral\\')  # Maquina da PUC
    arquivos = filedialog.askopenfilenames(title='ESCOLHA OS SUBLOGS *.XES',
                                           initialdir = 'C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\')  #casa

    # aquivos é do tipo tuple
    lista_sublog = sorted(list(arquivos))

    print("Selecione os MODELOS no formato *.PNML......................:")
    #arquivosm = filedialog.askopenfilenames() #aquivos é do tipo tuple

    #arquivosm = filedialog.askopenfilenames(title='ESCOLHA OS SUBLOGS',
    #                                       initialdir='"C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\s_cb5k\\models\\') # casa
    #arquivosm = filedialog.askopenfilenames(title='ESCOLHA OS SUBMODELOS *.PNML ',
    #                                       initialdir='C:\\Sheila\\FMP\\log_geral\\') #PUC

    #arquivosm = filedialog.askopenfilenames(title='ESCOLHA OS SUBLOGS *.PNML',
    #                                       initialdir='C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\')  #casa

    arquivosm = filedialog.askopenfilenames(title='ESCOLHA OS SUBLOGS *.PNML')


    lista_modelos = sorted(list(arquivosm))
    print(lista_modelos)
    print(tabulate(df.head(), headers='keys', tablefmt='simple_grid'))
    n = 0
    for nome in lista_sublog:
        nomenet = lista_modelos[n]
        print(nomenet)
        log = pm4py.read_xes(nome)
        net, initial_marking, final_marking = pm4py.read_pnml(os.path.join(nomenet))

        fitness = replay_fitness_evaluator.apply(
            log,
            net,
            initial_marking,
            final_marking,
            variant=replay_fitness_evaluator.Variants.TOKEN_BASED
        )
        fits = np.round((fitness['log_fitness']), 2)

        # Por Token
        prec_tok = precision_evaluator.apply(
            log,
            net,
            initial_marking,
            final_marking,
            variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
        prec_tok = np.round(prec_tok, 2)

        gen = generalization_evaluator.apply(
            log,
            net,
            initial_marking,
            final_marking)
        gen = np.round(gen, 2)
        # print(nomeArq+'Generalização: '+ str(gen))

        simp = simplicity_evaluator.apply(net)
        simp = np.round(simp, 2)
        # print(nomeArq+'Simplicidade: '+ str(simp))

        n += 1
        #print(nome + 'Fitness do log .............:' + str(fitness['log_fitness']))
        df.loc[n] = [nome, fits, prec_tok, gen, simp]

    # dir_path = os.getcwd()
    print('Escolher um caminho para criar o diretório com resultados .CSV ....:')
    #dir_path = filedialog.askdirectory()  # aquivos é do tipo tuple
    #dir_path = filedialog.askdirectory(title='ESCOLHA UM DIRETÓRIO PARA GUARDAR OS RESULTADOS...:',
    #                                       initialdir='"C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\s_cb5k\\') # casa

    #dir_path = filedialog.askdirectory(title='ESCOLHA UM DIRETÓRIO PARA GUARDAR OS RESULTADOS...:',
    #                                       initialdir='C:\\sheila\\FMP\\log_geral\\') #PUC
    dir_path ='C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\'

    p_nom = dir_path + '/' +npasta_csv
    os.makedirs(p_nom, exist_ok=True)
    df.to_csv(p_nom + '/aqr_'+ npasta_csv + '.csv', encoding='utf-8', index=False)
    df.to_excel(p_nom + '/aqr_' + npasta_csv + '.xlsx')
    print(tabulate(df.head(15), headers='keys', tablefmt='simple_grid'))

    #Calcula  média
    dfc = df.drop(0)
    totalFitness = np.round(dfc['fitness'].mean(), 2)
    dp_totFitness = np.round(dfc['fitness'].std(), 2)
    totalPrecisao = np.round(dfc['precisão'].mean(), 2)
    dp_totPrecisao = np.round(dfc['precisão'].std(), 2)
    totalGeneralizacao = np.round(dfc['generalização'].mean(), 2)
    dp_totGeneralizacao = np.round(dfc['generalização'].std(), 2)
    totalSimplicidade = np.round(dfc['simplicidade'].mean(), 2)
    dp_totSimplicidade = np.round(dfc['simplicidade'].std(), 2)

    dfm.loc[1] = [nome_arq_log + '- Medias', totalFitness, totalPrecisao, totalGeneralizacao, totalSimplicidade]
    dfm.loc[2] = ['DP - Medias', dp_totFitness, dp_totPrecisao, dp_totGeneralizacao, dp_totSimplicidade]
    media_des_padrao_submod = [totalFitness, totalPrecisao, totalGeneralizacao, totalSimplicidade,
                               dp_totFitness, dp_totPrecisao, dp_totGeneralizacao, dp_totSimplicidade]


    print('ESCOLHA UM DIRETÓRIO PARA GUARDAR OS RESULTADOS DAS MÉDIAS:')
    #dir_path = filedialog.askdirectory(title='ESCOLHA UM DIRETÓRIO PARA GUARDAR OS RESULTADOS DAS MÉDIAS:',
    #                                   initialdir='C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\s_cb5k\\') # casa
    #dir_path = filedialog.askdirectory(title='ESCOLHA UM DIRETÓRIO PARA GUARDAR OS RESULTADOS DAS MÉDIAS:',
    #                                 initialdir='C:\\sheila\\FMP\\log_geral\\') #PUC
    dir_path ='C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\'
    print('Fixo: C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\')

    #p_nom = dir_path + '/' + npasta_csv
    os.makedirs(dir_path, exist_ok=True)
    dfm.to_csv(dir_path + '/med_' + nome_arq_log + '.csv', encoding='utf-8', index=False)
    dfm.to_excel(dir_path + '/med_' + nome_arq_log + '.xlsx')
    print(tabulate(dfm.head(), headers='keys', tablefmt='simple_grid'))
    return(media_des_padrao_submod)

