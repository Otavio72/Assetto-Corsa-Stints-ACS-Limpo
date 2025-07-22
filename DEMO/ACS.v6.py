import customtkinter as tkc
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import google.generativeai as genai
import tkinter as tk
from functools import partial
import ctypes
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext, messagebox

load_dotenv()
API_IA_KEY = os.getenv("GEMINIIA_API_KEY")

genai.configure(api_key=API_IA_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])



stint1f = []
stint2f = []
lap_T1f = ()
lap_N1f = ()
lap_T2f = ()
lap_N2f = ()
stints = []
stintsIA = []
PASTA_CSV = "DEMO/demo_stints"


def processar_csv(csv):
    coluna_lapNum = 'lapNum'
    coluna_lap_time = 'lap_time'
    
   
    if coluna_lapNum not in csv.columns or coluna_lap_time not in csv.columns:
        ctypes.windll.user32.MessageBoxW(0,f"Colunas: {coluna_lap_time, coluna_lapNum} não encontradas",f"ARQUIVO INVALIDO",0x10)
        return
    else:
        pass

    lapN = csv['lapNum'].unique()
    lap_T = []
    lap_N = []
    for lap in lapN:
            lap_data = csv[csv['lapNum']== lap]
            lap_data = lap_data[lap_data['lap_time']!= -1]
            lap_time = lap_data['lap_time'].iloc[-1]
            lap_T.append(lap_time)
            lap_N.append(lap)

    return lap_T , lap_N



def IA_processar(lap_T,lap_N):                
    time_ia = []
    for x in lap_T:
        m = int(x / 60)
        s = round((x % 60), 2)
        time_ia.append(f"{m}:{s:05.2f}")
    lap_ia = [int(x) for x in lap_N]
    stint = f" voltas: {lap_ia} // Tempos: {time_ia}"
    print(stint)
    return stint

def img(track, car):
    track = Image.open(track).convert("RGBA")
    car = Image.open(car).convert("RGBA").resize((300,200))

    track.paste(car, (130,110), car)
    btn_wallpaper = track
    return btn_wallpaper



def mostrar_arquivo(stints_selecionados):
    
    args1 = stints_selecionados[0]
    args2 = stints_selecionados[1]
    caminho1 = os.path.join(PASTA_CSV, args1)
    caminho2 = os.path.join(PASTA_CSV, args2)

    for caminho, nome in zip([caminho1, caminho2], [args1, args2]):
        try:
            csv = pd.read_csv(caminho, sep='\t')
            lap_T ,lap_N = processar_csv(csv)
            stints.append({"Tempo": lap_T, "Volta": lap_N})
            
        except Exception as e:
            messagebox.showerror("Erro ao abrir arquivo", f"Erro ao abrir {nome}:\n{e}")
            return
    
    # Criar janela para mostrar dados
    #janela_dados = tk.Toplevel()
    #janela_dados.title(f"Conteúdo: {nome_arquivo}")
    #janela_dados.geometry("600x400")

    #texto = scrolledtext.ScrolledText(janela_dados)
    #texto.pack(fill=tk.BOTH, expand=True)

    #texto.insert(tk.END, df.head(20).to_string())  # mostra as 20 primeiras linhas
    #texto.config(state=tk.DISABLED)
    print(stints[0])
    print(stints[1])

def img(track, car):
    track = Image.open(track).convert("RGBA")
    car = Image.open(car).convert("RGBA").resize((300,200))
    track.paste(car, (130,110), car)
    btn_wallpaper = track
    return btn_wallpaper

