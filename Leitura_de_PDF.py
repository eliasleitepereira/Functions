#region Sobre a funcao
  """
  Função responsavel pela leitura de uma planilha que esteja em pdf e transformando ela em planilha 
  
  """
#endregion

import pdfplumber
import pandas as pd
import re
# Função para extrair a tabela do PDF
def extrair_tabela_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        
        # Supondo que a primeira página tenha a tabela
        pagina = pdf.pages[0]
        tabela = pagina.extract_text()
        
        # A partir do texto extraído, vamos dividir em linhas para organizar os dados
        linhas = tabela.split('\n')
         #Vamos filtrar e organizar os dados conforme os campos 
        dados = []
        dados1 = []
        for linha in linhas:
          
          #region espaço para extração da informação desejada
          # A expressão regular abaixo tenta capturar as linhas com os dados das transações
            
            N_Lote = re.findall(r'(?<=No\W)(.*?)(?=\WLOTE)', linha)
            Valor = re.findall(r'(?<=0,00\s)(.*?)(?=\s)', linha)
            if N_Lote and Valor:


                dados = {'Lote': (N_Lote[0]),'Valor':(Valor[0])}
                # Adiciona os dados extraídos à lista
                
                dados1.append(dados)

          #endregion
        # Criando o DataFrame
        colunas = ['Lote','Valor']
        df = pd.DataFrame(dados1, columns=colunas)


    return df

# Caminho do arquivo PDF
pdf_path = "razao 3.3.4.2.0005 juros de mora recebidos.pdf"

# Extrair a tabela
df_tabela = extrair_tabela_pdf(pdf_path)

print(df_tabela)

# Salvar a tabela em um arquivo Excel
df_tabela.to_excel("tabela_saida.xlsx", index=False)
