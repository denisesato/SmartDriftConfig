import caracteristicas_log_massivo
import carrega_log_DS_massivo
import pandas as pd
from tabulate import tabulate
from pathlib import Path
import os
import estatistica_log

def gera_massivo():
    diretorio =  'C:\\Users\\Sheila_freitas\\Documents\\Base_Dados\\dataset_real'

    #diretorio = 'C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\dataset_real'
            
    print('&&&&&&&')
    for nome_log_geral in os.listdir(diretorio):
        caminho = os.path.join(diretorio, nome_log_geral)

        t_resdf1 = ()
        t_resdf2 = ()
        df1 = pd.DataFrame(columns=['modelo', 'fitness', 'precisão', 'generalização', 'simplicidade'])
        dfm1 = pd.DataFrame(columns=['Modelo_Media', 'Fitness_Media', 'Precisão_Media', 'Generalização_Media', 'Simplicidade_Media'])

        #Carrega log geral
        t_resdf1 = carrega_log_DS_massivo.log_completo_m(df1, dfm1, caminho)

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

        #altera o caminho....
        caminho_pasta_sublog = 'C:\\Users\\Sheila Freitas\\Documents\\Base_Dados\\adaptive_real'

        nome_caminho_sublog = caminho_pasta_sublog +'\\'+nome_log_geral+'\\'
        #for pasta_sublog in os.listdir(caminho_pasta_sublog):
        #nome_caminho_sublog = os.path.join(caminho_pasta_sublog, pasta_sublog)
        #print(nome_caminho_sublog)
        cont = 1
        for pasta_delta in os.listdir(nome_caminho_sublog):
            t_res_carrega_log = ()
            lista_sublogs = []
            lista_modelos = []
            # cont = 1
            valor_pasta_delta = os.path.join(nome_caminho_sublog, pasta_delta)
            print(valor_pasta_delta)

            pasta_final_sublogs = valor_pasta_delta + '\\sublogs\\'
            for arq_xes in os.listdir(pasta_final_sublogs):
                cam_arq_xes = os.path.join(pasta_final_sublogs, arq_xes)
                if os.path.isfile(cam_arq_xes):
                    lista_sublogs.append(cam_arq_xes)

            print('pasta_final_sublogs  ' + pasta_final_sublogs)
            pasta_final_models = valor_pasta_delta + '\\models\\'
            for arq_pnml in os.listdir(pasta_final_models):
                cam_arq_pnml = os.path.join(pasta_final_models, arq_pnml)
                if os.path.isfile(cam_arq_pnml):
                    lista_modelos.append(cam_arq_pnml)

            print('pasta_final_models  ' + pasta_final_models)

            t_res_carrega_log = carrega_log_DS_massivo.sub_log(df1,
                                                               dfm1,
                                                               nome_pasta_csv,
                                                               nome_arquivo_log,
                                                               lista_sublogs,
                                                               lista_modelos)
            print('Carregou o sublog: ')
            print("recebi o retorno ")
            print(tabulate(df1.head(15), headers='keys', tablefmt='simple_grid'))

            if cont == 1:
                dlt = '0.002'
            if cont == 2:
                dlt = '0.05'
            if cont == 3:
                dlt = '0.1'
            if cont == 4:
                dlt = '0.3'

            lista_media_final_atividades = estatistica_log.carrega_gera_estatisticas(caminho)
            caracteristicas_log_massivo.carrega_gera_caracteristicas(logG, metricas_ger, nome_pasta_csv,
                                                                     t_res_carrega_log, dlt,lista_media_final_atividades)
            print(logG)
            cont += 1
            print('passei pela função de características e voltei para o main........... FIM da execução!!!!!!')

if __name__ == '__main__':
    gera_massivo()
