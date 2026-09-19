# StockFlow

Sistema web de controle de estoque desenvolvido em Python com Flask, SQLAlchemy e SQLite, com autenticação de usuários, controle de acesso por perfil, registro de produtos, movimentações de entrada e saída e alertas de estoque mínimo.

O projeto foi desenvolvido com foco em organização de código, separação de responsabilidades, validação das regras de negócio e integridade dos dados.

---

## Sobre o projeto

O **StockFlow** é uma aplicação web para controle de estoque, desenvolvida para centralizar o cadastro de produtos e o acompanhamento das movimentações realizadas no estoque.

A aplicação permite registrar entradas e saídas de produtos, consultar o estoque atual, identificar produtos abaixo do estoque mínimo e controlar o acesso às funcionalidades de acordo com o perfil do usuário.

Além das funcionalidades operacionais, o projeto foi estruturado com uma camada de serviços responsável pelas regras de negócio, modelos para representação dos dados, rotas para integração com a interface e uma suíte de testes automatizados.

---

## Objetivo

Desenvolver uma aplicação de controle de estoque que permita:

* Controlar produtos e seus respectivos estoques;
* Registrar movimentações de entrada e saída;
* Evitar saídas que resultem em estoque negativo;
* Identificar produtos abaixo do estoque mínimo;
* Controlar o acesso por perfil de usuário;
* Proteger as senhas por meio de hash;
* Manter o histórico das movimentações realizadas;
* Garantir integridade entre usuários, produtos e movimentações;
* Validar as principais regras de negócio de forma automatizada.

---

## Funcionalidades

### Autenticação

* Login de usuários;
* Validação de usuário e senha;
* Verificação de usuário ativo;
* Controle de sessão;
* Logout;
* Senhas armazenadas utilizando hash;
* Bloqueio de acesso a usuários inativos.

### Controle de usuários

Disponível exclusivamente para usuários com perfil **ADMIN**.

* Cadastro de usuários;
* Edição de usuários;
* Alteração de nome e username;
* Alteração de perfil;
* Ativação e inativação de usuários;
* Controle de usuários ADMIN e COMUM;
* Proteção contra a inativação do último administrador ativo;
* Impedimento de um usuário inativar a própria conta.

### Controle de produtos

* Cadastro de produtos;
* Edição de produtos;
* Ativação e inativação;
* Código de produto único;
* Controle de quantidade atual;
* Definição de estoque mínimo;
* Cadastro de preço;
* Cadastro de categoria e descrição;
* Validação de valores não negativos.

A quantidade atual do estoque não pode ser alterada diretamente na edição do produto. As alterações de estoque são realizadas exclusivamente por meio de movimentações.

### Movimentações

* Registro de entradas;
* Registro de saídas;
* Registro da quantidade movimentada;
* Registro do produto;
* Registro do usuário responsável;
* Registro de observações;
* Histórico de movimentações;
* Bloqueio de movimentações para produtos inativos;
* Bloqueio de quantidades iguais ou inferiores a zero;
* Bloqueio de saídas que deixariam o estoque negativo.

### Dashboard

O painel inicial apresenta uma visão resumida do estoque, incluindo:

* Quantidade de produtos;
* Quantidade de produtos abaixo do estoque mínimo;
* Quantidade de movimentações;
* Quantidade de usuários;
* Alertas de estoque baixo;
* Movimentações recentes.

---

## Perfis de acesso

O StockFlow utiliza dois perfis de usuário:

| Perfil    | Permissões                                             |
| --------- | ------------------------------------------------------ |
| **ADMIN** | Gerenciar usuários, produtos e movimentações           |
| **COMUM** | Consultar produtos e realizar movimentações de estoque |

O controle de autorização é realizado no backend, considerando o estado atual do usuário no banco de dados.

---

## Regras de negócio

Entre as principais regras implementadas estão:

1. O nome, username e senha são obrigatórios no cadastro de usuários.
2. O username deve ser único.
3. As senhas não são armazenadas em texto puro.
4. O perfil do usuário deve ser `ADMIN` ou `COMUM`.
5. Apenas usuários ADMIN podem gerenciar usuários.
6. Usuários inativos não podem realizar login.
7. O sistema deve manter pelo menos um ADMIN ativo.
8. O último ADMIN ativo não pode ser inativado.
9. Um usuário não pode inativar a própria conta.
10. Um ADMIN pode ser rebaixado para COMUM somente quando existir outro ADMIN ativo.
11. O código do produto deve ser único.
12. A quantidade atual do estoque não pode ser editada diretamente no cadastro do produto.
13. A quantidade inicial e o estoque mínimo não podem ser negativos.
14. O preço não pode ser negativo.
15. A quantidade de uma movimentação deve ser maior que zero.
16. Produtos inativos não podem receber movimentações.
17. Uma saída não pode resultar em estoque negativo.
18. Toda movimentação deve estar vinculada a um produto e a um usuário.
19. O tipo de movimentação deve ser `ENTRADA` ou `SAIDA`.
20. O alerta de estoque baixo ocorre quando a quantidade atual é menor que o estoque mínimo.
21. Usuários e produtos são inativados logicamente, preservando seus registros no banco de dados.
22. O SQLite utiliza Foreign Keys para garantir a integridade referencial.

