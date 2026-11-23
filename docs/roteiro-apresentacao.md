# Roteiro de apresentação — PetHouse MCP Server (versão com autenticação e contrato corrigidos)

16 slides, 4 apresentadores, alvo de **13 a 15 minutos** + perguntas (dos quais 58 s são o vídeo da demo).
A análise parte da **versão atual**: o que funciona hoje, e os insucessos que continuam de pé.
Decore a primeira e a última frase de cada bloco; o meio sai olhando o slide.

## Divisão

| Quem | Slides | Tempo | Papel |
|---|---|---|---|
| **P1** | 1 a 4 | ~3 min | abre, mostra a versão atual e apresenta o fix (~30 linhas) |
| **P2** | 5 a 9 | ~4 min | inventário, como foi validado, casos de uso, caso destaque e **a demo em vídeo** |
| **P3** | 10 a 12 | ~3 min | os insucessos que restam: identidade, contrato, operação |
| **P4** | 13 a 16 | ~3 min | segurança (o que o fix destravou), manutenção, roadmap e fechamento |

Sugestão de nomes (trocável): P1 Theo, P2 Mateus, P3 Eduardo, P4 Bernardo.
Eduardo escreveu o servidor MCP e fez o fix — deixá-lo no bloco 10–12 ajuda nas perguntas técnicas.

## Combinado de passagem (use sempre a mesma frase)

- P1 → P2: “e foi assim que a gente validou isso na prática.”
- P2 → P3: “com tudo funcionando, o que sobra são três insucessos — e é o que vem agora.”
- P3 → P4: “esses três viram risco concreto quando a gente olha o que o agente pode fazer.”
- P4 → grupo: “e é isso; ficamos à disposição para as perguntas.”

---

## P1 — slides 1 a 4 (~3 min)

**Slide 1 · Capa (20 s)**
“Boa noite. Somos o grupo do PetHouse, e este trabalho é de Manutenção e Evolução de Software.
O PetHouse é a nossa plataforma de adoção. O que a gente vai analisar é o servidor MCP que conecta um agente de IA a ela — e essa análise é da **versão atual**: a que já tem autenticação e contrato corrigidos.”

**Slide 2 · Tese e números (50 s)**
“Começando pelo retrato da versão atual. As 12 ferramentas e os 2 recursos funcionam: a validação com o cliente oficial passou em 15 de 15 checagens.
O conserto custou cerca de 30 linhas — o arquivo foi de 303 para 334 linhas, em dois commits.
E tem um número que a gente faz questão de mostrar desde o começo: **7 de 7**. Depois do conserto, a ferramenta de listar usuários passou a devolver o hash da senha de todos os usuários para o modelo. Isso é efeito colateral medido, não hipótese.
O quarto número é zero: o repositório do MCP continua sem teste, sem CI e sem lint.
A tese é essa: corrigir autenticação sem filtrar a resposta troca um erro por um incidente. O que sobrou para analisar é autorização, contrato e privacidade — não mais ‘não funciona’.”

**Slide 3 · O servidor hoje (40 s)**
“Só para situar: o PetHouse é front em React, back em Express com arquitetura hexagonal, Postgres, login por JWT em cookie e senha com bcrypt. O MCP é um cliente fino dessa API — 12 ferramentas e 2 recursos — e agora com identidade própria: ele faz login e mantém sessão.
No caminho, o detalhe novo é a caixa do meio: em vez de cliente anônimo, ele autentica.
Na tabela de baixo a gente separou duas coisas que costumam se misturar: o que o fix resolveu — as ferramentas que só davam erro passaram a devolver dado, a estatística saiu de zero, a busca passou a filtrar — e o que nunca foi problema de autenticação: o anúncio criado em nome do usuário 1, o cadastro sem foto que ainda dá 500 e a exclusão sem dono verificado. Esses três voltam nos slides 10, 11 e 13.”

**Slide 4 · O que mudou no código (40 s)**
“Para quem quiser ver o conserto: eram quatro pontos. O cliente HTTP era criado a cada requisição e morria no fim — a sessão se perdia; agora é um cliente com sessão, que faz login uma vez e reaproveita o cookie.
A resposta da API era tratada como lista, sendo que ela devolve mensagem e corpo; agora um helper extrai o corpo antes de filtrar ou contar.
A credencial, que não existia, vem de variável de ambiente — e está documentada no README.
E o resultado mudou de cinco ferramentas em erro, busca vazia e estatística zerada para 12 de 12 funcionando.
Dois commits, cerca de 30 linhas, nenhuma regra de negócio copiada para o adaptador. É o retorno de ter mantido o cliente fino — e foi assim que a gente validou isso na prática.” *(passa para P2)*

