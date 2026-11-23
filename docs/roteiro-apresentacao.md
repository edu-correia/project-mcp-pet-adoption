# Roteiro de apresentação — PetHouse MCP Server (análise da solução)

15 slides, 4 apresentadores, alvo de **13 a 15 minutos** + perguntas (dos quais 58 s são o vídeo da demo).
Regra do roteiro: a análise é do estado atual da solução. Não se fala de correção, versão anterior ou mudança — quem assiste apresenta como o sistema é.
Decore a primeira e a última frase de cada bloco; o meio sai olhando o slide.

## Divisão

| Quem | Slides | Tempo | Papel |
|---|---|---|---|
| **P1** | 1 a 4 | ~3min30 | abre, mostra os números, a arquitetura da ponte e o inventário das ferramentas |
| **P2** | 5 a 8 | ~3min30 | como verificamos, casos de uso, caso destaque e **a demo em vídeo** |
| **P3** | 9 a 11 | ~3 min | os três insucessos: identidade, contrato e operação |
| **P4** | 12 a 15 | ~3min30 | segurança, manutenção e o roadmap com as cinco frases |

Sugestão de nomes (trocável): P1 Theo, P2 Mateus, P3 Eduardo, P4 Bernardo.
Eduardo escreveu o servidor MCP — deixá-lo no bloco 9–11 ajuda nas perguntas técnicas.

## Combinado de passagem (use sempre a mesma frase)

- P1 → P2: “e foi assim que a gente foi verificar isso na prática.”
- P2 → P3: “com tudo isso funcionando, o que sobra são três insucessos — e é o que vem agora.”
- P3 → P4: “esses três viram risco concreto quando a gente olha o que o agente pode fazer.”
- P4 → grupo: “e é isso; ficamos à disposição para as perguntas.”

---

## P1 — slides 1 a 4 (~3 min 30)

**Slide 1 · Capa (20 s)**
“Boa noite. Somos o grupo do PetHouse, e este trabalho é de Manutenção e Evolução de Software.
O PetHouse é a nossa plataforma de adoção. O que a gente vai analisar é o servidor MCP — a ponte que conecta um agente de IA às funcionalidades da plataforma. A análise é do que essa ponte entrega hoje e do que ela abre junto.”

**Slide 2 · Números e tese (50 s)**
“Começando pelo retrato da solução. Doze ferramentas e dois recursos, todos respondendo: a bateria de verificação passou em 15 de 15 checagens, com o cliente MCP oficial.
O servidor inteiro são 334 linhas em um único arquivo — sem separação de camadas e sem teste automatizado.
E dois números que dão o tom da análise. O primeiro: a ferramenta de listar usuários devolve o hash da senha de todos — sete de sete usuários no ambiente que a gente analisou. O segundo: zero confirmações, zero registros de auditoria e zero limites de uso.
A tese é essa: a solução funciona. O risco não está em ela falhar, está no que ela autoriza — identidade escolhida pelo modelo, dado pessoal no contexto do agente e ações destrutivas sem confirmação.”

**Slide 3 · A solução e o fluxo (45 s)**
“Só para situar: o PetHouse é front em React, back em Express com arquitetura hexagonal, Postgres, login por JWT em cookie e senha com bcrypt. O servidor MCP traduz onze endpoints dessa API em ferramentas que um agente chama em linguagem natural.
Olhando o caminho: o usuário pergunta, o Claude escolhe a ferramenta, o servidor MCP conversa com a API na porta 3333, e a API fala com o banco. A caixa do meio é o que interessa: o adaptador tem credencial própria — faz login uma vez e mantém sessão por cookie.
Na tabela de baixo, quatro dimensões do desenho: a identidade do servidor existe, a identidade do usuário não; a leitura da resposta é tratada por um helper; e o escopo da conta é o mínimo que a API concede — permissão zero — mas é uma credencial só para todos.”

**Slide 4 · Inventário (50 s)**
“Este é o mapa completo. Cada linha é uma ferramenta, o endpoint que ela chama e a ressalva que permanece.
E é isso que eu quero que vocês olhem: não tem nenhuma ferramenta falhando — a análise aqui não é sobre o que não funciona, é sobre o que funciona. As ressalvas são de três naturezas.
Autorização: em curtir, publicar e denunciar, o identificador do usuário é um parâmetro escolhido pelo modelo.
Contrato: o cadastro de anúncio exige foto, e a data de criação é calculada no cliente porque o servidor não tem valor padrão.
E privacidade: a listagem de anúncios traz os dados do dono, e a de usuários traz o hash da senha.
Ou seja: daqui pra frente a apresentação não é sobre consertar bug, é sobre decidir o que um agente pode ver e fazer. E foi assim que a gente foi verificar isso na prática.” *(passa para P2)*

