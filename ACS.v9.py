import customtkinter as tkc
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import google.generativeai as genai
import tkinter as tk
import os
from dotenv import load_dotenv
from socket import *
import subprocess
import threading
import mysql.connector

load_dotenv()
API_IA_KEY = os.getenv("GEMINIIA_API_KEY")
hostsql = os.getenv("DB_HOST")
usersql = os.getenv("DB_USER")
passwordsql = os.getenv("DB_PASSWORD")
databasesql = os.getenv("DB_NAME")

genai.configure(api_key=API_IA_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])

conexaodb = mysql.connector.connect(
    host=hostsql,
    user=usersql,
    password=passwordsql,
    database=databasesql,
)
cursor = conexaodb.cursor()


stint1f = []
stint2f = []


lapgraf = []
timegraf = []

lapgra2f = []
timegra2f = []


server_logs = ""



def ACS_client():
    global client_ACS
    client_ACS = socket(AF_INET,SOCK_STREAM)
    client_ACS.connect(("192.168.15.77", 1111))

    while True:
        msg = client_ACS.recv(1024).decode('utf-8')
        
        
        if msg == "Code=00":
            log = ("ACS Conectado 😁")
            servidor_janela.insert(tk.END, log + "\n")
        
        if msg == "Code=01":
            log = ("Datalogger Conectado 😃")
            servidor_janela.insert(tk.END, log + "\n")
    

        if msg == "Code=02":
            log = ("Dados Recebidos Pelo Servidor 🫡")
            servidor_janela.insert(tk.END, log + "\n")
        
        if not msg:
            log = (f"Datalogger Desligado 🤐")
            servidor_janela.insert(tk.END, log + "\n")
            client_ACS.close()
            break
        


def start_server():
    global servidor, server_logs
    servidor = subprocess.Popen(['python','servidor_ACS.py'])
    client = threading.Thread(target=ACS_client)
    client.start()

def close_server():
    global servidor, client_ACS
    client_ACS.close()
    servidor.terminate()
    log = ("Servidor Encerrado 😴")
    servidor_janela.insert(tk.END, log + "\n")
    

def GUI3():
    global servidor_janela


    GUI_3 = tkc.CTkToplevel()
    GUI_3.title("SERVIDOR")
    GUI_3.geometry("500x450")
    servidor_frame = tkc.CTkFrame(master=GUI_3, width=400,height=300)
    servidor_frame.pack(pady=10)

    servidor_janela = tkc.CTkTextbox(master=servidor_frame,width=500,height=300)
    servidor_janela.configure(font=("Segoe UI Emoji" , 17),text_color="white", fg_color="black", corner_radius=20)
    servidor_janela.pack(side="top", pady=10)
    
    
    button_server_frame = tkc.CTkFrame(master=GUI_3, width=100, height=300)
    button_server_frame.pack(pady = 20)
    server_button_Start = tkc.CTkButton(master=button_server_frame,text="Start",command=start_server, width=50, height=50, corner_radius=30)
    server_button_Start.pack(side="right",pady = 10, padx = 10)

    server_button_stop = tkc.CTkButton(master=button_server_frame,text="Stop",command=close_server, width=50, height=50, corner_radius=30)
    server_button_stop.pack(side="left",pady = 10, padx = 10)


def processar_dados(stint1,stint2):
    lapf = []
    timef = []

    lapf2 = []
    timef2 = []
   
    comando2 = f"SELECT * FROM acs_data.laps_data WHERE stint_id IN ({stint1} , {stint2})"
    cursor.execute(comando2)
    datastint = cursor.fetchall()

    comando_car_name = f"SELECT car_name FROM acs_data.stints WHERE nome_stint IN ('Stint {stint1}', 'Stint {stint2}')"
    cursor.execute(comando_car_name)
    cars_names = cursor.fetchall()
    print(cars_names)

    for x in datastint:
        stint_id = x[3]
        lap = x[1]
        time = x[2]
        time = time / 1000
        m = int(time / 60)
        s = round((time % 60), 2)
        lap = int(lap)
        
        if stint_id == stint1:
            timef.append(f"{m}:{s:05.2f}")
            timegraf.append(m * 60 + s)
            lapgraf.append(lap)
            lapf.append(lap)
            
        
        elif stint_id == stint2:
            timef2.append(f"{m}:{s:05.2f}")
            timegra2f.append(m * 60 + s)
            lapgra2f.append(lap)
            lapf2.append(lap)
   

    stint1f = IA_processar(lapf,timef)
    stint2f = IA_processar(lapf2,timef2)   
    GUI2(stint1f,stint2f,cars_names)

    

