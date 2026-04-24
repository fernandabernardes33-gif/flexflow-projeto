# AUssistencia — Documentação do Sistema
**Versão:** 1.0.0  
**Data:** Abril 2026  
**Desenvolvido por:** Fernanda Bernardes  

---

## 1. Visão Geral

O **AUssistencia** é um sistema de gestão para assistência técnica de informática. Permite controlar clientes, ordens de serviço, orçamentos, estoque de produtos, serviços, financeiro e lembretes — tudo em uma única plataforma web.

---

## 2. Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.11 | Linguagem principal |
| FastAPI | 0.110+ | Framework de API REST |
| SQLAlchemy | 2.x | ORM (mapeamento banco de dados) |
| SQLite | — | Banco de dados local |
| python-jose | — | Geração e validação de tokens JWT |
| passlib (sha256_crypt) | — | Criptografia de senhas |
| ReportLab | — | Geração de PDFs |
| pandas + openpyxl | — | Exportação de Excel |
| python-dotenv | — | Variáveis de ambiente |

### Frontend
| Tecnologia | Versão | Função |
|---|---|---|
| React | 18 | Interface do usuário |
| Vite | — | Bundler e servidor de desenvolvimento |
| Tailwind CSS | — | Estilização |
| Axios | — | Requisições HTTP |
| React Router | — | Navegação entre páginas |
| Lucide React | — | Ícones |

---

## 3. Estrutura de Pastas

```
aussistencia/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Configurações gerais
│   │   │   └── security.py        # Criptografia e JWT
│   │   ├── models/                # Tabelas do banco de dados
│   │   │   ├── usuario.py
│   │   │   ├── cliente.py
│   │   │   ├── produto.py
│   │   │   ├── servico.py
│   │   │   ├── ordem_servico.py
│   │   │   ├── item_os.py
│   │   │   ├── orcamento.py
│   │   │   ├── item_orcamento.py
│   │   │   ├── movimentacao_estoque.py
│   │   │   ├── movimentacao_financeira.py
│   │   │   └── lembrete.py
│   │   ├── routers/               # Endpoints da API
│   │   │   ├── auth.py
│   │   │   ├── clientes.py
│   │   │   ├── produtos.py
│   │   │   ├── estoque.py
│   │   │   ├── servicos.py
│   │   │   ├── ordens_servico.py
│   │   │   ├── orcamentos.py
│   │   │   ├── financeiro.py
│   │   │   ├── lembretes.py
│   │   │   └── painel.py
│   │   ├── schemas/               # Validação de dados (Pydantic)
│   │   ├── services/
│   │   │   └── exportacao.py      # Excel com conformidade LGPD
│   │   ├── utils/
│   │   │   └── gerar_pdf.py       # Geração de PDFs
│   │   ├── database.py            # Conexão com banco de dados
│   │   ├── dependencies.py        # Autenticação via JWT
│   │   └── main.py                # Ponto de entrada da aplicação
│   ├── seed.py                    # Dados iniciais de teste
│   ├── criar_usuario.py           # Script para criar usuários
│   ├── requirements.txt
│   └── .env                       # Variáveis de ambiente (não enviar ao GitHub)
├── frontend/
│   ├── src/
│   │   ├── pages/                 # Páginas da aplicação
│   │   │   ├── Login.jsx
│   │   │   ├── Painel.jsx
│   │   │   ├── Clientes.jsx
│   │   │   ├── ClienteDetalhe.jsx
│   │   │   ├── Produtos.jsx
│   │   │   ├── Estoque.jsx
│   │   │   ├── Servicos.jsx
│   │   │   ├── OrdensServico.jsx
│   │   │   ├── OrdemServicoDetalhe.jsx
│   │   │   ├── OrdemServicoNova.jsx
│   │   │   ├── Orcamentos.jsx
│   │   │   ├── OrcamentoDetalhe.jsx
│   │   │   ├── OrcamentoNovo.jsx
│   │   │   ├── Financeiro.jsx
│   │   │   └── Lembretes.jsx
│   │   ├── components/            # Componentes reutilizáveis
│   │   ├── context/               # Contexto de autenticação
│   │   ├── services/
│   │   │   └── api.js             # Configuração do Axios + interceptadores
│   │   └── main.jsx
│   └── package.json
├── iniciar.bat                    # Inicia backend + frontend com um clique
└── setup.bat                      # Instala dependências (primeira vez)
```

---

## 4. Instalação e Execução

### Primeira vez (setup)
1. Ter instalado: **Python 3.11**, **Node.js 18+**
2. Dar duplo clique em `setup.bat`
3. Aguardar instalação das dependências

### Execução diária
Dar duplo clique em `iniciar.bat`

O sistema abre automaticamente em `http://localhost:5173`

### Manual (CMD)
**Backend:**
```
cd aussistencia\backend
venv\Scripts\activate
uvicorn app.main:app --port 8000 --reload
```

