from tabulate import tabulate
from tkinter import filedialog
import pandas as pd
import pm4py
import warnings
import os
import numpy as np

def carrega_gera_estatisticas(caminho_logG):
    logG = pm4py.read_xes(caminho_logG)
    lista_media_medias = []
    case_name = list(logG['case:concept:name'].value_counts().index)
    print(case_name[0:10])

    #Cria dataframe para guardar as informações de estatísticas por trace
    df_final = pd.DataFrame(index=case_name, columns=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    print(tabulate(df_final.head(3), headers='keys', tablefmt='simple_grid'))

    #Gera estatísticas
    warnings.filterwarnings("ignore")
    for name in case_name:
        log_aux = logG[logG['case:concept:name'] == name]
        performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(log_aux,
                                                                                           case_id_key='case:concept:name',
                                                                                           activity_key='concept:name',
                                                                                           timestamp_key='time:timestamp')
        df_perf = pd.DataFrame.from_dict(performance_dfg)
        df_perf = df_perf.T
        df_perf = df_perf['mean'][df_perf['mean'] != 0]
        df_perf = pd.DataFrame(df_perf.reset_index(drop=True))
        df_perf['time_norm'] = df_perf / df_perf.sum()
        df_perf.rename(columns={'mean': 'time_seg'}, inplace=True)
        df_desc = df_perf.time_norm.describe()
        df_desc = pd.DataFrame(df_desc)
        df_desc = df_desc.T
        df_final.loc[name] = df_desc.loc['time_norm']
        print(name)
    print(tabulate(df_final.head(11), headers='keys', tablefmt='simple_grid'))
    #para gravar um exemplo de estatística por case
    #df_final.to_excel('C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\pasta_cb5kxes\\estatistica\\tempo_por_case_normalizado.xlsx')

    # Calculo da estatística das estatísticas
    df_final_1 = df_final.reset_index(drop=True)
    print(tabulate(df_final_1.head(3), headers='keys', tablefmt='simple_grid'))

    #Tranforma todos os valores em float
    df_final_2 = df_final_1.astype(float)
    print(tabulate(df_final_2.head(3), headers='keys', tablefmt='simple_grid'))
    df_media_medias = df_final_2.describe()
    #df_media_medias.to_excel('C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\pasta_cb5kxes\\estatistica\\estatistica_do_tempo_normalizado.xlsx')
    print('Aqui...  temos o dataframe das medias das médias')
    print(tabulate(df_media_medias.head(8), headers='keys', tablefmt='simple_grid'))

    count_count_ativ = np.round(df_final_2['count'].describe()['count'],3)
    mean_mean_ativ = np.round(df_final_2['mean'].describe()['mean'],3)
    std_std_ativ = np.round(df_final_2['std'].describe()['std'],3)
    min_min_ativ = np.round(df_final_2['min'].describe()['min'],3)
    v25_v25_ativ = np.round(df_final_2['25%'].describe()['25%'],3)
    v50_v50_ativ = np.round(df_final_2['50%'].describe()['50%'],3)
    v75_v75_ativ = np.round(df_final_2['75%'].describe()['75%'],3)
    max_max_ativ = np.round(df_final_2['max'].describe()['max'],3)

    lista_media_medias.append(count_count_ativ)
    lista_media_medias.append(mean_mean_ativ)
    lista_media_medias.append(std_std_ativ)
    lista_media_medias.append(min_min_ativ)
    lista_media_medias.append(v25_v25_ativ)
    lista_media_medias.append(v50_v50_ativ)
    lista_media_medias.append(v75_v75_ativ)
    lista_media_medias.append(max_max_ativ)
    return (lista_media_medias)


#if __name__ == '__main__':
   #caminho_log = ('C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\dataset1_ok\\cb5k.xes')
   #listaF = carrega_gera_estatisticas(caminho_log)
   #print(listaF)