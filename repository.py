from typing import Optional

from database import get_connection
from models import (
    PerfilCreate,
    CursoCreate,
    TurmaCreate,
    UsuarioCreate,
    ProjetoCreate,
    IntegranteProjetoCreate,
    TagTecnologiaCreate,
    ProjetoTagCreate,
    CompetenciaCreate,
    ProjetoCompetenciaCreate,
    VersaoProjetoCreate,
    ArquivoProjetoCreate,
    AvaliacaoCreate,
    PortfolioCreate,
    PortfolioProjetoCreate,
    ConsentimentoPublicacaoCreate,
    NotificacaoCreate,
    RelatorioCreate
)


# FUNÇÃO AUXILIAR

def row_to_dict(row):
    """
    Converte uma linha retornada pelo SQLite em dicionário.
    facilita devolver os dados no formato JSON pela API
    """

    if row is None:
        return None

    return dict(row)


# PERFIL

def criar_perfil(perfil: PerfilCreate):
    """
    Insere um novo perfil no banco de dados.
    ex: Aluno, Professor, Coordenador ou Administrador.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO perfil (nome, descricao, status)
            VALUES (?, ?, ?)
            """,
            (perfil.nome, perfil.descricao, perfil.status)
        )

        connection.commit()

        id_perfil_criado = cursor.lastrowid

        return buscar_perfil_por_id(id_perfil_criado)

    finally:
        connection.close()


def listar_perfis():
    """
    Lista todos os perfis cadastrados
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id_perfil, nome, descricao, status
        FROM perfil
        ORDER BY id_perfil
        """
    )

    perfis = cursor.fetchall()

    connection.close()

    return [row_to_dict(perfil) for perfil in perfis]


def buscar_perfil_por_id(id_perfil: int):
    """
    Busca um perfil específico pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id_perfil, nome, descricao, status
        FROM perfil
        WHERE id_perfil = ?
        """,
        (id_perfil,)
    )

    perfil = cursor.fetchone()

    connection.close()

    return row_to_dict(perfil)


# CURSO

def criar_curso(curso: CursoCreate):
    """
    Insere um novo curso no banco de dados.
    Exemplo: Análise e Desenvolvimento de Sistemas.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO curso (nome, sigla, descricao, status)
            VALUES (?, ?, ?, ?)
            """,
            (curso.nome, curso.sigla, curso.descricao, curso.status)
        )

        connection.commit()

        id_curso_criado = cursor.lastrowid

        return buscar_curso_por_id(id_curso_criado)

    finally:
        connection.close()


def listar_cursos():
    """
    Lista todos os cursos cadastrados
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id_curso, nome, sigla, descricao, status
        FROM curso
        ORDER BY id_curso
        """
    )

    cursos = cursor.fetchall()

    connection.close()

    return [row_to_dict(curso) for curso in cursos]


def buscar_curso_por_id(id_curso: int):
    """
    Busca um curso específico pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id_curso, nome, sigla, descricao, status
        FROM curso
        WHERE id_curso = ?
        """,
        (id_curso,)
    )

    curso = cursor.fetchone()

    connection.close()

    return row_to_dict(curso)


# TURMA

def criar_turma(turma: TurmaCreate):
    """
    Insere uma nova turma no banco de dados.
    Cada turma pertence a um curso.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO turma (id_curso, nome, semestre, ano, turno, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                turma.id_curso,
                turma.nome,
                turma.semestre,
                turma.ano,
                turma.turno,
                turma.status
            )
        )

        connection.commit()

        id_turma_criada = cursor.lastrowid

        return buscar_turma_por_id(id_turma_criada)

    finally:
        connection.close()


def listar_turmas():
    """
    Lista todas as turmas cadastradas
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id_turma, id_curso, nome, semestre, ano, turno, status
        FROM turma
        ORDER BY id_turma
        """
    )

    turmas = cursor.fetchall()

    connection.close()

    return [row_to_dict(turma) for turma in turmas]


def buscar_turma_por_id(id_turma: int):
    """
    Busca uma turma específica pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id_turma, id_curso, nome, semestre, ano, turno, status
        FROM turma
        WHERE id_turma = ?
        """,
        (id_turma,)
    )

    turma = cursor.fetchone()

    connection.close()

    return row_to_dict(turma)


# USUÁRIO

def criar_usuario(usuario: UsuarioCreate):
    """
    Insere um novo usuário no banco de dados.
    O perfil define se ele é aluno, professor, coordenador ou administrador.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuario (
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                usuario.id_perfil,
                usuario.id_turma,
                usuario.nome,
                usuario.email,
                usuario.senha_hash,
                usuario.matricula,
                usuario.departamento,
                usuario.tipo_aluno,
                usuario.status,
                usuario.telefone,
                usuario.foto_perfil
            )
        )

        connection.commit()

        id_usuario_criado = cursor.lastrowid

        return buscar_usuario_por_id(id_usuario_criado)

    finally:
        connection.close()

