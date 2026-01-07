#Arrumar no arquivo import_sqlite:


        #arquivo_existe =  os.path.exists(caminho_csv) #Identifica se existe, para juntar os registros novos.

        qtd_arquivo = sum(1 for  arquivos in os.listdir(os.path.dirname(caminho_csv))if f"{os.path.basename(caminho_csv)[:-4]}" in arquivos)

        if qtd_arquivo >= 1:
            
            caminho_csv = re.sub(r".csv",f"_{qtd_arquivo+1}_.csv",caminho_csv)
        
        
        #modo = "a" if arquivo_existe else "w"
        modo =  "w"

        with open(caminho_csv, mode=modo, newline="", encoding="utf-8-sig") as csvfile:
        # with open(caminho_csv, mode=modo, newline="", encoding="utf-8-sig") as csvfile:
            escritor = csv.writer(csvfile)
          
            # if not arquivo_existe:
            #     escritor.writerow(colunas)  # Cabeçalho

            escritor.writerow(colunas)  # Cabeçalho
            escritor.writerows(registros)

        print(f"Arquivo CSV '{caminho_csv}' gerado com sucesso com {len(registros)} registro(s)!")