---

## Arquitetura

O projeto utiliza uma organização baseada na separação de responsabilidades:

```text
Routes
  ↓
Services
  ↓
Models
  ↓
Database
```

### Routes

Responsáveis pelo recebimento das requisições, navegação entre páginas e integração entre a interface e a camada de serviços.

### Services

Concentram as regras de negócio da aplicação, como:

* validações;
* criação e edição de registros;
* ativação e inativação;
* controle das movimentações;
* atualização do estoque;
* aplicação das regras relacionadas aos perfis de usuário.

### Models

Representam as entidades persistidas no banco de dados:

* `Usuario`
* `Produto`
* `Movimentacao`

### Templates

A interface utiliza HTML com Jinja2, com um template base compartilhado entre as páginas para manter consistência visual e evitar duplicação de estrutura.

### Static

Contém os arquivos de apresentação da aplicação, atualmente com uma folha de estilos CSS centralizada.

---

## Modelo de dados

O banco de dados é composto pelas seguintes entidades principais:

### Usuario

Representa os usuários do sistema.

Principais atributos:

* `id`
* `nome`
* `username`
* `senha_hash`
* `perfil`
* `ativo`
* `criado_em`

### Produto

Representa os produtos controlados pelo estoque.

Principais atributos:

* `id`
* `codigo`
* `nome`
* `descricao`
* `categoria`
* `quantidade_atual`
* `estoque_minimo`
* `preco`
* `ativo`
* `criado_em`

### Movimentacao

Registra as alterações realizadas no estoque.

Principais atributos:

* `id`
* `produto_id`
* `usuario_id`
* `tipo`
* `quantidade`
* `observacao`
* `realizado_em`

### Relacionamentos

```text
Usuario
   │
   │ 1:N
   ▼
Movimentacao
   ▲
   │ N:1
   │
Produto
```

Um usuário pode realizar várias movimentações.

Um produto pode possuir várias movimentações.

Cada movimentação pertence a um único usuário e a um único produto.

---

## Segurança e integridade

O projeto possui algumas medidas de segurança e integridade implementadas no backend.

### Senhas

As senhas dos usuários são armazenadas utilizando hash por meio das ferramentas de segurança do Werkzeug.

A aplicação não armazena a senha original no banco de dados.

### Controle de sessão

Após o login, a aplicação mantém na sessão as informações necessárias para identificar o usuário autenticado.

As áreas protegidas verificam a existência de uma sessão válida antes de permitir o acesso.

### Autorização

Além da autenticação, o sistema diferencia as permissões de acordo com o perfil do usuário.

As verificações de autorização são realizadas no backend.

### Integridade referencial

O SQLite é configurado para utilizar:

```sql
PRAGMA foreign_keys = ON;
```

Dessa forma, os relacionamentos entre usuários, produtos e movimentações são protegidos pelo banco de dados.

---

## Validações

As validações são realizadas principalmente na camada de serviços, evitando que regras importantes dependam exclusivamente da interface.

Entre as validações implementadas estão:

* Campos obrigatórios;
* Valores numéricos não negativos;
* Username duplicado;
* Código de produto duplicado;
* Perfil inválido;
* Produto inativo;
* Usuário inválido;
* Tipo de movimentação inválido;
* Quantidade inválida;
* Saída superior ao estoque disponível;
* Tentativa de inativação do último ADMIN;
* Tentativa de inativação da própria conta.

---

## Testes automatizados

O projeto utiliza **pytest** para validação automatizada das principais regras de negócio.

A suíte atual possui:

**43 testes automatizados — 43 aprovados.**

Os testes estão organizados por domínio:

```text
tests/
├── conftest.py
├── test_movimentacao_service.py
├── test_produto_service.py
└── test_usuario_service.py
```

### Cobertura funcional dos testes

#### Usuários

Testes relacionados a:

* criação;
* validação de campos;
* hash de senha;
* username duplicado;
* ativação;
* inativação;
* proteção do último ADMIN;
* proteção contra auto-inativação;
* edição;
* alteração de perfil.

#### Produtos

Testes relacionados a:

* criação;
* validação de campos;
* código duplicado;
* valores negativos;
* edição;
* preservação do estoque atual;
* ativação;
* inativação.

#### Movimentações

Testes relacionados a:

* entrada;
* saída;
* atualização do estoque;
* associação entre produto e usuário;
* observação;
* quantidade inválida;
* tipo inválido;
* produto inativo;
* usuário inválido;
* prevenção de estoque negativo.

Os testes utilizam um banco SQLite em memória, evitando alterações no banco utilizado pela aplicação durante a execução da suíte.