def listar_usuarios():
    """
    Lista todos os usuários cadastrados
    A senha n é retornada por segurança
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_usuario,
            id_perfil,
            id_turma,
            nome,
            email,
            matricula,
            departamento,
            tipo_aluno,
            status,
            telefone,
            foto_perfil,
            data_cadastro,
            data_ultimo_acesso
        FROM usuario
        ORDER BY id_usuario
        """
    )

    usuarios = cursor.fetchall()

    connection.close()

    return [row_to_dict(usuario) for usuario in usuarios]


def buscar_usuario_por_id(id_usuario: int):
    """
    Busca um usuário específico pelo ID
    A senha não é retornada por segurança
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_usuario,
            id_perfil,
            id_turma,
            nome,
            email,
            matricula,
            departamento,
            tipo_aluno,
            status,
            telefone,
            foto_perfil,
            data_cadastro,
            data_ultimo_acesso
        FROM usuario
        WHERE id_usuario = ?
        """,
        (id_usuario,)
    )

    usuario = cursor.fetchone()

    connection.close()

    return row_to_dict(usuario)


# PROJETO

def criar_projeto(projeto: ProjetoCreate):
    """
    Insere um novo projeto no banco de dados
    Cada projeto pertence a uma turma, possui um aluno responsável pela submissão
    e um professor orientador
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_projeto_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO projeto (
                id_turma,
                id_usuario_submissor,
                id_professor_orientador,
                titulo,
                descricao,
                problema,
                solucao,
                status,
                publicado,
                slug_publico
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                projeto.id_turma,
                projeto.id_usuario_submissor,
                projeto.id_professor_orientador,
                projeto.titulo,
                projeto.descricao,
                projeto.problema,
                projeto.solucao,
                projeto.status,
                projeto.publicado,
                projeto.slug_publico
            )
        )

        connection.commit()
        id_projeto_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_projeto_por_id(id_projeto_criado)


def listar_projetos():
    """
    Lista todos os projetos cadastrados
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
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
        FROM projeto
        ORDER BY id_projeto
        """
    )

    projetos = cursor.fetchall()

    connection.close()

    return [row_to_dict(projeto) for projeto in projetos]


def buscar_projeto_por_id(id_projeto: int):
    """
    Busca um projeto específico pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
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
        FROM projeto
        WHERE id_projeto = ?
        """,
        (id_projeto,)
    )

    projeto = cursor.fetchone()

    connection.close()

    return row_to_dict(projeto)


# INTEGRANTE DO PROJETO

def adicionar_integrante_projeto(integrante: IntegranteProjetoCreate):
    """
    Adiciona um usuario como integrante de um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_integrante_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO integrante_projeto (
                id_usuario,
                id_projeto,
                funcao
            )
            VALUES (?, ?, ?)
            """,
            (
                integrante.id_usuario,
                integrante.id_projeto,
                integrante.funcao
            )
        )

        connection.commit()
        id_integrante_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_integrante_projeto_por_id(id_integrante_criado)


def listar_integrantes_por_projeto(id_projeto: int):
    """
    Lista todos os integrantes vinculados a um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_integrante_projeto,
            id_usuario,
            id_projeto,
            funcao,
            data_vinculo
        FROM integrante_projeto
        WHERE id_projeto = ?
        ORDER BY id_integrante_projeto
        """,
        (id_projeto,)
    )

    integrantes = cursor.fetchall()

    connection.close()

    return [row_to_dict(integrante) for integrante in integrantes]


def buscar_integrante_projeto_por_id(id_integrante_projeto: int):
    """
    Busca um vínculo especifico entre usuario e projeto
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_integrante_projeto,
            id_usuario,
            id_projeto,
            funcao,
            data_vinculo
        FROM integrante_projeto
        WHERE id_integrante_projeto = ?
        """,
        (id_integrante_projeto,)
    )

    integrante = cursor.fetchone()

    connection.close()

    return row_to_dict(integrante)


# TAG / TECNOLOGIA

def criar_tag_tecnologia(tag: TagTecnologiaCreate):
    """
    Insere uma nova tag, tecnologia, ferramenta, metodologia
    Ex: Angular, Python, FastAPI, SQLite3, Bootstrap
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_tag_criada = None

    try:
        cursor.execute(
            """
            INSERT INTO tag_tecnologia (
                nome,
                categoria,
                cor,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                tag.nome,
                tag.categoria,
                tag.cor,
                tag.status
            )
        )

        connection.commit()
        id_tag_criada = cursor.lastrowid

    finally:
        connection.close()

    return buscar_tag_tecnologia_por_id(id_tag_criada)


def listar_tags_tecnologia():
    """
    lista todas as tags e tecnologias cadastradas
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_tag,
            nome,
            categoria,
            cor,
            status,
            data_criacao
        FROM tag_tecnologia
        ORDER BY id_tag
        """
    )

    tags = cursor.fetchall()

    connection.close()

    return [row_to_dict(tag) for tag in tags]


def buscar_tag_tecnologia_por_id(id_tag: int):
    """
    Busca uma tag ou tecnologia pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_tag,
            nome,
            categoria,
            cor,
            status,
            data_criacao
        FROM tag_tecnologia
        WHERE id_tag = ?
        """,
        (id_tag,)
    )

    tag = cursor.fetchone()

    connection.close()

    return row_to_dict(tag)


# TAGS DO PROJETO

def adicionar_tag_ao_projeto(projeto_tag: ProjetoTagCreate):
    """
    Associa uma tag ou tecnologia a um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_projeto_tag_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO projeto_tag (
                id_projeto,
                id_tag
            )
            VALUES (?, ?)
            """,
            (
                projeto_tag.id_projeto,
                projeto_tag.id_tag
            )
        )

        connection.commit()
        id_projeto_tag_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_projeto_tag_por_id(id_projeto_tag_criado)


def listar_tags_por_projeto(id_projeto: int):
    """
    Lista as tags e tecnologias associadas a um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            projeto_tag.id_projeto_tag,
            projeto_tag.id_projeto,
            projeto_tag.id_tag,
            tag_tecnologia.nome,
            tag_tecnologia.categoria,
            tag_tecnologia.cor,
            tag_tecnologia.status
        FROM projeto_tag
        INNER JOIN tag_tecnologia
            ON projeto_tag.id_tag = tag_tecnologia.id_tag
        WHERE projeto_tag.id_projeto = ?
        ORDER BY projeto_tag.id_projeto_tag
        """,
        (id_projeto,)
    )

    tags = cursor.fetchall()

    connection.close()

    return [row_to_dict(tag) for tag in tags]


def buscar_projeto_tag_por_id(id_projeto_tag: int):
    """
    Busca uma associação específica entre projeto e tag
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_projeto_tag,
            id_projeto,
            id_tag
        FROM projeto_tag
        WHERE id_projeto_tag = ?
        """,
        (id_projeto_tag,)
    )

    projeto_tag = cursor.fetchone()

    connection.close()

    return row_to_dict(projeto_tag)


# COMPETÊNCIA

def criar_competencia(competencia: CompetenciaCreate):
    """
    Insere uma nova competência que pode ser demonstrada em projetos
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_competencia_criada = None

    try:
        cursor.execute(
            """
            INSERT INTO competencia (
                nome,
                descricao,
                categoria,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                competencia.nome,
                competencia.descricao,
                competencia.categoria,
                competencia.status
            )
        )

        connection.commit()
        id_competencia_criada = cursor.lastrowid

    finally:
        connection.close()

    return buscar_competencia_por_id(id_competencia_criada)


def listar_competencias():
    """
    Lista todas as competencias cadastradas
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_competencia,
            nome,
            descricao,
            categoria,
            status
        FROM competencia
        ORDER BY id_competencia
        """
    )

    competencias = cursor.fetchall()

    connection.close()

    return [row_to_dict(competencia) for competencia in competencias]


def buscar_competencia_por_id(id_competencia: int):
    """
    Busca uma competência especifica pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_competencia,
            nome,
            descricao,
            categoria,
            status
        FROM competencia
        WHERE id_competencia = ?
        """,
        (id_competencia,)
    )

    competencia = cursor.fetchone()

    connection.close()

    return row_to_dict(competencia)


# COMPETÊNCIAS DO PROJETO

def adicionar_competencia_ao_projeto(projeto_competencia: ProjetoCompetenciaCreate):
    """
    Associa uma competência a um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_projeto_competencia_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO projeto_competencia (
                id_projeto,
                id_competencia,
                nivel
            )
            VALUES (?, ?, ?)
            """,
            (
                projeto_competencia.id_projeto,
                projeto_competencia.id_competencia,
                projeto_competencia.nivel
            )
        )

        connection.commit()
        id_projeto_competencia_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_projeto_competencia_por_id(id_projeto_competencia_criado)


def listar_competencias_por_projeto(id_projeto: int):
    """
    Lista as competencias associadas a um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            projeto_competencia.id_projeto_competencia,
            projeto_competencia.id_projeto,
            projeto_competencia.id_competencia,
            projeto_competencia.nivel,
            competencia.nome,
            competencia.descricao,
            competencia.categoria,
            competencia.status
        FROM projeto_competencia
        INNER JOIN competencia
            ON projeto_competencia.id_competencia = competencia.id_competencia
        WHERE projeto_competencia.id_projeto = ?
        ORDER BY projeto_competencia.id_projeto_competencia
        """,
        (id_projeto,)
    )

    competencias = cursor.fetchall()

    connection.close()

    return [row_to_dict(competencia) for competencia in competencias]


def buscar_projeto_competencia_por_id(id_projeto_competencia: int):
    """
    Busca uma associação específica entre projeto e competência
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_projeto_competencia,
            id_projeto,
            id_competencia,
            nivel
        FROM projeto_competencia
        WHERE id_projeto_competencia = ?
        """,
        (id_projeto_competencia,)
    )

    projeto_competencia = cursor.fetchone()

    connection.close()

    return row_to_dict(projeto_competencia)


# VERSÃO DO PROJETO

def criar_versao_projeto(versao: VersaoProjetoCreate):
    """
    Insere uma nova versão de um projeto
    permite manter o histprico quando o aluno reenvia o projeto corrigido
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_versao_criada = None

    try:
        cursor.execute(
            """
            INSERT INTO versao_projeto (
                id_projeto,
                numero_versao,
                descricao_alteracao,
                status_versao
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                versao.id_projeto,
                versao.numero_versao,
                versao.descricao_alteracao,
                versao.status_versao
            )
        )

        connection.commit()
        id_versao_criada = cursor.lastrowid

    finally:
        connection.close()

    return buscar_versao_projeto_por_id(id_versao_criada)


def listar_versoes_por_projeto(id_projeto: int):
    """
    Lista todas as versões enviadas de um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_versao,
            id_projeto,
            numero_versao,
            descricao_alteracao,
            data_envio,
            status_versao
        FROM versao_projeto
        WHERE id_projeto = ?
        ORDER BY numero_versao
        """,
        (id_projeto,)
    )

    versoes = cursor.fetchall()

    connection.close()

    return [row_to_dict(versao) for versao in versoes]


def buscar_versao_projeto_por_id(id_versao: int):
    """
    Busca uma versão específica pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_versao,
            id_projeto,
            numero_versao,
            descricao_alteracao,
            data_envio,
            status_versao
        FROM versao_projeto
        WHERE id_versao = ?
        """,
        (id_versao,)
    )

    versao = cursor.fetchone()

    connection.close()

    return row_to_dict(versao)


# ARQUIVO DO PROJETO

def criar_arquivo_projeto(arquivo: ArquivoProjetoCreate):
    """
    Cadastra as informações de um arquivo vinculado ao projeto
    No momento, estamos registrando os dados do arquivo, não fazendo upload real
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_arquivo_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO arquivo_projeto (
                id_projeto,
                id_versao,
                nome_arquivo,
                tipo_arquivo,
                url_arquivo,
                tamanho_arquivo,
                principal,
                nivel_acesso
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                arquivo.id_projeto,
                arquivo.id_versao,
                arquivo.nome_arquivo,
                arquivo.tipo_arquivo,
                arquivo.url_arquivo,
                arquivo.tamanho_arquivo,
                arquivo.principal,
                arquivo.nivel_acesso
            )
        )

        connection.commit()
        id_arquivo_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_arquivo_projeto_por_id(id_arquivo_criado)


def listar_arquivos_por_projeto(id_projeto: int):
    """
    Lista todos os arquivos vinculados a um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_arquivo,
            id_projeto,
            id_versao,
            nome_arquivo,
            tipo_arquivo,
            url_arquivo,
            tamanho_arquivo,
            data_upload,
            principal,
            nivel_acesso
        FROM arquivo_projeto
        WHERE id_projeto = ?
        ORDER BY id_arquivo
        """,
        (id_projeto,)
    )

    arquivos = cursor.fetchall()

    connection.close()

    return [row_to_dict(arquivo) for arquivo in arquivos]


def buscar_arquivo_projeto_por_id(id_arquivo: int):
    """
    Busca um arquivo específico pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_arquivo,
            id_projeto,
            id_versao,
            nome_arquivo,
            tipo_arquivo,
            url_arquivo,
            tamanho_arquivo,
            data_upload,
            principal,
            nivel_acesso
        FROM arquivo_projeto
        WHERE id_arquivo = ?
        """,
        (id_arquivo,)
    )

    arquivo = cursor.fetchone()

    connection.close()

    return row_to_dict(arquivo)


