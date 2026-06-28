# VIVA Back-end

Back-end do sistema **VIVA — Vitrine de Inovação e Valor Acadêmico**, desenvolvido para centralizar, organizar, avaliar, divulgar e preservar Projetos Integradores da Faculdade Senac.

O projeto utiliza **Python com FastAPI** no back-end e **SQLite3** como banco de dados embutido.

## Tecnologias utilizadas

* Python
* FastAPI
* Uvicorn
* Pydantic
* SQLite3

## Funcionalidades principais do back-end

* Cadastro e listagem de perfis
* Cadastro, listagem e atualização de usuários
* Login simples para o MVP
* Cadastro, listagem e atualização de cursos e turmas
* Submissão e gerenciamento de projetos
* Controle de integrantes dos projetos
* Cadastro e associação de tags/tecnologias
* Cadastro e associação de competências
* Controle de versões dos projetos
* Cadastro de arquivos vinculados aos projetos
* Avaliações de projetos
* Portfólio acadêmico dos alunos
* Consentimento de publicação
* Notificações
* Relatórios
* Vitrine pública de projetos
* Filtros na vitrine pública
* Resumo para dashboard do coordenador

## Como rodar o projeto

### 1. Clonar ou baixar o repositório

Acesse a pasta do projeto pelo terminal.

```powershell
cd viva-backend
```

### 2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Quando o ambiente estiver ativo, o terminal deve mostrar algo assim:

```powershell
(.venv) PS C:\caminho\do\projeto>
```

### 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 5. Rodar a API

```powershell
python -m uvicorn main:app --reload
```

### 6. Acessar a API

Página inicial da API:

```txt
http://127.0.0.1:8000
```

Documentação Swagger:

```txt
http://127.0.0.1:8000/docs
```

## Banco de dados

O projeto utiliza SQLite3. O arquivo do banco é criado automaticamente com o nome:

```txt
viva.db
```

Esse arquivo é gerado localmente quando a API é executada.

## Dados iniciais para teste

Como o arquivo `viva.db` é gerado localmente e não é enviado para o GitHub, o banco de dados nasce vazio quando o projeto é clonado em uma nova máquina.

Para facilitar os testes, o back cria automaticamente alguns dados iniciais quando a API é executada pela primeira vez

Esses dados incluem:

* Perfis do sistema;
* Curso de demonstração;
* Turma de demonstração;
* Usuários de teste;
* Tags e tecnologias;
* Competências;
* Projetos de exemplo;
* Portfólio público de aluno;
* Notificações iniciais.

### Usuários de teste

| Perfil        | Nome           | E-mail                                                              | Senha  |
| ------------- | -------------- | ------------------------------------------------------------------- | ------ |
| Aluno         | Yuji Itadori   | [yuji.itadori@jujutsu.local](mailto:yuji.itadori@jujutsu.local)     | 123456 |
| Professor     | Satoru Gojo    | [satoru.gojo@jujutsu.local](mailto:satoru.gojo@jujutsu.local)       | 123456 |
| Coordenador   | Masamichi Yaga | [masamichi.yaga@jujutsu.local](mailto:masamichi.yaga@jujutsu.local) | 123456 |
| Administrador | Ryomen Sukuna  | [ryomen.sukuna@jujutsu.local](mailto:ryomen.sukuna@jujutsu.local)   | 123456 |

## Observação sobre autenticação

A autenticação implementada neste MVP é simples, validando e-mail, senha e status ativo do usuário.

Em uma versão futura, o sistema poderá evoluir para autenticação com senha criptografada etc.

## Observação sobre arquivos

Neste MVP, os arquivos dos projetos são cadastrados no banco por meio de informações como nome, tipo, caminho e nível de acesso.

O upload físico de arquivos PDF poderá ser implementado em uma etapa futura.

## Integração com o front-end

O CORS já está configurado para permitir comunicação com o front-end Angular rodando em:

```txt
http://localhost:4200
```

ou

```txt
http://127.0.0.1:4200
```

## Equipe

* ERIK GUILHERME
* HÁLLEFE DANIEL
* BARBARA SIQUEIRA
* CID JOSÉ
* MATHEUS DE ARAÚJO
* VINICIUS MEDEIROS