---

## Tecnologias utilizadas

* **Python 3.12** ou superior
* **Flask**
* **Flask-SQLAlchemy**
* **SQLAlchemy**
* **SQLite**
* **Jinja2**
* **HTML5**
* **CSS3**
* **pytest**
* **Werkzeug**

---

## Estrutura do projeto

```text
stockflow/
├── app/
│   ├── auth/
│   │   └── decorators.py
│   │
│   ├── models/
│   │   ├── movimentacao.py
│   │   ├── produto.py
│   │   └── usuario.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── movimentacoes.py
│   │   ├── produtos.py
│   │   └── usuarios.py
│   │
│   ├── services/
│   │   ├── movimentacao_service.py
│   │   ├── produto_service.py
│   │   └── usuario_service.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   │   ├── movimentacoes/
│   │   ├── produtos/
│   │   ├── usuarios/
│   │   ├── 403.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── login.html
│   │
│   └── __init__.py
│
├── database/
│   ├── schema.sql
│   └── stockflow.db
│
├── tests/
│   ├── conftest.py
│   ├── test_movimentacao_service.py
│   ├── test_produto_service.py
│   └── test_usuario_service.py
│
├── .gitignore
├── config.py
├── create_admin.py
├── init_db.py
├── pytest.ini
├── requirements.txt
├── run.py
└── README.md
```

---

## Como executar

### 1. Criar o ambiente virtual

No terminal:

```bash
python -m venv .venv
```

### 2. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicializar o banco de dados

```bash
python init_db.py
```

Esse comando cria as tabelas necessárias para a aplicação.

### 5. Criar o usuário administrador

Execute o script de criação do administrador:

```bash
python create_admin.py
```

Informe os dados solicitados no terminal.

### 6. Executar a aplicação

```bash
python run.py
```

Após iniciar a aplicação, acesse o endereço local informado pelo Flask no terminal.

---

## Executando os testes

Com o ambiente virtual ativado:

```bash
pytest -v
```

O arquivo `pytest.ini` já configura a raiz do projeto no caminho de importação (`pythonpath = .`), então o comando acima funciona diretamente, sem precisar de `python -m pytest` nem de configurar `PYTHONPATH` manualmente.

Resultado esperado:

```text
43 passed
```

Os testes utilizam um banco SQLite em memória e não alteram o banco de dados utilizado pela aplicação.

---

## Banco de dados

O projeto utiliza **SQLite** como banco de dados.

O arquivo principal está localizado em:

```text
database/stockflow.db
```

O projeto também possui o script:

```text
database/schema.sql
```

contendo a estrutura SQL das tabelas.

---

## Decisões técnicas

### Separação entre Routes e Services

As regras de negócio foram concentradas na camada de serviços em vez de serem distribuídas diretamente pelas rotas.

Essa decisão facilita:

* manutenção;
* reutilização das regras;
* testes automatizados;
* leitura do código;
* evolução futura da aplicação.

### Controle de estoque por movimentações

A quantidade atual do produto não é alterada diretamente durante sua edição.

Alterações de estoque acontecem exclusivamente por meio de movimentações de entrada e saída.

Essa abordagem mantém o histórico das operações e evita alterações silenciosas no saldo do estoque.

### Inativação em vez de exclusão

Usuários e produtos são inativados em vez de serem fisicamente excluídos.

Isso preserva os registros existentes e evita a perda de informações relacionadas ao histórico da aplicação.

### Banco de testes isolado

A suíte de testes utiliza SQLite em memória.

Dessa forma, os testes podem criar e destruir seus próprios dados sem modificar o banco utilizado pela aplicação.

---

## Status do projeto

**Concluído — versão acadêmica funcional.**

O sistema possui as funcionalidades propostas, regras de negócio implementadas, interface web, persistência em banco de dados e testes automatizados.

---

## Considerações finais

O StockFlow foi desenvolvido com foco não apenas na implementação das funcionalidades solicitadas, mas também na organização interna da aplicação e na aplicação de regras de negócio de forma consistente.

A separação entre rotas, serviços e modelos permite que a aplicação seja compreendida e mantida com maior facilidade, enquanto os testes automatizados ajudam a verificar o comportamento das principais operações do sistema.

O projeto também foi estruturado considerando possibilidades de evolução futura, como ampliação das funcionalidades, melhoria da interface, novos relatórios e substituição do banco SQLite por uma solução adequada a ambientes de produção.

---

## Autora

Projeto desenvolvido por **Marinize Fonseca de Godoy Santana**, como avaliação prática da disciplina **Development with Python**, do curso de Análise e Desenvolvimento de Sistemas (EAD) da **UniFECAF**.

* GitHub: <https://github.com/marinizedev>
* LinkedIn: <https://linkedin.com/in/marinize-santana-47bb2b372>
* E-mail: <marinize.santana.dev@gmail.com>