# AVALIAÇÃO

def criar_avaliacao(avaliacao: AvaliacaoCreate):
    """
    Registra a avaliação feita pelo professor sobre uma versão do projeto
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_avaliacao_criada = None

    try:
        cursor.execute(
            """
            INSERT INTO avaliacao (
                id_projeto,
                id_versao,
                id_professor,
                parecer,
                status_resultante,
                nota_final
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                avaliacao.id_projeto,
                avaliacao.id_versao,
                avaliacao.id_professor,
                avaliacao.parecer,
                avaliacao.status_resultante,
                avaliacao.nota_final
            )
        )

        connection.commit()
        id_avaliacao_criada = cursor.lastrowid

    finally:
        connection.close()

    return buscar_avaliacao_por_id(id_avaliacao_criada)


def listar_avaliacoes_por_projeto(id_projeto: int):
    """
    Lista todas as avaliações registradas para um projeto.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_avaliacao,
            id_projeto,
            id_versao,
            id_professor,
            parecer,
            status_resultante,
            nota_final,
            data_avaliacao
        FROM avaliacao
        WHERE id_projeto = ?
        ORDER BY id_avaliacao
        """,
        (id_projeto,)
    )

    avaliacoes = cursor.fetchall()

    connection.close()

    return [row_to_dict(avaliacao) for avaliacao in avaliacoes]


