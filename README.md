# StockFlow

[![CI](https://github.com/marinizedev/stockflow-inventory-system/actions/workflows/ci.yml/badge.svg)](https://github.com/marinizedev/stockflow-inventory-system/actions/workflows/ci.yml)
[![Security](https://github.com/marinizedev/stockflow-inventory-system/actions/workflows/security.yml/badge.svg)](https://github.com/marinizedev/stockflow-inventory-system/actions/workflows/security.yml)
[![CD](https://github.com/marinizedev/stockflow-inventory-system/actions/workflows/cd.yml/badge.svg)](https://github.com/marinizedev/stockflow-inventory-system/actions/workflows/cd.yml)

**Sistema web de controle de estoque desenvolvido com Python e Flask.**

O StockFlow permite cadastrar produtos, registrar entradas e saídas, acompanhar os níveis de estoque, identificar itens abaixo do mínimo definido e consultar o histórico das movimentações. A aplicação conta com autenticação, autorização por perfil, validações de regras de negócio e testes automatizados.

Iniciado como projeto acadêmico com Flask e SQLite, o StockFlow evoluiu para uma aplicação publicada na nuvem, utilizando PostgreSQL no Neon, Gunicorn, Render e automações de CI/CD com GitHub Actions.

**Aplicação publicada:** [Acessar o StockFlow](https://stockflow-inventory-system-zaqc.onrender.com)

## Índice

* [Demonstração](#demonstração)
* [Sobre o projeto](#sobre-o-projeto)
* [Funcionalidades](#funcionalidades)
* [Perfis de acesso](#perfis-de-acesso)
* [Regras de negócio](#regras-de-negócio)
* [Arquitetura](#arquitetura)
* [Modelo de dados](#modelo-de-dados)
* [Segurança e integridade](#segurança-e-integridade)
* [Testes automatizados](#testes-automatizados)
* [CI/CD](#cicd)
* [Tecnologias](#tecnologias)
* [Estrutura do projeto](#estrutura-do-projeto)
* [Executar localmente](#executar-localmente)
* [Configuração por ambiente](#configuração-por-ambiente)
* [Deploy e infraestrutura](#deploy-e-infraestrutura)
* [Decisões técnicas](#decisões-técnicas)
* [Evolução do projeto](#evolução-do-projeto)
* [Possíveis evoluções](#possíveis-evoluções)
* [Autoria](#autoria)
* [Referências](#referências)
* [Licença](#licença)

---

## Demonstração

**Aplicação publicada:** https://stockflow-inventory-system-zaqc.onrender.com

O ambiente público permite conhecer as principais funcionalidades por meio de uma conta de demonstração com permissões exclusivamente de leitura.

> **Disponibilidade:** por utilizar o plano gratuito do Render, a aplicação pode levar alguns segundos para responder após períodos de inatividade.

### Acesso de demonstração

| Campo      | Valor                                           |
| ---------- | ----------------------------------------------- |
| Usuário    | `visitante.demo`                                |
| Senha      | `StockFlowDemo2026!`                            |
| Perfil     | `DEMO`                                          |
| Permissões | Consulta ao dashboard, produtos e movimentações |

A credencial é pública e exclusiva para demonstração do StockFlow. Não deve ser reutilizada em outros serviços ou projetos.

O perfil `DEMO` não pode criar, editar ou inativar usuários e produtos, nem registrar movimentações. As restrições são aplicadas no backend.

### Demonstração visual

As imagens apresentam as principais telas da aplicação. Elas podem ter sido capturadas em ambiente local, com dados fictícios, e não representam necessariamente a sessão ou as permissões da conta pública `DEMO`.

#### Login

![Tela de login do StockFlow](docs/images/login.png)

#### Dashboard

![Dashboard do StockFlow](docs/images/dashboard.png)

#### Catálogo de produtos

![Catálogo de produtos do StockFlow](docs/images/produtos.png)

#### Histórico de movimentações

![Histórico de movimentações do StockFlow](docs/images/movimentacoes.png)

---

## Sobre o projeto

O StockFlow é uma aplicação web destinada ao controle de produtos e movimentações de estoque. Seu objetivo é centralizar as informações operacionais, manter o histórico das operações e reduzir inconsistências no registro das quantidades disponíveis.

O projeto foi estruturado com separação entre rotas, serviços e modelos. Essa organização permite concentrar as regras de negócio em uma camada específica, facilitando a manutenção, os testes e a evolução da aplicação.

## Funcionalidades

### Autenticação e gerenciamento de sessão

* Login e logout.
* Verificação do status do usuário.
* Senhas armazenadas como hash utilizando Werkzeug.
* Controle de sessão e proteção de páginas restritas.
* Redirecionamento de usuários não autenticados.
* Bloqueio de login para usuários inativos.

### Gerenciamento de usuários

Funcionalidades administrativas disponíveis para o perfil `ADMIN`:

* Cadastro e edição de usuários.
* Alteração de nome, username e perfil.
* Perfis `ADMIN`, `COMUM` e `DEMO`.
* Ativação e inativação lógica.
* Proteção contra a inativação do último administrador ativo.
* Impedimento de auto-inativação.
* Regras para impedir o rebaixamento indevido de administradores.

### Gerenciamento de produtos

* Cadastro e edição de produtos.
* Código único por produto.
* Nome, categoria, descrição opcional e preço.
* Definição do estoque mínimo.
* Ativação e inativação lógica.
* Validação de valores não negativos.
* Preservação do saldo durante a edição cadastral.

O estoque atual não é alterado diretamente pela edição do produto. As alterações de saldo ocorrem por meio de movimentações.

### Movimentações de estoque

* Registro de entradas e saídas.
* Associação da movimentação ao produto e ao usuário responsável.
* Registro de quantidade, data e observação.
* Atualização do saldo após uma movimentação válida.
* Bloqueio de movimentações para produtos inativos.
* Validação de quantidades.
* Prevenção de saídas superiores ao saldo disponível.
* Consulta ao histórico de movimentações.
* Bloqueio de operações de escrita para o perfil `DEMO`.

### Dashboard

* Total de produtos cadastrados.
* Quantidade de produtos abaixo do estoque mínimo.
* Total de movimentações.
* Total de usuários.
* Alertas de estoque mínimo.
* Exibição de movimentações recentes.

---

## Perfis de acesso

| Perfil  | Permissões                                                                                             |
| ------- | ------------------------------------------------------------------------------------------------------ |
| `ADMIN` | Gerencia usuários e produtos e realiza movimentações de estoque.                                                           |
| `COMUM` | Consulta produtos e realiza movimentações de estoque, sem acesso ao gerenciamento de usuários.         |
| `DEMO`  | Consulta o dashboard, os produtos e o histórico de movimentações, sem permissão para alterar os dados. |

A autorização é verificada no backend. A ocultação de botões na interface não é utilizada como único mecanismo de controle de acesso.

---

## Regras de negócio

O StockFlow implementa regras para manter a consistência das operações e proteger o histórico do estoque.

1. Nome, username e senha são obrigatórios no cadastro de usuários.
2. O username deve ser único.
3. As senhas não são armazenadas em texto puro.
4. O perfil deve corresponder a um dos perfis permitidos.
5. Somente usuários `ADMIN` podem gerenciar usuários.
6. Usuários inativos não podem realizar login.
7. Deve existir pelo menos um administrador ativo.
8. O último administrador ativo não pode ser inativado.
9. Um usuário não pode inativar a própria conta.
10. O rebaixamento de um administrador depende da existência de outro administrador ativo.
11. O perfil `DEMO` não pode realizar operações de escrita.
12. O código do produto deve ser único.
13. O estoque atual não pode ser alterado diretamente na edição cadastral.
14. Quantidade em estoque e estoque mínimo não podem ser negativos.
15. O preço não pode ser negativo.
16. A quantidade de uma movimentação deve ser maior que zero.
17. Produtos inativos não podem receber movimentações.
18. Uma saída não pode gerar estoque negativo.
19. Toda movimentação deve estar relacionada a um produto e a um usuário.
20. O tipo de movimentação deve ser `ENTRADA` ou `SAIDA`.
21. Produtos com saldo inferior ao estoque mínimo são identificados nos alertas.
22. Usuários e produtos são inativados logicamente, preservando seus registros e relacionamentos históricos.

---

## Arquitetura

A aplicação utiliza uma arquitetura organizada em camadas, separando o tratamento das requisições das regras de negócio e da persistência.

```text
Navegador
    |
    v
Routes
    |
    v
Services
Regras de negócio e validações
    |
    v
Models
Entidades e mapeamento ORM
    |
    v
Banco de dados
SQLite / PostgreSQL
```

### Responsabilidades

* **Routes:** recebem requisições e controlam o fluxo de navegação.
* **Services:** concentram regras de negócio, validações e operações do domínio.
* **Models:** representam as entidades e seus relacionamentos por meio do SQLAlchemy.
* **Templates:** renderizam as páginas HTML utilizando Jinja2.
* **Static:** reúne os recursos estáticos, incluindo os estilos CSS.
* **Banco de dados:** armazena usuários, produtos e movimentações.

---

## Modelo de dados

O sistema utiliza três entidades principais.

### `usuarios`

Armazena os dados de identificação, o hash da senha, o perfil de acesso, o status da conta e a data de criação.

### `produtos`

Armazena o código, o nome, a descrição, a categoria, o preço, o saldo atual, o estoque mínimo, o status e a data de criação.

### `movimentacoes`

Armazena o produto relacionado, o usuário responsável, o tipo da operação, a quantidade, a observação e a data da movimentação.

### Relacionamentos

```text
Usuario 1 ───── N Movimentacao N ───── 1 Produto
```

Um usuário pode realizar várias movimentações, e um produto pode possuir várias movimentações registradas.

As chaves estrangeiras estabelecem os relacionamentos entre as entidades e contribuem para a integridade referencial.

---

## Segurança e integridade

A aplicação adota mecanismos de segurança e validação em diferentes camadas:

* **Hash de senhas:** utilização das funções de segurança do Werkzeug.
* **Chave de sessão:** configuração por meio da variável de ambiente `STOCKFLOW_SECRET_KEY`, sem fallback para uma chave padrão no código.
* **Configuração externa:** credenciais e configurações sensíveis não devem ser armazenadas no repositório.
* **Autorização no backend:** validação das permissões antes de executar operações restritas.
* **Controle de sessão:** proteção das áreas destinadas a usuários autenticados.
* **Perfil DEMO:** bloqueio de operações de escrita.
* **Validação de negócio:** verificação dos dados antes de executar as operações.
* **Integridade referencial:** relacionamentos entre usuários, produtos e movimentações.
* **Inativação lógica:** preservação dos registros necessários ao histórico.
* **Auditoria de dependências:** utilização do pip-audit para verificar vulnerabilidades conhecidas nas dependências Python.

A configuração da chave de sessão é obrigatória em todos os ambientes nos quais a aplicação é iniciada. No ambiente publicado, o valor deve ser fornecido pelas variáveis de ambiente do Render.

---

## Testes automatizados

O projeto utiliza **pytest** para verificar as principais regras de negócio.

A suíte de testes possui **43 testes automatizados**, com resultado registrado de:

```text
43 passed
```

A cobertura funcional inclui:

* Autenticação e hash de senha.
* Permissões por perfil.
* Restrições de usuários e administradores.
* Cadastro e edição de produtos.
* Validação de valores.
* Entradas e saídas de estoque.
* Atualização do saldo.
* Prevenção de estoque negativo.
* Regras relacionadas a produtos inativos.

Os testes utilizam um banco SQLite em memória, isolando suas operações dos dados da instalação local e do banco de produção.

Para executar os testes:

```bash
pytest -v
```

A suíte atualmente possui 43 testes automatizados. Na última execução realizada localmente, todos os 43 testes foram aprovados (`43 passed`).

---

## CI/CD

O repositório utiliza GitHub Actions para automatizar testes, verificações de segurança e validação da disponibilidade da aplicação após a publicação.

| Workflow     | Responsabilidade                                                                                                                                                                             |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CI**       | Executa verificações de compilação, integridade do diff e testes automatizados em pushes para `main` e pull requests direcionados à `main`.                                                  |
| **Security** | Executa verificações de segurança, análise estática com `Bandit` e auditoria de dependências com `pip-audit` em pushes para `main`, pull requests direcionados à `main` e execuções manuais. |
| **CD**       | Após pushes para `main`, aguarda o deploy no Render e verifica por HTTP se a aplicação publicada está disponível e respondendo corretamente.                                                 |

### Fluxo de publicação

```text
Pull Request
     |
     +------------------+
     |                  |
     v                  v
    CI              Security
     |                  |
     +--------+---------+
              |
              v
       Merge na branch main
              |
              v
     Deploy automático
         no Render
              |
              v
       Verificação HTTP
         pós-deploy
```

O smoke test verifica a disponibilidade da rota pública `/login`. Essa verificação confirma a resposta HTTP da rota, mas não substitui testes completos de todas as funcionalidades da aplicação.

---

## Tecnologias

| Tecnologia       | Utilização                                       |
| ---------------- | ------------------------------------------------ |
| Python           | Linguagem de programação.                        |
| Flask            | Framework web.                                   |
| Flask-SQLAlchemy | Integração entre Flask e SQLAlchemy.             |
| SQLAlchemy       | ORM e mapeamento das entidades.                  |
| SQLite           | Banco de dados local e ambiente de testes.       |
| PostgreSQL       | Banco de dados do ambiente publicado.            |
| Neon             | Serviço gerenciado de PostgreSQL.                |
| Psycopg          | Driver de conexão com PostgreSQL.                |
| Gunicorn         | Servidor WSGI utilizado na publicação.           |
| Jinja2           | Renderização de templates.                       |
| HTML5 e CSS3     | Estrutura e apresentação da interface.           |
| Werkzeug         | Recursos de segurança, incluindo hash de senhas. |
| pytest           | Testes automatizados.                            |
| GitHub Actions   | Automação de CI/CD e verificações.               |
| Render           | Hospedagem da aplicação.                         |
| pip-audit        | Auditoria de dependências Python.                |

---

## Estrutura do projeto

```text
stockflow/
├── app/
│   ├── auth/
│   │   └── decorators.py
│   ├── models/
│   │   ├── movimentacao.py
│   │   ├── produto.py
│   │   └── usuario.py
│   ├── routes/
│   │   ├── dashboard.py
│   │   ├── movimentacoes.py
│   │   ├── produtos.py
│   │   └── usuarios.py
│   ├── services/
│   │   ├── movimentacao_service.py
│   │   ├── produto_service.py
│   │   └── usuario_service.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── templates/
│   │   ├── movimentacoes/
│   │   │   ├── index.html
│   │   │   └── nova.html
│   │   ├── produtos/
│   │   │   ├── editar.html
│   │   │   ├── index.html
│   │   │   └── novo.html
│   │   ├── usuarios/
│   │   │   ├── editar.html
│   │   │   ├── index.html
│   │   │   └── novo.html
│   │   ├── 403.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── login.html
│   ├── __init__.py
│   └── logging_config.py
│
├── database/
│   └── schema.sql
├── docs/
│   └── images/
│       ├── dashboard.png
│       ├── login.png
│       ├── movimentacoes.png
│       └── produtos.png
├── tests/
│   ├── conftest.py
│   ├── test_movimentacao_service.py
│   ├── test_produto_service.py
│   └── test_usuario_service.py
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── security.yml
│       └── cd.yml
├── .env.example
├── .gitattributes
├── .gitignore
├── config.py
├── create_admin.py
├── init_db.py
├── LICENSE
├── pytest.ini
├── requirements-production.txt
├── requirements.txt
├── run.py
└── README.md
```

---

## Executar localmente

### Requisitos

* Python 3.12 ou superior.
* Git.
* PowerShell no Windows ou um terminal compatível.

### 1. Clonar o repositório

```bash
git clone https://github.com/marinizedev/stockflow-inventory-system.git
cd stockflow-inventory-system
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar a chave de sessão

A aplicação exige a variável `STOCKFLOW_SECRET_KEY`. Para gerar uma chave aleatória no PowerShell:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Copie o valor gerado e defina-o na sessão atual do terminal:

```powershell
$env:STOCKFLOW_SECRET_KEY = "COLE_A_CHAVE_GERADA_AQUI"
```

Use uma chave própria para o ambiente local. Não utilize a chave de produção nem compartilhe o valor gerado.

Essa variável definida no PowerShell permanece disponível somente naquela sessão. Se abrir outro terminal, será necessário configurá-la novamente, salvo se você adotar outro mecanismo local de configuração.

### 5. Inicializar o banco e criar o administrador

```bash
python init_db.py
python create_admin.py
```

O banco SQLite local é independente e inicialmente vazio. O script `create_admin.py` solicita os dados necessários para criar a conta administrativa inicial.

### 6. Iniciar a aplicação

```bash
python run.py
```

Acesse:

http://127.0.0.1:5000

### Banco de dados local

Na ausência de `DATABASE_URL`, a aplicação utiliza o SQLite configurado para o ambiente local.

Cada instalação possui seus próprios usuários, produtos e movimentações. O repositório contém o código e os arquivos de estrutura necessários, mas não versiona os dados operacionais das instalações.

### Executar os testes

```bash
pytest -v
```

---

## Configuração por ambiente

O StockFlow seleciona o banco de dados de acordo com a variável `DATABASE_URL`.

| Configuração                    | Comportamento                                               |
| ------------------------------- | ----------------------------------------------------------- |
| `DATABASE_URL` ausente          | Utiliza SQLite local.                                       |
| `DATABASE_URL` definida         | Utiliza o banco indicado pela URL.                          |
| `STOCKFLOW_SECRET_KEY` ausente  | Impede a inicialização da aplicação.                        |
| `STOCKFLOW_SECRET_KEY` definida | Fornece a chave utilizada pelo Flask para assinar a sessão. |
| `LOG_LEVEL` ausente             | Utiliza `INFO` como nível de log.                           |

```env
DATABASE_URL=
STOCKFLOW_SECRET_KEY=
LOG_LEVEL=INFO
```

O arquivo `.env.example` documenta as variáveis esperadas. As variáveis podem ser fornecidas pelo ambiente de execução ou por um mecanismo de carregamento de variáveis configurado localmente. Valores sensíveis não devem ser versionados no repositório.

A URL do banco e a chave de sessão não devem ser incluídas no código-fonte, no README ou em capturas de tela públicas.

---

## Deploy e infraestrutura

### Render

A aplicação publicada utiliza o Render para hospedar o serviço web.

Configuração informada para o serviço:

| Campo         | Valor                                        |
| ------------- | -------------------------------------------- |
| Branch        | `main`                                       |
| Build Command | `pip install -r requirements-production.txt` |
| Start Command | `gunicorn run:app`                           |
| Runtime       | Python 3                                     |

As variáveis de ambiente são configuradas no painel do serviço.

### Neon

O banco de produção utiliza PostgreSQL gerenciado no Neon.

A connection string é fornecida ao Render por meio de `DATABASE_URL`. Dessa forma, as credenciais do banco permanecem fora do repositório.

O SQLite continua sendo utilizado no desenvolvimento local e nos testes, sem exigir uma instalação local de PostgreSQL.

---

## Decisões técnicas

### Separação entre rotas e serviços

A separação das responsabilidades evita concentrar todas as regras nas rotas. Os serviços são responsáveis pelas regras de negócio, enquanto as rotas coordenam as requisições e respostas HTTP.

### Estoque controlado por movimentações

O saldo atual é alterado por entradas e saídas válidas. A edição cadastral não permite alterar diretamente a quantidade em estoque, preservando a relação entre o saldo e as operações registradas.

### Inativação lógica

Usuários e produtos são inativados em vez de excluídos fisicamente. Essa decisão preserva registros e relacionamentos necessários ao histórico das movimentações.

### Perfil público de demonstração

O perfil `DEMO` permite apresentar o sistema sem conceder permissões de alteração sobre os dados compartilhados. As restrições são aplicadas no backend.

### Configuração por ambiente

O SQLite é utilizado no desenvolvimento local e o PostgreSQL no ambiente publicado. A seleção do banco ocorre por meio de `DATABASE_URL`, enquanto a chave de sessão é fornecida separadamente por `STOCKFLOW_SECRET_KEY`.

---

## Evolução do projeto

O StockFlow começou como uma atividade acadêmica e foi ampliado progressivamente para incorporar práticas de organização de software, segurança e publicação.

### Etapa acadêmica

* Desenvolvimento da aplicação com Flask.
* Persistência em SQLite.
* Autenticação e perfis `ADMIN` e `COMUM`.
* Cadastro e gerenciamento de produtos.
* Movimentações de entrada e saída.
* Controle de estoque mínimo.
* Histórico das operações.
* Testes automatizados.

### Evolução posterior

1. Organização da aplicação em rotas, serviços e modelos.
2. Ampliação das regras de autenticação e autorização.
3. Testes automatizados para as regras de negócio.
4. Implementação de logging estruturado.
5. CI e auditoria de dependências.
6. Integração com PostgreSQL no Neon.
7. Publicação com Gunicorn no Render.
8. Pipeline de CD com verificação HTTP pós-deploy.
9. Criação de um perfil público `DEMO` somente para leitura.
10. Documentação visual e técnica no repositório.

Essa evolução permitiu levar uma aplicação inicialmente acadêmica a um ambiente público, mantendo o foco no controle de estoque, na integridade dos dados e na rastreabilidade das operações.

---

## Possíveis evoluções

As funcionalidades abaixo são possibilidades futuras e não fazem parte do escopo funcional descrito nesta versão:

* Relatórios gerenciais de estoque.
* Indicadores históricos e análise de movimentações.
* Gestão de múltiplos depósitos.
* Leitura de códigos de barras.
* Regras de reposição automática.
* Integrações com outros sistemas.

---

## Autoria

Projeto desenvolvido por **Marinize Santana**.

* **GitHub:** [marinizedev](https://github.com/marinizedev)
* **LinkedIn:** [Marinize Santana](https://linkedin.com/in/marinize-santana-47bb2b372)
* **E-mail:** [marinize.santana.dev@gmail.com](mailto:marinize.santana.dev@gmail.com)

---

## Referências

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Render — Deploy a Flask App](https://render.com/docs/deploy-flask)
* [Render — Environment Variables](https://render.com/docs/configure-environment-variables)
* [Neon Documentation](https://neon.com/docs/)
* [pytest Documentation](https://docs.pytest.org/)
* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [Gunicorn Documentation](https://gunicorn.org/)
* [Werkzeug — Security Utilities](https://werkzeug.palletsprojects.com/en/stable/utils/)
* [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
* [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## Licença

Este projeto está disponibilizado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para conhecer os termos de utilização e reutilização do código.
