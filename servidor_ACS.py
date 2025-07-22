import socket
import select
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

hostsql = os.getenv("DB_HOST")
usersql = os.getenv("DB_USER")
passwordsql = os.getenv("DB_PASSWORD")
databasesql = os.getenv("DB_NAME")


ACSdb = mysql.connector.connect(
    host = hostsql,
    user = usersql,
    password = passwordsql,
    database = databasesql,
)

cursor = ACSdb.cursor()


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 1111))
servidor.listen(5)
servidor.setblocking(False) 

clientes = [servidor]  
conexao_ativa = True

session_counter = 1
session_counter_file = "session_counter.txt"


def load_session_counter():
    if os.path.exists(session_counter_file):
        with open(session_counter_file, "r") as f:
            return int(f.read().strip())
    return 1


def save_session_counter(session_counter):
        with open(session_counter_file, "w") as f:
            f.write(str(session_counter))

session_counter = load_session_counter()

while conexao_ativa:

    leitura, _, _ = select.select(clientes, [], [])

    for s in leitura:
        if s is servidor:
            cliente, endereco = servidor.accept()
            clientes.append(cliente)
            cliente.send(f"Code=00".encode('utf-8'))
            print(clientes)
            if len(clientes) > 2:
                client1 = clientes[1]
                client1.send(f"Code=01".encode('utf-8'))
                session_counter += 1        
                stint_counter = f"Stint {session_counter}"        
                comando_insert2 = f'INSERT INTO stints (nome_stint) VALUES ("{stint_counter}")'
                cursor.execute(comando_insert2)
                ACSdb.commit()
            
            save_session_counter(session_counter)

        else:

            try:
                msg = s.recv(2000).decode('utf-8')

                if not msg:  
                    clientes.remove(s)
                    s.close()

                    continue

                if msg.strip() == "Code=01":
                    
                    conexao_ativa = False
                    break

                msg = msg.strip()
                msg_parts = msg.split('\n')
                
                data = msg_parts[0]
                code = msg_parts[1]
                car = msg_parts [2]
                track = msg_parts[3]
                

                if code.strip() == "Code=02":
                    
                    for c in clientes:
                        if c is not servidor and c is not s:
                            c.send("Code=02".encode('utf-8'))

                if "Car:" in car:
                    car_parts = car.split(":")
                    car_name = car_parts[1]
                    comand_update1 = f'UPDATE stints SET car_name = "{car_name}" WHERE nome_stint = "{stint_counter}"'
                    cursor.execute(comand_update1)
                    ACSdb.commit()
                
                if "Track:" in track:
                    track_parts = track.split(":")
                    track_name = track_parts[1]
                    comand_update2 = f'UPDATE stints SET track_name = "{track_name}" WHERE nome_stint = "{stint_counter}"'
                    cursor.execute(comand_update2)
                    ACSdb.commit()
                
                                       
                if "||" in data:
                    
                    values = data.split("||")
                    if len(values) == 2:
                        lap_number = int(values[0].strip())
                        lap_time = float(values[1].strip())
                        
                        comando_insert = f'INSERT INTO laps_data (lap_number, lap_time, stint_id) VALUES ({lap_number}, {lap_time}, {session_counter})'
                        cursor.execute(comando_insert)
                        ACSdb.commit()
                                      
                    else:
                        print("ErrorCode=02")
                else:
                    print("ErrorCode=03")

            except Exception as e:
                print(f"Erro de conexão: {e}")

for c in clientes:
    if c is not servidor:
        c.close()

servidor.close()
