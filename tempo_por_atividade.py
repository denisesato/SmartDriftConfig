from tkinter import filedialog
import pm4py
import warnings
import pickle

#guardando o dicionário de atividades por caso
def gera_arq_tempo_atividade(logG):
    warnings.filterwarnings("ignore")
    case_name = list(logG['case:concept:name'].value_counts().index)
    print(case_name[0:10])

    for name in case_name:
        log_aux = logG[logG['case:concept:name'] == name]
        performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(log_aux,
                                                                                           case_id_key='case:concept:name',
                                                                                           activity_key='concept:name',
                                                                                           timestamp_key='time:timestamp')
        with open('C:\\Users\\Sheila Freitas\\pythonProject\\FMP\\log_geral\\pasta_cb5kxes\\' + name + '_dict.pkl',"wb") as tf:
            pickle.dump(performance_dfg, tf)

# Lendo um arquivo de dicionário (extensão .pkl)
def ler_arq_tempo_atividade(logG):
    with open("caminho/meu _arquivo_dicionario.pkl", "wb") as tf:
        dicionario = pickle.load(tf)


if __name__ == '__main__':
    print("Selecione o arquivo de Log principal/completo .............")
    caminho_log = filedialog.askopenfilenames(title='ESCOLHA O LOG PRINCIPAL',
                                              initialdir= 'C:\\Users\\freit\\Documents\\Base_dados\\')  #note
    logG = pm4py.read_xes(caminho_log[0])
    gera_arq_tempo_atividade(logG)