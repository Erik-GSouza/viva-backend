from sqlite3 import IntegrityError

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import create_tables
from models import (
    PerfilCreate,
    PerfilResponse,
    CursoCreate,
    CursoResponse,
    TurmaCreate,
    TurmaResponse,
    UsuarioCreate,
    UsuarioResponse,
    ProjetoCreate,
    ProjetoResponse,
    IntegranteProjetoCreate,
    IntegranteProjetoResponse,
    IntegranteProjetoVincular,
    TagTecnologiaCreate,
    TagTecnologiaResponse,
    ProjetoTagCreate,
    ProjetoTagResponse,
    ProjetoTagVincular,
    CompetenciaCreate,
    CompetenciaResponse,
    ProjetoCompetenciaCreate,
    ProjetoCompetenciaResponse,
    ProjetoCompetenciaVincular,
    VersaoProjetoCreate,
    VersaoProjetoResponse,
    VersaoProjetoVincular,
    ArquivoProjetoCreate,
    ArquivoProjetoResponse,
    ArquivoProjetoVincular,
    AvaliacaoCreate,
    AvaliacaoResponse,
    AvaliacaoVincular,
    PortfolioCreate,
    PortfolioResponse,
    PortfolioProjetoCreate,
    PortfolioProjetoResponse,
    PortfolioProjetoVincular,
    ConsentimentoPublicacaoCreate,
    ConsentimentoPublicacaoResponse,
    ConsentimentoPublicacaoVincular,
    NotificacaoCreate,
    NotificacaoResponse,
    RelatorioCreate,
    RelatorioResponse,
    ProjetoPublicoResponse,
    LoginRequest,
    LoginResponse,
    ProjetoStatusUpdate,
    StatusUpdate,
    UsuarioUpdate,
    CursoUpdate,
    TurmaUpdate
)

from repository import (
    criar_perfil,
    listar_perfis,
    buscar_perfil_por_id,
    criar_curso,
    listar_cursos,
    buscar_curso_por_id,
    criar_turma,
    listar_turmas,
    buscar_turma_por_id,
    criar_usuario,
    listar_usuarios,
    buscar_usuario_por_id,
    criar_projeto,
    listar_projetos,
    buscar_projeto_por_id,
    adicionar_integrante_projeto,
    listar_integrantes_por_projeto,
    criar_tag_tecnologia,
    listar_tags_tecnologia,
    buscar_tag_tecnologia_por_id,
    adicionar_tag_ao_projeto,
    listar_tags_por_projeto,
    criar_competencia,
    listar_competencias,
    buscar_competencia_por_id,
    adicionar_competencia_ao_projeto,
    listar_competencias_por_projeto,
    criar_versao_projeto,
    listar_versoes_por_projeto,
    buscar_versao_projeto_por_id,
    criar_arquivo_projeto,
    listar_arquivos_por_projeto,
    buscar_arquivo_projeto_por_id,
    criar_avaliacao,
    listar_avaliacoes_por_projeto,
    buscar_avaliacao_por_id,
    criar_portfolio,
    listar_portfolios,
    buscar_portfolio_por_id,
    buscar_portfolio_por_usuario,
    adicionar_projeto_ao_portfolio,
    listar_projetos_por_portfolio,
    buscar_portfolio_projeto_por_id,
    registrar_consentimento_publicacao,
    listar_consentimentos_por_projeto,
    buscar_consentimento_publicacao_por_id,
    criar_notificacao,
    listar_notificacoes_por_usuario,
    buscar_notificacao_por_id,
    marcar_notificacao_como_lida,
    criar_relatorio,
    listar_relatorios,
    listar_relatorios_por_usuario,
    buscar_relatorio_por_id,
    listar_projetos_publicos,
    buscar_projeto_publico_por_slug,
    publicar_projeto,
    autenticar_usuario,
    atualizar_status_projeto,
    aprovar_projeto,
    solicitar_revisao_projeto,
    rejeitar_projeto,
    atualizar_usuario,
    atualizar_status_usuario,
    atualizar_curso,
    atualizar_status_curso,
    atualizar_turma,
    atualizar_status_turma
)