**Frontend:**
```
cd aussistencia\frontend
npm run dev
```

---

## 5. Acesso ao Sistema

| Campo | Valor |
|---|---|
| URL | http://localhost:5173 |
| Email padrão | admin@aussistencia.com |
| Senha padrão | admin123 |

Para criar novos usuários, rodar dentro de `backend\`:
```
python criar_usuario.py
```

---

## 6. Funcionalidades

### Painel (Dashboard)
- Resumo de ordens abertas, receita do mês, produtos com baixo estoque e lembretes do dia

### Clientes
- Cadastro, edição e remoção de clientes
- Visualização de histórico de ordens por cliente
- Exportação em Excel (com CPF mascarado — LGPD)

### Produtos e Estoque
- Cadastro de produtos com controle de quantidade
- Registro de entradas e saídas de estoque
- Alerta de baixo estoque no painel

### Serviços
- Cadastro de tipos de serviço com preço padrão

### Ordens de Serviço
- Criação com seleção de cliente, problema, itens (produtos/serviços)
- Status: ABERTA → EM_ANDAMENTO → CONCLUIDA / CANCELADA
- Exportação em PDF com rodapé LGPD
- Exportação da lista em Excel

### Orçamentos
- Criação de orçamentos vinculados a clientes
- Status: PENDENTE → APROVADO / RECUSADO
- Exportação em PDF com rodapé LGPD

### Financeiro
- Registro de receitas e despesas
- Filtro por período
- Exportação em Excel

### Lembretes
- Criação de lembretes com data e descrição
- Exibição no painel do dia

---

## 7. API — Endpoints Principais

**Base URL:** `http://localhost:8000`

### Autenticação
| Método | Rota | Descrição |
|---|---|---|
| POST | /auth/login | Login, retorna JWT |

### Clientes
| Método | Rota | Descrição |
|---|---|---|
| GET | /clientes | Lista todos |
| POST | /clientes | Cria novo |
| GET | /clientes/{id} | Busca por ID |
| PUT | /clientes/{id} | Atualiza |
| DELETE | /clientes/{id} | Remove |
| GET | /clientes/exportar/excel | Exporta Excel |

### Ordens de Serviço
| Método | Rota | Descrição |
|---|---|---|
| GET | /ordens-servico | Lista todas |
| POST | /ordens-servico | Cria nova |
| GET | /ordens-servico/{id} | Busca por ID |
| PUT | /ordens-servico/{id} | Atualiza status |
| GET | /ordens-servico/{id}/pdf | Gera PDF |
| GET | /ordens-servico/exportar/excel | Exporta Excel |

### Orçamentos
| Método | Rota | Descrição |
|---|---|---|
| GET | /orcamentos | Lista todos |
| POST | /orcamentos | Cria novo |
| GET | /orcamentos/{id} | Busca por ID |
| PUT | /orcamentos/{id} | Atualiza status |
| GET | /orcamentos/{id}/pdf | Gera PDF |

*Todos os endpoints (exceto login) exigem token JWT no header:*  
`Authorization: Bearer <token>`

---

## 8. Banco de Dados

**Tipo:** SQLite (arquivo local)  
**Localização:** `backend/aussistencia.db`

Para visualizar o banco de dados:
- Instalar **DB Browser for SQLite** (gratuito em sqlitebrowser.org)
- Abrir o arquivo `aussistencia.db`

### Tabelas principais
| Tabela | Descrição |
|---|---|
| usuarios | Usuários do sistema |
| clientes | Clientes da assistência |
| produtos | Produtos em estoque |
| servicos | Tipos de serviço |
| ordens_servico | Ordens de serviço |
| itens_os | Itens de cada OS |
| orcamentos | Orçamentos emitidos |
| itens_orcamento | Itens de cada orçamento |
| movimentacoes_estoque | Entradas e saídas de estoque |
| movimentacoes_financeiras | Receitas e despesas |
| lembretes | Lembretes do sistema |

---

## 9. Conformidade LGPD

O sistema foi desenvolvido seguindo princípios da **Lei Geral de Proteção de Dados (Lei nº 13.709/2018)**:

- **CPF mascarado** nas exportações Excel (exibe apenas últimos 2 dígitos)
- **Dados mínimos** nos PDFs (apenas nome e telefone do cliente)
- **Rodapé legal** em todos os PDFs informando sobre proteção de dados
- **Logs sem dados pessoais** (nível WARNING no servidor)
- **CORS restrito** apenas às origens do frontend

---

## 10. Variáveis de Ambiente

Arquivo `.env` em `backend/`:

```
DATABASE_URL=sqlite:///./aussistencia.db
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

> **Importante:** O arquivo `.env` não deve ser enviado ao GitHub (já está no `.gitignore`)

---

## 11. Repositório

GitHub: https://github.com/fernandabernardes33-gif/flexflow-projeto