---

## P2 — slides 5 a 8 (~3 min 30, inclui o vídeo)

**Slide 5 · Como verificamos (45 s)**
“Antes de afirmar qualquer coisa, a gente executou. Leu os dois repositórios no estado analisado — rotas, middlewares, repositórios e casos de uso — e subiu o sistema por inteiro: Postgres com o schema do projeto, backend em Node 18 na porta 3333, cliente MCP oficial falando por stdio.
No bloco cinza está a matriz: cada ferramenta testada em quatro configurações — sem credencial, com credencial inválida, com login e com token direto. Nas cinco que dependem de sessão, o comportamento é exatamente o esperado: falha sem credencial, funciona com credencial, sem regressão e sem laço de login.
E o dado honesto: 15 de 15 checagens, mas essa bateria é um script externo que eu rodei no meu ambiente. Ela não está no repositório. O repositório não tem teste nem integração contínua — e isso volta no slide 14.”

**Slide 6 · Casos de uso (45 s)**
“Com o sistema na mão, esses são os casos de uso que justificam a existência do projeto, cada um com a prova do que a gente executou.
Busca conversacional: pedindo raça igual a Pug, a ferramenta devolve o pug cadastrado — é o caso que dá sentido ao projeto. Moderação assistida: a denúncia é criada e lida por conversa, e a estatística mostra seis denúncias no ambiente. Panorama para quem decide, sem abrir banco nem dashboard: cinco posts, oito usuários, seis denúncias e a lista de raças. E cadastro assistido do adotante, com a ressalva de que a API descarta telefone, endereço e descrição.
E um ganho de engenharia que vale para os quatro: como o adaptador é fino, expor uma nova função da API ao agente custa poucas linhas.”

**Slide 7 · Caso destaque: a busca (40 s)**
“Vale destacar o caso que mais importa. O agente chama a busca com um ou mais filtros — raça, idade máxima, palavra na descrição — e o adaptador responde com os anúncios que casam: aqui, a Lulu, pug de doze anos.
Só que a análise tem uma observação importante: **o filtro roda no adaptador**, sobre a base inteira que a API devolve. Não tem paginação, não tem consulta no servidor. Com cinco anúncios isso é instantâneo; na base real significa custo, latência e os dados pessoais de todos os anunciantes dentro do contexto do modelo.
E esse mesmo padrão aparece nos outros recursos: quem filtra e quem conta é o adaptador, não a API.”

**Slide 8 · Demo em vídeo (58 s)**
*Antes de dar play (15 s):* “Vou mostrar isso acontecendo, no Claude Desktop falando com o servidor. Olhem três coisas: o rótulo da ferramenta que ele chama, o que o pedido teve de informar e o que aparece na tela no fim.”
*Durante (o vídeo é mudo — narre em duas frases):* “aqui ele escolhe a ferramenta sozinho, e o rótulo na tela é a nossa: Pethouse, listar todos os pets” (aos ~0:40) e “para cadastrar, o pedido levou `ownerId: 1`” (aos ~0:25).
*Depois (20 s):* “Três coisas para levar. Um: quem respondeu foi o consumidor do nosso servidor, e a ferramenta é a nossa. Dois: para cadastrar, a identidade foi digitada no chat — `ownerId: 1` — e o agente confirmou ‘Dono: ID 1, Eduardo Sereia’. Ninguém estava logado. Três: na listagem seguinte o payload cru subiu na tela com nome, e-mail, telefone e endereço do dono.
Com tudo isso funcionando, o que sobra são três insucessos — e é o que vem agora.” *(passa para P3)*

---

## P3 — slides 9 a 11 (~3 min)

**Slide 9 · Insucesso 1: identidade (50 s)**
“O primeiro insucesso é o mais estrutural. O servidor tem credencial própria, mas o usuário que está conversando é anônimo: quem escolhe o dono do anúncio, quem curte e quem denuncia é o modelo, por parâmetro de ferramenta. O `owner_id` tem valor padrão 1, e a denúncia aceita qualquer identificador.
A prova está no vídeo que vocês acabaram de ver: o anúncio entrou no sistema como ‘Dono: ID 1, Eduardo Sereia’, sem ninguém logado, e a listagem mostrou o payload completo daquele dono.
A frase para levar: autenticar o servidor resolve o acesso, não a autorização. Enquanto a identidade vem do modelo, a pergunta ‘quem pode o quê’ deixa de existir — e não dá erro, não gera log, e a API responde 201 com sucesso.”

