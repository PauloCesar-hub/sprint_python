#!/usr/bin/env python3
"""
Passa a Bola - CLI completa com CRUD para jogadoras e partidas.
Salva dados em CSV no diretório `data/`.

Funcionalidades:
 - CRUD completo para jogadoras (create, read/list, update, delete)
 - CRUD completo para partidas (create, read/list, update, delete)
 - Estatísticas agregadas (gols, assistências, minutos e score)
 - Exportar CSVs de backup
"""
import os
import csv
import uuid
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
JOGADORAS_CSV = os.path.join(DATA_DIR, "jogadoras.csv")
PARTIDAS_CSV = os.path.join(DATA_DIR, "partidas.csv")

JOGADORAS_HEADERS = ["id","nome","posicao","time","created_at"]
PARTIDAS_HEADERS = ["id","data","jogadora_id","gols","assistencias","minutos","observacoes","created_at"]

def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(JOGADORAS_CSV):
        with open(JOGADORAS_CSV,"w",newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(JOGADORAS_HEADERS)
    if not os.path.exists(PARTIDAS_CSV):
        with open(PARTIDAS_CSV,"w",newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(PARTIDAS_HEADERS)

def read_csv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path,newline='',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def write_csv(path, rows, headers):
    with open(path,"w",newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

# ---------- Jogadoras CRUD ----------
def listar_jogadoras():
    jogs = read_csv(JOGADORAS_CSV)
    if not jogs:
        print("Nenhuma jogadora cadastrada.")
        return
    print(f"{'ID':36} | Nome - Posição - Time")
    print("-"*80)
    for j in jogs:
        print(f"{j['id']} | {j['nome']} - {j['posicao']} - {j['time']}")

def criar_jogadora():
    nome = input("Nome: ").strip()
    if not nome:
        print("Nome obrigatório.")
        return
    pos = input("Posição: ").strip()
    time = input("Time/Seleção: ").strip()
    new = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "posicao": pos,
        "time": time,
        "created_at": datetime.utcnow().isoformat()
    }
    rows = read_csv(JOGADORAS_CSV)
    rows.append(new)
    write_csv(JOGADORAS_CSV, rows, JOGADORAS_HEADERS)
    print("Jogadora criada com id:", new["id"])

def buscar_jogadora_por_id(jid):
    rows = read_csv(JOGADORAS_CSV)
    for r in rows:
        if r["id"] == jid:
            return r
    return None

def atualizar_jogadora():
    jid = input("ID da jogadora a atualizar: ").strip()
    if not jid:
        print("ID obrigatório.")
        return
    rows = read_csv(JOGADORAS_CSV)
    found = False
    for r in rows:
        if r["id"] == jid:
            found = True
            print("Deixe em branco para não alterar o campo.")
            novo_nome = input(f"Nome [{r['nome']}]: ").strip()
            novo_pos = input(f"Posição [{r['posicao']}]: ").strip()
            novo_time = input(f"Time [{r['time']}]: ").strip()
            if novo_nome:
                r['nome'] = novo_nome
            if novo_pos:
                r['posicao'] = novo_pos
            if novo_time:
                r['time'] = novo_time
            break
    if not found:
        print("Jogadora não encontrada.")
        return
    write_csv(JOGADORAS_CSV, rows, JOGADORAS_HEADERS)
    print("Atualização salva.")

def excluir_jogadora():
    jid = input("ID da jogadora a excluir: ").strip()
    if not jid:
        print("ID obrigatório.")
        return
    # Remove partidas relacionadas também (cascade)
    jogs = read_csv(JOGADORAS_CSV)
    novas = [j for j in jogs if j['id'] != jid]
    if len(novas) == len(jogs):
        print("Jogadora não encontrada.")
        return
    write_csv(JOGADORAS_CSV, novas, JOGADORAS_HEADERS)
    partidas = read_csv(PARTIDAS_CSV)
    partidas = [p for p in partidas if p['jogadora_id'] != jid]
    write_csv(PARTIDAS_CSV, partidas, PARTIDAS_HEADERS)
    print("Jogadora e partidas relacionadas excluídas.")

# ---------- Partidas CRUD ----------
def listar_partidas():
    parts = read_csv(PARTIDAS_CSV)
    if not parts:
        print("Nenhuma partida registrada.")
        return
    print(f"{'ID':36} | Data | Jogadora ID | Gols | Assist | Min")
    print("-"*100)
    for p in parts:
        print(f"{p['id']} | {p['data']} | {p['jogadora_id']} | {p['gols']} | {p['assistencias']} | {p['minutos']}")

def criar_partida():
    jog_id = input("ID da jogadora (use 'listar jogadoras' para ver IDs): ").strip()
    if not buscar_jogadora_por_id(jog_id):
        print("Jogadora não encontrada.")
        return
    data = input("Data (YYYY-MM-DD) [hoje]: ").strip()
    if not data:
        data = datetime.utcnow().date().isoformat()
    # validate date
    try:
        datetime.fromisoformat(data)
    except Exception:
        print("Data inválida.")
        return
    def to_int(prompt):
        v = input(prompt).strip()
        if not v:
            return "0"
        try:
            return str(int(v))
        except:
            print("Valor inválido, usando 0.")
            return "0"
    gols = to_int("Gols: ")
    assists = to_int("Assistências: ")
    minutos = to_int("Minutos jogados: ")
    obs = input("Observações (opcional): ").strip()
    new = {
        "id": str(uuid.uuid4()),
        "data": data,
        "jogadora_id": jog_id,
        "gols": gols,
        "assistencias": assists,
        "minutos": minutos,
        "observacoes": obs,
        "created_at": datetime.utcnow().isoformat()
    }
    rows = read_csv(PARTIDAS_CSV)
    rows.append(new)
    write_csv(PARTIDAS_CSV, rows, PARTIDAS_HEADERS)
    print("Partida criada com id:", new["id"])

def buscar_partida_por_id(pid):
    parts = read_csv(PARTIDAS_CSV)
    for p in parts:
        if p["id"] == pid:
            return p
    return None

def atualizar_partida():
    pid = input("ID da partida a atualizar: ").strip()
    if not pid:
        print("ID obrigatório.")
        return
    parts = read_csv(PARTIDAS_CSV)
    found = False
    for p in parts:
        if p["id"] == pid:
            found = True
            print("Deixe em branco para não alterar.")
            novo_data = input(f"Data [{p['data']}]: ").strip()
            if novo_data:
                try:
                    datetime.fromisoformat(novo_data)
                    p['data'] = novo_data
                except:
                    print("Data inválida. Mantendo original.")
            novo_jog = input(f"Jogadora ID [{p['jogadora_id']}]: ").strip()
            if novo_jog:
                if buscar_jogadora_por_id(novo_jog):
                    p['jogadora_id'] = novo_jog
                else:
                    print("Jogadora nova não encontrada. Mantendo original.")
            for field in ('gols','assistencias','minutos'):
                novo = input(f"{field} [{p[field]}]: ").strip()
                if novo:
                    try:
                        p[field] = str(int(novo))
                    except:
                        print(f"Valor inválido para {field}. Mantendo original.")
            novo_obs = input(f"Observações [{p.get('observacoes','')}]: ").strip()
            if novo_obs:
                p['observacoes'] = novo_obs
            break
    if not found:
        print("Partida não encontrada.")
        return
    write_csv(PARTIDAS_CSV, parts, PARTIDAS_HEADERS)
    print("Partida atualizada.")

def excluir_partida():
    pid = input("ID da partida a excluir: ").strip()
    if not pid:
        print("ID obrigatório.")
        return
    parts = read_csv(PARTIDAS_CSV)
    novas = [p for p in parts if p['id'] != pid]
    if len(novas) == len(parts):
        print("Partida não encontrada.")
        return
    write_csv(PARTIDAS_CSV, novas, PARTIDAS_HEADERS)
    print("Partida excluída.")

# ---------- Estatísticas ----------
def calcular_estatisticas():
    jogs = read_csv(JOGADORAS_CSV)
    parts = read_csv(PARTIDAS_CSV)
    stats = defaultdict(lambda: {"gols":0,"assistencias":0,"minutos":0,"partidas":0})
    for p in parts:
        jid = p['jogadora_id']
        try:
            gols = int(p.get('gols') or 0)
            ass = int(p.get('assistencias') or 0)
            mins = int(p.get('minutos') or 0)
        except:
            gols = ass = mins = 0
        stats[jid]["gols"] += gols
        stats[jid]["assistencias"] += ass
        stats[jid]["minutos"] += mins
        stats[jid]["partidas"] += 1
    # join with players
    result = []
    for j in jogs:
        jid = j['id']
        s = stats[jid]
        # score example: gols*4 + assist*3 + minutos/90
        score = s["gols"]*4 + s["assistencias"]*3 + (s["minutos"]/90)
        result.append({
            "id": jid,
            "nome": j["nome"],
            "time": j.get("time",""),
            "posicao": j.get("posicao",""),
            "gols": s["gols"],
            "assistencias": s["assistencias"],
            "minutos": s["minutos"],
            "partidas": s["partidas"],
            "score": round(score,2)
        })
    # sort by score desc
    result.sort(key=lambda x: x["score"], reverse=True)
    return result

def mostrar_ranking():
    rank = calcular_estatisticas()
    if not rank:
        print("Sem dados para ranking.")
        return
    print(f"{'Pos':3} {'Nome':30} {'Gols':5} {'Ast':4} {'Min':5} {'Pts':6}")
    print("-"*70)
    for i,r in enumerate(rank, start=1):
        print(f"{i:>3} {r['nome'][:30]:30} {r['gols']:>5} {r['assistencias']:>4} {r['minutos']:>5} {r['score']:>6}")

# ---------- Export ----------
def exportar_backup():
    now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(BASE_DIR, f"backup_{now}.zip")
    import zipfile
    with zipfile.ZipFile(dest,'w') as z:
        if os.path.exists(JOGADORAS_CSV):
            z.write(JOGADORAS_CSV, arcname="jogadoras.csv")
        if os.path.exists(PARTIDAS_CSV):
            z.write(PARTIDAS_CSV, arcname="partidas.csv")
    print("Backup criado:", dest)

# ---------- CLI ----------


# ---------- Gráficos ----------
def grafico_evolucao_jogadora():
    jog_id = input("ID da jogadora (use 'Listar jogadoras' para ver IDs): ").strip()
    if not buscar_jogadora_por_id(jog_id):
        print("Jogadora não encontrada.")
        return
    parts = read_csv(PARTIDAS_CSV)
    dados = [p for p in parts if p['jogadora_id'] == jog_id]
    if not dados:
        print("Sem partidas para esta jogadora.")
        return
    # Ordenar por data
    try:
        dados.sort(key=lambda x: x['data'])
    except:
        pass
    gols = []
    assists = []
    labels = []
    for p in dados:
        labels.append(p['data'])
        try:
            gols.append(int(p['gols']))
            assists.append(int(p['assistencias']))
        except:
            gols.append(0)
            assists.append(0)
    plt.figure()
    plt.plot(labels, gols, marker='o', label='Gols')
    plt.plot(labels, assists, marker='o', label='Assistências')
    plt.xlabel("Partidas (Data)")
    plt.ylabel("Quantidade")
    plt.title("Evolução da Jogadora")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafico_ranking():
    rank = calcular_estatisticas()
    if not rank:
        print("Sem dados para ranking.")
        return
    nomes = [r['nome'] for r in rank]
    scores = [r['score'] for r in rank]
    plt.figure()
    plt.bar(nomes, scores)
    plt.xlabel("Jogadoras")
    plt.ylabel("Score")
    plt.title("Ranking Geral - Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def mostrar_menu():
    print("""
=== PASSA A BOLA - Menu ===
1) Listar jogadoras
2) Criar jogadora
3) Atualizar jogadora
4) Excluir jogadora
5) Listar partidas
6) Criar partida
7) Atualizar partida
8) Excluir partida
9) Mostrar ranking/estatísticas
10) Exportar backup (zip)
11) Gráfico - Evolução por Jogadora
12) Gráfico - Ranking Geral
0) Sair
""")

def main():
    ensure_storage()
    while True:
        mostrar_menu()
        op = input("Escolha: ").strip()
        if op == "1":
            listar_jogadoras()
        elif op == "2":
            criar_jogadora()
        elif op == "3":
            atualizar_jogadora()
        elif op == "4":
            excluir_jogadora()
        elif op == "5":
            listar_partidas()
        elif op == "6":
            criar_partida()
        elif op == "7":
            atualizar_partida()
        elif op == "8":
            excluir_partida()
        elif op == "9":
            mostrar_ranking()
        elif op == "10":
            exportar_backup()
        elif op == "11":
            grafico_evolucao_jogadora()
        elif op == "12":
            grafico_ranking()
        elif op == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    main()