# Cria as tabelas do banco de dados quando a API iniciar
create_tables()

app = FastAPI(
    title="VIVA API",
    description="Back-end do sistema VIVA com FastAPI e SQLite3.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "API do VIVA funcionando!"}


# ENDPOINTS DE PERFIL

@app.post("/api/v1/perfis", response_model=PerfilResponse, status_code=201)
def endpoint_criar_perfil(perfil: PerfilCreate):
    """
    Cadastra um novo perfil de usuário.
    Exemplos: Aluno, Professor, Coordenador ou Administrador.
    """

    try:
        return criar_perfil(perfil)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o perfil. Verifique se o nome já está cadastrado."
        )


@app.get("/api/v1/perfis", response_model=list[PerfilResponse])
def endpoint_listar_perfis():
    """
    Lista todos os perfis cadastrados
    """

    return listar_perfis()


@app.get("/api/v1/perfis/{id_perfil}", response_model=PerfilResponse)
def endpoint_buscar_perfil_por_id(id_perfil: int):
    """
    Busca um perfil específico pelo ID
    """

    perfil = buscar_perfil_por_id(id_perfil)

    if perfil is None:
        raise HTTPException(
            status_code=404,
            detail="Perfil não encontrado."
        )

    return perfil


# ENDPOINTS DE CURSO

@app.post("/api/v1/cursos", response_model=CursoResponse, status_code=201)
def endpoint_criar_curso(curso: CursoCreate):
    """
    Cadastra um novo curso.
    """

    try:
        return criar_curso(curso)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o curso. Verifique se a sigla já está cadastrada."
        )


@app.get("/api/v1/cursos", response_model=list[CursoResponse])
def endpoint_listar_cursos():
    """
    Lista todos os cursos cadastrados
    """

    return listar_cursos()


@app.get("/api/v1/cursos/{id_curso}", response_model=CursoResponse)
def endpoint_buscar_curso_por_id(id_curso: int):
    """
    Busca um curso específico pelo ID
    """

    curso = buscar_curso_por_id(id_curso)

    if curso is None:
        raise HTTPException(
            status_code=404,
            detail="Curso não encontrado."
        )

    return curso


# ENDPOINTS DE TURMA

@app.post("/api/v1/turmas", response_model=TurmaResponse, status_code=201)
def endpoint_criar_turma(turma: TurmaCreate):
    """
    Cadastra uma nova turma
    Cada turma precisa estar vinculada a um curso existente
    """

    try:
        return criar_turma(turma)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar a turma. Verifique se o curso informado existe."
        )


@app.get("/api/v1/turmas", response_model=list[TurmaResponse])
def endpoint_listar_turmas():
    """
    Lista todas as turmas cadastradas
    """

    return listar_turmas()


@app.get("/api/v1/turmas/{id_turma}", response_model=TurmaResponse)
def endpoint_buscar_turma_por_id(id_turma: int):
    """
    Busca uma turma específica pelo ID
    """

    turma = buscar_turma_por_id(id_turma)

    if turma is None:
        raise HTTPException(
            status_code=404,
            detail="Turma não encontrada."
        )

    return turma


# ENDPOINTS DE USUARIO

@app.post("/api/v1/usuarios", response_model=UsuarioResponse, status_code=201)
def endpoint_criar_usuario(usuario: UsuarioCreate):
    """
    Cadastra um novo usuaio
    O usuário precisa estar vinculado a um perfil existente
    A turma é opcional, pq nem todo usuário será aluno
    """

    try:
        return criar_usuario(usuario)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o usuário. Verifique perfil, turma, e-mail ou matrícula."
        )


@app.get("/api/v1/usuarios", response_model=list[UsuarioResponse])
def endpoint_listar_usuarios():
    """
    Lista todos os usuarios cadastrados
    senha não retornada
    """

    return listar_usuarios()


@app.get("/api/v1/usuarios/{id_usuario}", response_model=UsuarioResponse)
def endpoint_buscar_usuario_por_id(id_usuario: int):
    """
    Busca um usuário específico pelo ID
    senha não retornada
    """

    usuario = buscar_usuario_por_id(id_usuario)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario


