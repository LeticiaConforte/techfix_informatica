-- =====================================================
-- SISTEMA TECHFIX INFORMÁTICA - DDL SCHEMA
-- =====================================================

-- 1. Criação da Tabela de Clientes
CREATE TABLE IF NOT EXISTS public.clientes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    celular_whatsapp TEXT NOT NULL,
    data_cadastro TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    CONSTRAINT ck_email_formato CHECK (
        email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    ),
    CONSTRAINT ck_celular_digitos CHECK (
        celular_whatsapp ~ '^[0-9]{10,13}$'
    )
);

COMMENT ON TABLE public.clientes IS 'Armazena as informações cadastrais dos clientes.';
COMMENT ON COLUMN public.clientes.email IS 'E-mail do cliente, único no sistema.';

-- 2. Criação da Tabela de Ordens de Serviço
CREATE TABLE IF NOT EXISTS public.ordens_servico (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cliente_id BIGINT NOT NULL,
    modelo_computador TEXT NOT NULL,
    problema_relatado TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Aberto',
    data_abertura TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    data_atualizacao TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    CONSTRAINT fk_ordens_cliente 
        FOREIGN KEY (cliente_id) 
        REFERENCES public.clientes (id) 
        ON DELETE CASCADE,

    CONSTRAINT ck_status_permitidos CHECK (
        status IN ('Aberto', 'Em análise', 'Aguardando peça', 'Concluído', 'Entregue')
    )
);

COMMENT ON TABLE public.ordens_servico IS 'Registros das ordens de serviço de manutenção técnica.';
COMMENT ON COLUMN public.ordens_servico.status IS 'Status do fluxo de reparo.';

-- 3. Índices para Otimização
CREATE INDEX IF NOT EXISTS idx_clientes_email ON public.clientes (email);
CREATE INDEX IF NOT EXISTS idx_ordens_cliente_id ON public.ordens_servico (cliente_id);
CREATE INDEX IF NOT EXISTS idx_ordens_status ON public.ordens_servico (status);

-- 4. Função e Trigger para Atualização de data_atualizacao
CREATE OR REPLACE FUNCTION public.set_data_atualizacao()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_atualiza_ordens_servico ON public.ordens_servico;
CREATE TRIGGER trg_atualiza_ordens_servico
    BEFORE UPDATE ON public.ordens_servico
    FOR EACH ROW
    EXECUTE FUNCTION public.set_data_atualizacao();