**Slide 10 · Insucesso 2: contrato (50 s)**
“O segundo grupo é de contrato — e é tudo regra do servidor morando na cabeça do cliente.
A foto é opcional para o agente, mas obrigatória no banco: sem foto, erro 500 sem mensagem útil. Quem define a data de criação é o cliente, no relógio da máquina de quem conversa, porque a coluna é obrigatória e não tem valor padrão. O cadastro de usuário aceita telefone, endereço e descrição — e o caso de uso sobrescreve os três: o dado é descartado em silêncio e o agente acha que salvou. A política de senha não está documentada em lugar nenhum: o modelo descobre no erro 400. E a autenticação só funciona por cookie: token no cabeçalho Authorization é ignorado.
O adaptador precisa saber coisas que são do banco e da política do servidor. A correção estrutural é no contrato da API — e aí o adaptador volta a ser burro, como deve ser.”

**Slide 11 · Insucesso 3: operação (45 s)**
“O terceiro insucesso não é de código, é de operação. Zero confirmações antes de uma ação irreversível. Zero registros de auditoria: nada diz qual conversa pediu a exclusão. E zero paginação e limite de taxa — a busca baixa a base inteira a cada pergunta.
Com cinco anúncios parece instantâneo. Na base real vira custo, latência e dado pessoal de todo mundo no contexto do modelo, sem nenhum freio para um agente em laço criando contas ou publicando.
E o ponto que eu queria deixar claro: isso não é falta de polimento, é o que separa um assistente de um executor sem supervisão. Esses três viram risco concreto quando a gente olha o que o agente pode fazer.” *(passa para P4)*

---

## P4 — slides 12 a 15 (~3 min 30)

**Slide 12 · Segurança: o que o agente pode fazer (50 s)**
“Aqui está o que o agente pode fazer hoje, e a resposta honesta sobre confirmação: em quase tudo, nenhuma.
Pode listar todos os anúncios — e o payload traz e-mail, telefone e endereço de cada anunciante. Pode listar usuários — e aí vem o hash da senha de todos: sete de sete no ambiente que a gente rodou. Pode criar anúncio em nome de qualquer identificador, apagar anúncio de qualquer identificador, criar contas em série e denunciar em nome de qualquer pessoa.
O que segura o estrago é o escopo da conta: ela tem permissão zero, então não exclui usuário. Mas é uma chave única para todos os usuários da plataforma.
O mínimo a fazer hoje é filtrar o que as ferramentas devolvem e exigir confirmação no que escreve.”

**Slide 13 · Segurança: o que entra no contexto (50 s)**
“Esse é o slide que a análise considerou mais crítico, e ele tem dois lados.
À esquerda, instrução escondida no dado: o campo de descrição do anúncio é texto livre, escrito por qualquer usuário, e chega ao modelo no mesmo lugar em que ele busca informação. O trecho na tela foi escrito por nós no teste e voltou inteiro — pedindo ao assistente para chamar a função de remover. No front isso seria um anúncio feio; aqui é uma instrução ao lado de ferramentas de escrita.
À direita, o que entra no prompt: dados pessoais de todos os anunciantes e de todos os usuários, o hash da senha, a senha em texto claro quando alguém cadastra alguém pela conversa, e a credencial de serviço guardada em texto no arquivo de configuração do cliente.
E duas camadas do backend que agravam: o token é assinado com segredo vazio se a variável não estiver no ambiente, e o seed versionado tem quatro usuários com o mesmo hash — uma senha comprometida abre quatro contas.”

**Slide 14 · Manutenção e evolução (45 s)**
“A leitura de manutenção, comparando com o backend do produto: de um lado, 43 suítes e 231 testes passando, integração contínua em três sistemas, arquitetura hexagonal. Do outro, a solução analisada: zero testes, zero CI, um arquivo de 334 linhas sem separação de camadas.
E vale reconhecer: a bateria que mostrei no slide 5 é um script externo, que eu rodei no meu ambiente. Ela não está no repositório. Ou seja, hoje a única rede de segurança é alguém lembrar de validar à mão.
Nos outros pontos: duas dependências sem nenhuma referência no código, e uma camada de compatibilidade com a versão 2 do MCP que existe no código — a gente testou, sobe e registra as doze ferramentas — mas o requirements fixa a versão 1.
A leitura: essa ponte nasceu fora da disciplina que o produto já tem. Não é falta de capacidade do time; é o custo de tratar ‘expor a API para IA’ como protótipo — e é o que mais encarece a próxima mudança.”

