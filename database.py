import sqlite3

# Nome do banco de dados
# Quando o sistema rodar, esse arquivo vai ser criado automaticamente na pasta do projeto
DATABASE_NAME = "viva.db"


def get_connection():
    """
    Cria e retorna uma conexão com o banco de dados SQLite
    Essa função será usada sempre que precisar consultar, inserir,
    atualizar ou remover dados do banco
    """

    connection = sqlite3.connect(DATABASE_NAME)

    # Faz com que os resultados possam ser acessados pelo nome da coluna
    # Exemplo: usuario["nome"] em vez de usuario[1]
    connection.row_factory = sqlite3.Row

    # Ativa o uso de chaves estrangeiras no SQLite
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """
    Cria as tabelas iniciais do banco de dados
    Se as tabelas já existirem, o SQLite não cria again
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfil (
            id_perfil INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            status TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS curso (
            id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sigla TEXT NOT NULL UNIQUE,
            descricao TEXT,
            status TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turma (
            id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
            id_curso INTEGER NOT NULL,
            nome TEXT NOT NULL,
            semestre TEXT NOT NULL,
            ano INTEGER NOT NULL,
            turno TEXT NOT NULL,
            status TEXT NOT NULL,

            FOREIGN KEY (id_curso)
                REFERENCES curso(id_curso)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            id_perfil INTEGER NOT NULL,
            id_turma INTEGER,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            matricula TEXT UNIQUE,
            departamento TEXT,
            tipo_aluno TEXT,
            status TEXT NOT NULL,
            telefone TEXT,
            foto_perfil TEXT,
            data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
            data_ultimo_acesso TEXT,

            FOREIGN KEY (id_perfil)
                REFERENCES perfil(id_perfil),

            FOREIGN KEY (id_turma)
                REFERENCES turma(id_turma)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projeto (
            id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turma INTEGER NOT NULL,
            id_usuario_submissor INTEGER NOT NULL,
            id_professor_orientador INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            problema TEXT,
            solucao TEXT,
            status TEXT NOT NULL,
            publicado INTEGER DEFAULT 0,
            slug_publico TEXT UNIQUE,
            data_submissao TEXT DEFAULT CURRENT_TIMESTAMP,
            data_aprovacao TEXT,
            data_atualizacao TEXT,

            FOREIGN KEY (id_turma)
                REFERENCES turma(id_turma),

            FOREIGN KEY (id_usuario_submissor)
                REFERENCES usuario(id_usuario),

            FOREIGN KEY (id_professor_orientador)
                REFERENCES usuario(id_usuario)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS integrante_projeto (
            id_integrante_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_projeto INTEGER NOT NULL,
            funcao TEXT NOT NULL,
            data_vinculo TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_usuario)
                REFERENCES usuario(id_usuario),

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            UNIQUE (id_usuario, id_projeto)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_tecnologia (
            id_tag INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            categoria TEXT NOT NULL,
            cor TEXT,
            status TEXT NOT NULL,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projeto_tag (
            id_projeto_tag INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projeto INTEGER NOT NULL,
            id_tag INTEGER NOT NULL,

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            FOREIGN KEY (id_tag)
                REFERENCES tag_tecnologia(id_tag),

            UNIQUE (id_projeto, id_tag)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competencia (
            id_competencia INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            categoria TEXT NOT NULL,
            status TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projeto_competencia (
            id_projeto_competencia INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projeto INTEGER NOT NULL,
            id_competencia INTEGER NOT NULL,
            nivel TEXT NOT NULL,

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            FOREIGN KEY (id_competencia)
                REFERENCES competencia(id_competencia),

            UNIQUE (id_projeto, id_competencia)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS versao_projeto (
            id_versao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projeto INTEGER NOT NULL,
            numero_versao INTEGER NOT NULL,
            descricao_alteracao TEXT,
            data_envio TEXT DEFAULT CURRENT_TIMESTAMP,
            status_versao TEXT NOT NULL,

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            UNIQUE (id_projeto, numero_versao)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arquivo_projeto (
            id_arquivo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projeto INTEGER NOT NULL,
            id_versao INTEGER,
            nome_arquivo TEXT NOT NULL,
            tipo_arquivo TEXT NOT NULL,
            url_arquivo TEXT NOT NULL,
            tamanho_arquivo INTEGER,
            data_upload TEXT DEFAULT CURRENT_TIMESTAMP,
            principal INTEGER DEFAULT 0,
            nivel_acesso TEXT NOT NULL,

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            FOREIGN KEY (id_versao)
                REFERENCES versao_projeto(id_versao)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacao (
            id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projeto INTEGER NOT NULL,
            id_versao INTEGER NOT NULL,
            id_professor INTEGER NOT NULL,
            parecer TEXT NOT NULL,
            status_resultante TEXT NOT NULL,
            nota_final REAL,
            data_avaliacao TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            FOREIGN KEY (id_versao)
                REFERENCES versao_projeto(id_versao),

            FOREIGN KEY (id_professor)
                REFERENCES usuario(id_usuario)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id_portfolio INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            bio TEXT,
            slug_publico TEXT UNIQUE,
            status TEXT NOT NULL,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TEXT,

            FOREIGN KEY (id_usuario)
                REFERENCES usuario(id_usuario),

            UNIQUE (id_usuario)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_projeto (
            id_portfolio_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_portfolio INTEGER NOT NULL,
            id_projeto INTEGER NOT NULL,
            ordem_exibicao INTEGER,
            destaque INTEGER DEFAULT 0,
            data_adicao TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_portfolio)
                REFERENCES portfolio(id_portfolio),

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            UNIQUE (id_portfolio, id_projeto)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consentimento_publicacao (
            id_consentimento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projeto INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            autorizado INTEGER NOT NULL,
            observacao TEXT,
            data_consentimento TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_projeto)
                REFERENCES projeto(id_projeto),

            FOREIGN KEY (id_usuario)
                REFERENCES usuario(id_usuario),

            UNIQUE (id_projeto, id_usuario)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificacao (
            id_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            tipo TEXT NOT NULL,
            lida INTEGER DEFAULT 0,
            link_destino TEXT,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_usuario)
                REFERENCES usuario(id_usuario)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relatorio (
            id_relatorio INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            tipo_relatorio TEXT NOT NULL,
            filtros TEXT,
            formato TEXT NOT NULL,
            caminho_arquivo TEXT,
            status TEXT NOT NULL,
            data_geracao TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_usuario)
                REFERENCES usuario(id_usuario)
        );
    """)

    connection.commit()
    connection.close()