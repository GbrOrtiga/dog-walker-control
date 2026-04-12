# 🐾 Dog Walker Control

![CI](https://github.com/SEU_USUARIO/dog-walker-control/actions/workflows/ci.yml/badge.svg)

## Descrição do Problema

Passeadores de cachorros autônomos frequentemente enfrentam dificuldades para controlar quantos passeios realizaram para cada cliente e calcular o valor total a receber no final do mês. O controle feito no papel ou em planilhas genéricas é suscetível a erros e perda de informações.

## Proposta da Solução

O **Dog Walker Control** é uma aplicação de linha de comando (CLI) em Python que permite ao passeador registrar os passeios realizados por cachorro, consultar o histórico e calcular automaticamente o total a receber no mês.

## Público-alvo

Passeadores de cachorros autônomos e pequenos prestadores de serviços pet que precisam de um controle simples e confiável.

## Funcionalidades Principais

- Registrar passeios informando nome do cachorro, dono e quantidade
- Listar todos os registros do mês em formato tabular
- Calcular o valor total a receber no mês
- Buscar registros pelo nome do dono
- Remover registros

## Tecnologias Utilizadas

- Python 3.12
- pytest (testes automatizados)
- ruff (linting / análise estática)
- GitHub Actions (CI)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/dog-walker-control.git
cd dog-walker-control

# (Opcional) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Execução

```bash
python -m src.main
```

## Rodando os Testes

```bash
pytest tests/ -v
```

## Rodando o Lint

```bash
ruff check src/ tests/
```

## Versão Atual

`1.0.0`

## Autor

Seu Nome Completo

## Repositório

[https://github.com/SEU_USUARIO/dog-walker-control](https://github.com/SEU_USUARIO/dog-walker-control)