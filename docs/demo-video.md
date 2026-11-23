# Demo em vídeo — Claude chamando o servidor MCP do PetHouse

Vídeo de **~1min30** para o slide 8. Objetivo: mostrar o agente em ação **e** mostrar o defeito acontecendo ao vivo — não é vídeo de “olha que legal”, é evidência.

O que o vídeo prova, em ordem: (1) o agente está plugado no nosso servidor; (2) ele resolve um caso simples; (3) ele **contorna** a ferramenta de busca quebrada baixando a base inteira; (4) a ferramenta de busca devolve vazio com o pet no banco; (5) ele publica anúncio **sem login**, em nome do usuário 1.

---

## 1. Antes de gravar (5 minutos)

```bash
# 1) subir a stack do PetHouse (API em :3333 + Postgres)
docker start petpg && sleep 4 && docker start petapi && sleep 18
curl -s -o /dev/null -w "API: %{http_code}\n" http://localhost:3333/posts/all      # espera 200

# 2) banco limpo: só os 5 anúncios do seed (se tiver sobrado anúncio de teste, apague pelo id)
curl -s http://localhost:3333/posts/all | python3 -c "import sys,json;[print(p['id'],p['name']) for p in json.load(sys.stdin)['body']]"

# 3) plugar o servidor MCP no Claude (uma vez só)
cd ~/FACULDADE_MCP_PET/project-mcp-pet-adoption
claude mcp add pethouse --scope local -- ~/FACULDADE_MCP_PET/.venv/bin/python \
  ~/FACULDADE_MCP_PET/project-mcp-pet-adoption/pethouse_mcp_server.py
claude mcp list        # deve mostrar: pethouse ... ✓ Connected
```

Se os containers não existirem mais (foram removidos), recriar:
```bash
docker run -d --name petpg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=pethouse -p 55432:5432 \
  -v ~/FACULDADE_MCP_PET/PetHouse/database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro postgres:14
docker run -d --name petapi --network host -v ~/FACULDADE_MCP_PET/PetHouse/backend:/app -w /app \
  node:18.17.1 bash -c "npm install --no-audit --no-fund && exec npx ts-node src/index.ts"
```

**Alternativa ao Claude CLI — Claude Desktop.** No arquivo de config (`~/Library/Application Support/Claude/claude_desktop_config.json` no macOS, `%APPDATA%\Claude\...` no Windows, `~/.config/Claude/...` no Linux):
```json
{"mcpServers": {"pethouse": {
  "command": "/home/<usuario>/FACULDADE_MCP_PET/.venv/bin/python",
  "args": ["/home/<usuario>/FACULDADE_MCP_PET/project-mcp-pet-adoption/pethouse_mcp_server.py"],
  "env": {"PETHOUSE_API_URL": "http://localhost:3333"}}}}
```
Reinicie o app por completo e confira o ícone de ferramenta (🔨) no campo de mensagem.

**Alternativa sem Claude — MCP Inspector** (útil para mostrar o retorno cru da ferramenta e gravar a tela do navegador):
```bash
cd ~/FACULDADE_MCP_PET/project-mcp-pet-adoption
npx @modelcontextprotocol/inspector ~/FACULDADE_MCP_PET/.venv/bin/python pethouse_mcp_server.py
# abre em http://localhost:5173 → aba Tools → buscar_pet_por_criterios
```

---

## 2. Storyboard (as cenas, na ordem)

| # | Cena | Tempo | O que aparece na tela |
|---|---|---|---|
| 1 | Prova do plug | 10 s | terminal: `claude mcp list` → `pethouse … ✓ Connected` |
| 2 | Caso que funciona | 20 s | prompt 1 → tabela com os 5 pets |
| 3 | O contorno | 25 s | prompt 2 (“tem algum pug?”) → resposta certa, e a explicação de que ele **não** usou a busca |
| 4 | O defeito | 20 s | prompt 3 → `{"result": []}` |
| 5 | Escrita sem login | 20 s | prompt 4 → “Anúncio publicado” + o anúncio na listagem com `ownerId 1` |
| 6 | (opcional) banco | 10 s | Inspector ou `psql` mostrando a linha criada |

