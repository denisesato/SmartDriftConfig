from tabulate import tabulate
from tkinter import filedialog
import pandas as pd
import pm4py
import os
import numpy as np

eps = np.finfo(float).eps  # me dê o menor número positivo possível que o tipo de dados float pode representar na minha máquina”.
from numpy import log2 as log


def carrega_gera_caracteristicas(logG, metricas_ger, nome_pasta_csv, media_sublogs, lista_ativ_media_final):
    type(logG)
    print("Selecione o aqruivo de CARACTERÍSTICAS no formato .CSV............: ")
    # caminho_caracteristicas = filedialog.askopenfilenames(title='ESCOLHA O ARQUIVO DE CARACTERISTICAS',
    #                                                      initialdir='C:\\Users\\Sheila Freitas\\pythonProject\\FMP') #casa
    # caminho_caracteristicas = filedialog.askopenfilenames(title='ESCOLHA O ARQUIVO DE CARACTERISTICAS',
    #                                                      initialdir='C:\\sheila\\FMP') #PUC
    # caminho_caracteristicas = filedialog.askopenfilenames()

    caminho_caracteristicas = 'C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\Base_caracteristicasT.csv'  # casa
    print('****CAMINHO DE CARACTERÍSTICAS ******')
    print(caminho_caracteristicas)

    #df2 = pd.read_csv(caminho_caracteristicas[0], delimiter=';')
    df2 = pd.read_csv(caminho_caracteristicas, delimiter=';')

    print(tabulate(df2.head(), headers='keys', tablefmt='simple_grid'))
    print('estou na função de gera as caracteristicas de log')

    # descobrindo o número de atividadaes
    logGer = pm4py.read_xes(logG)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(logGer)
    start_activities = pm4py.get_start_activities(logGer)
    end_activities = pm4py.get_end_activities(logGer)
    df3 = pm4py.convert_to_dataframe(logGer)
    event_log = pm4py.convert_to_event_log(df3)

    df3 = pm4py.convert_to_dataframe(logGer)
    print(tabulate(df3.head(), headers='keys', tablefmt='simple_grid'))

    print('Caminho para guarda o csv do log para descobrir as  características')
    # dir_path = filedialog.askdirectory(title='ESCOLHA UM DIRETÓRIO PARA GUARDAR CSV DO LOG PARA DESCOBRIR AS CARACTERÍSTICAS:',
    #                                   initialdir='C:\\sheila\\FMP\\log_geral\\') #PUC

    # dir_path = filedialog.askdirectory()
    dir_path = 'C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\' + nome_pasta_csv + '\\'
    print(dir_path)
    type(logG)
    os.makedirs(dir_path, exist_ok=True)
    df3.to_csv(dir_path + '/logGc.csv', encoding='utf-8', index=False)

    atividades = df3['concept:name'].nunique()
    print("Número de atividades do log............: ", atividades)

    lis_freq = []
    activities_freq = dict(df3["concept:name"].value_counts())
    # print("Frequencia das atividades:...... ", activities_freq)
    lis_freq = activities_freq.values()
    lis_freq = list(lis_freq)
    # print(lis_freq)
    media_freq = np.mean(lis_freq)
    mediana_freq = np.median(lis_freq)
    # print("Média das frequencia das atividades....: ", media_freq)
    # print("Mediana das frequencia das atividades..: ", mediana_freq)

    num_eventos = len(logGer)
    # print("Número de eventos.......................: ", num_eventos)

    count_events = 0  # número de eventos
    trace_casos_log = 0  # Número de casos
    for trace in event_log:
        trace_casos_log += 1
        for event in trace:
            count_events += 1
    # print("Número de casos...............: ", trace_casos_log)

    # Número de variants
    # variants_log = pm4py.get_variants_as_tuples(logG)
    variants_log = pm4py.get_variants(logGer)
    num_variants = len(variants_log)
    # print("Número de variantes", num_variants, " ", variants_log)

    # média do tempo de duração dos casos
    all_case_durations = pm4py.get_all_case_durations(logGer)
    media_tempo_casos = np.mean(all_case_durations)
    mediana_tempo_casos = np.median(all_case_durations)
    print("Média do tempo dos casos", media_tempo_casos, " ", mediana_tempo_casos)

    abordagem = "trace_by_trace"  # trace_by_trace, Fixa, adptative, windows
    perspectiva = "Control_Flow"  # control_flow, time, data
    detector = "adwin"
    parametro = "delta"

    #valor_parametro="0.1"
    #valor_parametro="0.002"
    #valor_parametro="0.3"
    valor_parametro="0.05"

    f1score = 1.0

    fitnessG = metricas_ger[0]
    prec_tokG = metricas_ger[1]
    genG = metricas_ger[2]
    simpG = metricas_ger[3]

    # Prepara o nome do arquivo para guardar no log de características
    tam = len(logG)
    nome_semraiz = (logG[2:tam])
    nome_arquivo_log = os.path.basename(nome_semraiz)
    chars = '.,'
    res_nome_arquivo_log = nome_arquivo_log.translate(str.maketrans('', '', chars))

    xteste = media_sublogs[6]
    x2teste = media_sublogs[7]

    nova_entrada = [len(df2), res_nome_arquivo_log, num_eventos, trace_casos_log, atividades, media_tempo_casos,
                    mediana_tempo_casos,num_variants, media_freq, mediana_freq, abordagem, perspectiva, detector, parametro,
                    valor_parametro, fitnessG, prec_tokG, genG, simpG, f1score, media_sublogs[0], media_sublogs[1],
                    media_sublogs[2], media_sublogs[3], media_sublogs[4], media_sublogs[5], media_sublogs[6],media_sublogs[7],
                    lista_ativ_media_final[0],lista_ativ_media_final[1], lista_ativ_media_final[2],lista_ativ_media_final[3],
                    lista_ativ_media_final[4], lista_ativ_media_final[5], lista_ativ_media_final[6],lista_ativ_media_final[7]]

    df2.loc[len(df2)] = nova_entrada
    # print(tabulate(df2.head(), headers='keys', tablefmt='simple_grid'))
    print(tabulate(df2.tail(5), headers='keys', tablefmt='simple_grid'))

    print("Selecione um diretório para guardar o log de CARACTERÍSTICAS no formato .CSV............: ")
    # dir_path = filedialog.askdirectory(title='ESCOLHA UM DIRETÓRIO PARA GUARDAR LOG DE CARACTERÍSTICAS:',
    #                                   initialdir='"C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\')
    # dir_path = filedialog.askdirectory(title='ESCOLHA UM DIRETÓRIO PARA GUARDAR LOG DE CARACTERÍSTICAS:',
    #                                   initialdir='C:\\sheila\\FMP\\log_geral\\') #PUC
    dir_path = 'C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\'
    df2.to_csv(dir_path + '/Base_caracteristicasT.csv', sep=';', encoding='utf-8', index=False)
    df2.to_excel(dir_path + '/Base_caracteristicasT.xlsx')
