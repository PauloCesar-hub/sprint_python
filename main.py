import os
import csv
from datetime import datetime
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
JOGADORAS_CSV = os.path.join(DATA_DIR, "jogadoras.csv")
PARTIDAS_CSV = os.path.join(DATA_DIR, "partidas.csv")

def init_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(JOGADORAS_CSV):
        with open(JOGADORAS_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id","nome","posicao","time"])
    if not os.path.exists(PARTIDAS_CSV):
        with open(PARTIDAS_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id","jogadora_id","data","gols","assistencias","minutos"])

def ler_jogadoras():
    with open(JOGADORAS_CSV, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r)

def salvar_jogadora(nome, posicao, time):
    jogadoras = ler_jogadoras()
    new_id = 1 + max([int(j["id"]) for j in jogadoras], default=0)
    with open(JOGADORAS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([new_id, nome.strip(), posicao.strip(), time.strip()])
    return new_id

def ler_partidas():
    with open(PARTIDAS_CSV, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r)

def salvar_partida(jogadora_id, data_str, gols, assistencias, minutos):
    partidas = ler_partidas()
    new_id = 1 + max([int(p["id"]) for p in partidas], default=0)
    
    try:
        _ = datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida. Use o formato YYYY-MM-DD.")
    with open(PARTIDAS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([new_id, jogadora_id, data_str, gols, assistencias, minutos])
    return new_id

usuario = {
    "login": "",
    "senha": ""
}   

def calcular_score(gols, assistencias, minutos):
    return (gols * 4) + (assistencias * 3) + (minutos / 90.0) * 0.5

def consolidar_estatisticas():
    jogadoras = {int(j["id"]): j for j in ler_jogadoras()}
    base = {jid: {"nome": j["nome"], "posicao": j["posicao"], "time": j["time"],
                  "gols": 0, "assistencias": 0, "minutos": 0, "jogos": 0, "score": 0.0}
            for jid, j in jogadoras.items()}
    for p in ler_partidas():
        jid = int(p["jogadora_id"])
        if jid not in base:
            
            continue
        g = int(p["gols"]); a = int(p["assistencias"]); m = int(p["minutos"])
        base[jid]["gols"] += g
        base[jid]["assistencias"] += a
        base[jid]["minutos"] += m
        base[jid]["jogos"] += 1
        base[jid]["score"] += calcular_score(g, a, m)
    return base

def ranking(top_n=20):
    estat = consolidar_estatisticas()
    linhas = []
    for jid, d in estat.items():
        linhas.append({
            "id": jid,
            "nome": d["nome"],
            "time": d["time"],
            "posicao": d["posicao"],
            "jogos": d["jogos"],
            "gols": d["gols"],
            "assistencias": d["assistencias"],
            "minutos": d["minutos"],
            "score": round(d["score"], 2)
        })
    linhas.sort(key=lambda x: x["score"], reverse=True)
    return linhas[:top_n]

def estatisticas_jogadora(jid):
    jid = int(jid)
    estat = consolidar_estatisticas().get(jid)
    if not estat:
        return None, []
    
    partidas = [p for p in ler_partidas() if int(p["jogadora_id"]) == jid]
    partidas.sort(key=lambda p: p["data"])
    return estat, partidas

def exportar_consolidado_csv(path):
    linhas = ranking(top_n=10**6)  
    campos = ["id","nome","time","posicao","jogos","gols","assistencias","minutos","score"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)

def menu():
    print("\n=== PASSA A BOLA — Ranking & Estatísticas (Futebol Feminino) ===")
    print("1) Adicionar jogadora")
    print("2) Registrar partida")
    print("3) Ver ranking")
    print("4) Ver estatísticas de uma jogadora")
    print("5) Gerar gráfico de evolução (gols/assistências por jogo) [opcional]")
    print("6) Exportar consolidado para CSV")
    print("0) Sair")

def escolher_jogadora():
    jogadoras = ler_jogadoras()
    if not jogadoras:
        print("Nenhuma jogadora cadastrada.")
        return None
    print("\nJogadoras:")
    for j in jogadoras:
        print(f'[{j["id"]}] {j["nome"]} — {j["posicao"]} ({j["time"]})')
    try:
        jid = int(input("Digite o ID da jogadora: ").strip())
    except ValueError:
        print("ID inválido.")
        return None
    ok = any(int(j["id"]) == jid for j in jogadoras)
    return jid if ok else None

def acao_adicionar_jogadora():
    nome = input("Nome: ").strip()
    pos = input("Posição (ex.: Atacante, Meia, Zagueira, Goleira): ").strip()
    time = input("Time/Seleção: ").strip()
    jid = salvar_jogadora(nome, pos, time)
    print(f"✅ Jogadora adicionada com ID {jid}.")

def acao_registrar_partida():
    jid = escolher_jogadora()
    if not jid:
        print("Operação cancelada.")
        return
    data = input("Data (YYYY-MM-DD): ").strip()
    try:
        gols = int(input("Gols: ").strip())
        assist = int(input("Assistências: ").strip())
        minutos = int(input("Minutos jogados: ").strip())
    except ValueError:
        print("Valores de gols/assistências/minutos precisam ser inteiros.")
        return
    try:
        pid = salvar_partida(jid, data, gols, assist, minutos)
        print(f"✅ Partida registrada com ID {pid}.")
    except Exception as e:
        print(f"Erro: {e}")

def acao_ver_ranking():
    linhas = ranking()
    if not linhas:
        print("Sem dados para ranking.")
        return
    print("\n-- RANKING --")
    print(f'{"#":>2} {"Jogadora":<22} {"Time":<14} {"Pos":<10} {"J":>2} {"G":>2} {"A":>2} {"Min":>5} {"Score":>7}')
    for i, l in enumerate(linhas, start=1):
        print(f'{i:>2} {l["nome"]:<22.22} {l["time"]:<14.14} {l["posicao"]:<10.10} {l["jogos"]:>2} {l["gols"]:>2} {l["assistencias"]:>2} {l["minutos"]:>5} {l["score"]:>7.2f}')

def acao_estatisticas_jogadora():
    jid = escolher_jogadora()
    if not jid:
        print("Operação cancelada.")
        return
    estat, partidas = estatisticas_jogadora(jid)
    if not estat:
        print("Jogadora não encontrada.")
        return
    print(f'\nEstatísticas — {estat["nome"]} ({estat["posicao"]}, {estat["time"]})')
    jogos = max(estat["jogos"], 1)
    print(f'Totais: Gols {estat["gols"]}, Assistências {estat["assistencias"]}, Min {estat["minutos"]}, Jogos {estat["jogos"]}, Score {estat["score"]:.2f}')
    print(f'Médias: G/J {estat["gols"]/jogos:.2f}, A/J {estat["assistencias"]/jogos:.2f}, Min/J {estat["minutos"]/jogos:.1f}')
    if partidas:
        print("\nÚltimos jogos:")
        for p in partidas[-5:]:
            print(f'{p["data"]} — G:{p["gols"]} A:{p["assistencias"]} Min:{p["minutos"]}')

def acao_grafico():
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib não está instalado. Rode: pip install matplotlib")
        return
    jid = escolher_jogadora()
    if not jid:
        print("Operação cancelada.")
        return
    _, partidas = estatisticas_jogadora(jid)
    if not partidas:
        print("Sem partidas para plotar.")
        return
    datas = [p["data"] for p in partidas]
    gols = [int(p["gols"]) for p in partidas]
    assist = [int(p["assistencias"]) for p in partidas]

    
    plt.figure()
    plt.plot(datas, gols, marker="o")
    plt.title("Gols por Jogo")
    plt.xlabel("Jogo (data)")
    plt.ylabel("Gols")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    
    plt.figure()
    plt.plot(datas, assist, marker="o")
    plt.title("Assistências por Jogo")
    plt.xlabel("Jogo (data)")
    plt.ylabel("Assistências")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def acao_exportar():
    path = os.path.join(DATA_DIR, "consolidado.csv")
    exportar_consolidado_csv(path)
    print(f"✅ Exportado para {path}")

def main():
    init_storage()
    while True:
        menu()
        op = input("Escolha: ").strip()
        if op == "1":
            acao_adicionar_jogadora()
        elif op == "2":
            acao_registrar_partida()
        elif op == "3":
            acao_ver_ranking()
        elif op == "4":
            acao_estatisticas_jogadora()
        elif op == "5":
            acao_grafico()
        elif op == "6":
            acao_exportar()
        elif op == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