def IA_processar(lap,time):                
    stint = f"Volta: {lap} // {time}"
    return stint


def GUI2 (stint1f,stint2f,car_names):

    GUI_2 = tkc.CTkToplevel()
    GUI_2.title("ACS")
    GUI_2.geometry("1300x550")
    intro = f"""
Você é um engenheiro de corridas altamente qualificado, especializado em análise de desempenho em stints de pilotagem. Os pilotos enviaram os tempos de volta registrados, e sua tarefa consiste em:

1. Calcular a média dos tempos de volta para cada stint.
2. Determinar o desvio padrão dos tempos, avaliando a consistência.
3. Identificar voltas que sejam inconsistentes ou fora do padrão esperado.
4. Propor estratégias de melhoria com base nos dados analisados.
5. Atribuir uma nota de desempenho de 1 a 10 para cada stint, justificando sua avaliação.

Seja técnico, claro e objetivo em suas respostas, garantindo precisão na análise e recomendações.

 Dados enviados pelos pilotos:
- Stint 1: {stint1f}
- Stint 2: {stint2f}
"""
    
    frame_right2 = tkc.CTkFrame(master=GUI_2, fg_color="#474a51")
    frame_right2.pack(side="right", pady=10,padx=10)

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

    def start_IA(intro):
        intro = chat.send_message(intro)
        chat_janela.insert(tk.END, f"\n ENGENHEIRO: {intro.text}\n")
        chat_janela.pack()

    user_message = tkc.CTkEntry(master=chat_frame_input, width=390,text_color="black", height=50,corner_radius=20, fg_color="white")
    user_message.pack(side="left",padx=5,pady=0)
    
    send_button = tkc.CTkButton(master=chat_frame_input,text="Enviar",command=enviar_m, width=50, height=50, corner_radius=30)
    send_button.pack(side="right", padx=5, pady=0)
    
    
    grafico(frame_right2,GUI_2,car_names)
    
    Thread_IA = threading.Thread(target=start_IA, args=(intro,))
    Thread_IA.start()


def img(track, car):
    track = Image.open(track).convert("RGBA")
    car = Image.open(car).convert("RGBA").resize((300,200))

    track.paste(car, (130,110), car)
    btn_wallpaper = track
    return btn_wallpaper

