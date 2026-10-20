CREATE TABLE IF NOT EXISTS movimentacoes (
    data_movimentacao DATE NOT NULL,
    valor NUMERIC(14, 2) NOT NULL,
    descricao TEXT NOT NULL,
    CONSTRAINT movimentacoes_unica UNIQUE (data_movimentacao, valor, descricao)
);
