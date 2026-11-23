# Demo em vídeo — o que ele mostra e como usar na apresentação

Arquivo: `WhatsApp Video 2026-11-22 at 18.25.19.mp4` — **58 s, 1208×868, 300 kbps, sem áudio**.
Link no slide 8: `<colar aqui o link do Drive/YouTube>` (no Google Slides: *Inserir → Vídeo*).
A fala em volta do vídeo está no `roteiro-apresentacao.md`, bloco do P2 (slide 8).

## 1. Mapa do vídeo (conferido quadro a quadro)

| Tempo | O que aparece |
|---|---|
| 0:00–0:12 | Claude Desktop (tema escuro, modelo Sonnet): o pedido “liste todos os posts do pet house” sendo digitado |
| 0:12–0:20 | resposta com **7 anúncios em tabela**; o próprio agente nota que os posts 6 e 7 parecem duplicados |
| 0:20–0:30 | pedido de cadastro estruturado: name Leaozinho, description, breed Rottweiler, photoUrl, age 5, **ownerId: 1** |
| 0:28–0:38 | “Post cadastrado com sucesso” com **“Dono: ID 1 (Eduardo Sereia)”** — sem nenhum login |
| 0:38–0:47 | “ok, liste denovo os posts” e o rótulo **`Pethouse: Listar todos os pets`** (prova de que a ferramenta chamada é a nossa) |
| 0:47–0:52 | **payload cru na tela**: bloco `owner` com nome, e-mail, telefone e endereço do dono |
| 0:52–0:58 | tabela final com 8 anúncios (Leaozinho, id 8) |

Duas conclusões que o vídeo sustenta sozinho: **a identidade foi digitada no chat** (ownerId 1) e **dado pessoal do dono subiu na tela** na listagem.

## 2. O que o vídeo NÃO mostra (e onde essa prova está no deck)

- o comportamento da busca por raça e por idade — **não aparece no vídeo**; a saída real está no slide 7;
- exclusão de anúncio sem dono verificado — também não aparece; está no slide 12, com a saída real dos comandos;
- e a bateria de verificação em quatro configurações de credencial está no slide 5.
Por isso o roteiro do slide 8 não narra como se estivesse na tela o que o vídeo não mostra: só o rótulo da ferramenta, o `ownerId` digitado no chat e o payload com os dados do dono.

## 3. Antes de apresentar (2 minutos)

- [ ] baixar o arquivo para o notebook: não depender da internet da sala para dar play.
- [ ] **decisão sobre os dados pessoais**: entre 0:47 e 0:52 aparecem nome, e-mail, telefone e endereço de um dos integrantes (dados do seed do projeto). Ou você mantém — é a evidência do argumento de privacidade, e é dado de vocês mesmos — ou tarja/corta esse trecho antes de projetar. Se a disciplina pedir cuidado com dado pessoal, tarje.
- [ ] o vídeo veio por WhatsApp (300 kbps): se existir o arquivo original da gravação, use **o original** para projetar — a recompressão deixa o texto mais mole em tela grande.
- [ ] o vídeo é **mudo**: você narra por cima (falas do P2 no roteiro). Teste o volume da sala antes.
- [ ] na tabela final aparecem posts de teste (“John Doe”, ids 6 e 7). Se alguém perguntar, é anúncio de teste do ambiente local — ou re-recorte para terminar antes disso.
- [ ] teste o play em tela cheia e feche notificações do sistema.

## 4. Anexo — como reproduzir a demo (para uma regravação)

```bash
# stack do PetHouse (API em :3333 + Postgres)
docker start petpg && sleep 4 && docker start petapi && sleep 18
curl -s -o /dev/null -w "API: %{http_code}\n" http://localhost:3333/posts/all     # espera 200

# clientes: Claude Desktop com o config abaixo, ou o CLI (já configurado nesta máquina)
cd ~/FACULDADE_MCP_PET/project-mcp-pet-adoption
claude mcp add pethouse --scope local -- ~/FACULDADE_MCP_PET/.venv/bin/python \
  ~/FACULDADE_MCP_PET/project-mcp-pet-adoption/pethouse_mcp_server.py
claude mcp list      # pethouse … ✓ Connected
```

Config do Claude Desktop (arquivo do app: `~/Library/Application Support/Claude/…` no macOS, `%APPDATA%\Claude\…` no Windows, `~/.config/Claude/…` no Linux):
```json
{"mcpServers": {"pethouse": {
  "command": "/home/<usuario>/FACULDADE_MCP_PET/.venv/bin/python",
  "args": ["/home/<usuario>/FACULDADE_MCP_PET/project-mcp-pet-adoption/pethouse_mcp_server.py"],
  "env": {"PETHOUSE_API_URL": "http://localhost:3333"}}}}
```

Prompts do vídeo, com a saída real: “liste todos os posts do pet house” → tabela com os anúncios; cadastro de Leaozinho com `ownerId: 1` → “Dono: ID 1 (Eduardo Sereia)”; “ok, liste denovo os posts” → payload cru + tabela com 8 posts.
Extras que valem regravar um dia (não estão no vídeo): a busca explícita, que devolve `{"result": []}` com o pug cadastrado, e a exclusão de um anúncio sem login (saídas reais já registradas nesta análise).

Limpeza depois do ensaio/regravação:
```bash
curl -s -X DELETE http://localhost:3333/posts/<id_do_leaozinho>
docker stop petapi petpg
```
