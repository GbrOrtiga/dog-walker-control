# 🐾 Dog Walker Control - Interface Web

Guia de instalação e uso da nova interface web do Dog Walker Control.

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação Rápida

### 1. Clone ou acesse a pasta do projeto

```bash
cd dog-walker-control
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🌐 Executando a Interface Web

```bash
python -m src.web
```

A aplicação estará disponível em **http://localhost:5000**

## 🎯 Funcionalidades da Interface Web

### 📊 Dashboard
- Visualizar o total a receber no mês
- Ver resumo de passeios e donos
- Preview da semana com próximos passeios

### ➕ Registrar Passeio
- Interface intuitiva para registrar novos passeios
- Seleção visual dos dias da semana
- Cálculo em tempo real do valor estimado
- Validação automática de dados

### 📋 Listar Passeios
- Tabela completa com todos os passeios
- Mostre todas as informações relevantes
- Opção de remover registros

### 📅 Agenda da Semana
- Visualize os passeios organizados por dia
- Veja o total de passeios e valor por dia
- Interface limpa e responsiva

### 🔍 Buscar por Dono
- Procure passeios de um dono específico
- Veja o total que esse dono deve pagar
- Busca em tempo real

## 🏃 Interface CLI (Original)

A interface CLI original ainda funciona normalmente:

```bash
python -m src.main
```

## 📚 Estrutura de Pastas

```
dog-walker-control/
├── src/
│   ├── core.py              # Lógica de negócio
│   ├── main.py              # Interface CLI
│   ├── web.py               # Servidor Flask
│   ├── templates/
│   │   └── index.html       # Interface web
│   └── static/
│       ├── css/
│       │   └── style.css    # Estilos
│       └── js/
│           └── app.js       # Lógica frontend
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── data.json                # Armazenamento de dados
├── requirements.txt         # Dependências
└── README.md
```

## 🛠️ API REST

A aplicação expõe os seguintes endpoints:

### GET `/api/walks`
Lista todos os passeios

**Response:**
```json
{
  "success": true,
  "data": [...]
}
```

### POST `/api/walks`
Registra um novo passeio

**Body:**
```json
{
  "dog_name": "Rex",
  "owner_name": "João",
  "walks_per_day": 1,
  "days_of_week": ["Segunda-feira", "Quarta-feira"],
  "phone": "(11) 9999-9999"
}
```

### DELETE `/api/walks/<dog_name>`
Remove um passeio

### GET `/api/total`
Retorna o total a receber no mês

### GET `/api/owner/<owner_name>`
Busca passeios por dono

### GET `/api/schedule`
Retorna passeios agrupados por dia da semana

### GET `/api/config`
Retorna configurações (dias, preço por passeio, etc)

## 📱 Responsividade

A interface web é totalmente responsiva e funciona em:
- Desktop (1920px+)
- Tablet (768px - 1024px)
- Mobile (até 480px)

## 🎨 Tecnologias Utilizadas

- **Backend:** Python + Flask
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Persistência:** JSON (mesmo arquivo `data.json`)
- **Design:** Moderno, com gradientes e animações suaves

## ⚙️ Configurações

### Preço por Passeio
Modificar em `src/core.py`:
```python
PRICE_PER_WALK = 25.0  # em Reais
```

### Máximo de Dias
Modificar em `src/core.py`:
```python
MAX_DAYS = 5  # máximo de dias por passeio
```

## 🔄 Sincronização de Dados

A interface web e a CLI compartilham o mesmo arquivo de dados (`data.json`). Qualquer mudança feita em uma interface é imediatamente refletida na outra.

## 🐛 Troubleshooting

### Porta 5000 já está em uso
```bash
# Use uma porta diferente
flask run --port 5001
```

### Erro ao importar Flask
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

### Dados não carregam
Verifique se `data.json` existe e está no diretório raiz do projeto.

## 📝 Notas

- A aplicação gera automaticamente `data.json` na primeira execução
- Todos os dados são salvos em tempo real
- Não há autenticação (use em rede segura)
- Para uso em produção, configure um servidor WSGI como Gunicorn

## 🚀 Deploy em Produção

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.web:app"
```

## 📧 Autor

Gabriel Ortiga Vassallo Fernández

## 📄 Licença

Projeto acadêmico - RA 22503789
