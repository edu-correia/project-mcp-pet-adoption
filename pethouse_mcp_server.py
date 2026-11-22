import datetime
import os
from typing import Any, Dict, List, Optional
import httpx

# Compatibilidade garantida tanto para MCP v1 (FastMCP) quanto para v2 (MCPServer)
try:
  from mcp.server.fastmcp import FastMCP

  mcp = FastMCP("PetHouse-MCP-Server")
except (ImportError, ModuleNotFoundError):
  from mcp.server.mcpserver import MCPServer

  mcp = MCPServer(name="PetHouse-MCP-Server")

# URL base real da API PetHouse conforme documentação do Swagger
API_BASE_URL = os.getenv("PETHOUSE_API_URL", "http://localhost:3333").rstrip("/")


async def _fazer_requisicao(
    metodo: str, endpoint: str, **kwargs
) -> Dict[str, Any] | List[Any]:
  """Função auxiliar para executar requisições HTTP seguras à API do PetHouse."""
  url = f"{API_BASE_URL}{endpoint}"
  try:
    async with httpx.AsyncClient(timeout=10.0) as client:
      response = await client.request(metodo, url, **kwargs)
      response.raise_for_status()

      # Se a resposta for vazia (ex: status 204 ou DELETE)
      if not response.content:
        return {"sucesso": True, "status_code": response.status_code}

      return response.json()
  except httpx.HTTPStatusError as e:
    return {
        "erro": True,
        "status_code": e.response.status_code,
        "mensagem": f"Erro HTTP {e.response.status_code}: {e.response.text}",
    }
  except httpx.RequestError as e:
    return {
        "erro": True,
        "mensagem": (
            f"Não foi possível conectar à API PetHouse em {url}. Certifique-se"
            f" de que o backend está rodando na porta 3333. Detalhes: {str(e)}"
        ),
    }


# =====================================================================
# RECURSOS (RESOURCES)
# =====================================================================


@mcp.resource("pethouse://estatisticas")
async def obter_estatisticas_gerais() -> str:
  """Retorna um panorama geral: total de pets (posts), usuários e denúncias ativas."""
  posts = await _fazer_requisicao("GET", "/posts/all")
  users = await _fazer_requisicao("GET", "/users/all")
  complaints = await _fazer_requisicao("GET", "/complaints/all")

  total_posts = len(posts) if isinstance(posts, list) else 0
  total_users = len(users) if isinstance(users, list) else 0
  total_complaints = len(complaints) if isinstance(complaints, list) else 0

  return (
      f"Estatísticas PetHouse:\n"
      f"- Total de Pets/Posts cadastrados: {total_posts}\n"
      f"- Total de Usuários/Adotantes: {total_users}\n"
      f"- Total de Denúncias: {total_complaints}"
  )


@mcp.resource("pethouse://racas")
async def listar_racas_disponiveis() -> str:
  """Lista todas as raças distintas de pets atualmente publicadas."""
  posts = await _fazer_requisicao("GET", "/posts/all")
  if not isinstance(posts, list):
    return "Nenhum pet encontrado."

  racas = sorted(
      list(set(p.get("breed") for p in posts if p.get("breed") is not None))
  )
  return "Raças cadastradas: " + (", ".join(racas) if racas else "Nenhuma")


# =====================================================================
# FERRAMENTAS (TOOLS) - PETS (POSTS)
# =====================================================================


@mcp.tool()
async def listar_todos_os_pets() -> List[Dict[str, Any]] | Dict[str, Any]:
  """Lista todos os posts de pets disponíveis para adoção cadastrados no PetHouse."""
  return await _fazer_requisicao("GET", "/posts/all")


@mcp.tool()
async def buscar_pet_por_criterios(
    raca: Optional[str] = None,
    idade_maxima: Optional[int] = None,
    termo_busca: Optional[str] = None,
) -> List[Dict[str, Any]] | Dict[str, Any]:
  """Busca e filtra pets cadastrados por raça, idade máxima ou palavra-chave (no nome ou descrição).

  Parâmetros:
  - raca: Raça do pet (ex: 'Rottweiler', 'Vira-lata', 'Poodle').
  - idade_maxima: Idade máxima em anos.
  - termo_busca: Palavra para buscar no nome ou na descrição do post.
  """
  posts = await _fazer_requisicao("GET", "/posts/all")
  if isinstance(posts, dict) and posts.get("erro"):
    return posts

  if not isinstance(posts, list):
    return []

  resultados = []
  for post in posts:
    # Filtro por raça
    if raca and raca.lower() not in (post.get("breed") or "").lower():
      continue

    # Filtro por idade máxima
    if idade_maxima is not None:
      idade_pet = post.get("age")
      if idade_pet is None or idade_pet > idade_maxima:
        continue

    # Filtro por termo genérico (nome ou descrição)
    if termo_busca:
      termo = termo_busca.lower()
      nome = (post.get("name") or "").lower()
      desc = (post.get("description") or "").lower()
      if termo not in nome and termo not in desc:
        continue

    resultados.append(post)

  return resultados