**Slide 15 · Roadmap e fechamento (50 s)**
“Fechando com o que fazer primeiro.
P0, os dois mais urgentes: filtrar o que as ferramentas devolvem — sem hash de senha, sem dado pessoal desnecessário — e exigir confirmação humana em escrita e exclusão; e trocar identidade por parâmetro por identidade real de quem conversa.
P1: testes de contrato e integração contínua no repositório, aproveitando o padrão que o backend já tem; e mover filtro e paginação para o servidor, alinhando o contrato da API.
P2: auditoria, limite de taxa, versão, licença e README com seção de segurança.
As cinco frases: a solução funciona, com doze ferramentas respondendo e dois recursos com dado real; o risco não está em falhar, e sim no que ela autoriza; a identidade do usuário vem do modelo, logo autorização não existe; o dado pessoal entra no contexto do agente pelo caminho mais curto, que é a listagem; e sem teste no repositório cada mudança depende de alguém lembrar de validar.
Embaixo estão os repositórios, o commit analisado, como reproduzir e o limite da análise: o que está marcado como observado foi executado localmente, e o ambiente local não tem proxy, WAF ou cotas de produção.
E é isso; ficamos à disposição para as perguntas.”

---

## Perguntas prováveis (quem responde)

| Pergunta | Responde | Resposta curta |
|---|---|---|
| “O que é MCP?” | P1 | É o protocolo que permite a um agente de IA chamar ferramentas de um sistema. Aqui ele expõe 12 ferramentas da API do PetHouse em linguagem natural. |
| “Como vocês verificaram que funciona?” | P2 | Executamos o sistema inteiro e rodamos uma bateria em quatro configurações de credencial com o cliente MCP oficial: 15/15 checagens. O script é externo, não está no repositório. |
| “Por que o agente consegue apagar anúncio de qualquer pessoa?” | P3 | Porque a exclusão não verifica dono e não pede confirmação — e a identidade que poderia autorizar não existe no caminho do agente. |
| “O agente é inseguro?” | P4 | O agente usa o que está exposto. O que falta é política no adaptador: filtrar o que a ferramenta devolve, confirmar ação e agir com identidade do usuário. |
| “Qual o risco mais grave hoje?” | P4 | Listar usuários devolve o hash da senha de todos e apagar anúncio não exige dono nem confirmação — as duas coisas com a mesma credencial de serviço. |
| “Por que o repositório não tem teste?” | P4 | Foi tratado como protótipo: a verificação ficou fora do repositório. É o primeiro item de P1 no roadmap, e o backend do produto já tem o padrão para copiar. |
| “Por que o dado pessoal aparece no contexto do modelo?” | P4 | Porque a listagem de anúncios e a de usuários devolvem o objeto completo, incluindo e-mail, telefone, endereço e hash de senha. A mitigação é selecionar campos na origem. |
| “O que falta para isso ir para produção?” | P1 | O P0 do roadmap: filtro de campos, confirmação humana e identidade por usuário. O resto do caminho é teste automatizado e paginação. |

## Checklist de ensaio

- [ ] rodar o deck inteiro com cronômetro: alvo 13–15 min; se passar, encurte o slide 4 (Inventário) falando só as três naturezas de ressalva.
- [ ] cada pessoa ensaia a primeira e a última frase do seu bloco sem olhar o slide.
- [ ] o vídeo da demo abre **sem internet** (baixe o arquivo) e é mudo: ensaie a narração por cima e teste o volume da sala.
- [ ] decidir sobre os dados pessoais visíveis no vídeo entre 0:47 e 0:52 (nome, e-mail, telefone, endereço): manter como evidência ou tarjar antes de projetar.
- [ ] combinar quem controla a passagem de slide e usar sempre a mesma frase de deixa.
- [ ] **não falar**: nada sobre correção, versão anterior ou mudança do código — a apresentação descreve o sistema como ele é; também não citar dados reais do seed além do que o vídeo já mostra, e nunca dizer que “o agente errou” (o defeito é do desenho do adaptador ou do contrato da API).
- [ ] números sempre com a mesma fonte: 12 tools, 2 resources, 15/15 checagens, 334 linhas, 7 hashes em 7 usuários, 5 posts / 8 usuários / 6 denúncias, 231 testes no backend, 15 slides.
