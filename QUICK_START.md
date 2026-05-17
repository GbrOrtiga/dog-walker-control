# 🐾 Dog Walker Control - Guia Rápido da Interface Web

## 🚀 Começar em 3 Passos

### 1️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Inicie o servidor

```bash
python -m src.web
```

### 3️⃣ Acesse no navegador

Abra seu navegador em **http://localhost:5000**

---

## 📋 O que a Interface Web Oferece?

### ✨ Características

| Funcionalidade | CLI | Web |
|---|---|---|
| Registrar passeios | ✅ | ✅ |
| Listar passeios | ✅ | ✅ (tabela interativa) |
| Ver total do mês | ✅ | ✅ (dashboard) |
| Buscar por dono | ✅ | ✅ (em tempo real) |
| Ver agenda semanal | ✅ | ✅ (preview visual) |
| Remover registros | ✅ | ✅ (com 1 clique) |
| Responsividade | ❌ | ✅ (desktop/tablet/mobile) |

---

## 🎯 Funcionalidades da Interface Web

### 📊 **Dashboard**
- Total a receber no mês
- Informações rápidas (donos, cães)
- Preview dos próximos passeios

### ➕ **Registrar Passeio**
- Formulário intuitivo com validação
- Seleção visual de dias (até 5)
- Cálculo em tempo real do valor
- Feedback visual após registro

### 📋 **Listar Passeios**
- Tabela completa com todos os dados
- Removedor de registros rápido
- Formatação automática de valores

### 📅 **Agenda da Semana**
- Passeios organizados por dia
- Total de passeios e valor por dia
- Layout limpo e legível

### 🔍 **Buscar por Dono**
- Busca em tempo real
- Resume todos os cães do dono
- Calcula total que o dono deve pagar

---

## 🎨 Design

- **Moderno** com gradientes e animações suaves
- **Responsivo** funciona em qualquer dispositivo
- **Intuitivo** interface clara e fácil de usar
- **Rápido** sem carregamentos desnecessários

---

## 📚 Estrutura de Dados

Os dados continuam sendo salvos em **`data.json`** no formato:

```json
{
  "dog_name": "Rex",
  "owner_name": "João",
  "phone": "(11) 9999-9999",
  "walks_per_day": 1,
  "days_of_week": ["Segunda-feira", "Quarta-feira"],
  "total_walks": 2,
  "total": 50.0,
  "date": "2026-05-17"
}
```

---

## 🔄 Sincronização CLI ↔️ Web

A interface web e a CLI compartilham **o mesmo arquivo de dados**. Você pode:

- ✅ Registrar no web e consultar no CLI
- ✅ Registrar no CLI e ver atualizado no web
- ✅ Usar ambas simultaneamente

---

## ⚙️ Configurações

### Mudar Preço por Passeio
Editar em [src/core.py](src/core.py):
```python
PRICE_PER_WALK = 25.0  # seu preço em reais
```

### Mudar Máximo de Dias
Editar em [src/core.py](src/core.py):
```python
MAX_DAYS = 5  # máximo de dias
```

---

## 🐛 Troubleshooting

**Erro: "Port 5000 already in use"?**
```bash
# Use outra porta
flask run --port 5001
```

**Dados não aparecem?**
- Verifique se `data.json` existe no diretório raiz
- Reinicie o servidor

**Página em branco?**
- Abra o DevTools (F12) e procure por erros
- Verifique se os arquivos CSS/JS foram carregados

---

## 📸 Screenshots

### Dashboard
- Total do mês destacado em verde
- Informações rápidas em cards
- Preview da semana com todos os passeios

### Registrar Passeio
- Formulário com 2 colunas
- Seleção visual de dias com checkboxes
- Cálculo do preço em tempo real

### Listar Passeios
- Tabela completa com todos os dados
- Botão de remover para cada passeio
- Responsivo em mobile

### Buscar
- Entrada de texto com botão buscar
- Resultados com detalhes do cachorro
- Total que o dono deve pagar

---

## 🔗 Endpoints da API

```
GET  /api/walks              # Listar todos
POST /api/walks              # Registrar novo
DELETE /api/walks/<dog_name> # Remover
GET  /api/total              # Total do mês
GET  /api/owner/<name>       # Buscar por dono
GET  /api/schedule           # Agenda por dia
GET  /api/config             # Configurações
```

---

## 📝 Notas

- A aplicação roda em modo **desenvolvimento** por padrão (com debug)
- Para produção, use um WSGI server como **Gunicorn**
- **Sem autenticação** - use em rede segura
- Dados em **JSON local** - perfeito para uso pessoal

---

## 🚀 Próximas Melhorias Possíveis

- [ ] Autenticação de usuários
- [ ] Múltiplos passeadores
- [ ] Gráficos de receita
- [ ] Exportar para PDF/Excel
- [ ] Notificações de passeios
- [ ] Integração com WhatsApp
- [ ] App mobile (React Native/Flutter)
- [ ] Backup automático na nuvem

---

## 💡 Tips

- Acesse [WEB_README.md](WEB_README.md) para documentação completa
- Use a CLI em paralelo para testes: `python -m src.main`
- A interface auto-atualiza após cada ação
- Todos os erros mostram mensagens amigáveis

---

**Boa sorte com seu negócio de passeios de cães! 🐕**