# ENDPOINTS DE PROJETO

@app.post("/api/v1/projetos", response_model=ProjetoResponse, status_code=201)
def endpoint_criar_projeto(projeto: ProjetoCreate):
    """
    Submete um novo Projeto Integrador
    """

    try:
        return criar_projeto(projeto)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o projeto. Verifique turma, usuário submissor, professor orientador ou slug público."
        )


@app.get("/api/v1/projetos", response_model=list[ProjetoResponse])
def endpoint_listar_projetos():
    """
    Lista todos os projetos cadastrados
    """

    return listar_projetos()


@app.get("/api/v1/projetos/{id_projeto}", response_model=ProjetoResponse)
def endpoint_buscar_projeto_por_id(id_projeto: int):
    """
    busca um projeto específico pelo ID
    """

    projeto = buscar_projeto_por_id(id_projeto)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    return projeto


# ENDPOINTS DE INTEGRANTES DO PROJETO

@app.post("/api/v1/projetos/{id_projeto}/integrantes", response_model=IntegranteProjetoResponse, status_code=201)
def endpoint_adicionar_integrante_projeto(id_projeto: int, integrante: IntegranteProjetoVincular):
    """
    Adiciona um integrante a um projeto
    só lembrando que ID do projeto vem pela URL
    """

    try:
        dados_integrante = IntegranteProjetoCreate(
            id_usuario=integrante.id_usuario,
            id_projeto=id_projeto,
            funcao=integrante.funcao
        )

        return adicionar_integrante_projeto(dados_integrante)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível adicionar o integrante. Verifique se o usuário e o projeto existem ou se o integrante já foi adicionado."
        )


@app.get("/api/v1/projetos/{id_projeto}/integrantes", response_model=list[IntegranteProjetoResponse])
def endpoint_listar_integrantes_por_projeto(id_projeto: int):
    """
    lista os integrantes de um projeto
    """

    return listar_integrantes_por_projeto(id_projeto)


# ENDPOINTS DE TAGS / TECNOLOGIAS

@app.post("/api/v1/tags", response_model=TagTecnologiaResponse, status_code=201)
def endpoint_criar_tag_tecnologia(tag: TagTecnologiaCreate):
    """
    cadastra uma nova tag, tecnologia, ferramenta, metodologia
    """

    try:
        return criar_tag_tecnologia(tag)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar a tag. Verifique se o nome já está cadastrado."
        )


@app.get("/api/v1/tags", response_model=list[TagTecnologiaResponse])
def endpoint_listar_tags_tecnologia():
    """
    lista todas as tags e tecnologias cadastradas
    """

    return listar_tags_tecnologia()


@app.get("/api/v1/tags/{id_tag}", response_model=TagTecnologiaResponse)
def endpoint_buscar_tag_tecnologia_por_id(id_tag: int):
    """
    Busca uma tag / tecnologia específica pelo ID
    """

    tag = buscar_tag_tecnologia_por_id(id_tag)

    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Tag ou tecnologia não encontrada."
        )

    return tag


# ENDPOINTS DE TAGS DO PROJETO

@app.post("/api/v1/projetos/{id_projeto}/tags", response_model=ProjetoTagResponse, status_code=201)
def endpoint_adicionar_tag_ao_projeto(id_projeto: int, tag: ProjetoTagVincular):
    """
    associa uma tag ou tecnologia a um projeto
    ID do projeto vem pela URL
    """

    try:
        dados_projeto_tag = ProjetoTagCreate(
            id_projeto=id_projeto,
            id_tag=tag.id_tag
        )

        return adicionar_tag_ao_projeto(dados_projeto_tag)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível associar a tag ao projeto. Verifique se o projeto e a tag existem ou se essa tag já foi adicionada ao projeto."
        )


@app.get("/api/v1/projetos/{id_projeto}/tags")
def endpoint_listar_tags_por_projeto(id_projeto: int):
    """
    Lista as tags e tecnologias associadas a um projeto.
    """

    return listar_tags_por_projeto(id_projeto)


# ENDPOINTS DE COMPETÊNCIAS