---

## P2 — slides 5 a 9 (~4 min, inclui o vídeo)

**Slide 5 · Inventário (50 s)**
“Este slide é o mapa do que existe hoje na versão atual. Cada linha é uma ferramenta, o endpoint, o status e a ressalva que permanece.
Não tem nenhuma ferramenta quebrada — a coluna de status é toda OK. O que vocês vão ler na última coluna são ressalvas de três naturezas: de autorização — ‘o user_id é escolhido pelo modelo’; de contrato — ‘exige foto, a data é calculada no cliente’; e de privacidade — ‘devolve hash da senha de todos’.
Ou seja: a partir daqui a apresentação não é sobre consertar bug, é sobre decidir o que um agente pode ver e fazer.”

**Slide 6 · Como foi validado (50 s)**
“Antes de afirmar qualquer coisa, a gente validou executando. Mesmo servidor, cliente MCP oficial por linha de comando, em quatro cenários: o original sem credencial, com credencial errada, com login correto e com token direto por variável de ambiente.
No bloco cinza vocês veem a matriz das cinco ferramentas que dependiam de login: no cenário A e B, erro; no C e no D, tudo respondendo.
Três coisas essa bateria garante: nenhuma regressão no que já funcionava; credencial errada degrada igual ao original, sem quebrar nem entrar em laço de login; e a sessão persiste entre chamadas — que era exatamente o defeito original.
E o dado honesto: 15 de 15 checagens, mas essa bateria é um script externo. O repositório continua sem teste e sem CI, e isso volta no slide 15.”

**Slide 7 · Casos de uso (45 s)**
“Agora os casos de uso que passaram a funcionar de verdade, cada um com a prova do que a gente executou.
Busca conversacional: pedindo raça igual a Pug, a ferramenta devolve a Lulu, pug de 12 anos. Moderação assistida: a denúncia é criada e lida, e a estatística mostra seis denúncias no ambiente. Panorama: o recurso devolve 5 posts, 8 usuários e 6 denúncias, com a lista de raças. Cadastro assistido: a conta é criada pela conversa, com a ressalva de que a API descarta telefone, endereço e descrição.
E o ganho de engenharia que o próprio conserto comprova: mexer nesse adaptador custou 30 linhas, sem tocar no produto.”

**Slide 8 · Caso destaque: a busca (45 s)**
“Vale destacar o caso que mais importa. Antes o defeito era esse: a ferramenta devolvia lista vazia com o pet no banco, porque o código perguntava ‘isso é uma lista?’ e a API devolve um objeto com mensagem e corpo. O agente até escapava disso — baixando a base inteira e filtrando sozinho, o que funcionava com cinco anúncios e seria caro e invasivo com a base real.
Depois do conserto, o mesmo pedido responde pela ferramenta certa, e o mesmo helper que corrigiu isso corrigiu a lista de raças e a estatística.
Fica a lição: duas linhas de conserto que só apareceram porque alguém executou o sistema em vez de ler o código.”

**Slide 9 · Demo em vídeo (58 s)**
*Antes de dar play (15 s):* “Vou mostrar isso acontecendo, no Claude Desktop falando com o nosso servidor. Olhem três coisas: o rótulo da ferramenta que ele chama, o que o pedido teve de informar e o que aparece na tela no fim.”
*Durante (o vídeo é mudo — narre em duas frases):* “aqui ele escolhe a ferramenta sozinho, e o rótulo na tela é a nossa: Pethouse, listar todos os pets” (aos ~0:40) e “para cadastrar, o pedido levou `ownerId: 1`” (aos ~0:25).
*Depois (20 s):* “Três coisas para levar. Um: quem respondeu foi o nosso servidor. Dois: o anúncio entrou como ‘Dono: ID 1’, sem ninguém logado — a identidade foi digitada no chat, e isso continua verdadeiro depois do fix, porque o fix autenticou o servidor, não o usuário. Três: o payload cru subiu na tela com nome, e-mail, telefone e endereço do dono.
Com tudo funcionando, o que sobra são três insucessos — e é o que vem agora.” *(passa para P3)*

---

## P3 — slides 10 a 12 (~3 min)

