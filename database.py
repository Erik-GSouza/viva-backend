import sqlite3

# Nome do banco de dados
# Quando o sistema rodar, esse arquivo vai ser criado automaticamente na pasta do projeto
DATABASE_NAME = "viva.db"


def get_connection():
    """
    Cria e retorna uma conexão com o banco de dados
    função usada sempre que precisar consultar, inserir,
    atualizar ou remover dados do banco
    """

    connection = sqlite3.connect(DATABASE_NAME)

    # Faz com que os resultados possam ser acessados pelo nome da coluna
    # Ex: usuario["nome"] em vez de usuario[1]
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


def create_initial_data():
    """
    dados iniciais para o sistema funcionar em outros pcs.

    só para evitar criar perfis, usuários, curso etc
    manualmente pelo Swagger.

    Usa INSERT OR IGNORE para não duplicar dados caso a função rode mais
    de 1 vez.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Perfis fixos usados pelo front
    cursor.execute("""
        INSERT OR IGNORE INTO perfil (id_perfil, nome, descricao, status)
        VALUES
            (1, 'Aluno', 'Perfil de aluno do sistema.', 'ativo'),
            (2, 'Professor', 'Perfil de professor orientador.', 'ativo'),
            (3, 'Coordenador', 'Perfil de coordenação acadêmica.', 'ativo'),
            (4, 'Administrador', 'Perfil administrativo do sistema.', 'ativo');
    """)

    # Curso pra demonstração
    cursor.execute("""
        INSERT OR IGNORE INTO curso (id_curso, nome, sigla, descricao, status)
        VALUES
            (
                1,
                'Tecnologia Jujutsu Aplicada',
                'TJA',
                'Curso voltado ao uso de tecnologia, análise de ocorrências e soluções no universo jujutsu.',
                'ativo'
            );
    """)

    # Turma
    cursor.execute("""
        INSERT OR IGNORE INTO turma (id_turma, id_curso, nome, semestre, ano, turno, status)
        VALUES
            (
                1,
                1,
                'Tokyo 1º Ano',
                '2026.1',
                2026,
                'Manhã',
                'ativo'
            );
    """)

    # Usuários
    cursor.execute("""
        INSERT OR IGNORE INTO usuario (
            id_usuario,
            id_perfil,
            id_turma,
            nome,
            email,
            senha_hash,
            matricula,
            departamento,
            tipo_aluno,
            status,
            telefone,
            foto_perfil
        )
        VALUES
            (
                1,
                1,
                1,
                'Yuji Itadori',
                'yuji.itadori@jujutsu.local',
                '123456',
                'TJA2026001',
                NULL,
                'regular',
                'ativo',
                '81999999991',
                NULL
            ),
            (
                2,
                2,
                NULL,
                'Satoru Gojo',
                'satoru.gojo@jujutsu.local',
                '123456',
                NULL,
                'Departamento de Técnicas Jujutsu',
                NULL,
                'ativo',
                '81999999992',
                NULL
            ),
            (
                3,
                3,
                NULL,
                'Masamichi Yaga',
                'masamichi.yaga@jujutsu.local',
                '123456',
                NULL,
                'Coordenação da Escola Técnica Jujutsu',
                NULL,
                'ativo',
                '81999999993',
                NULL
            ),
            (
                4,
                4,
                NULL,
                'Ryomen Sukuna',
                'ryomen.sukuna@jujutsu.local',
                '123456',
                NULL,
                'Administração Operacional',
                NULL,
                'ativo',
                '81999999994',
                NULL
            );
    """)

    # Portfólio público do aluno
    cursor.execute("""
        INSERT OR IGNORE INTO portfolio (
            id_portfolio,
            id_usuario,
            titulo,
            bio,
            slug_publico,
            status
        )
        VALUES
            (
                1,
                1,
                'Portfólio de Yuji Itadori',
                'Portfólio acadêmico com projetos desenvolvidos durante o curso Jujutsu.',
                'yuji-itadori',
                'ativo'
            );
    """)

    # Tags e tecnologias iniciais
    cursor.execute("""
        INSERT OR IGNORE INTO tag_tecnologia (id_tag, nome, categoria, cor, status)
        VALUES
            (1, 'Angular', 'Framework', '#dd0031', 'ativo'),
            (2, 'TypeScript', 'Linguagem', '#3178c6', 'ativo'),
            (3, 'Python', 'Linguagem', '#3776ab', 'ativo'),
            (4, 'FastAPI', 'Framework', '#009688', 'ativo'),
            (5, 'SQLite', 'Banco de Dados', '#0f4c81', 'ativo'),
            (6, 'Mapeamento de Ocorrências', 'Ferramenta', '#7c3aed', 'ativo');
    """)

    # Competências iniciais
    cursor.execute("""
        INSERT OR IGNORE INTO competencia (id_competencia, nome, descricao, categoria, status)
        VALUES
            (
                1,
                'Desenvolvimento Web',
                'Capacidade de criar interfaces e sistemas web funcionais.',
                'Técnica',
                'ativo'
            ),
            (
                2,
                'Integração Front-end e Back-end',
                'Capacidade de conectar interfaces web a APIs e consumir dados reais.',
                'Técnica',
                'ativo'
            ),
            (
                3,
                'Trabalho em Equipe',
                'Capacidade de colaborar com outros integrantes no desenvolvimento de um projeto.',
                'Comportamental',
                'ativo'
            ),
            (
                4,
                'Análise de Ocorrências',
                'Capacidade de observar, registrar e interpretar situações para propor soluções adequadas.',
                'Pesquisa',
                'ativo'
            );
    """)

    # Projeto publicado para a vitrine pública
    cursor.execute("""
        INSERT OR IGNORE INTO projeto (
            id_projeto,
            id_turma,
            id_usuario_submissor,
            id_professor_orientador,
            titulo,
            descricao,
            problema,
            solucao,
            status,
            publicado,
            slug_publico,
            data_submissao,
            data_aprovacao,
            data_atualizacao
        )
        VALUES
            (
                1,
                1,
                1,
                2,
                'Expansão de domínio',
                'Como desenvolver uma expansão de domínio adequada para você.',
                'A escola precisava encontrar informações sobre domínio: ocorrências, responsáveis e soluções propostas pelos alunos.',
                'Deixa com Satoru Gojo.',
                'aprovado',
                1,
                'expansao-de-dominio',
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            );
    """)

    # Projeto pendente para o professor conseguir testar avaliação
    cursor.execute("""
        INSERT OR IGNORE INTO projeto (
            id_projeto,
            id_turma,
            id_usuario_submissor,
            id_professor_orientador,
            titulo,
            descricao,
            problema,
            solucao,
            status,
            publicado,
            slug_publico,
            data_submissao,
            data_atualizacao
        )
        VALUES
            (
                2,
                1,
                1,
                2,
                'Mapa de Ocorrências Amaldiçoadas',
                'Projeto para testar o fluxo de submissão, avaliação e publicação dentro do VIVA.',
                'As ocorrências ficavam espalhadas em registros diferentes, dificultando o acompanhamento pelos professores.',
                'Criar um mapa digital para organizar registros, status e responsáveis por cada ocorrência analisada.',
                'pendente',
                0,
                NULL,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            );
    """)

    # Integrantes dos projetos
    cursor.execute("""
        INSERT INTO integrante_projeto (id_usuario, id_projeto, funcao)
        SELECT 1, 1, 'Desenvolvedor Full Stack'
        WHERE NOT EXISTS (
            SELECT 1
            FROM integrante_projeto
            WHERE id_usuario = 1
            AND id_projeto = 1
        );
    """)

    cursor.execute("""
        INSERT INTO integrante_projeto (id_usuario, id_projeto, funcao)
        SELECT 1, 2, 'Desenvolvedor Front-end'
        WHERE NOT EXISTS (
            SELECT 1
            FROM integrante_projeto
            WHERE id_usuario = 1
            AND id_projeto = 2
        );
    """)

    # Versões iniciais dos projetos
    cursor.execute("""
        INSERT INTO versao_projeto (
            id_projeto,
            numero_versao,
            descricao_alteracao,
            status_versao
        )
        SELECT
            1,
            1,
            'Versão inicial do projeto publicado.',
            'aprovada'
        WHERE NOT EXISTS (
            SELECT 1
            FROM versao_projeto
            WHERE id_projeto = 1
            AND numero_versao = 1
        );
    """)

    cursor.execute("""
        INSERT INTO versao_projeto (
            id_projeto,
            numero_versao,
            descricao_alteracao,
            status_versao
        )
        SELECT
            2,
            1,
            'Versão inicial enviada para avaliação.',
            'enviada'
        WHERE NOT EXISTS (
            SELECT 1
            FROM versao_projeto
            WHERE id_projeto = 2
            AND numero_versao = 1
        );
    """)

    # Tags vinculadas aos projetos
    vinculos_tags = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 1),
        (2, 2),
        (2, 6)
    ]

    for id_projeto, id_tag in vinculos_tags:
        cursor.execute(
            """
            INSERT INTO projeto_tag (id_projeto, id_tag)
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM projeto_tag
                WHERE id_projeto = ?
                AND id_tag = ?
            );
            """,
            (id_projeto, id_tag, id_projeto, id_tag)
        )

    # Competências vinculadas aos projetos
    vinculos_competencias = [
        (1, 1, 'avancado'),
        (1, 2, 'avancado'),
        (1, 3, 'intermediario'),
        (1, 4, 'intermediario'),
        (2, 1, 'intermediario'),
        (2, 2, 'intermediario'),
        (2, 4, 'basico')
    ]

    for id_projeto, id_competencia, nivel in vinculos_competencias:
        cursor.execute(
            """
            INSERT INTO projeto_competencia (
                id_projeto,
                id_competencia,
                nivel
            )
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM projeto_competencia
                WHERE id_projeto = ?
                AND id_competencia = ?
            );
            """,
            (
                id_projeto,
                id_competencia,
                nivel,
                id_projeto,
                id_competencia
            )
        )

    # Projeto escolhido pelo aluno para aparecer no portfólio público
    cursor.execute("""
        INSERT INTO portfolio_projeto (
            id_portfolio,
            id_projeto,
            ordem_exibicao,
            destaque
        )
        SELECT
            1,
            1,
            1,
            1
        WHERE NOT EXISTS (
            SELECT 1
            FROM portfolio_projeto
            WHERE id_portfolio = 1
            AND id_projeto = 1
        );
    """)

    # Notificações iniciais
    cursor.execute("""
        INSERT INTO notificacao (
            id_usuario,
            titulo,
            mensagem,
            tipo,
            lida,
            link_destino
        )
        SELECT
            1,
            'Bem-vindo ao VIVA',
            'Seu acesso de aluno está pronto para uso.',
            'sistema',
            0,
            '/aluno/projetos'
        WHERE NOT EXISTS (
            SELECT 1
            FROM notificacao
            WHERE id_usuario = 1
            AND titulo = 'Bem-vindo ao VIVA'
        );
    """)

    cursor.execute("""
        INSERT INTO notificacao (
            id_usuario,
            titulo,
            mensagem,
            tipo,
            lida,
            link_destino
        )
        SELECT
            2,
            'Projeto aguardando avaliação',
            'Há um projeto pendente na sua fila de aprovação.',
            'avaliacao',
            0,
            '/professor/fila-aprovacao'
        WHERE NOT EXISTS (
            SELECT 1
            FROM notificacao
            WHERE id_usuario = 2
            AND titulo = 'Projeto aguardando avaliação'
        );
    """)

    connection.commit()
    connection.close()