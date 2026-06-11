from typing import Optional
from pydantic import BaseModel


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