**Slide 10 · Insucesso 1: identidade (50 s)**
“O primeiro insucesso que resta é o mais estrutural. O servidor MCP agora tem credencial — uma conta de serviço. Mas o usuário que está conversando continua anônimo: quem escolhe o dono do anúncio e o autor da denúncia é o modelo, por parâmetro de ferramenta. O `owner_id` tem valor padrão 1, e a denúncia aceita qualquer id de denunciante.
A prova está no vídeo que vocês acabaram de ver: o anúncio criado pela conversa entrou no sistema como ‘Dono: ID 1, Eduardo Sereia’, sem ninguém logado.
A frase para levar: autenticar o servidor resolve o acesso, não a autorização. Enquanto a identidade vem do modelo, a pergunta ‘quem pode o quê’ deixa de existir — e não dá erro, não gera log, e a API responde 201 com sucesso.”

**Slide 11 · Insucesso 2: contrato (50 s)**
“O segundo grupo de insucessos é de contrato — e nenhuma dessas linhas o fix resolve, porque são do servidor, não do adaptador.
A foto é opcional na descrição da ferramenta, mas é obrigatória no banco: sem foto, erro 500. Quem define a data de criação é o cliente, no relógio da máquina de quem conversa, porque a coluna é obrigatória e não tem valor padrão no servidor. O cadastro de usuário aceita telefone, endereço e descrição e o caso de uso sobrescreve os três — o dado é descartado em silêncio e o agente acha que salvou. A política de senha não está documentada em lugar nenhum: o modelo descobre no erro 400. E a autenticação só funciona por cookie: mandar token no cabeçalho Authorization é ignorado.
Ou seja: o adaptador precisa saber coisas que são do banco e da política do servidor. O conserto certo é lá, e o adaptador volta a ser burro — como deve ser.”

**Slide 12 · Insucesso 3: operação (45 s)**
“O terceiro insucesso não é de código, é de operação: funciona, mas não está pronto para operar. Zero confirmações antes de uma ação irreversível. Zero registros de auditoria — nada diz qual conversa pediu a exclusão. E zero paginação ou limite de taxa: a busca ainda baixa a base inteira a cada pergunta.
Com cinco anúncios isso parece instantâneo. Na base real vira custo, latência e dados pessoais de todo mundo no contexto do modelo.
E aqui está o ponto mais desconfortável do trabalho: **consertar aumentou a superfície de dano**. Antes, metade das ferramentas não funcionava e isso era visível; agora tudo funciona — inclusive a listagem que devolve hash de senha e a exclusão sem dono verificado.
Esses três viram risco concreto quando a gente olha o que o agente pode fazer.” *(passa para P4)*

---

## P4 — slides 13 a 16 (~3 min)

**Slide 13 · Segurança: o que o agente pode fazer (50 s)**
“Aqui está o que o agente pode fazer hoje, com a credencial que ganhou, e a resposta honesta sobre confirmação: em quase tudo, nenhuma.
Pode listar todos os anúncios — e o payload traz e-mail, telefone e endereço de cada anunciante. Pode listar usuários — e medimos: sete hashes de senha em sete usuários. Pode criar anúncio em nome de qualquer id, apagar anúncio de qualquer id, criar contas em série e denunciar em nome de qualquer pessoa.
O que segura o estrago é o escopo da conta: ela tem permissão zero, então não apaga usuário. Mas é uma chave única para todos os usuários da plataforma.
O mínimo a fazer hoje é filtrar o que as ferramentas devolvem e exigir confirmação no que escreve.”

**Slide 14 · Segurança: o que entra no contexto (50 s)**
“Esse é o slide que o conserto tornou mais urgente, e ele tem dois lados.
À esquerda, instrução escondida no dado: o campo de descrição do anúncio é texto livre escrito por qualquer usuário e chega ao modelo no mesmo lugar em que ele busca informação. O trecho na tela foi escrito por nós no teste e voltou inteiro, pedindo ao assistente para chamar a função de remover. No front isso seria um anúncio feio; aqui é uma instrução ao lado de ferramentas autenticadas de escrita.
À direita, o que entra no prompt: dados pessoais de todos os anunciantes, agora também de todos os usuários, o hash da senha, a senha em texto claro quando alguém cadastra alguém pela conversa, e a credencial de serviço guardada em texto no arquivo de configuração do cliente.
E duas camadas do backend que agravam: o token é assinado com segredo vazio se a variável não estiver no ambiente, e o seed versionado tem os quatro usuários com o mesmo hash — uma senha comprometida abre quatro contas.”