@app.post("/api/v1/competencias", response_model=CompetenciaResponse, status_code=201)
def endpoint_criar_competencia(competencia: CompetenciaCreate):
    """
    cadastra uma nova competência
    """

    try:
        return criar_competencia(competencia)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar a competência. Verifique se o nome já está cadastrado."
        )


@app.get("/api/v1/competencias", response_model=list[CompetenciaResponse])
def endpoint_listar_competencias():
    """
    lista todas as competências cadastradas
    """

    return listar_competencias()


@app.get("/api/v1/competencias/{id_competencia}", response_model=CompetenciaResponse)
def endpoint_buscar_competencia_por_id(id_competencia: int):
    """
    Busca uma competência específica pelo ID.
    """

    competencia = buscar_competencia_por_id(id_competencia)

    if competencia is None:
        raise HTTPException(
            status_code=404,
            detail="Competência não encontrada."
        )

    return competencia


# ENDPOINTS DE COMPETÊNCIAS DO PROJETO

@app.post("/api/v1/projetos/{id_projeto}/competencias", response_model=ProjetoCompetenciaResponse, status_code=201)
def endpoint_adicionar_competencia_ao_projeto(id_projeto: int, competencia: ProjetoCompetenciaVincular):
    """
    Associa uma competência a um projeto
    ID do projeto vem pela URL
    """

    try:
        dados_projeto_competencia = ProjetoCompetenciaCreate(
            id_projeto=id_projeto,
            id_competencia=competencia.id_competencia,
            nivel=competencia.nivel
        )

        return adicionar_competencia_ao_projeto(dados_projeto_competencia)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível associar a competência ao projeto. Verifique se o projeto e a competência existem ou se essa competência já foi adicionada ao projeto."
        )


@app.get("/api/v1/projetos/{id_projeto}/competencias")
def endpoint_listar_competencias_por_projeto(id_projeto: int):
    """
    lista as competências associadas a um projeto.
    """

    return listar_competencias_por_projeto(id_projeto)


# ENDPOINTS DE VERSÕES DO PROJETO

@app.post("/api/v1/projetos/{id_projeto}/versoes", response_model=VersaoProjetoResponse, status_code=201)
def endpoint_criar_versao_projeto(id_projeto: int, versao: VersaoProjetoVincular):
    """
    Cria uma nova versão para um projeto
    O ID do projeto vem da url
    """

    try:
        dados_versao = VersaoProjetoCreate(
            id_projeto=id_projeto,
            numero_versao=versao.numero_versao,
            descricao_alteracao=versao.descricao_alteracao,
            status_versao=versao.status_versao
        )

        return criar_versao_projeto(dados_versao)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar a versão. Verifique se o projeto existe ou se esse número de versão já foi cadastrado."
        )


@app.get("/api/v1/projetos/{id_projeto}/versoes", response_model=list[VersaoProjetoResponse])
def endpoint_listar_versoes_por_projeto(id_projeto: int):
    """
    Lista todas as versões de um projeto.
    """

    return listar_versoes_por_projeto(id_projeto)


@app.get("/api/v1/projetos/{id_projeto}/versoes/{id_versao}", response_model=VersaoProjetoResponse)
def endpoint_buscar_versao_projeto_por_id(id_projeto: int, id_versao: int):
    """
    Busca uma versão específica de um projeto.
    """

    versao = buscar_versao_projeto_por_id(id_versao)

    if versao is None or versao["id_projeto"] != id_projeto:
        raise HTTPException(
            status_code=404,
            detail="Versão não encontrada para este projeto."
        )

    return versao


# ENDPOINTS DE ARQUIVOS DO PROJETO

