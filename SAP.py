import win32com.client
import subprocess
import time
import psutil
from datetime import datetime
import easygui
from pathlib import Path
import pandas as pd
import os
from pywinauto import Desktop
from dotenv import load_dotenv


load_dotenv()

SAP_PATH = os.getenv("SAP_PATH")
SAP_CONNECTION = os.getenv("SAP_CONNECTION")
SAP_USER = os.getenv("SAP_USER")
SAP_PASSWORD = os.getenv("SAP_PASSWORD")

if not all([SAP_PATH, SAP_CONNECTION, SAP_USER, SAP_PASSWORD]):
    raise ValueError(
        "Variáveis de ambiente do SAP não configuradas."
    )


class SAP:
    def __init__(self):
        self.connection = None
        self.session = None
        self.application = None

    def Fechar_SAP(self):
        for proc in psutil.process_iter(['name']):

            if 'saplogon' in proc.info['name'].lower():

                print(proc)

                #Fechar o SAP caso ele esteja aberto
                try:

                    subprocess.run(["taskkill","/f","/im","saplogon.exe"])

                except Exception:
                    pass
    
    def Login_SAP(self,transacao: str,):
            self.Fechar_SAP()
            subprocess.Popen(SAP_PATH)
            
            sap_gui_auto = win32com.client.GetObject("SAPGUI")
            self.application = sap_gui_auto.GetScriptingEngine
            
            # Abre a conexão
            self.connection = self.application.OpenConnection(SAP_CONNECTION, True)
            self.session = self.connection.Children(0)

            # Em vez de VBS externo, faça o login direto pelo Python para manter o controle:
            self.session.findById("wnd[0]/usr/txtRSYST-BNAME").text = SAP_USER
            self.session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = SAP_PASSWORD
            self.session.findById("wnd[0]/tbar[0]/btn[0]").press()
            self.session.findById("wnd[0]/tbar[0]/okcd").text = transacao
            self.session.findById("wnd[0]").sendVKey(0)

    # Exemplo de como pode utilizar
    def _Aplicando_datas(self):

        dia = datetime.now().strftime("%d")
        mes = datetime.now().strftime("%m")
        ano = datetime.now().strftime("%Y")
        data_inicio = f"01.{mes}.{ano}"
        data_fim = f"{dia}.{mes}.{ano}"
        

        # try:
           
        self.session.findById("wnd[0]").maximize()
        self.session.findById("xpath do sap").text = "Valor" #Aplicando valores
        self.session.findById("xpath do sap").setFocus()
        self.session.findById("xpath do sap").caretPosition = 1
        self.session.findById("wnd[0]").sendVKey (2)
        self.session.findById("xpath do sap").text = data_inicio
        self.session.findById("xpath do sap").text = data_fim
        self.session.findById("xpath do sap").setFocus()
        self.session.findById("xpath do sap").caretPosition = 10
        self.session.findById("wnd[0]").sendVKey (8)


    def _Gerar_PDF_NF(self,doc_fatur: str,linha: int):
        self.session.findById("xpath do sap").currentCellColumn = ""
        # self.session.findById("xpath do sap").selectedRows = "0"
        self.session.findById("xpath do sap").selectedRows = linha
        self.session.findById("xpath do sap").press()
        self.session.findById("xpath do sap").selected = True
        self.session.findById("xpath do sap").key = "Microsoft Print to PDF"
        self.session.findById("xpath do sap").setFocus()
        self.session.findById("xpath do sap").press()
        self._Janela_salvar(diretorio = f"Nome do que for salvar {doc_fatur}",nome_janela="Salvar Saída de Impressão como")
        if not self.verificar_janela_info(parte_nome_janela="parte do nome da janela"):
            time.sleep(0.3)
            self.session.findById("xpath do sap").press()
    
    
    def _Janela_salvar(self,diretorio: str,nome_janela: str):
        # Conecta à janela "Salvar como" do Windows
        app = Desktop(backend="win32").window(title_re=nome_janela)

        # Aguarda a janela ficar pronta
        app.wait('visible', timeout=30)

        # Digita o nome do arquivo no campo de edição
        app.Edit.type_keys( diretorio, with_spaces=True)
        app.Button.click() # Clica no botão Salvar


        # --- VALIDAR SE ARQUIVO JÁ EXISTENTE ---
        janela_confirmar = Desktop(backend="win32").window(title_re="Confirmar Salvar como") # Mudar caso o sistema esteja em ingles

        # Verificamos se ela apareceu (esperamos até 2 segundos)
        if janela_confirmar.exists(timeout=2):
            print("Arquivo já existe, será substituido")
            janela_confirmar.type_keys("%s")

    def _Carregar_pdf_existentes(self,diretorios: list[str]) -> set[str]: 
        pdfs = set() # criar um lista sem nome repetido
        cont = 0
        for diretorio in diretorios:
            base = Path(diretorio)
            if not base.exists():
                continue
            
            for arquivo in base.rglob("*.pdf"):
                cont += 1
                print(f"\rCarregando arquivos ja baixados: [ {cont}", end="")
                pdfs.add(arquivo.name)
        
        return pdfs

    def _Confirmar_baixar(self, doc_fatur: str,cancelados_set: set[str],pdfs_existentes:set[str]) -> bool:
         doc_fatur = str(doc_fatur)

         if doc_fatur in cancelados_set:
              return False
         if doc_fatur in pdfs_existentes:
              return False
         
         return True

    def Baixar_nota(self):
        # try:    
            # Verifica se a sessão existe
            if not self.session:
                raise Exception("Sessão SAP não iniciada. Chame Login_SAP primeiro.")

            self._Aplicando_datas()
            self._Aplicando_filtros()
            exit()
            # Identifica a  tabela
            grid = self.session.findById("xpath do sap")
            # Obtém a quantidade de linhas
            total_linhas = grid.rowCount
            print(grid.rowCount)
            # total_linhas = 50 -> caso queira um teste por quantidade pré determinada
            
            ## Carrega lista de notas canceladas
            cancelados_set = {
                 str(linha['num_nf'])
                 for linha in lista_cancelados
            }

            #region Caregando os pdfs em memoria
            diretorios = [
                 "Diretorio1",
                 "Diretorio2",
                 "Diretorio3"
            ]
            pdfs_existentes = self._Carregar_pdf_existentes(diretorios) #Salvando Pdfs em memoria
            #endregion

            linha = 0
            MAX_TENTATIVAS = 3
            tentativas = 0
            #Colocar um log para mostrar a diferença de arquivos para baixar
            #colocar um log para quantidade de arquivo ja baixado para ir dando update
            while linha < total_linhas:
                    print(linha)
                    try:
                        grid.firstVisibleRow = linha
                        grid.setCurrentCell(linha, "VBELN_VF")# -> nome tecnico da coluna no SAP
                        doc_fatur = grid.getCellValue (linha, "VBELN_VF") # -> nome tecnico da coluna no SAP
                        print(doc_fatur)
                        
                        if self._Confirmar_baixar(doc_fatur=f"{doc_fatur}.pdf",cancelados_set=cancelados_set,pdfs_existentes=pdfs_existentes):
                        
                            self._Gerar_PDF_NF(doc_fatur=doc_fatur,linha=linha)
                        
                        grid = self.session.findById("xpath do sap")
                        linha +=1
                        tentativas = 0     
                        
                    except Exception as e:
                        tentativas += 1
                        print(f"Erro na linha{linha}: {e}")
                        if tentativas > MAX_TENTATIVAS:
                             print(f"Linha {linha} ignorada após {MAX_TENTATIVAS} tentativas.")
                             linha +=1
                             tentativas = 0
                             #Log para caso tenha gerado erro
                             continue
                        #Recuperando SAP
                        self.Login_SAP(transacao="nome transacao")
                        self._Aplicando_datas()
                        grid = self.session.findById("xpath do sap")


           #Log da quantidade de item na tabela de SAP
            self.db_rpa.log(processo="Finalizado",status="Sucesso",descricao=f"Quantidade de notas na tabela do SAP: {total_linhas}")

    #Janela que aparecia após o download
    def verificar_janela_info(self,parte_nome_janela:str):
        try:
            cont = 0 
            while True:
                cont +=1
                # Tenta encontrar a janela wnd[1]
                janela = self.session.findById("wnd[1]")
                
                # Verifica se o título da janela contém "Imprimir"
                if parte_nome_janela in janela.text:
                    print("Janela de impressão identificada.")
                    self.session.findById("wnd[0]").sendVKey(12)
                    time.sleep(1)

                    # 2. Aperta F3 para Voltar
                    self.session.findById("wnd[0]").sendVKey(3)
                    return True
                else:
                     return False
                
        except:
            # Se der erro, significa que a wnd[1] não existe no momento
            return False
       
    