# YouTube Trending Brazil — ELT Pipeline

Pipeline ELT que monitora diariamente os vídeos em alta no YouTube Brasil, constrói histórico de canais e responde perguntas de negócio sobre o comportamento do algoritmo.

## Objetivo

Entender quais nichos o algoritmo do YouTube favorece no Brasil, quais canais aparecem consistentemente nos trending e quem está crescendo mais rápido — com dados coletados diariamente e transformados para análise.

## Arquitetura

```
YouTube Data API v3
        │
        ▼
   Python (coleta)
        │
        ▼
   DuckDB (raw)
        │
        ▼
   dbt Core (transformação)
        │
        ▼
   Metabase / Evidence (BI)
```

## Stack

| Camada | Tecnologia |
|---|---|
| Coleta | Python + Google API Client |
| Armazenamento | DuckDB |
| Transformação | dbt Core |
| Visualização | Metabase / Evidence |

## Modelagem dbt

```
raw/
├── videos          — snapshot diário de vídeos em alta por categoria
├── channels        — snapshot diário de estatísticas de canais
└── video_categories — categorias disponíveis no Brasil

staging/
├── stg_videos
├── stg_channels
└── stg_trending_slots

intermediate/
├── int_channel_daily_growth     — delta de inscritos e views dia a dia
├── int_video_engagement         — ratio likes+comentários/views
└── int_channel_trending_history — frequência de aparição nos trending

marts/
├── dim_channels
├── dim_categories
├── fct_daily_snapshots
└── fct_trending
```

## Perguntas de negócio respondidas

- Quais nichos o algoritmo do YouTube favorece no Brasil?
- Canais que aparecem mais nos trending crescem mais rápido?
- Qual categoria tem mais engajamento relativo?
- Quem são os canais emergentes — pequenos mas frequentes nos trending?
- Como frequência de publicação afeta presença nos trending?

## Como executar

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .youtube
source .youtube/Scripts/activate

# 2. Instalar dependências
pip install -r ingestion/requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Adicionar YOUTUBE_API_KEY no .env

# 4. Rodar a coleta
python ingestion/collect.py

# 5. Rodar as transformações
cd dbt_project
dbt run
```

## Estrutura do projeto

```
youtube-trending/
├── ingestion/
│   ├── collect.py          # Orquestração da coleta diária
│   ├── youtube_client.py   # Wrapper da YouTube Data API v3
│   └── requirements.txt
├── data/
│   └── youtube.duckdb      # Banco local (não versionado)
├── dbt_project/            # Modelos de transformação
└── .env.example
```

## Status

🚧 Em desenvolvimento — fase 1 (coleta e transformações locais)

**Fase 2 planejada:** orquestração com Airflow, containerização com Docker e deploy em cloud.