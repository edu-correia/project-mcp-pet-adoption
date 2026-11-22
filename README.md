# 🐾 PetHouse MCP Server

Servidor MCP (*Model Context Protocol*) construído para expor as funcionalidades da API do **PetHouse** (adoção de pets) para agentes de Inteligência Artificial, permitindo consultas em linguagem natural, cadastro de adotantes, filtros de pets e interações pelo **Claude Desktop** e **MCP Inspector**.

---

## Pré-requisitos

* **Python 3.10+**
* **Node.js** (opcional, necessário para rodar o MCP Inspector)
* **[Backend do PetHouse](https://github.com/edu-correia/PetHouse)** rodando localmente na porta `3333`

---

## Instalação e Configuração

### 1. Clonar o repositório e entrar na pasta
```bash
git clone https://github.com/edu-correia/project-mcp-pet-adoption.git
cd project-mcp-pet-adoption
```

### 2. Criar e ativar o ambiente virtual (venv)

No Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

Instale as dependencias:

```bash
pip install -r requirements.txt
```

## Executando o Projeto

### 1. Iniciar o Backend do PetHouse

Antes de iniciar qualquer cliente de IA, garanta que a API REST do PetHouse esteja em execução:
Bash

#### Certifique-se de que a API está rodando em:
http://localhost:3333

### 2. Integração com o Claude Desktop

O Claude Desktop inicializa o servidor MCP automaticamente em segundo plano. Basta adicionar a configuração no arquivo claude_desktop_config.json.
Localização do arquivo de configuração:

Windows: %APPDATA%\Claude\claude_desktop_config.json

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

Linux: ~/.config/Claude/claude_desktop_config.json

Conteúdo do arquivo:

No Linux / macOS:
```json
{
  "mcpServers": {
    "pethouse": {
      "command": "/caminho/completo/para/PetHouse/.venv/bin/python",
      "args": [
        "/caminho/completo/para/PetHouse/pethouse_mcp_server.py"
      ],
      "env": {
        "PETHOUSE_API_URL": "http://localhost:3333"
      }
    }
  }
}
```

No Windows (atenção às barras duplas \\):

```json
{
  "mcpServers": {
    "pethouse": {
      "command": "C:\\caminho\\para\\PetHouse\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\caminho\\para\\PetHouse\\pethouse_mcp_server.py"
      ],
      "env": {
        "PETHOUSE_API_URL": "http://localhost:3333"
      }
    }
  }
}
```

Atenção: Reinicie o Claude Desktop completamente após salvar o arquivo. Um ícone de martelo/ferramenta (🔨) aparecerá no canto inferior do campo de mensagens.

### 3. Teste Rápido via MCP Inspector (Alternativa sem Claude)

Se preferir validar visualmente pelo navegador sem abrir o Claude Desktop, execute:

```
npx @modelcontextprotocol/inspector@latest .venv/bin/python pethouse_mcp_server.py
```

(No Windows, troque .venv/bin/python por .venv\Scripts\python.exe).

Acesse o endereço exibido no terminal (http://localhost:5173) para testar as chamadas das ferramentas via interface web.