def criar_menu():
    GUI4 = tkc.CTkToplevel()
    GUI4.geometry("500x400")
    GUI4.title("Selecionar Stint")
    label = tkc.CTkLabel(master=GUI4, text="Selecione 1 ou 2 Stints")
    label.pack(side="top")

    row_num = 0
    col_num = 0
    stints_selecionados = []

    stints_frame = tkc.CTkScrollableFrame(master=GUI4,fg_color="black",width=400,height=300)
    stints_frame.pack(anchor="center",padx=10)

    img_list_track = {"ks_drag": r"img\ks_drag.png",
                      "ks_highlands (layout_short)" : r"img\ks_highlands.png",
                      "ks_red_bull_ring": r"img\ks_red_bull_ring.png",
                      "ks_nurburgring": r"img\ks_nurburgring.png",
                      "ks_vallelunga": r"img\ks_vallelunga.png",
                      "spa": r"img\spa.png",
                      "ks_laguna_seca": r"img\ks_laguna_seca.png"
                }   
    
    img_list_car = {"ks_ferrari_f138": r"img\ks_ferrari_f138.png",
                    "ks_ferrari_f2004": r"img\ks_ferrari_f2004.png",
                    "ks_audi_r18_etron_quattro": r"img\ks_audi_r18_etron_quattro.png",
                    "ks_ferrari_fxx_k": r"img\ks_ferrari_fxx_k.png",
                    "pagani_zonda_r": r"img\pagani_zonda_r.png",
                    "ks_glickenhaus_scg003": r"img\ks_glickenhaus_scg003.png",
                    "ks_ford_gt40": r"img\ks_ford_gt40.png"
                    }
    
    arquivos = [f for f in os.listdir(PASTA_CSV) if f.endswith(".csv")]

    for arquivo in arquivos:

        arquivo_sem_extenção = arquivo.replace(".csv", "")
        partes = arquivo_sem_extenção.split("__")
        car = partes[0]
        track = partes[1]
        #print(car)
        #print(track)
        if track in img_list_track and car in img_list_car:
            track_path = img_list_track[track]
            car_path = img_list_car[car]
            btn_wallpaper = img(track_path,car_path)
            btn_wallpaperf = tkc.CTkImage(light_image=btn_wallpaper, size=(150,150))
            button = tkc.CTkButton(master=stints_frame, text=f"",fg_color="gray",image=btn_wallpaperf, width=100, height=100, command=lambda a=arquivo: selecao_stints(a))
            button.grid(row=row_num, column=col_num, padx=5, pady=5)
            col_num +=1
            if col_num == 2:
                row_num+=1
                col_num=0
    
    def selecao_stints(arquivo):
        global stint1, stint2
            
        stint1 = 0
        stint2 = 0
        stints_selecionados.append(arquivo)
        print(stints_selecionados)
           
        if len(stints_selecionados) == 1:
            stint1 = stints_selecionados[0]        
                    
        if len(stints_selecionados) == 2:
            stint1 = stints_selecionados[0]
            stint2 = stints_selecionados[1]
            #stints_selecionados.clear()

    buttonstart = tkc.CTkButton(master=GUI4, text="Analisar",corner_radius=32,width=150, command=lambda: mostrar_arquivo(stints_selecionados))
    buttonstart.pack(side="bottom", pady=10)



def GUI2 ():
    GUI_2 = tkc.CTkToplevel()
    GUI_2.title("ACS")
    GUI_2.geometry("1000x450")
    
    intro = f"""
Você é um engenheiro de corridas altamente qualificado, especializado em análise de desempenho em stints de pilotagem. Os pilotos enviaram os tempos de volta registrados, e sua tarefa consiste em:

1. Calcular a **média dos tempos de volta** para cada stint.
2. Determinar o **desvio padrão** dos tempos, avaliando a consistência.
3. Identificar voltas que sejam **inconsistentes ou fora do padrão** esperado.
4. Propor **estratégias de melhoria** com base nos dados analisados.
5. Atribuir uma **nota de desempenho** de 1 a 10 para cada stint, justificando sua avaliação.

Seja técnico, claro e objetivo em suas respostas, garantindo precisão na análise e recomendações.

### Dados enviados pelos pilotos:
- **Stint 1**: {stint1f}
- **Stint 2**: {stint2f}
"""

    
    frame_right2 = tkc.CTkFrame(master=GUI_2, fg_color="#474a51")
    frame_right2.pack(side="right", pady=10,padx=10)
    
#////////////////////////////////////////////////////////////////////

    frame_left2 = tkc.CTkFrame(master=GUI_2, fg_color="#2b2b2b", corner_radius=10)
    frame_left2.pack(side="left", padx=20,pady=20)
    
    chat_frame = tkc.CTkFrame(master=frame_left2, width=400,height=300)
    chat_frame.pack(pady = 10)
    
    chat_janela = tkc.CTkTextbox(master=chat_frame,width=500,height=300)
    chat_janela.configure(font=("Arial" , 11),text_color="black", fg_color="white", corner_radius=20)
    chat_janela.pack(side="top", pady=5,padx=5)
    
    chat_frame_input = tkc.CTkFrame(master=frame_left2, width=500,height=300)
    chat_frame_input.pack(side="bottom", pady=10)



    def enviar_m():
        mensagem_user = user_message.get()
        chat_janela.insert(tk.END, f"\n \n VOCÊ: {mensagem_user} \n \n", "user")
        user_message.delete(0 , tk.END)
        chat_janela.tag_config("user", foreground="#00008b")

        mensagem_chat = chat.send_message(mensagem_user)
        chat_janela.insert(tk.END, f"\n ENGENHEIRO: {mensagem_chat.text}\n")


    intro = chat.send_message(intro)
    chat_janela.insert(tk.END, f"\n ENGENHEIRO: {intro.text}\n")
    chat_janela.pack()

    user_message = tkc.CTkEntry(master=chat_frame_input, width=390,text_color="black", height=50,corner_radius=20, fg_color="white")
    user_message.pack(side="left",padx=5,pady=0)
    
    send_button = tkc.CTkButton(master=chat_frame_input,text="Enviar",command=enviar_m, width=50, height=50, corner_radius=30)
    send_button.pack(side="right", padx=5, pady=0)

    grafico(frame_right2)