def abrir_arquivos():
    GUI4 = tkc.CTkToplevel()
    GUI4.geometry("500x400")
    GUI4.title("Selecionar Stint")
    label = tkc.CTkLabel(master=GUI4, text="Selecione 1 ou 2 Stints")
    label.pack(side="top")

    stints_frame = tkc.CTkScrollableFrame(master=GUI4,fg_color="black",width=400,height=300)
    stints_frame.pack(anchor="center",padx=10)

    comando_select1 = "SELECT * FROM acs_data.stints"
    cursor.execute(comando_select1)
    datadb = cursor.fetchall()
    
    img_list_track = {"ks_drag": r"img\ks_drag.png",
                      "ks_highlands" : r"img\ks_highlands.png",
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
    
    row_num = 0
    col_num = 0
    
    stints_selecionados = []

    for row in datadb:
        stint_id = row[0]
        car = row[2]
        track = row[3]

        if track in img_list_track and car in img_list_car:
            track_path = img_list_track[track]
            car_path = img_list_car[car]
            btn_wallpaper = img(track_path,car_path)
            btn_wallpaperf = tkc.CTkImage(light_image=btn_wallpaper, size=(150,150))
            button = tkc.CTkButton(master=stints_frame, text=f"",fg_color="gray",image=btn_wallpaperf, width=100, height=100, command=lambda s=stint_id:selecao_stints(s))
            button.grid(row=row_num, column=col_num, padx=5, pady=5)
            col_num +=1
            if col_num == 2:
                row_num+=1
                col_num=0

    def selecao_stints(stint_id):
            global stint1, stint2
            
            stint1 = 0
            stint2 = 0
            stints_selecionados.append(stint_id)
           
            if len(stints_selecionados) == 1:
                    stint1 = stints_selecionados[0]        
                    
            if len(stints_selecionados) == 2:
                    stint1 = stints_selecionados[0]
                    stint2 = stints_selecionados[1]
                    stints_selecionados.clear()

         
    
                

    buttonstart = tkc.CTkButton(master=GUI4, text="Analisar",corner_radius=32,width=150, command=lambda: processar_dados(stint1,stint2))
    buttonstart.pack(side="bottom", pady=10)

GUI = tkc.CTk()
GUI.geometry("500x400")
GUI.title("ACS")


frame_right = tkc.CTkFrame(master=GUI, fg_color="white")
frame_right.pack(side="right", fill="both", expand=True)

frame_1 = tkc.CTkFrame(master=frame_right, fg_color="white")
frame_1.pack(padx=10, pady=80)

ACS_logo = tkc.CTkImage(Image.open(r"img\ACSv9_logo.png"), size=(160,130))
img_label_logo = tkc.CTkLabel(master=frame_1, text="", image=ACS_logo)
img_label_logo.pack(padx=30, pady=5)


btn1 = tkc.CTkButton(master=frame_1, text="Enviar", corner_radius=32,width=150, fg_color="black", command=abrir_arquivos)
btn1.pack(pady=0, padx=10)

btn2 = tkc.CTkButton(master=frame_1, text="Iniciar", corner_radius=32,width=150, fg_color="black", command=GUI3)
btn2.pack(pady=5, padx=10)

frame_2 = tkc.CTkFrame(master=frame_right, fg_color="white")
frame_2.pack(side="bottom")

frame_left = tkc.CTkFrame(master=GUI, fg_color="white")
frame_left.pack(side="left", fill="both", expand=True)

wallpaper_left = tkc.CTkImage(Image.open(r"img\Wallpaper.png"), size=(400,400))
img_label1 = tkc.CTkLabel(master=frame_left, text="", image=wallpaper_left)
img_label1.pack(fill="both", expand = True)



def grafico(frame_right2,GUI_2):
    

    def limpar_canvas():
        timegraf.clear()
        timegra2f.clear()
        lapgraf.clear()
        lapgra2f.clear()
        canvas.get_tk_widget().destroy()
        GUI_2.destroy()


    GUI_2.protocol("WM_DELETE_WINDOW", limpar_canvas)
    
    fig, ax = plt.subplots()
    
    canvas = FigureCanvasTkAgg(fig, master=frame_right2)
    canvas.get_tk_widget().grid(row=0, column=1,sticky="nsew", padx=10, pady=10)
    

    
    
    plt.plot(lapgraf,timegraf ,color='red', marker='o', label="Stint 1")
    plt.plot(lapgra2f, timegra2f ,color='blue', marker='o',label="Stint 2")
 
    for i, (l , t) in enumerate(zip(lapgraf,timegraf)):
        if l == lapgraf[-1]:
             plt.text(l, t, "Fim do stint", ha="left", va="bottom")

        plt.text(l, t, f"{t}", ha='right', va='top')


    
    for i, (l , t) in enumerate(zip(lapgra2f,timegra2f)):
        if l == lapgra2f[-1]:
             plt.text(l, t, "Fim do stint", ha="left", va="bottom")

        plt.text(l, t, f"{t}", ha='left', va='top')

    
    plt.xlabel("Volta")
    plt.ylabel("Tempo")
    plt.title("Stints")
    plt.legend()


    canvas.draw()

GUI.mainloop()
