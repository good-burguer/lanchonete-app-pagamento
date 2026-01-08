# 🍔 Lanchonete – Serviço de Pagamento

Este microsserviço é responsável pelo **processamento e registro de pagamentos** no ecossistema da aplicação *Lanchonete*, desenvolvido como parte do **Tech Challenge – Fase 4 (FIAP SOAT)**.

Ele foi projetado seguindo princípios de **arquitetura limpa**, **microsserviços**, **CI/CD automatizado** e **segurança por design**, utilizando **Python**, **FastAPI** e **MongoDB Atlas (NoSQL)**.

---

## 📌 Responsabilidades do Serviço

- Receber solicitações de pagamento via API REST
- Registrar transações de pagamento
- Atualizar status do pagamento
- Expor endpoint de webhook para eventos externos
- Persistir dados em banco **NoSQL (MongoDB)**

---

## 🧱 Arquitetura

- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **Banco de Dados:** MongoDB Atlas (NoSQL)
- **Arquitetura:** Clean Architecture / Hexagonal
- **Orquestração:** Kubernetes (EKS)
- **CI/CD:** GitHub Actions

### Estrutura de Camadas

```
app/
├── api/              # Rotas FastAPI
├── controllers/      # Controllers (entrada HTTP)
├── use_cases/        # Casos de uso
├── gateways/         # Gateways de persistência
├── entities/         # Entidades de domínio
├── models/           # Modelos de dados
├── infrastructure/  # Infraestrutura (MongoDB)
└── main.py           # Bootstrap da aplicação
```

---

## 🔐 Configuração de Ambiente

O serviço utiliza **variáveis de ambiente** para configuração sensível.

### Variáveis obrigatórias

| Variável | Descrição |
|--------|----------|
| `MONGODB_URI` | String de conexão com o MongoDB Atlas |

> ⚠️ A URI **não deve ser versionada**. Ela é injetada via **Kubernetes Secret** no deploy.

---

## 🚀 Executando Localmente

### Pré-requisitos

- Python 3.12+
- pip
- MongoDB Atlas (ou MongoDB local)

### Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Execução

```bash
uvicorn app.main:app --reload --port 8080
```

---

## 🧪 Testes e Qualidade

O projeto possui **testes unitários e de integração**, incluindo **BDD**.

### Executar testes

```bash
pytest --cov=app
```

### Cobertura

- ✔️ Cobertura mínima exigida: **80%**
- ✔️ Quality Gate configurado no pipeline CI

> Os relatórios de cobertura são gerados automaticamente no pipeline de CI/CD.

---

## 🔄 CI/CD

O pipeline automatizado executa:

1. Instalação de dependências
2. Execução de testes
3. Análise de qualidade
4. Build da imagem Docker
5. Push para ECR
6. Deploy automático no Kubernetes (EKS)

Fluxo controlado por **Pull Request**, com branch `main` protegida.

---

## ☸️ Deploy em Kubernetes

O deploy utiliza manifestos Kubernetes com:

- Deployment
- Service
- Configuração via `Secrets`
- Healthcheck (`/health`)

Exemplo de verificação:

```bash
kubectl -n app get pods
kubectl -n app logs -l app=lanchonete-pagamento
```

---

## ❤️ Health Check

```http
GET /health/
```

Resposta esperada:

```json
{"status": "ok"}
```

---

## 🎯 Contexto Acadêmico

Este serviço foi desenvolvido para atender aos requisitos do **Tech Challenge – Fase 4** da pós-graduação **FIAP – Software Architecture (SOAT)**, contemplando:

- Microsserviços
- CI/CD
- Kubernetes
- Testes automatizados
- Boas práticas de arquitetura

---

## 👤 Autor

**The Code Crafters**  
Pós-Tech FIAP – Software Architecture
