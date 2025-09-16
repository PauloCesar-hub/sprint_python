# 🏟️ Passa a Bola --- Ranking & Estatísticas do Futebol Feminino

Este projeto é uma aplicação de terminal em Python para **gerenciar
jogadoras, registrar partidas e gerar rankings e estatísticas
consolidadas** do futebol feminino.\
Ele salva os dados localmente em arquivos CSV e permite visualizações
gráficas da evolução de gols e assistências.

------------------------------------------------------------------------

## ⚙️ Funcionalidades Principais

-   📋 Cadastro de jogadoras (nome, posição e time/seleção)\
-   📝 Registro de partidas com data, gols, assistências e minutos
    jogados\
-   📊 Geração de ranking por pontuação (score calculado com base no
    desempenho)\
-   📈 Exibição de estatísticas individuais e médias por jogo\
-   🖼️ Geração opcional de gráficos (gols e assistências por partida)\
-   📁 Exportação do ranking consolidado em CSV

------------------------------------------------------------------------

## 🧩 Estrutura do Projeto

    pythonV2/
    │
    ├── main.py               # Código principal e menu de interação
    ├── requirements.txt      # Dependências necessárias
    └── data/
        ├── jogadoras.csv     # Banco de dados local das jogadoras
        └── partidas.csv      # Banco de dados local das partidas

------------------------------------------------------------------------

## 🧪 Requisitos

-   Python 3.9+\
-   Bibliotecas listadas em `requirements.txt`:

``` txt
pandas>=2.1.0
matplotlib>=3.7.0
```

------------------------------------------------------------------------

## 🚀 Como Executar

1.  Instale as dependências:

    ``` bash
    pip install -r requirements.txt
    ```

2.  Execute o sistema:

    ``` bash
    python main.py
    ```

3.  Use o menu interativo para navegar pelas opções.

------------------------------------------------------------------------

## 📝 Menu Principal

  Opção   Ação
  ------- -----------------------------------------------
  1       Adicionar jogadora
  2       Registrar partida
  3       Ver ranking
  4       Ver estatísticas de uma jogadora
  5       Gerar gráfico de evolução (gols/assistências)
  6       Exportar consolidado CSV
  0       Sair

------------------------------------------------------------------------

## 🧮 Fórmula de Score (padrão)
```
score = (gols * 4) + (assistencias * 3) + (minutos / 90) * 0.5
```
> Você pode trocar esses pesos dentro do código (função `calcular_score`).
------------------------------------------------------------------------


## 🗃️ Dados de exemplo
- Ao rodar a primeira vez, os arquivos `data/jogadoras.csv` e `data/partidas.csv` são criados automaticamente.
- Você pode alimentar pela CLI ou editar via Excel/Google Sheets (mantenha os cabeçalhos!).

- 
------------------------------------------------------------------------


## 📈 Gráficos
- A opção de gráfico usa `matplotlib`. Se não quiser gráficos, basta não instalar a lib que o app funciona do mesmo jeito.
------------------------------------------------------------------------


## 🧱 Roadmap de melhorias (ideias simples)
- API Flask com endpoints `/jogadoras`, `/partidas`, `/ranking`
- Persistência em SQLite (via `sqlite3`)
- Importar dados de campeonatos (CSV/planilhas) para automatizar
- Métricas avançadas por posição (ex.: Goleira: defesas, SG; Meia: passes-chave; etc.)


------------------------------------------------------------------------
## 📤 Exportação e Dados

-   Os dados ficam salvos localmente na pasta `data/`.
-   O ranking consolidado pode ser exportado como
    `data/consolidado.csv`.

------------------------------------------------------------------------

## 👨‍💻 Autores

- Paulo Cesar de Govea Junior - (RM:566034)
- Guilherme Vilela Perez - (RM:564422)
- Gustavo Panham Dourado - (RM:563904)
- Christian Schunck de Almeida - (RM:563850)
- Thomas Jeferson Santana Wang - (RM565104)
  
------------------------------------------------------------------------
## 📄 Licença

Projeto criado para fins educativos e sem fins lucrativos.\
Sinta-se livre para modificar e reutilizar.