@app.post("/api/v1/projetos/{id_projeto}/arquivos", response_model=ArquivoProjetoResponse, status_code=201)
def endpoint_criar_arquivo_projeto(id_projeto: int, arquivo: ArquivoProjetoVincular):
    """
    Cadastra as informações de um arquivo vinculado ao projeto
    """

    try:
        dados_arquivo = ArquivoProjetoCreate(
            id_projeto=id_projeto,
            id_versao=arquivo.id_versao,
            nome_arquivo=arquivo.nome_arquivo,
            tipo_arquivo=arquivo.tipo_arquivo,
            url_arquivo=arquivo.url_arquivo,
            tamanho_arquivo=arquivo.tamanho_arquivo,
            principal=arquivo.principal,
            nivel_acesso=arquivo.nivel_acesso
        )

        return criar_arquivo_projeto(dados_arquivo)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível cadastrar o arquivo. Verifique se o projeto e a versão informados existem."
        )


@app.get("/api/v1/projetos/{id_projeto}/arquivos", response_model=list[ArquivoProjetoResponse])
def endpoint_listar_arquivos_por_projeto(id_projeto: int):
    """
    Lsta todos os arquivos vinculados a um projeto
    """

    return listar_arquivos_por_projeto(id_projeto)


@app.get("/api/v1/projetos/{id_projeto}/arquivos/{id_arquivo}", response_model=ArquivoProjetoResponse)
def endpoint_buscar_arquivo_projeto_por_id(id_projeto: int, id_arquivo: int):
    """
    Busca um arquivo específico de um projeto
    """

    arquivo = buscar_arquivo_projeto_por_id(id_arquivo)

    if arquivo is None or arquivo["id_projeto"] != id_projeto:
        raise HTTPException(
            status_code=404,
            detail="Arquivo não encontrado para este projeto."
        )

    return arquivo


# ENDPOINTS DE AVALIAÇÕES

@app.post("/api/v1/projetos/{id_projeto}/avaliacoes", response_model=AvaliacaoResponse, status_code=201)
def endpoint_criar_avaliacao(id_projeto: int, avaliacao: AvaliacaoVincular):
    """
    Registra uma avaliação feita pelo professor para uma ver. do projeto
    """

    try:
        dados_avaliacao = AvaliacaoCreate(
            id_projeto=id_projeto,
            id_versao=avaliacao.id_versao,
            id_professor=avaliacao.id_professor,
            parecer=avaliacao.parecer,
            status_resultante=avaliacao.status_resultante,
            nota_final=avaliacao.nota_final
        )

        return criar_avaliacao(dados_avaliacao)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível registrar a avaliação. Verifique se projeto, versão e professor existem."
        )


@app.get("/api/v1/projetos/{id_projeto}/avaliacoes", response_model=list[AvaliacaoResponse])
def endpoint_listar_avaliacoes_por_projeto(id_projeto: int):
    """
    Lista todas as avaliaçOes de um projeto.
    """

    return listar_avaliacoes_por_projeto(id_projeto)


@app.get("/api/v1/avaliacoes/{id_avaliacao}", response_model=AvaliacaoResponse)
def endpoint_buscar_avaliacao_por_id(id_avaliacao: int):
    """
    Busca uma avaliação especIfica pelo ID
    """

    avaliacao = buscar_avaliacao_por_id(id_avaliacao)

    if avaliacao is None:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada."
        )

    return avaliacao


# ENDPOINTS DE PORTFÓLIO

@app.post("/api/v1/portfolios", response_model=PortfolioResponse, status_code=201)
def endpoint_criar_portfolio(portfolio: PortfolioCreate):
    """
    cria um portfólio para um usuario
    Normalmente será usado para criar o portfolio de um aluno
    """

    try:
        return criar_portfolio(portfolio)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o portfólio. Verifique se o usuário existe ou se ele já possui um portfólio."
        )


@app.get("/api/v1/portfolios", response_model=list[PortfolioResponse])
def endpoint_listar_portfolios():
    """
    lista todos os portfolios cadastrados
    """

    return listar_portfolios()


@app.get("/api/v1/portfolios/{id_portfolio}", response_model=PortfolioResponse)
def endpoint_buscar_portfolio_por_id(id_portfolio: int):
    """
    Busca um portfólio pelo ID
    """

    portfolio = buscar_portfolio_por_id(id_portfolio)

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Portfólio não encontrado."
        )

    return portfolio


