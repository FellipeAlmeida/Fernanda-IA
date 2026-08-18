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
│   ├── graph/
│   │   ├── _init_.py
│   │   ├── education_graph.py
│   ├── services/
│   │   ├── _init_.py
│   │   ├── llm_service.py
│   ├── utils/
│   │   └── state.py
│   └── main.py
├── tests/
└── docs/
```

## Como rodar o Projeto

### Pré-requisitos

- Docker instalado
- Git instalado
- Ollama instalado ([ollama.com](https://ollama.com))

**Passo 1** - Clonar repo
```
git clone <url do repositorio>
cd Fernanda-IA
```

### Passo 2 - Instalar e configurar o Ollama

Instale o modelo:
```bash
ollama pull llama3.1:8b
```

Configure o Ollama para aceitar conexões dos containers Docker
(necessário apenas uma vez na máquina):

```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo -e "[Service]\nEnvironment=\"OLLAMA_HOST=0.0.0.0\"" | sudo tee /etc/systemd/system/ollama.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

> **Windows/Mac:** Este passo não é necessário. O Ollama já aceita conexões externas por padrão.

### Passo 3 - Criar rede Docker compartilhada

> Só é necessário fazer isso **uma vez** na máquina. Se a rede já existir, pule este passo.

```bash
docker network create fernanda-network
```

### Passo 4 - Criar o arquivo `.env` na raiz do projeto

```env
MODEL_NAME=llama3.1:8b
OLLAMA_BASE_URL=http://172.17.0.1:11434
EMBEDDING_MODEL=nomic-embed-text
```

> **Atenção:** O IP `172.17.0.1` é o gateway padrão do Docker no Linux.
> Se mudar de máquina, confirme o IP correto com:
> ```bash
> ip route | grep docker0 | awk '{print $9}'
> ```

### Passo 5 - Subir o container

```bash
docker compose up -d --build
```

### Passo 6 - Verificar se está rodando

```bash
docker ps
# O container fernanda-ai deve estar com status Up

docker logs fernanda-ai
# Deve aparecer: Application startup complete
```
## Arquitetura

### Alto Nível
Em desenvolvimento...

### IA
- agents -> Agentes de IA
- services -> Lógica da LLM e memória
- graph -> define ordem dos agentes
- utils -> helpers

## Diagramas

### Diagrama de caso de uso
Em desenvolvimento...

### Diagrama ER
Em desenvolvimento...