def buscar_avaliacao_por_id(id_avaliacao: int):
    """
    Busca uma avaliação específica pelo ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_avaliacao,
            id_projeto,
            id_versao,
            id_professor,
            parecer,
            status_resultante,
            nota_final,
            data_avaliacao
        FROM avaliacao
        WHERE id_avaliacao = ?
        """,
        (id_avaliacao,)
    )

    avaliacao = cursor.fetchone()

    connection.close()

    return row_to_dict(avaliacao)


# PORTFÓLIO

def criar_portfolio(portfolio: PortfolioCreate):
    """
    Cria um portfólio para um usuario
    Normalmente esse usuário será um aluno
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_portfolio_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO portfolio (
                id_usuario,
                titulo,
                bio,
                slug_publico,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                portfolio.id_usuario,
                portfolio.titulo,
                portfolio.bio,
                portfolio.slug_publico,
                portfolio.status
            )
        )

        connection.commit()
        id_portfolio_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_portfolio_por_id(id_portfolio_criado)


def listar_portfolios():
    """
    Lista todos os portfolios cadastrados
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_portfolio,
            id_usuario,
            titulo,
            bio,
            slug_publico,
            status,
            data_criacao,
            data_atualizacao
        FROM portfolio
        ORDER BY id_portfolio
        """
    )

    portfolios = cursor.fetchall()

    connection.close()

    return [row_to_dict(portfolio) for portfolio in portfolios]


def buscar_portfolio_por_id(id_portfolio: int):
    """
    busca um portfolio pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_portfolio,
            id_usuario,
            titulo,
            bio,
            slug_publico,
            status,
            data_criacao,
            data_atualizacao
        FROM portfolio
        WHERE id_portfolio = ?
        """,
        (id_portfolio,)
    )

    portfolio = cursor.fetchone()

    connection.close()

    return row_to_dict(portfolio)


def buscar_portfolio_por_usuario(id_usuario: int):
    """
    Busca o portfólio de um usuário especifico
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_portfolio,
            id_usuario,
            titulo,
            bio,
            slug_publico,
            status,
            data_criacao,
            data_atualizacao
        FROM portfolio
        WHERE id_usuario = ?
        """,
        (id_usuario,)
    )

    portfolio = cursor.fetchone()

    connection.close()

    return row_to_dict(portfolio)


# PROJETOS NO PORTFÓLIO

def adicionar_projeto_ao_portfolio(portfolio_projeto: PortfolioProjetoCreate):
    """
    Adiciona um projeto ao portfólio de um usuario
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_portfolio_projeto_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO portfolio_projeto (
                id_portfolio,
                id_projeto,
                ordem_exibicao,
                destaque
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                portfolio_projeto.id_portfolio,
                portfolio_projeto.id_projeto,
                portfolio_projeto.ordem_exibicao,
                portfolio_projeto.destaque
            )
        )

        connection.commit()
        id_portfolio_projeto_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_portfolio_projeto_por_id(id_portfolio_projeto_criado)