### Prompts exatos (copiar e colar)

**Prompt 1 — o caso que funciona**
> quais pets estão disponíveis para adoção? Liste nome, raça e idade.

Saída real obtida: tabela com Lulu (Pug, 12), Pipoca (Chihuahua, 2), Totó (Shithzu, 1), Darth Vader (Rotweiller, 7), Doce de leite (Poodle, 5).

**Prompt 2 — o agente chega na resposta por outro caminho**
> tem algum pug para adoção? Se tiver, me diga nome e idade.

Saída real: “Sim! Tem um Pug para adoção — Nome: Lulu, Idade: 12 anos (Descrição: ‘Só dorme’)”.

**Prompt 3 — o defeito, forçando a ferramenta certa**
> use a ferramenta buscar_pet_por_criterios com raça = 'Pug' e me diga exatamente o que ela retornou, o conteúdo, não a sua interpretação.

Saída real: `{"result": []}` — “uma lista vazia”.

**Prompt 4 — escrita sem identidade**
> publique um anúncio de adoção para uma gata chamada Nina, SRD, 3 anos, dócil, foto em https://i.imgur.com/z9sCEqU.jpeg

Saída real: “Anúncio publicado com sucesso!” — e no banco o anúncio entra com `ownerId 1` (dono: o usuário 1), sem ninguém logado.

---

## 3. Falas (para narrar por cima do vídeo ou virar legenda)

> “Primeiro, a prova de que o agente está falando com o **nosso** servidor: aqui está o servidor plugado, conectado.
> Agora um pedido simples: quais pets estão para adoção. Ele escolheu sozinho a ferramenta de listagem e devolveu os cinco.
> Vou pedir um pug. Ele acerta: Lulu, doze anos. **Mas repare no que ele fez para chegar nessa resposta** — ele não usou a ferramenta de busca, ele baixou a lista inteira e filtrou por conta própria. Ou seja: a ferramenta existe e está quebrada, e o agente está contornando.
> Vamos pedir a ferramenta de busca explicitamente, então. Pedido: pug. Resposta: `{result: []}`. Lista vazia — com o pug no banco. É a falha silenciosa que aparece no nosso slide anterior.
> E o último: publique um anúncio. Ele publica. Só que ninguém está logado — o anúncio entra no sistema como se fosse do usuário 1, que é o valor padrão que o próprio adaptador define.
> O agente não é o vilão da história: ele usou exatamente o que estava exposto. O defeito é do adaptador — e é o que a gente analisa a partir de agora.”

---

## 4. Cuidados na gravação

- **Não deixe os dados dos colegas na tela.** O retorno da listagem traz e-mail, telefone e endereço de cada dono. Se abrir o payload cru (Inspector), corte ou cubra essa parte. No vídeo, prefira a resposta em linguagem natural do Claude, que não mostra esses campos.
- **O agente é não determinístico**: ele pode escolher outra ferramenta. Se no prompt 2 ele usar a busca e responder “não encontrei”, fica ainda melhor para a análise — mas não conte com a mesma cena duas vezes. Grave duas ou três tomadas e escolha.
- **Não faça a demo ao vivo na apresentação**: vídeo já gravado é imune a instabilidade de rede, cota e aleatoriedade.
- Antes de gravar, esconda do terminal qualquer caminho com seu nome de usuário e nunca mostre token/credencial.
- Grave em 1080p, com a fonte do terminal grande (≥ 16 pt) e a janela ocupando a tela toda — o vídeo vai ser projetado.

## 5. Depois de gravar

```bash
# limpar o anúncio criado durante a demo (o id aparece na listagem)
curl -s -X DELETE http://localhost:3333/posts/<id_da_nina>
# encerrar a stack
docker stop petapi petpg
```

- Subir o vídeo no Drive/YouTube (não listado) e colar o link no slide 8 do deck; no Google Slides, use **Inserir → Vídeo** para ele tocar dentro do slide.
- No roteiro, o vídeo está com o P2 (slides 5 a 8): quem apresenta o caso destaque conduz a demo, com alguém do lado controlando o play.