@mcp.tool()
async def obter_detalhes_do_pet(post_id: int) -> Dict[str, Any]:
  """Obtém as informações detalhadas de um pet específico a partir do seu ID.

  Parâmetros:
  - post_id: ID numérico do post do pet.
  """
  return await _fazer_requisicao("GET", f"/posts/{post_id}")


@mcp.tool()
async def cadastrar_pet_para_adocao(
    description: str,
    name: Optional[str] = None,
    breed: Optional[str] = None,
    age: Optional[int] = None,
    owner_id: Optional[int] = 1,
    photo_url: Optional[str] = None,
) -> Dict[str, Any]:
  """Cria uma nova publicação de pet para adoção.

  Parâmetros:
  - description: Descrição do pet e do post (obrigatório).
  - name: Nome do pet.
  - breed: Raça do pet (ex: 'SRD', 'Golden', 'Siamês').
  - age: Idade do pet em anos.
  - owner_id: ID do usuário dono da publicação (padrão: 1).
  - photo_url: Link da foto do pet.
  """
  payload = {
      "description": description,
      "name": name,
      "breed": breed,
      "age": age,
      "ownerId": owner_id,
      "photoUrl": photo_url,
      "createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  }
  # Remove campos nulos para não enviar dados desnecessários
  payload = {k: v for k, v in payload.items() if v is not None}
  return await _fazer_requisicao("POST", "/posts", json=payload)


@mcp.tool()
async def remover_pet(post_id: int) -> Dict[str, Any]:
  """Remove uma publicação de pet (útil quando o pet já foi adotado).

  Parâmetros:
  - post_id: ID do post a ser deletado.
  """
  return await _fazer_requisicao("DELETE", f"/posts/{post_id}")


# =====================================================================
# FERRAMENTAS (TOOLS) - USUÁRIOS / ADOTANTES
# =====================================================================


@mcp.tool()
async def listar_usuarios() -> List[Dict[str, Any]] | Dict[str, Any]:
  """Lista todos os usuários/adotantes cadastrados no sistema."""
  return await _fazer_requisicao("GET", "/users/all")


@mcp.tool()
async def cadastrar_usuario(
    name: str,
    email: str,
    password: str,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
  """Cadastra um novo usuário ou adotante no sistema PetHouse.

  Parâmetros:
  - name: Nome completo do usuário.
  - email: E-mail para login e contato.
  - password: Senha de acesso.
  - phone: Telefone de contato.
  - address: Endereço do usuário.
  - description: Breve biografia ou informações sobre a casa/perfil do adotante.
  """
  payload = {
      "name": name,
      "email": email,
      "password": password,
      "phone": phone,
      "address": address,
      "description": description,
      "permissions": 1,
  }
  payload = {k: v for k, v in payload.items() if v is not None}
  return await _fazer_requisicao("POST", "/users", json=payload)


@mcp.tool()
async def obter_usuario_por_id(user_id: int) -> Dict[str, Any]:
  """Retorna os dados detalhados de um usuário/adotante pelo ID."""
  return await _fazer_requisicao("GET", f"/users/{user_id}")


# =====================================================================
# FERRAMENTAS (TOOLS) - INTERAÇÕES (CURTIDAS, REAÇÕES, AVALIAÇÕES)
# =====================================================================


@mcp.tool()
async def curtir_ou_descurtir_pet(user_id: int, post_id: int) -> Dict[str, Any]:
  """Alterna o 'like' (curtida/interesse) de um usuário em um post de pet.

  Parâmetros:
  - user_id: ID do usuário que está curtindo.
  - post_id: ID do pet que recebeu o interesse.
  """
  payload = {"userId": user_id, "postId": post_id}
  return await _fazer_requisicao("POST", "/reactions/toggleLike", json=payload)


@mcp.tool()
async def obter_total_curtidas_do_pet(post_id: int) -> Dict[str, Any]:
  """Retorna a contagem total de curtidas/reações de um pet específico.

  Parâmetros:
  - post_id: ID do post do pet.
  """
  return await _fazer_requisicao("GET", f"/reactions/total/{post_id}")


@mcp.tool()
async def obter_media_avaliacao_usuario(user_id: int) -> Dict[str, Any]:
  """Calcula a nota média de reputação de um usuário/tutor.

  Parâmetros:
  - user_id: ID do usuário a ser consultado.
  """
  return await _fazer_requisicao("GET", f"/ratings/average/{user_id}")


@mcp.tool()
async def criar_denuncia(
    reporter_user_id: int, reported_post_id: int, reason: str
) -> Dict[str, Any]:
  """Registra uma denúncia contra um post de pet suspeito ou impróprio.

  Parâmetros:
  - reporter_user_id: ID do usuário denunciante.
  - reported_post_id: ID do post denunciado.
  - reason: Motivo da denúncia.
  """
  payload = {
      "reporterUserId": reporter_user_id,
      "reportedPostId": reported_post_id,
      "reason": reason,
  }
  return await _fazer_requisicao("POST", "/complaints", json=payload)


if __name__ == "__main__":
  # Executa o servidor MCP via STDIO
  mcp.run()