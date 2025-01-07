import os
import time
from datetime import datetime, timedelta

caminho_pasta = r"<diretorio>l" # -> Caminho da pasta para excluir os arquivos
listinha = os.listdir(caminho_pasta) #Montando a lista de arquivos
prazo_em_meses = 3 #Prazo em meses para as exclusoes

Obtém a data atual
data_atual = datetime.now()

#Calcula a data limite para exclusão (3 meses atrás)
data_limite = data_atual - timedelta(days=prazo_em_meses * 30)

for arquivo in listinha: #Percorre a lista de arquivos
    caminho_arquivo = os.path.join(caminho_pasta, arquivo) # Pega o diretorio do arquivo 

    if os.path.isfile(caminho_arquivo) and caminho_arquivo[-4:] == "xlsx": # verifica o arquivo e o formato certo que ele seja
        # Obtém o tempo de criação do arquivo em segundos desde a época (epoch)
        tempo_arquivo = os.path.getctime(caminho_arquivo)
        # Converte o tempo para um objeto datetime
        data_criacao = datetime.fromtimestamp(tempo_arquivo)

        if data_criacao < data_limite: #Valida se a data de criaçao do arquivo é antes do prazo estipulado
            # Exclui o arquivo
            os.remove(caminho_arquivo)
            print(f"Arquivo {arquivo} excluído com sucesso.")
