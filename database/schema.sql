-- =========================================================
-- StockFlow - Estrutura do banco de dados (SQLite)
-- Gerado a partir do modelo utilizado pela aplicacao Flask
-- (app/models/usuario.py, produto.py, movimentacao.py)
-- =========================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------
-- Tabela: usuarios
-- Armazena os usuarios do sistema e seu perfil de acesso.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id          INTEGER NOT NULL,
    nome        VARCHAR(100) NOT NULL,
    username    VARCHAR(50)  NOT NULL,
    senha_hash  VARCHAR(255) NOT NULL,
    perfil      VARCHAR(20)  NOT NULL DEFAULT 'COMUM',
    ativo       BOOLEAN      NOT NULL DEFAULT 1,
    criado_em   DATETIME     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (username),
    CHECK (perfil IN ('ADMIN', 'COMUM'))
);

-- ---------------------------------------------------------
-- Tabela: produtos
-- Armazena os produtos controlados pelo estoque.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS produtos (
    id                INTEGER NOT NULL,
    codigo            VARCHAR(30)  NOT NULL,
    nome              VARCHAR(100) NOT NULL,
    descricao         TEXT,
    categoria         VARCHAR(50),
    quantidade_atual  INTEGER NOT NULL DEFAULT 0,
    estoque_minimo    INTEGER NOT NULL DEFAULT 0,
    preco             NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    ativo             BOOLEAN NOT NULL DEFAULT 1,
    criado_em         DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (codigo),
    CHECK (quantidade_atual >= 0),
    CHECK (estoque_minimo >= 0),
    CHECK (preco >= 0)
);

-- ---------------------------------------------------------
-- Tabela: movimentacoes
-- Registra as entradas e saidas de estoque, vinculando
-- cada movimentacao a um produto e a um usuario responsavel.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS movimentacoes (
    id            INTEGER NOT NULL,
    produto_id    INTEGER NOT NULL,
    usuario_id    INTEGER NOT NULL,
    tipo          VARCHAR(10) NOT NULL,
    quantidade    INTEGER NOT NULL,
    observacao    TEXT,
    realizado_em  DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    CHECK (tipo IN ('ENTRADA', 'SAIDA')),
    CHECK (quantidade > 0)
);

-- ---------------------------------------------------------
-- Indices auxiliares para consultas frequentes
-- ---------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_movimentacoes_produto_id
    ON movimentacoes (produto_id);

CREATE INDEX IF NOT EXISTS idx_movimentacoes_usuario_id
    ON movimentacoes (usuario_id);

CREATE INDEX IF NOT EXISTS idx_produtos_ativo
    ON produtos (ativo);