def listar_projetos_por_portfolio(id_portfolio: int):
    """
    Lista os projetos adicionados a um portfólio
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_portfolio_projeto,
            id_portfolio,
            id_projeto,
            ordem_exibicao,
            destaque,
            data_adicao
        FROM portfolio_projeto
        WHERE id_portfolio = ?
        ORDER BY ordem_exibicao, id_portfolio_projeto
        """,
        (id_portfolio,)
    )

    projetos = cursor.fetchall()

    connection.close()

    return [row_to_dict(projeto) for projeto in projetos]


def buscar_portfolio_projeto_por_id(id_portfolio_projeto: int):
    """
    Busca um vínculo específico entre portfólio e projeto.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_portfolio_projeto,
            id_portfolio,
            id_projeto,
            ordem_exibicao,
            destaque,
            data_adicao
        FROM portfolio_projeto
        WHERE id_portfolio_projeto = ?
        """,
        (id_portfolio_projeto,)
    )

    portfolio_projeto = cursor.fetchone()

    connection.close()

    return row_to_dict(portfolio_projeto)


# CONSENTIMENTO DE PUBLICAÇÃO

def registrar_consentimento_publicacao(consentimento: ConsentimentoPublicacaoCreate):
    """
    Registra se um usuário autorizou ou não a publicação de um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_consentimento_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO consentimento_publicacao (
                id_projeto,
                id_usuario,
                autorizado,
                observacao
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                consentimento.id_projeto,
                consentimento.id_usuario,
                consentimento.autorizado,
                consentimento.observacao
            )
        )

        connection.commit()
        id_consentimento_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_consentimento_publicacao_por_id(id_consentimento_criado)


def listar_consentimentos_por_projeto(id_projeto: int):
    """
    Lista todos os consentimentos registrados para um projeto
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_consentimento,
            id_projeto,
            id_usuario,
            autorizado,
            observacao,
            data_consentimento
        FROM consentimento_publicacao
        WHERE id_projeto = ?
        ORDER BY id_consentimento
        """,
        (id_projeto,)
    )

    consentimentos = cursor.fetchall()

    connection.close()

    return [row_to_dict(consentimento) for consentimento in consentimentos]


def buscar_consentimento_publicacao_por_id(id_consentimento: int):
    """
    Busca um consentimento específico pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_consentimento,
            id_projeto,
            id_usuario,
            autorizado,
            observacao,
            data_consentimento
        FROM consentimento_publicacao
        WHERE id_consentimento = ?
        """,
        (id_consentimento,)
    )

    consentimento = cursor.fetchone()

    connection.close()

    return row_to_dict(consentimento)

# =========================
# NOTIFICAÇÕES
# =========================

def criar_notificacao(notificacao: NotificacaoCreate):
    """
    Cria uma notificação para um usuário.
    Exemplo: projeto aprovado, revisão solicitada ou projeto publicado.
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_notificacao_criada = None

    try:
        cursor.execute(
            """
            INSERT INTO notificacao (
                id_usuario,
                titulo,
                mensagem,
                tipo,
                lida,
                link_destino
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                notificacao.id_usuario,
                notificacao.titulo,
                notificacao.mensagem,
                notificacao.tipo,
                notificacao.lida,
                notificacao.link_destino
            )
        )

        connection.commit()
        id_notificacao_criada = cursor.lastrowid

    finally:
        connection.close()

    return buscar_notificacao_por_id(id_notificacao_criada)


def listar_notificacoes_por_usuario(id_usuario: int):
    """
    Lista todas as notificações de um usuário.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_notificacao,
            id_usuario,
            titulo,
            mensagem,
            tipo,
            lida,
            link_destino,
            data_criacao
        FROM notificacao
        WHERE id_usuario = ?
        ORDER BY id_notificacao DESC
        """,
        (id_usuario,)
    )

    notificacoes = cursor.fetchall()

    connection.close()

    return [row_to_dict(notificacao) for notificacao in notificacoes]


def buscar_notificacao_por_id(id_notificacao: int):
    """
    Busca uma notificação específica pelo ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_notificacao,
            id_usuario,
            titulo,
            mensagem,
            tipo,
            lida,
            link_destino,
            data_criacao
        FROM notificacao
        WHERE id_notificacao = ?
        """,
        (id_notificacao,)
    )

    notificacao = cursor.fetchone()

    connection.close()

    return row_to_dict(notificacao)


def marcar_notificacao_como_lida(id_notificacao: int): # quando o cara abrir uma notificação no front-end. A API vai poder mudar lida de 0 para 1.
    """
    Marca uma notificação como lida.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE notificacao
            SET lida = 1
            WHERE id_notificacao = ?
            """,
            (id_notificacao,)
        )

        connection.commit()

    finally:
        connection.close()

    return buscar_notificacao_por_id(id_notificacao)


# RELATÓRIOS

def criar_relatorio(relatorio: RelatorioCreate):
    """
    Registra um relatório gerado no sistema.
    """

    connection = get_connection()
    cursor = connection.cursor()
    id_relatorio_criado = None

    try:
        cursor.execute(
            """
            INSERT INTO relatorio (
                id_usuario,
                tipo_relatorio,
                filtros,
                formato,
                caminho_arquivo,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                relatorio.id_usuario,
                relatorio.tipo_relatorio,
                relatorio.filtros,
                relatorio.formato,
                relatorio.caminho_arquivo,
                relatorio.status
            )
        )

        connection.commit()
        id_relatorio_criado = cursor.lastrowid

    finally:
        connection.close()

    return buscar_relatorio_por_id(id_relatorio_criado)


