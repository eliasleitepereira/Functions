import os
import shutil

home_usuario = os.path.expanduser("~")
diretotrio_download = os.path.join(home_usuario, "Downloads")
extensoes_imagem = ('.jpg', '.jpeg', '.png', '.webp', '.gif','.jfif','.dds')
extensoes_video = ('.mp4')
extensoes_texto = ('.txt','.docx')
extensoes_executaveis = ('.exe')
extensoes_planilhas = ('.xlsx','.xls')
extensoes_compacto = ('.zip','.rar')
extensoes_pdfs = ('.pdf')
extensoes_musicas = ('.mp3', '.m4a', '.aac', '.wav', '.flac', '.ogg')

lista_de_pasta = ("imagens","videos","planilhas","executaveis","pdfs","texto","outros","zips","musicas")

for pasta in lista_de_pasta:
    if not os.path.isdir(os.path.join(diretotrio_download, pasta)):
        os.makedirs(os.path.join(diretotrio_download,pasta))

for arquivo in os.listdir(diretotrio_download):
    nome, extensao = os.path.splitext(arquivo)

    if os.path.isfile(os.path.join(diretotrio_download,arquivo)):
        
        if extensao in extensoes_imagem:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"imagens"))

        elif extensao in extensoes_video:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"videos"))
            
        elif extensao in extensoes_texto:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"texto"))

        elif extensao in extensoes_executaveis:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"executaveis"))
            
        elif extensao in extensoes_planilhas:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"planilhas"))
            
        elif extensao in extensoes_compacto:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"zips"))

        elif extensao in extensoes_pdfs:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"pdfs"))

        elif extensao in extensoes_musicas:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"musicas"))
            
        else:
            shutil.move(os.path.join(diretotrio_download,arquivo),os.path.join(diretotrio_download,"outros"))
        
        
#==Niyx==