@app.get("/api/v1/usuarios/{id_usuario}/portfolio", response_model=PortfolioResponse)
def endpoint_buscar_portfolio_por_usuario(id_usuario: int):
    """
    Busca o portfolio de um usuário específico
    """

    portfolio = buscar_portfolio_por_usuario(id_usuario)

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Este usuário ainda não possui portfólio."
        )

    return portfolio


# ENDPOINTS DE PROJETOS NO PORTFÓLIO

@app.post("/api/v1/portfolios/{id_portfolio}/projetos", response_model=PortfolioProjetoResponse, status_code=201)
def endpoint_adicionar_projeto_ao_portfolio(id_portfolio: int, portfolio_projeto: PortfolioProjetoVincular):
    """
    adiciona um projeto ao portfólio
    O ID do portfolio vem pela url
    """

    try:
        dados_portfolio_projeto = PortfolioProjetoCreate(
            id_portfolio=id_portfolio,
            id_projeto=portfolio_projeto.id_projeto,
            ordem_exibicao=portfolio_projeto.ordem_exibicao,
            destaque=portfolio_projeto.destaque
        )

        return adicionar_projeto_ao_portfolio(dados_portfolio_projeto)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível adicionar o projeto ao portfólio. Verifique se o portfólio e o projeto existem ou se esse projeto já foi adicionado."
        )


@app.get("/api/v1/portfolios/{id_portfolio}/projetos", response_model=list[PortfolioProjetoResponse])
def endpoint_listar_projetos_por_portfolio(id_portfolio: int):
    """
    Lista os projetos adicionados a um portfólio
    """

    return listar_projetos_por_portfolio(id_portfolio)


@app.get("/api/v1/portfolios/{id_portfolio}/projetos/{id_portfolio_projeto}", response_model=PortfolioProjetoResponse)
def endpoint_buscar_portfolio_projeto_por_id(id_portfolio: int, id_portfolio_projeto: int):
    """
    busca um vínculo específico entre portfolio e projeto.
    """

    portfolio_projeto = buscar_portfolio_projeto_por_id(id_portfolio_projeto)

    if portfolio_projeto is None or portfolio_projeto["id_portfolio"] != id_portfolio:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado neste portfólio."
        )

    return portfolio_projeto


# ENDPOINTS DE CONSENTIMENTO DE PUBLICAÇÃO

@app.post("/api/v1/projetos/{id_projeto}/consentimentos", response_model=ConsentimentoPublicacaoResponse, status_code=201)
def endpoint_registrar_consentimento_publicacao(id_projeto: int, consentimento: ConsentimentoPublicacaoVincular):
    """
    Registra se um usuario autorizou ou não a publicação de um projeto
    """

    try:
        dados_consentimento = ConsentimentoPublicacaoCreate(
            id_projeto=id_projeto,
            id_usuario=consentimento.id_usuario,
            autorizado=consentimento.autorizado,
            observacao=consentimento.observacao
        )

        return registrar_consentimento_publicacao(dados_consentimento)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível registrar o consentimento. Verifique se o projeto e o usuário existem ou se esse consentimento já foi registrado."
        )


@app.get("/api/v1/projetos/{id_projeto}/consentimentos", response_model=list[ConsentimentoPublicacaoResponse])
def endpoint_listar_consentimentos_por_projeto(id_projeto: int):
    """
    Lista os consentimentos de publicação de um projeto
    """

    return listar_consentimentos_por_projeto(id_projeto)


@app.get("/api/v1/consentimentos/{id_consentimento}", response_model=ConsentimentoPublicacaoResponse)
def endpoint_buscar_consentimento_publicacao_por_id(id_consentimento: int):
    """
    Busca um consentimento específico pelo ID
    """

    consentimento = buscar_consentimento_publicacao_por_id(id_consentimento)

    if consentimento is None:
        raise HTTPException(
            status_code=404,
            detail="Consentimento não encontrado."
        )

    return consentimento


# ENDPOINTS DE NOTIFICAÇÕES

@app.post("/api/v1/notificacoes", response_model=NotificacaoResponse, status_code=201)
def endpoint_criar_notificacao(notificacao: NotificacaoCreate):
    """
    cria uma notificação para um usuário
    """

    try:
        return criar_notificacao(notificacao)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar a notificação. Verifique se o usuário informado existe."
        )


