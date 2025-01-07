import os
from pathlib import Path

#Diretorio que quer verificar.
caminho_raiz = r"C:\Digite\seu\Diretorio"

def calcular_tamanho_pasta(caminho):
    tamanho_total = 0
    
    # Percorre todos arquivos e subpastas
    for diretorio_atual, subdiretorios, arquivos in os.walk(caminho):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(diretorio_atual, arquivo)
            # Adiciona tamanho se o arquivo existe
            if os.path.exists(caminho_arquivo):
                tamanho_total += os.path.getsize(caminho_arquivo)
    
    return tamanho_total

def formatar_tamanho(tamanho_bytes):
    """Converte bytes para KB, MB, GB"""
    for unidade in ['B', 'KB', 'MB', 'GB']:
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes:.2f} {unidade}"
        tamanho_bytes /= 1024
    return f"{tamanho_bytes:.2f} TB"


for arquivo in os.listdir(caminho_raiz):

    if not "." in arquivo:
        caminho_pasta = f"{caminho_raiz}\{arquivo}"
        tamanho = calcular_tamanho_pasta(caminho_pasta)
        print(f"{caminho_pasta} - {formatar_tamanho(tamanho)}")
