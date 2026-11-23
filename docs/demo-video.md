# Demo em vídeo — o que ele mostra e como usar na apresentação

Vídeo **já gravado** (~1min30). Link: `<colar aqui o link do Drive/YouTube>` (no Google Slides: *Inserir → Vídeo*).
O roteiro da fala em volta do vídeo está no `roteiro-apresentacao.md`, bloco do P2 (slide 8).
Este arquivo serve para (1) conferir se o vídeo sustenta o que o slide afirma, (2) não ter surpresa na sala e (3) reproduzir a demo, se precisar regravar.

## 1. O vídeo tem de mostrar estas cinco coisas (bate com o slide 8)

| # | Cena | Por que importa |
|---|---|---|
| 1 | O servidor MCP conectado no cliente (`claude mcp list` → ✓ Connected) | prova que o agente fala com o **nosso** servidor |
| 2 | “quais pets estão para adoção?” → lista dos 5 | o caso que funciona |
| 3 | “tem algum pug?” → resposta certa, **sem** usar a ferramenta de busca | o contorno: ele baixa a base inteira e filtra |
| 4 | Pedido explícito da busca → `{"result": []}` | o defeito silencioso, com o pet no banco |
| 5 | “publique um anúncio da gata Nina” → criado (no banco entra como `ownerId 1`) | escrita sem nenhum login |

Se algum item não estiver no vídeo, o certo é **ajustar o slide e a fala** — não narrar o que não aparece na tela. As cenas 3 e 4 são as que sustentam a análise; se só existir a 3, corte a frase do `{"result": []}` no slide.

## 2. Conferências antes de apresentar (2 minutos)

- [ ] baixe o arquivo do vídeo para o notebook da apresentação: **não dependa da internet da sala** para dar play.
- [ ] assista uma vez inteira e olhe **os dados do dono na tela**: o retorno da listagem traz e-mail, telefone e endereço de cada usuário. Se aparecerem no vídeo, cubra com uma tarja ou corte o trecho (dado de terceiro não circula no material).
- [ ] confira se aparece caminho com nome de usuário, token ou credencial no terminal — se aparecer, corte.
- [ ] valide legibilidade na projeção: em 1080p, o texto do terminal tem de ser lido de longe; se estiver pequeno, exiba o vídeo em tela cheia (feche qualquer outro app antes).
- [ ] teste o áudio, se o vídeo tiver narração; se for mudo, você narra por cima (falas na seção 3 do roteiro do P2).
- [ ] depois do ensaio geral: apagar o anúncio criado na demo e parar a stack (`docker stop petapi petpg`).

## 3. Anexo — como reproduzir a demo (para uma regravação)

```bash
# stack do PetHouse (API em :3333 + Postgres)
docker start petpg && sleep 4 && docker start petapi && sleep 18
curl -s -o /dev/null -w "API: %{http_code}\n" http://localhost:3333/posts/all     # espera 200

# plugar o servidor MCP no cliente (uma vez só; já está configurado nesta máquina)
cd ~/FACULDADE_MCP_PET/project-mcp-pet-adoption
claude mcp add pethouse --scope local -- ~/FACULDADE_MCP_PET/.venv/bin/python \
  ~/FACULDADE_MCP_PET/project-mcp-pet-adoption/pethouse_mcp_server.py
claude mcp list      # pethouse … ✓ Connected
```

Se os containers não existirem mais:
```bash
docker run -d --name petpg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=pethouse -p 55432:5432 \
  -v ~/FACULDADE_MCP_PET/PetHouse/database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro postgres:14
docker run -d --name petapi --network host -v ~/FACULDADE_MCP_PET/PetHouse/backend:/app -w /app \
  node:18.17.1 bash -c "npm install --no-audit --no-fund && exec npx ts-node src/index.ts"
```

Claude Desktop (nas máquinas da equipe), no arquivo de config do app:
```json
{"mcpServers": {"pethouse": {
  "command": "/home/<usuario>/FACULDADE_MCP_PET/.venv/bin/python",
  "args": ["/home/<usuario>/FACULDADE_MCP_PET/project-mcp-pet-adoption/pethouse_mcp_server.py"],
  "env": {"PETHOUSE_API_URL": "http://localhost:3333"}}}}
```

Sem Claude, o MCP Inspector mostra o retorno cru da ferramenta (útil para provar o `{"result": []}`):
```bash
cd ~/FACULDADE_MCP_PET/project-mcp-pet-adoption
npx @modelcontextprotocol/inspector ~/FACULDADE_MCP_PET/.venv/bin/python pethouse_mcp_server.py
```

Prompts usados (e saídas reais obtidas em 22-23/11/2026):
1. `quais pets estão disponíveis para adoção? Liste nome, raça e idade.` → Lulu (Pug, 12), Pipoca (Chihuahua, 2), Totó (Shithzu, 1), Darth Vader (Rotweiller, 7), Doce de leite (Poodle, 5).
2. `tem algum pug para adoção? Se tiver, me diga nome e idade.` → “Sim! Lulu, 12 anos” — usando a listagem completa, não a busca.
3. `use a ferramenta buscar_pet_por_criterios com raça = 'Pug' e me diga exatamente o que ela retornou, o conteúdo, não a sua interpretação.` → `{"result": []}`.
4. `publique um anúncio de adoção para uma gata chamada Nina, SRD, 3 anos, dócil, foto em https://i.imgur.com/z9sCEqU.jpeg` → “Anúncio publicado com sucesso!”, entrada no banco com `ownerId 1`.

Limpeza depois de gravar:
```bash
curl -s -X DELETE http://localhost:3333/posts/<id_da_nina>
docker stop petapi petpg
```