@app.get("/api/v1/usuarios/{id_usuario}/notificacoes", response_model=list[NotificacaoResponse])
def endpoint_listar_notificacoes_por_usuario(id_usuario: int):
    """
    lista todas as notificaçoes de um usuário
    """

    return listar_notificacoes_por_usuario(id_usuario)


@app.get("/api/v1/notificacoes/{id_notificacao}", response_model=NotificacaoResponse)
def endpoint_buscar_notificacao_por_id(id_notificacao: int):
    """
    Busca uma notificação específica pelo ID
    """

    notificacao = buscar_notificacao_por_id(id_notificacao)

    if notificacao is None:
        raise HTTPException(
            status_code=404,
            detail="Notificação não encontrada."
        )

    return notificacao


@app.patch("/api/v1/notificacoes/{id_notificacao}/marcar-como-lida", response_model=NotificacaoResponse)
def endpoint_marcar_notificacao_como_lida(id_notificacao: int):
    """
    Marca uma notificação como lida
    """

    notificacao = marcar_notificacao_como_lida(id_notificacao)

    if notificacao is None:
        raise HTTPException(
            status_code=404,
            detail="Notificação não encontrada."
        )

    return notificacao


# ENDPOINTS DE RELATÓRIOS

@app.post("/api/v1/relatorios", response_model=RelatorioResponse, status_code=201)
def endpoint_criar_relatorio(relatorio: RelatorioCreate):
    """
    Registra um relatório gerado no sistema.
    """

    try:
        return criar_relatorio(relatorio)

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o relatório. Verifique se o usuário informado existe."
        )


@app.get("/api/v1/relatorios", response_model=list[RelatorioResponse])
def endpoint_listar_relatorios():
    """
    Lista todos os relatórios registrados no sistema
    """

    return listar_relatorios()


@app.get("/api/v1/usuarios/{id_usuario}/relatorios", response_model=list[RelatorioResponse])
def endpoint_listar_relatorios_por_usuario(id_usuario: int):
    """
    lista todos os relatórios gerados por um usuário específico
    """

    return listar_relatorios_por_usuario(id_usuario)


@app.get("/api/v1/relatorios/{id_relatorio}", response_model=RelatorioResponse)
def endpoint_buscar_relatorio_por_id(id_relatorio: int):
    """
    Busca um relatorio específico pelo ID
    """

    relatorio = buscar_relatorio_por_id(id_relatorio)

    if relatorio is None:
        raise HTTPException(
            status_code=404,
            detail="Relatório não encontrado."
        )

    return relatorio


# ENDPOINTS DA VITRINE PÚBLICA

@app.get("/api/v1/publico/projetos", response_model=list[ProjetoPublicoResponse])
def endpoint_listar_projetos_publicos():
    """
    Lista os projetos publicados na vitrine pública
    """

    return listar_projetos_publicos()


@app.get("/api/v1/publico/projetos/{slug_publico}", response_model=ProjetoPublicoResponse)
def endpoint_buscar_projeto_publico_por_slug(slug_publico: str):
    """
    Busca um projeto público pelo slug
    """

    projeto = buscar_projeto_publico_por_slug(slug_publico)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto público não encontrado."
        )

    return projeto


# ENDPOINT DE PUBLICAÇÃO DE PROJETO

@app.patch("/api/v1/projetos/{id_projeto}/publicar", response_model=ProjetoResponse)
def endpoint_publicar_projeto(id_projeto: int):
    """
    Publica um projeto na vitrine pública
    """

    projeto = publicar_projeto(id_projeto)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    return projeto


# ENDPOINT DE LOGIN

@app.post("/api/v1/login", response_model=LoginResponse)
def endpoint_login(dados_login: LoginRequest):
    """
    faz login no sistema
    """

    usuario = autenticar_usuario(
        dados_login.email,
        dados_login.senha
    )

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos, ou usuário inativo."
        )

    return usuario


# ENDPOINTS DE STATUS E AÇÕES DO PROJETO

