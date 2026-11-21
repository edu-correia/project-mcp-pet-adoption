import os
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Inicializa o servidor MCP
mcp = FastMCP(name="PetHouse-MCP-Server")

# URL base da sua API REST PetHouse (ajuste via variável de ambiente ou use o padrão)
API_BASE_URL = os.getenv("PETHOUSE_API_URL", "http://localhost:3000").rstrip("/")


async def _fazer_requisicao(
    metodo: str, endpoint: str, **kwargs
) -> Dict[str, Any] | List[Any]:
  """Função auxiliar para chamadas HTTP seguras à API do PetHouse."""
  url = f"{API_BASE_URL}{endpoint}"
  try:
    async with httpx.AsyncClient(timeout=10.0) as client:
      response = await client.request(metodo, url, **kwargs)
      response.raise_for_status()
      return response.json()
  except httpx.HTTPStatusError as e:
    return {
        "erro": True,
        "status_code": e.response.status_code,
        "mensagem": f"Erro retornado pela API: {e.response.text}",
    }
  except httpx.RequestError as e:
    return {
        "erro": True,
        "mensagem": (
            f"Não foi possível conectar à API PetHouse em {url}. O servidor"
            f" está rodando? Detalhes: {str(e)}"
        ),
    }


# =====================================================================
# RECURSOS (RESOURCES)
# =====================================================================


@mcp.resource("pethouse://estatisticas")
async def obter_estatisticas_abrigo() -> str:
  """Fornece um resumo contextual sobre o total de pets cadastrados e disponíveis."""
  resultado = await _fazer_requisicao("GET", "/pets")
  if isinstance(resultado, dict) and resultado.get("erro"):
    return "Estatísticas indisponíveis no momento (API offline)."

  pets = resultado if isinstance(resultado, list) else []
  total = len(pets)
  disponiveis = sum(1 for p in pets if p.get("status") == "disponivel")
  adotados = sum(1 for p in pets if p.get("status") == "adotado")

  return f"Total de Pets: {total} | Disponíveis: {disponiveis} | Adotados: {adotados}"


# =====================================================================
# FERRAMENTAS (TOOLS)
# =====================================================================


@mcp.tool()
async def listar_pets_disponiveis() -> List[Dict[str, Any]] | Dict[str, Any]:
  """Lista todos os pets cadastrados que estão disponíveis para adoção."""
  # Envia query param status=disponivel
  return await _fazer_requisicao(
      "GET", "/pets", params={"status": "disponivel"}
  )


@mcp.tool()
async def buscar_pet_por_criterios(
    especie: Optional[str] = None,
    porte: Optional[str] = None,
    idade_maxima: Optional[int] = None,
    raca: Optional[str] = None,
) -> List[Dict[str, Any]] | Dict[str, Any]:
  """Filtra e busca pets disponíveis por critérios específicos: espécie, porte, raça ou idade máxima.

  Parâmetros:
  - especie: Ex: 'cachorro', 'gato'
  - porte: Ex: 'pequeno', 'medio', 'grande'
  - idade_maxima: idade limite em anos
  - raca: raça desejada
  """
  params = {"status": "disponivel"}
  if especie:
    params["especie"] = especie
  if porte:
    params["porte"] = porte
  if idade_maxima is not None:
    params["idade_max"] = str(idade_maxima)
  if raca:
    params["raca"] = raca

  return await _fazer_requisicao("GET", "/pets", params=params)


@mcp.tool()
async def cadastrar_adotante(nome: str, cpf: str, telefone: str) -> Dict[str, Any]:
  """Cadastra um novo adotante no sistema PetHouse.

  Parâmetros:
  - nome: Nome completo do adotante.
  - cpf: CPF do adotante (ex: '123.456.789-00').
  - telefone: Telefone para contato com DDD.
  """
  payload = {"nome": nome, "cpf": cpf, "telefone": telefone}
  return await _fazer_requisicao("POST", "/adotantes", json=payload)


@mcp.tool()
async def registrar_adocao(pet_id: int, adotante_id: int) -> Dict[str, Any]:
  """Registra o processo de adoção de um pet por um adotante.

  Parâmetros:
  - pet_id: Identificador numérico (ID) do pet a ser adotado.
  - adotante_id: Identificador numérico (ID) da pessoa adotante.
  """
  payload = {"petId": pet_id, "adotanteId": adotante_id}
  return await _fazer_requisicao("POST", "/adocoes", json=payload)


@mcp.tool()
async def obter_relatorio_adocoes(dias: int = 30) -> Dict[str, Any]:
  """Gera um relatório de adoções efetuadas nos últimos N dias (padrão: 30 dias),

  agrupando os totais por espécie do pet.
  """
  return await _fazer_requisicao(
      "GET", "/adocoes/relatorio", params={"dias": dias}
  )


if __name__ == "__main__":
  # Executa o servidor MCP via STDIO
  mcp.run()