def listar_relatorios():
    """
    Lista todos os relatorios registrados no sistema
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_relatorio,
            id_usuario,
            tipo_relatorio,
            filtros,
            formato,
            caminho_arquivo,
            status,
            data_geracao
        FROM relatorio
        ORDER BY id_relatorio DESC
        """
    )

    relatorios = cursor.fetchall()

    connection.close()

    return [row_to_dict(relatorio) for relatorio in relatorios]


def listar_relatorios_por_usuario(id_usuario: int):
    """
    Lista todos os relatórios gerados por um usuário específico
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_relatorio,
            id_usuario,
            tipo_relatorio,
            filtros,
            formato,
            caminho_arquivo,
            status,
            data_geracao
        FROM relatorio
        WHERE id_usuario = ?
        ORDER BY id_relatorio DESC
        """,
        (id_usuario,)
    )

    relatorios = cursor.fetchall()

    connection.close()

    return [row_to_dict(relatorio) for relatorio in relatorios]


def buscar_relatorio_por_id(id_relatorio: int):
    """
    Busca um relatorio específico pelo ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id_relatorio,
            id_usuario,
            tipo_relatorio,
            filtros,
            formato,
            caminho_arquivo,
            status,
            data_geracao
        FROM relatorio
        WHERE id_relatorio = ?
        """,
        (id_relatorio,)
    )

    relatorio = cursor.fetchone()

    connection.close()

    return row_to_dict(relatorio)