@app.patch("/api/v1/projetos/{id_projeto}/status", response_model=ProjetoResponse)
def endpoint_atualizar_status_projeto(id_projeto: int, dados_status: ProjetoStatusUpdate):
    """
    Atualiza o status de um projeto
    """

    projeto = atualizar_status_projeto(
        id_projeto,
        dados_status.status
    )

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    return projeto


@app.patch("/api/v1/projetos/{id_projeto}/aprovar", response_model=ProjetoResponse)
def endpoint_aprovar_projeto(id_projeto: int):
    """
    Aprova um projeto
    """

    projeto = aprovar_projeto(id_projeto)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    return projeto


@app.patch("/api/v1/projetos/{id_projeto}/solicitar-revisao", response_model=ProjetoResponse)
def endpoint_solicitar_revisao_projeto(id_projeto: int):
    """
    Solicita revisão de um projeto
    """

    projeto = solicitar_revisao_projeto(id_projeto)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    return projeto


@app.patch("/api/v1/projetos/{id_projeto}/rejeitar", response_model=ProjetoResponse)
def endpoint_rejeitar_projeto(id_projeto: int):
    """
    Rejeita um projeto
    """

    projeto = rejeitar_projeto(id_projeto)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    return projeto


# ENDPOINTS DE ATUALIZAÇÃO DE USUÁRIOS

@app.put("/api/v1/usuarios/{id_usuario}", response_model=UsuarioResponse)
def endpoint_atualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    """
    Atualiza os dados de um usuário.
    """

    try:
        usuario_atualizado = atualizar_usuario(id_usuario, usuario)

        if usuario_atualizado is None:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        return usuario_atualizado

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível atualizar o usuário. Verifique se perfil, turma, e-mail ou matrícula são válidos."
        )


@app.patch("/api/v1/usuarios/{id_usuario}/status", response_model=UsuarioResponse)
def endpoint_atualizar_status_usuario(id_usuario: int, dados_status: StatusUpdate):
    """
    Atualiza apenas o status de um usuario
    """

    usuario = atualizar_status_usuario(id_usuario, dados_status.status)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario


# ENDPOINTS DE ATUALIZAÇÃO DE CURSOS

@app.put("/api/v1/cursos/{id_curso}", response_model=CursoResponse)
def endpoint_atualizar_curso(id_curso: int, curso: CursoUpdate):
    """
    Atualiza os dados de um curso.
    """

    try:
        curso_atualizado = atualizar_curso(id_curso, curso)

        if curso_atualizado is None:
            raise HTTPException(
                status_code=404,
                detail="Curso não encontrado."
            )

        return curso_atualizado

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível atualizar o curso. Verifique se os dados informados são válidos."
        )


@app.patch("/api/v1/cursos/{id_curso}/status", response_model=CursoResponse)
def endpoint_atualizar_status_curso(id_curso: int, dados_status: StatusUpdate):
    """
    Atualiza apenas o status de um curso.
    """

    curso = atualizar_status_curso(id_curso, dados_status.status)

    if curso is None:
        raise HTTPException(
            status_code=404,
            detail="Curso não encontrado."
        )

    return curso


# ENDPOINTS DE ATUALIZAÇÃO DE TURMAS

@app.put("/api/v1/turmas/{id_turma}", response_model=TurmaResponse)
def endpoint_atualizar_turma(id_turma: int, turma: TurmaUpdate):
    """
    Atualiza os dados de uma turma
    """

    try:
        turma_atualizada = atualizar_turma(id_turma, turma)

        if turma_atualizada is None:
            raise HTTPException(
                status_code=404,
                detail="Turma não encontrada."
            )

        return turma_atualizada

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível atualizar a turma. Verifique se o curso informado existe."
        )


@app.patch("/api/v1/turmas/{id_turma}/status", response_model=TurmaResponse)
def endpoint_atualizar_status_turma(id_turma: int, dados_status: StatusUpdate):
    """
    Atualiza apenas o status de uma turma
    """

    turma = atualizar_status_turma(id_turma, dados_status.status)

    if turma is None:
        raise HTTPException(
            status_code=404,
            detail="Turma não encontrada."
        )

    return turma