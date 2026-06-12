from typing import Optional # uma variável pode ser de um tipo específico ou None
from pydantic import BaseModel #  Importa a classe base do Pydantic para criar modelos de dados 
                               #  Ao herdar de BaseModel, seus campos são automaticamente validados e convertidos para tipos definidos


# MODELOS DE PERFIL

class PerfilCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    status: str


class PerfilResponse(BaseModel):
    id_perfil: int
    nome: str
    descricao: Optional[str] = None
    status: str


# MODELOS DE CURSO

class CursoCreate(BaseModel):
    nome: str
    sigla: str
    descricao: Optional[str] = None
    status: str


class CursoResponse(BaseModel):
    id_curso: int
    nome: str
    sigla: str
    descricao: Optional[str] = None
    status: str


# MODELOS DE TURMA

class TurmaCreate(BaseModel):
    id_curso: int
    nome: str
    semestre: str
    ano: int
    turno: str
    status: str


class TurmaResponse(BaseModel):
    id_turma: int
    id_curso: int
    nome: str
    semestre: str
    ano: int
    turno: str
    status: str


# MODELOS DE USUÁRIO

class UsuarioCreate(BaseModel):
    id_perfil: int
    id_turma: Optional[int] = None
    nome: str
    email: str
    senha_hash: str
    matricula: Optional[str] = None
    departamento: Optional[str] = None
    tipo_aluno: Optional[str] = None
    status: str
    telefone: Optional[str] = None
    foto_perfil: Optional[str] = None


class UsuarioResponse(BaseModel):
    id_usuario: int
    id_perfil: int
    id_turma: Optional[int] = None
    nome: str
    email: str
    matricula: Optional[str] = None
    departamento: Optional[str] = None
    tipo_aluno: Optional[str] = None
    status: str
    telefone: Optional[str] = None
    foto_perfil: Optional[str] = None
    data_cadastro: Optional[str] = None
    data_ultimo_acesso: Optional[str] = None


# MODELOS DE PROJETO

class ProjetoCreate(BaseModel):
    id_turma: int
    id_usuario_submissor: int
    id_professor_orientador: int
    titulo: str
    descricao: str
    problema: Optional[str] = None
    solucao: Optional[str] = None
    status: str
    publicado: int = 0
    slug_publico: Optional[str] = None


class ProjetoResponse(BaseModel):
    id_projeto: int
    id_turma: int
    id_usuario_submissor: int
    id_professor_orientador: int
    titulo: str
    descricao: str
    problema: Optional[str] = None
    solucao: Optional[str] = None
    status: str
    publicado: int
    slug_publico: Optional[str] = None
    data_submissao: Optional[str] = None
    data_aprovacao: Optional[str] = None
    data_atualizacao: Optional[str] = None


# MODELOS DE INTEGRANTE DO PROJETO

class IntegranteProjetoCreate(BaseModel):
    id_usuario: int
    id_projeto: int
    funcao: str


class IntegranteProjetoResponse(BaseModel):
    id_integrante_projeto: int
    id_usuario: int
    id_projeto: int
    funcao: str
    data_vinculo: Optional[str] = None


# MODELOS DE TAG / TECNOLOGIA

class TagTecnologiaCreate(BaseModel):
    nome: str
    categoria: str
    cor: Optional[str] = None
    status: str


class TagTecnologiaResponse(BaseModel):
    id_tag: int
    nome: str
    categoria: str
    cor: Optional[str] = None
    status: str
    data_criacao: Optional[str] = None


# MODELOS DE TAGS DO PROJETO

class ProjetoTagCreate(BaseModel):
    id_projeto: int
    id_tag: int


class ProjetoTagResponse(BaseModel):
    id_projeto_tag: int
    id_projeto: int
    id_tag: int


# MODELOS DE COMPETENCIA

class CompetenciaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    categoria: str
    status: str


class CompetenciaResponse(BaseModel):
    id_competencia: int
    nome: str
    descricao: Optional[str] = None
    categoria: str
    status: str


# MODELOS DE COMPETÊNCIAS DO PROJETO

class ProjetoCompetenciaCreate(BaseModel):
    id_projeto: int
    id_competencia: int
    nivel: str


class ProjetoCompetenciaResponse(BaseModel):
    id_projeto_competencia: int
    id_projeto: int
    id_competencia: int
    nivel: str


# MODELOS AUXILIARES PARA ROTAS ANINHADAS

# Pq na documentação o endpoint ta assim: /api/v1/projetos/{id_projeto}/integrantes
# Aí o id_projeto já vem pela URL ent não precisa repetir ele no JSON. o Json fica mais limpinho

class IntegranteProjetoVincular(BaseModel):
    id_usuario: int
    funcao: str


class ProjetoTagVincular(BaseModel):
    id_tag: int


class ProjetoCompetenciaVincular(BaseModel):
    id_competencia: int
    nivel: str


# MODELOS DE VERSÃO DO PROJETO

class VersaoProjetoCreate(BaseModel):
    id_projeto: int
    numero_versao: int
    descricao_alteracao: Optional[str] = None
    status_versao: str


