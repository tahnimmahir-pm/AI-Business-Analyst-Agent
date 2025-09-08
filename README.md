# The AI Business Analyst Agent

Michael is an AI-powered Business Analyst agent that understands natural-language business questions, translates them into SQL, executes against a relational database, and returns human-friendly answers, tables, and simple charts. It also stores conversation history for later analysis.

## Features
- Natural language to SQL (NL→SQL) via LLM
- Relational database integration (PostgreSQL by default)
- Human-friendly responses with tabular results and optional charts (base64 PNG)
- Conversation history persistence
- Introspect schema via API
- Docker Compose for local DBs (PostgreSQL + MongoDB for auxiliary examples)

## Tech Stack
- Backend: FastAPI, Uvicorn
- AI: LangChain, LangGraph, Groq LLM (`llama3-70b-8192`)
- DB: PostgreSQL (SQLAlchemy), psycopg2
- Data/Charts: Pandas, Matplotlib
- Infra: Docker Compose (Postgres, Mongo)

## Repository Structure
```
D:\Ai Agent\Al Business Analyst Agent
├── backend\
│   └── main.py                # FastAPI app with /ask, /history, /schema
├── docker-compose-infra.yml   # Postgres + MongoDB for local development
├── requirements.txt           # Python dependencies
├── sql\
│   └── init.sql               # Relational schema (customers, products, sales, conversations)
├── seed\
│   └── seed.sql               # Sample dataset for the relational schema
├── insert_data_pgsql.py       # Alternative Python seeding for Postgres
├── insert_data_mongo.py       # MongoDB example data (optional)
├── agent_with_postgres.ipynb  # Notebook: NL→SQL over Postgres (reference)
├── agent_with_mongodb.ipynb   # Notebook: NL→Aggregation over Mongo (reference)
└── README.md                  # This file
```

## System Architecture & Workflow
- User sends a business question to the backend (`/ask`).
- LLM generates a SQL query using the schema context and prompt.
- Backend executes SQL on PostgreSQL and collects results.
- Backend formats a concise human-friendly answer; optionally generates a chart for time-series/numeric results.
- Backend stores `question`, `generated_sql`, and `answer_text` in `conversations`.

Mermaid (high-level):
```mermaid
flowchart LR
  U[User] -->|Question| API[/FastAPI /ask/]
  API -->|Prompt| LLM[Groq LLM]
  LLM -->|SQL| API
  API -->|Execute| DB[(PostgreSQL)]
  DB -->|Rows| API
  API -->|Answer + Table + Chart| U
  API -->|Persist| Store[(conversations)]
```

## Database Schema (PostgreSQL)
Tables created by `sql/init.sql`:
- customers(customer_id, name, email, created_at)
- products(product_id, product_name, description)
- sales(order_id, product_id, customer_id, quantity, unit_price, order_date)
- conversations(id, question, generated_sql, answer_text, created_at)

Key relations:
- `sales.product_id` → `products.product_id`
- `sales.customer_id` → `customers.customer_id`

## Sample Dataset
`seed/seed.sql` inserts realistic sample rows into `customers`, `products`, and `sales`. You can also use `insert_data_pgsql.py` to seed via Python.

## Getting Started

### Prerequisites
- Windows with Docker Desktop running
- Python 3.10+ in PATH
- PowerShell

### 1) Start databases
```powershell
cd "D:\Ai Agent\Al Business Analyst Agent"
docker compose -f docker-compose-infra.yml up -d
```

### 2) Create and activate Python virtual environment
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Install dependencies
```powershell
pip install -U pip
pip install -r requirements.txt
```

### 4) Configure environment variables
Set in the current shell before running the API:
```powershell
$env:GROQ_API_KEY = "YOUR_GROQ_API_KEY"
$env:POSTGRES_URI = "postgresql://postgres:password@localhost:5433/ecommerce"
```

### 5) Initialize schema and seed data (PostgreSQL)
Option A: Use psql
```powershell
psql -U postgres -h localhost -p 5433 -d ecommerce
```
In psql:
```
\i 'D:/Ai Agent/Al Business Analyst Agent/sql/init.sql'
\i 'D:/Ai Agent/Al Business Analyst Agent/seed/seed.sql'
\q
```

Option B: Seed via Python
```powershell
python insert_data_pgsql.py
```

### 6) Run the API server
```powershell
uvicorn backend.main:app --reload
```
- Open API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/`

## Usage
### Ask a question (PowerShell)
```powershell
Invoke-RestMethod -Method POST `
  -Uri http://127.0.0.1:8000/ask `
  -ContentType "application/json" `
  -Body (@{ question = "What were the top 5 products sold last month?"; want_chart = $true } | ConvertTo-Json)
```

### View history
```powershell
Invoke-RestMethod http://127.0.0.1:8000/history
```

### Inspect schema
```powershell
Invoke-RestMethod http://127.0.0.1:8000/schema
```

## API Endpoints
- `GET /` — health
- `POST /ask` — body: `{ question: string, want_chart?: boolean }`; returns `{ answer, table, chart_png_base64, generated_sql }`
- `GET /history` — recent conversations
- `GET /schema` — table/column metadata (from `information_schema.columns`)

## Notebooks (Reference)
- `agent_with_postgres.ipynb`: demonstrates LangChain+LangGraph NL→SQL against PostgreSQL.
- `agent_with_mongodb.ipynb`: demonstrates a pipeline approach over MongoDB (optional for this project).

## Troubleshooting
- 400 on `/ask`: Ensure `$env:GROQ_API_KEY` is set in your shell.
- DB connection errors: Check Docker is running and ports match compose (Postgres at 5433).
- No data: Re-run schema and seed steps (5).

## Security Notes
- Do not commit real API keys. Use environment variables.
- SQL is LLM-generated; in production, apply schema guards, allowlists, or a SQL validator.

## Roadmap
- Richer charting and visualization selection
- Semantic caching of questions/answers
- Recommendation engine for inventory/pricing suggestions

## License
MIT (or your preferred license)
