# Projeto Fernanda

Projeto de Chatbot sobre educação fiscal. A ideia do projeto é ensinar às pessoas sobre educação fiscal e espalhar conteúdo informativo sobre a fiscalização brasileira.

## Tecnologias e Ferramentas

- **LangGraph** - Lógica dos agentes
- **FastAPI** - Backend
- **Docker** - Conteinarização
- **PostgreSQL** - Banco de Dados
- **Ollama (Llama 3.1 8B)** - Modelo de IA pré-treinado

## Estrutura do Projeto
```
Fernanda-IA/
├── docker-compose.yml
├── README.md
├── requirements.txt
├── .env
├── src/
│   ├── _init_.py
│   ├── agents/
│   │   ├── _init_.py
│   │   ├── pedagogical_agent.py
│   │   ├── specialist_agent.py
│   │   ├── evaluator_agent.py
│   │   └── integrator_agent.py
│   ├── services/
│   │   ├── _init_.py
│   │   ├── llm_service.py
│   │   └── memory_service.py
│   ├── utils/
│   │   └── config.py
│   └── main.py
├── tests/
└── docs/
```

## Como rodar o Projeto

### Pré-requisitos

Certifique-se de ter o docker e o git instalado.

**Passo 1** - Clonar repo
```
git clone <url do repositorio>
```

**Passo 2** - Entrar no projeto
```
cd Fernanda-IA
```

**Passo 3** - Criar ambiente virtual
```
python3 -m venv venv
source venv/bin/activate
```

**Passo 4** - Criar .env na **raiz do projeto**
```
MODEL_NAME=tinyllama
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

**Passo 4** - Rodar LLM **local** (por enquanto)
```
ollama run tinyllama
```

**Passo 5** - Comando docker para buildar
```
docker compose up -d --build
```

## Arquitetura

### Alto Nível
Em desenvolvimento...

### IA
- agents -> Agentes de IA
- services -> Lógica da LLM e memória
- utils -> helpers

## Diagramas

### Diagrama de caso de uso
Em desenvolvimento...

### Diagrama ER
Em desenvolvimento...
