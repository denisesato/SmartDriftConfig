import caracteristicas_log
import carrega_log_DS
import pandas as pd
from tabulate import tabulate
import estatistica_log

from pathlib import Path

if __name__ == '__main__':
    lista_media_final_atividades = []
    t_resdf1 = ()
    t_resdf2 = ()
    t_res_carrega_log = ()
    df1 = pd.DataFrame(columns=['modelo', 'fitness', 'precisão', 'generalização', 'simplicidade'])
    dfm1 = pd.DataFrame(columns=['Modelo_Media', 'Fitness_Media', 'Precisão_Media', 'Generalização_Media', 'Simplicidade_Media'])

    #Carrega log completo
    t_resdf1 = carrega_log_DS.log_completo(df1,dfm1)
    df1 = t_resdf1[0]
    dfm1 = t_resdf1[1]
    nome_pasta_csv = t_resdf1[2]
    logG = t_resdf1[3]
    metricas_ger = t_resdf1[4]
    nome_arquivo_log = t_resdf1[5]
    print('********** log retornado da função******' + logG)
    print('Carregou log: ')
    print("recebi o retorno ")
    print(tabulate(df1.head(), headers='keys', tablefmt='simple_grid'))

    #df1 = carrega_log_DS.sub_log(df1, dfm1, nome_pasta_csv, nome_arquivo_log)
    t_res_carrega_log = carrega_log_DS.sub_log(df1, dfm1, nome_pasta_csv, nome_arquivo_log)
    print('Carregou o sublog: ')
    print("recebi o retorno ")
    #print(tabulate(df1.head(15), headers='keys', tablefmt='simple_grid'))

    #arq_log_ger = ('C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\dataset1_ok\\cb5k.xes')
    lista_media_final_atividades = estatistica_log.carrega_gera_estatisticas(arq_log_ger)

    caracteristicas_log.carrega_gera_caracteristicas(logG, metricas_ger,nome_pasta_csv, t_res_carrega_log, lista_media_final_atividades)
    print(logG)
    print('passei pela função de características e voltei para o main........... FIM da execução!!!!!!')