# VITRINE PÚBLICA

def listar_projetos_publicos():
    """
    Lista os projetos publicados na vitrine pública
    Por agora, considera público todo projeto com publicado = 1
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            projeto.id_projeto,
            projeto.titulo,
            projeto.descricao,
            projeto.problema,
            projeto.solucao,
            projeto.status,
            projeto.publicado,
            projeto.slug_publico,
            projeto.data_submissao,
            projeto.data_aprovacao,
            turma.nome AS turma,
            curso.nome AS curso,
            curso.sigla AS sigla_curso
        FROM projeto
        INNER JOIN turma
            ON projeto.id_turma = turma.id_turma
        INNER JOIN curso
            ON turma.id_curso = curso.id_curso
        WHERE projeto.publicado = 1
        ORDER BY projeto.data_aprovacao DESC
        """
    )

    projetos = cursor.fetchall()

    connection.close()

    return [row_to_dict(projeto) for projeto in projetos]


def buscar_projeto_publico_por_slug(slug_publico: str):
    """
    Busca um projeto publico pelo slug
    Ex de slug: sistema-viva
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            projeto.id_projeto,
            projeto.titulo,
            projeto.descricao,
            projeto.problema,
            projeto.solucao,
            projeto.status,
            projeto.publicado,
            projeto.slug_publico,
            projeto.data_submissao,
            projeto.data_aprovacao,
            turma.nome AS turma,
            curso.nome AS curso,
            curso.sigla AS sigla_curso
        FROM projeto
        INNER JOIN turma
            ON projeto.id_turma = turma.id_turma
        INNER JOIN curso
            ON turma.id_curso = curso.id_curso
        WHERE projeto.publicado = 1
        AND projeto.slug_publico = ?
        """,
        (slug_publico,)
    )

    projeto = cursor.fetchone()

    connection.close()

    return row_to_dict(projeto)


# PUBLICAÇÃO DE PROJETO

def publicar_projeto(id_projeto: int):
    """
    Publica um projeto na vitrine pública
    Ao publicar o projeto passa a aparecer nos endpoints publicos
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE projeto
            SET
                publicado = 1,
                status = 'aprovado',
                data_aprovacao = COALESCE(data_aprovacao, CURRENT_TIMESTAMP), 
                data_atualizacao = CURRENT_TIMESTAMP
            WHERE id_projeto = ?
            """,
            (id_projeto,)
        )

        connection.commit()

    finally:
        connection.close()

    return buscar_projeto_por_id(id_projeto)
# linha 2064 = se data_aprovacao ainda estiver vazia, coloque a data atual; se já tiver uma data, mantenha a data antiga
# evita trocar a data de aprovação toda vez que alguem chamar o endpoint