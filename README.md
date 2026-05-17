# 🐾 Dog Walker Control
Sou o Gabriel Ortiga RA 22503789, estou montando uma "Gerenciado de Passeios" em Python para facilitar o meu dia a dia e meu controle sobre os passeios ao mesmo tempo fazendo isso como um projeto real para da faculdade resolvendo um problema real meu 

# Link do Deploy
https://gbrortiga.github.io/dog-walker-control/

## Descrição do Problema

Nós passeadores de cachorros autônomos frequentemente enfrentam dificuldades para controlar quantos passeios realizaram para cada cliente e calcular o valor total a receber no final do mês
O controle feito no papel ou em planilhas genéricas e é bem provável que erros aconteçam

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

- Python 3.14.4
- pytest (testes automatizados)
- ruff (linting / análise estática)
- GitHub Actions (CI)

## Exemplos de Uso

(.venv) PS C:\Users\Denise Ortiga\Downloads\dog-walker-control> python -m src.main

=============================================
       🐾  DOG WALKER CONTROL  🐾
=============================================
📂 Dados carregados do histórico salvo.

[1] Registrar passeio
[2] Listar todos os passeios
[3] Ver total a receber no mês
[4] Buscar por dono
[5] Remover registro
[6] Ver agenda da semana
[0] Sair
---------------------------------------------
Escolha uma opção: 1
Nome do cachorro: Arceus
Nome do dono: Cecilia
Telefone do dono (Enter para pular): 
Passeios por dia: 1

Dias selecionados (0/5): nenhum

  [1] [ ] Segunda-feira
  [2] [ ] Terça-feira
  [3] [ ] Quarta-feira
  [4] [ ] Quinta-feira
  [5] [ ] Sexta-feira
  [6] [ ] Sábado
  [7] [ ] Domingo

  [0] Confirmar seleção
  (selecione até 5 dias, digite o número para marcar/desmarcar)

Opção: 1
  ✓ 'Segunda-feira' selecionado.

Dias selecionados (1/5): Segunda-feira

  [1] [✓] Segunda-feira
  [2] [ ] Terça-feira
  [3] [ ] Quarta-feira
  [4] [ ] Quinta-feira
  [5] [ ] Sexta-feira
  [6] [ ] Sábado
  [7] [ ] Domingo

  [0] Confirmar seleção
  (selecione até 5 dias, digite o número para marcar/desmarcar)

Opção: 2
  ✓ 'Terça-feira' selecionado.

Dias selecionados (2/5): Segunda-feira, Terça-feira

  [1] [✓] Segunda-feira
  [2] [✓] Terça-feira
  [3] [ ] Quarta-feira
  [4] [ ] Quinta-feira
  [5] [ ] Sexta-feira
  [6] [ ] Sábado
  [7] [ ] Domingo

  [0] Confirmar seleção
  (selecione até 5 dias, digite o número para marcar/desmarcar)

Opção: 4
  ✓ 'Quinta-feira' selecionado.

Dias selecionados (3/5): Segunda-feira, Terça-feira, Quinta-feira

  [1] [✓] Segunda-feira
  [2] [✓] Terça-feira
  [3] [ ] Quarta-feira
  [4] [✓] Quinta-feira
  [5] [ ] Sexta-feira
  [6] [ ] Sábado
  [7] [ ] Domingo

  [0] Confirmar seleção
  (selecione até 5 dias, digite o número para marcar/desmarcar)

Opção: 5
  ✓ 'Sexta-feira' selecionado.

Dias selecionados (4/5): Segunda-feira, Terça-feira, Quinta-feira, Sexta-feira

  [1] [✓] Segunda-feira
  [2] [✓] Terça-feira
  [3] [ ] Quarta-feira
  [4] [✓] Quinta-feira
  [5] [✓] Sexta-feira
  [6] [ ] Sábado
  [7] [ ] Domingo

  [0] Confirmar seleção
  (selecione até 5 dias, digite o número para marcar/desmarcar)

Opção: 0

✅ Registrado! Arceus — Seg / Ter / Qui / Sex — 4 passeio(s)/semana — R$ 100.00

[1] Registrar passeio
[2] Listar todos os passeios
[3] Ver total a receber no mês
[4] Buscar por dono
[5] Remover registro
[6] Ver agenda da semana
[0] Sair
---------------------------------------------
Escolha uma opção: 6

📅  Segunda-feira  (4 passeio(s) — R$ 100.00)
    ----------------------------------------------------
    🐕 Sacy e Percy    Dono: Patrícia        Tel: sem telefone
    🐕 Zeus            Dono: Carla           Tel: sem telefone
    🐕 Dora e Nola     Dono: Rafaela         Tel: sem telefone
    🐕 Arceus          Dono: Cecilia         Tel: sem telefone

📅  Terça-feira  (2 passeio(s) — R$ 50.00)
    ----------------------------------------------------
    🐕 Zeus            Dono: Carla           Tel: sem telefone
    🐕 Arceus          Dono: Cecilia         Tel: sem telefone

📅  Quarta-feira  (2 passeio(s) — R$ 50.00)
    ----------------------------------------------------
    🐕 Sacy e Percy    Dono: Patrícia        Tel: sem telefone
    🐕 Dora e Nola     Dono: Rafaela         Tel: sem telefone

📅  Quinta-feira  (2 passeio(s) — R$ 50.00)
    ----------------------------------------------------
    🐕 Zeus            Dono: Carla           Tel: sem telefone
    🐕 Arceus          Dono: Cecilia         Tel: sem telefone

📅  Sexta-feira  (4 passeio(s) — R$ 100.00)
    ----------------------------------------------------
    🐕 Sacy e Percy    Dono: Patrícia        Tel: sem telefone
    🐕 Zeus            Dono: Carla           Tel: sem telefone
    🐕 Dora e Nola     Dono: Rafaela         Tel: sem telefone
    🐕 Arceus          Dono: Cecilia         Tel: sem telefone


## Instalação

```bash
# Clone o repositório
git clone https://github.com/GbrOrtiga/dog-walker-control.git
cd dog-walker-control

# (Opcional) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Execução

### Interface CLI
```bash
python -m src.main
```

### Interface Web local
```bash
python -m src.web
```

Depois acesse:
```bash
http://localhost:5000
```

### GitHub Pages / Live Server
Se estiver usando GitHub Pages ou Live Server, abra o arquivo `index.html` na raiz do projeto.

## Rodando os Testes

```bash
pytest tests/ -v
```

## Rodando o Lint

```bash
ruff check src/ tests/
```

## Versão Atual

`3.2.2`

## Autor

Gabriel Ortiga Vassallo Fernández

## Repositório

[https://github.com/GbrOrtiga/dog-walker-control](https://github.com/GbrOrtiga/dog-walker-control