#def abrir_arquivos():
 #   global lap_T1f, lap_N1f, lap_T2f, lap_N2f
  #  arqs = filedialog.askopenfilenames(
   # title="ABRIR ARQUIVOS",
   # filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
   # initialdir="C:/")

   # if len(arqs) > 2:
    #    ctypes.windll.user32.MessageBoxW(0,f"Apenas 2 arquivos",f"ARQUIVO INVALIDO",0x10)
     #   return
    #else:
     #    pass

    #for arquivo in arqs:
     #   if not arquivo.endswith(".csv"):
      #      ctypes.windll.user32.MessageBoxW(0,f"{arquivo}",f"ARQUIVO INVALIDO",0x10)
       #     return  
        #else:
         #   continue

    #arquivo1 = arqs[0] 
    #arquivo2 = arqs[1]
    #csv1 = pd.read_csv(arquivo1, delimiter='\t')
    #csv2 = pd.read_csv(arquivo2, delimiter='\t')
    #lap_T1 , lap_N1 = processar_csv(csv1)
    #lap_T2 , lap_N2 = processar_csv(csv2)
    #stint1 = IA_processar(lap_T1, lap_N1)
    #stint2 = IA_processar(lap_T2, lap_N2)
    #stint1f.append(stint1)
    #stint2f.append(stint2)
    #lap_T1f = tuple(lap_T1)
    #lap_T2f = tuple(lap_T2)
    #lap_N1f = tuple(lap_N1)
    #lap_N2f = tuple(lap_N2)
    #GUI2()
    #abrir_arquivos()
    #menustinst()
    #return lap_T1f , lap_N1f, lap_T2f, lap_N2f



GUI = tkc.CTk()
GUI.geometry("500x400")
GUI.title("ACS")


frame_right = tkc.CTkFrame(master=GUI, fg_color="white")
frame_right.pack(side="right", fill="both", expand=True)

frame_1 = tkc.CTkFrame(master=frame_right, fg_color="white")
frame_1.pack(padx=10, pady=100)

ACS_logo = tkc.CTkImage(Image.open("DEMO\\img\\ACS_icon.png"), size=(150,130))
img_label_logo = tkc.CTkLabel(master=frame_1, text="", image=ACS_logo)
img_label_logo.pack(padx=30, pady=0)


btn1 = tkc.CTkButton(master=frame_1, text="Enviar", corner_radius=32,width=150, fg_color="black", command=criar_menu)
btn1.pack(pady=0, padx=10)

frame_2 = tkc.CTkFrame(master=frame_right, fg_color="white")
frame_2.pack(side="bottom")
label_csv = tkc.CTkLabel(master=frame_2, text="Apenas arquivos .csv",text_color="black")
label_csv.pack(side="left", padx=5)

CSV_logo = tkc.CTkImage(Image.open("DEMO\\img\\csv_9496460.png"), size=(30,30))
img_CSV_logo = tkc.CTkLabel(master=frame_2, text="", image=CSV_logo)
img_CSV_logo.pack(side="right", padx=5)




frame_left = tkc.CTkFrame(master=GUI, fg_color="white")
frame_left.pack(side="left", fill="both", expand=True)

wallpaper_left = tkc.CTkImage(Image.open("DEMO\\img\\DALL·E-2025-01-02-14.35.png"), size=(400,400))
img_label1 = tkc.CTkLabel(master=frame_left, text="", image=wallpaper_left)
img_label1.pack(fill="both", expand = True)

def grafico(frame_right2):

    fig, ax = plt.subplots()
    plt.plot(lap_N1f, lap_T1f ,color='red', marker='o', label="Stint 1")
    plt.plot(lap_N2f, lap_T2f ,color='blue', marker='o',label="Stint 2")

    for i, (x , y) in enumerate(zip(lap_N1f, lap_T1f)):
        if y < 15:
             plt.text(x, y, " Fim do stint ", ha="right", va="top")
             break
        mm = int(y // 60)
        ss = int(y % 60)
        plt.text(x,y, f"\n{mm}:{ss:02d}", ha='center', va='top')
        
    
    #mostrar o tempo das voltas nos pontos do grafico de linha 2
    for i2, (x2 , y2) in enumerate(zip(lap_N2f, lap_T2f)):
        if y2 < 15:
             plt.text(x2 , y2 , " Fim do stint ", ha="left", va="bottom")
             break
        mm2 = int(y2 // 60)
        ss2 = int(y2 % 60)
        plt.text(x2,y2, f"{mm2}:{ss2:02d}", ha='center', va='bottom')
    
    plt.xlabel("Volta")
    plt.ylabel("Tempo (Segundos)")
    plt.title("Stints")
    plt.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=frame_right2)
    canvas.get_tk_widget().grid(row=0, column=1,sticky="nsew", padx=10, pady=10)
    canvas.draw()
    plt.close(fig)

GUI.mainloop()