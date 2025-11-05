# 📊 Sistema de Gerenciamento de Jogadoras e Estatísticas de Partidas

Este projeto é um sistema em **Python** para gerenciamento de jogadoras de futebol e registro de partidas, permitindo o acompanhamento de desempenho, estatísticas e geração de gráficos visuais de evolução.

O sistema trabalha com as seguintes funcionalidades principais:
- Cadastro, consulta, edição e exclusão de jogadoras (CRUD completo)
- Registro detalhado de partidas (gols, assistências, etc.)
- Calculadora de score para ranking geral
- Geração de gráficos com `matplotlib`
- Exportação dos dados em `.json` (persistência local)

---

## 🏗️ Estrutura do Projeto

sprint_python/
│
├── data/
│ └── jogadores.json # Base de dados local
│
├── graficos/ # Pasta onde os gráficos PNG são salvos
│
├── main.py # Código principal do sistema (menu)
├── jogadores.py # Funções de CRUD das jogadoras
├── partidas.py # Registro e controle de partidas
├── estatisticas.py # Cálculos e ranking
├── graficos.py # Funções de geração de gráficos
│
└── README.md # Documentação

yaml
Copiar código

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

| Tecnologia | Uso |
|-----------|-----|
| Python 3  | Linguagem principal |
| `json`    | Salvamento dos dados |
| `matplotlib` | Geração de gráficos |
| `os`      | Manipulação de arquivos e diretórios |

---

## 🚀 Como Executar o Projeto

### **1. Instale o Python (se necessário)**
https://www.python.org/downloads/

### **2. Instale as dependências**
```bash
pip install matplotlib
3. Execute o sistema
bash
Copiar código
python main.py
🎮 Como Usar (Menu Principal)
Ao abrir o sistema, você verá um menu como este:

Copiar código
1) Cadastrar jogadora
2) Listar jogadoras
3) Editar jogadora
4) Excluir jogadora
5) Registrar partida
6) Listar partidas
7) Mostrar ranking geral
11) Gráfico - Evolução por jogadora
12) Gráfico - Ranking geral
0) Sair
📈 Gráficos Disponíveis
1) Evolução por Jogadora
Mostra o desempenho da jogadora ao longo das partidas:

Linha de Gols

Linha de Assistências

Gerado automaticamente e salvo em:

bash
Copiar código
/graficos/evolucao_nome_da_jogadora.png
2) Ranking Geral
Compara o score total de todas jogadoras cadastradas.

Salvo em:

bash
Copiar código
/graficos/ranking.png
🏅 Cálculo do Score
O score total da jogadora segue a seguinte fórmula:

ini
Copiar código
Score = (Gols × 2) + Assistências
📦 Backup e Persistência
Todos os dados são salvos no arquivo:

bash
Copiar código
data/jogadores.json
Ele é atualizado automaticamente conforme o CRUD é utilizado.

👥 Autores
Paulo Cesar de Govea Junior - (RM:566034)

Guilherme Vilela Perez - (RM:564422)

Gustavo Panham Dourado - (RM:563904)

Christian Schunck de Almeida - (RM:563850)

Thomas Jeferson Santana Wang - (RM565104)