class VersaoProjetoResponse(BaseModel):
    id_versao: int
    id_projeto: int
    numero_versao: int
    descricao_alteracao: Optional[str] = None
    data_envio: Optional[str] = None
    status_versao: str


# MODELOS DE ARQUIVO DO PROJETO

class ArquivoProjetoCreate(BaseModel):
    id_projeto: int
    id_versao: Optional[int] = None
    nome_arquivo: str
    tipo_arquivo: str
    url_arquivo: str
    tamanho_arquivo: Optional[int] = None
    principal: int = 0
    nivel_acesso: str


class ArquivoProjetoResponse(BaseModel):
    id_arquivo: int
    id_projeto: int
    id_versao: Optional[int] = None
    nome_arquivo: str
    tipo_arquivo: str
    url_arquivo: str
    tamanho_arquivo: Optional[int] = None
    data_upload: Optional[str] = None
    principal: int
    nivel_acesso: str


# MODELOS DE AVALIAÇÃO

class AvaliacaoCreate(BaseModel):
    id_projeto: int
    id_versao: int
    id_professor: int
    parecer: str
    status_resultante: str
    nota_final: Optional[float] = None


class AvaliacaoResponse(BaseModel):
    id_avaliacao: int
    id_projeto: int
    id_versao: int
    id_professor: int
    parecer: str
    status_resultante: str
    nota_final: Optional[float] = None
    data_avaliacao: Optional[str] = None


# MODELOS AUXILIARES PARA VERSÕES, ARQUIVOS E AVALIAÇOES
# MESMA LOGICA DO ANTERIOR

class VersaoProjetoVincular(BaseModel):
    numero_versao: int
    descricao_alteracao: Optional[str] = None
    status_versao: str


class ArquivoProjetoVincular(BaseModel):
    id_versao: Optional[int] = None
    nome_arquivo: str
    tipo_arquivo: str
    url_arquivo: str
    tamanho_arquivo: Optional[int] = None
    principal: int = 0
    nivel_acesso: str


class AvaliacaoVincular(BaseModel):
    id_versao: int
    id_professor: int
    parecer: str
    status_resultante: str
    nota_final: Optional[float] = None


# MODELOS DE PORTFOLIO

class PortfolioCreate(BaseModel):
    id_usuario: int
    titulo: str
    bio: Optional[str] = None
    slug_publico: Optional[str] = None
    status: str


class PortfolioResponse(BaseModel):
    id_portfolio: int
    id_usuario: int
    titulo: str
    bio: Optional[str] = None
    slug_publico: Optional[str] = None
    status: str
    data_criacao: Optional[str] = None
    data_atualizacao: Optional[str] = None


# MODELOS DE PROJETO NO PORTFÓLIO

class PortfolioProjetoCreate(BaseModel):
    id_portfolio: int
    id_projeto: int
    ordem_exibicao: Optional[int] = None
    destaque: int = 0


class PortfolioProjetoResponse(BaseModel):
    id_portfolio_projeto: int
    id_portfolio: int
    id_projeto: int
    ordem_exibicao: Optional[int] = None
    destaque: int
    data_adicao: Optional[str] = None


# MODELOS DE CONSENTIMENTO DE PUBLICAÇÃO

class ConsentimentoPublicacaoCreate(BaseModel):
    id_projeto: int
    id_usuario: int
    autorizado: int
    observacao: Optional[str] = None


class ConsentimentoPublicacaoResponse(BaseModel):
    id_consentimento: int
    id_projeto: int
    id_usuario: int
    autorizado: int
    observacao: Optional[str] = None
    data_consentimento: Optional[str] = None

# MODELOS AUXILIARES PARA PORTFÓLIO E CONSENTIMENTO
# MESMA LOGICA DO ANTERIOR, inves de mandar no corpo passa na url

class PortfolioProjetoVincular(BaseModel):
    id_projeto: int
    ordem_exibicao: Optional[int] = None
    destaque: int = 0


class ConsentimentoPublicacaoVincular(BaseModel):
    id_usuario: int
    autorizado: int
    observacao: Optional[str] = None


# MODELOS DE NOTIFICAÇÃO

class NotificacaoCreate(BaseModel):
    id_usuario: int
    titulo: str
    mensagem: str
    tipo: str
    lida: int = 0
    link_destino: Optional[str] = None


class NotificacaoResponse(BaseModel):
    id_notificacao: int
    id_usuario: int
    titulo: str
    mensagem: str
    tipo: str
    lida: int
    link_destino: Optional[str] = None
    data_criacao: Optional[str] = None


# MODELOS DE RELATÓRIO

class RelatorioCreate(BaseModel):
    id_usuario: int
    tipo_relatorio: str
    filtros: Optional[str] = None
    formato: str
    caminho_arquivo: Optional[str] = None
    status: str


class RelatorioResponse(BaseModel):
    id_relatorio: int
    id_usuario: int
    tipo_relatorio: str
    filtros: Optional[str] = None
    formato: str
    caminho_arquivo: Optional[str] = None
    status: str
    data_geracao: Optional[str] = None