## 🏟️ Passa a Bola — Ranking & Estatísticas do Futebol Feminino

Este projeto é uma aplicação de terminal em Python para gerenciar jogadoras, registrar partidas e gerar rankings e estatísticas consolidadas do futebol feminino.
Ele salva os dados localmente em arquivos CSV e permite visualizações gráficas da evolução de gols e assistências.

## ⚙️ Funcionalidades Principais

📋 Cadastro de jogadoras (nome, posição e time/seleção)

📝 Registro de partidas com data, gols, assistências e minutos jogados

📊 Geração de ranking por pontuação (score calculado com base no desempenho)

📈 Exibição de estatísticas individuais e médias por jogo

🖼️ Geração opcional de gráficos (gols e assistências por partida)

📁 Exportação do ranking consolidado em CSV

---

🧩 Estrutura do Projeto
pythonV2/
│
├── main.py               # Código principal e menu de interação
├── requirements.txt      # Dependências necessárias
└── data/
    ├── jogadoras.csv     # Banco de dados local das jogadoras
    └── partidas.csv      # Banco de dados local das partidas
    
---
## 🧪 Requisitos

Python 3.9+

Bibliotecas listadas em requirements.txt:

pandas>=2.1.0
matplotlib>=3.7.0


requirements

🚀 Como Executar

Instale as dependências:

pip install -r requirements.txt


Execute o sistema:

python main.py


Use o menu interativo para navegar pelas opções.

📝 Menu Principal
Opção	Ação
1	Adicionar jogadora
2	Registrar partida
3	Ver ranking
4	Ver estatísticas de uma jogadora
5	Gerar gráfico de evolução (gols/assistências)
6	Exportar consolidado CSV
0	Sair
📤 Exportação e Dados

Os dados ficam salvos localmente na pasta data/.

O ranking consolidado pode ser exportado como data/consolidado.csv.

📄 Licença

Projeto criado para fins educativos e sem fins lucrativos.
Sinta-se livre para modificar e reutilizar.