**Slide 15 · Manutenção e evolução (45 s)**
“A leitura de manutenção, comparando com o backend do projeto: 43 suítes e 231 testes passando, integração contínua em três sistemas, de um lado; do outro, zero testes, zero CI.
E vale reconhecer: a validação que mostrei no slide 6 é um script externo, que eu rodei no meu ambiente. Ela não está no repositório. Ou seja, **a única rede de segurança do conserto foi alguém lembrar de rodar a bateria**.
Nos outros pontos: duas dependências sem nenhuma referência no código, uma camada de compatibilidade com a versão 2 do MCP que funciona — testamos, sobe e registra as 12 ferramentas — mas nunca roda, porque o requirements fixa a versão 1; e o acoplamento que sobra: o adaptador ainda decide data de criação, dono padrão e a busca em memória.
A lição: o conserto foi barato porque o adaptador era fino, e foi arriscado porque não havia teste protegendo.”

**Slide 16 · Roadmap e fechamento (50 s)**
“Fechando com o que fazer agora.
P0, e os dois são consequência direta do conserto: filtrar o que as ferramentas devolvem — sem hash de senha, sem dado pessoal desnecessário — e exigir confirmação humana em escrita e exclusão; e trocar a identidade por parâmetro por identidade real de quem conversa.
P1: testes de contrato e integração contínua no repositório do MCP, aproveitando o padrão que o backend já tem; e mover filtro e paginação para o servidor, alinhando o contrato da API.
P2: auditoria, limite de taxa, versão, licença e README com seção de segurança.
As cinco frases: o adaptador funciona hoje, e o que resta é arquitetura, não bug; o conserto custou 30 linhas porque o cliente era fino; autenticar o servidor não substitui autorizar o usuário; o fix ampliou a superfície — o que destravou o uso destravou o abuso; e sem teste no repositório, cada correção depende de alguém lembrar de validar.
Embaixo estão os repositórios, o branch e os dois commits, como reproduzir e o limite da análise: o que está marcado como observado foi executado localmente, e o ambiente local não tem proxy, WAF ou cotas de produção.
E é isso; ficamos à disposição para as perguntas.”

---

## Perguntas prováveis (quem responde)

| Pergunta | Responde | Resposta curta |
|---|---|---|
| “O que exatamente vocês consertaram?” | P1 | Dois defeitos independentes: o cliente não autenticava (5 tools em erro) e tratava a resposta como lista, sendo `{message, body}` (busca vazia e estatística zerada). ~30 linhas, 2 commits. |
| “E como vocês sabem que funciona?” | P2 | Executamos: 15/15 checagens com o cliente MCP oficial, em quatro cenários, incluindo credencial errada e token direto. O script é externo, não está no repositório. |
| “Por que o Claude acertou o pug mesmo antes do fix?” | P2 | Ele contornava a ferramenta quebrada baixando a listagem completa e filtrando sozinho — funcionava com 5 anúncios e seria caro e invasivo com a base real. |
| “Isso não é problema do backend, e não do MCP?” | P3 | Os três insucessos que restam são de contrato e de identidade: parte é do servidor (foto obrigatória, data sem default, política de senha, só cookie) e parte é decisão do adaptador (identidade por parâmetro). |
| “O agente é inseguro?” | P4 | O agente usou o que estava exposto. O que falta é política no adaptador: filtrar resposta, confirmar ação e agir com identidade do usuário. |
| “Qual o risco mais grave hoje?” | P4 | Listar usuários devolve hash de senha de todos e apagar anúncio não exige dono nem confirmação — os dois com a mesma credencial de serviço. |
| “Quanto tempo para o P0?” | P2 | Estimativa, não medição: filtro de campos é uma tarde; confirmação humana e identidade por usuário exigem mudar o fluxo do cliente e da API, algo como uma semana. |

## Checklist de ensaio

- [ ] rodar o deck inteiro com cronômetro: alvo 13–15 min; se passar, encurte o slide 5 (Inventário) falando só as três naturezas de ressalva.
- [ ] cada pessoa ensaia a primeira e a última frase do seu bloco sem olhar o slide.
- [ ] o vídeo da demo abre **sem internet** (baixe o arquivo), é mudo: ensaie a narração por cima e teste o volume da sala.
- [ ] decidir sobre os dados pessoais visíveis no vídeo entre 0:47 e 0:52 (nome, e-mail, telefone, endereço): manter como evidência ou tarjar antes de projetar.
- [ ] combinar quem controla a passagem de slide e usar sempre a mesma frase de deixa.
- [ ] **não falar**: dados reais do seed além do que o vídeo já mostra, token ou caminho de usuário na tela, e nunca dizer que “o agente errou” — o defeito é do adaptador ou do contrato da API.
- [ ] números da apresentação sempre com a mesma fonte: 12 tools, 12/12 operacionais, 15/15 checagens, ~30 linhas, 7 hashes em 7 usuários, 5 posts / 8 usuários / 6 denúncias, 231 testes no backend, 16 slides.
