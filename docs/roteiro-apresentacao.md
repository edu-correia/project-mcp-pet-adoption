# Roteiro de apresentação — PetHouse MCP Server (análise de manutenção e evolução)

16 slides, 4 apresentadores, alvo de **13 a 15 minutos** + perguntas — dos quais 1min30 é o vídeo da demo. Cada pessoa fala ~3 minutos.
O roteiro está escrito para ser falado (não lido): decore a primeira e a última frase de cada bloco e improvise o meio olhando o slide.

## Divisão

| Quem | Slides | Tempo | Papel |
|---|---|---|---|
| **P1** | 1 a 4 | ~3 min | abre, situa o produto e mostra o inventário (o problema) |
| **P2** | 5 a 8 | ~4 min | como verificamos, o que a solução deveria entregar e **a demo em vídeo (58 s)** |
| **P3** | 9 a 12 | ~3 min | os insucessos técnicos: contrato, falha silenciosa, identidade, segurança |
| **P4** | 13 a 16 | ~3 min | segurança no contexto do modelo, manutenção, roadmap e fechamento |

Sugestão de nomes (trocar à vontade): P1 Theo, P2 Mateus, P3 Eduardo, P4 Bernardo.
Eduardo escreveu o servidor MCP — deixá-lo no bloco 8–11 ajuda nas perguntas técnicas.

## Combinado de passagem (use sempre a mesma frase)

- P1 → P2: “e foi assim que a gente foi verificar isso na prática.”
- P2 → P3 (depois do vídeo): “o agente não é o vilão — ele usou o que estava exposto. O defeito é do adaptador, e é o que vem agora.”
- P3 → P4: “tudo isso tem uma camada a mais, que é o que entra no contexto do modelo.”
- P4 (fechamento) → grupo: “e é isso; ficamos à disposição para as perguntas.”

---

## P1 — slides 1 a 4 (~3 min)

**Slide 1 · Capa (20 s)**
“Boa noite. Somos o grupo do PetHouse, e este trabalho é de Manutenção e Evolução de Software.
O PetHouse é a nossa plataforma de adoção de cães e gatos. Em vez de apresentar o que a gente construiu, a gente vai fazer uma análise crítica de uma evolução que fizemos nele: um servidor MCP, que é uma ponte para um agente de IA conversar com a nossa API e fazer coisas no sistema.”

**Slide 2 · Tese e números (45 s)**
“Começando pelos números que interessam. O repositório novo tem cinco arquivos versionados, 303 linhas de Python e quatro commits em dois dias. Ele expõe doze ferramentas e dois recursos para o agente.
E o número que dá o tom desta apresentação: **seis dessas doze ferramentas não entregam o que prometem** — cinco falham sempre e uma devolve vazio sem avisar. Testes, lint e integração contínua: zero.
A nossa tese é uma frase: o MCP não é só mais uma integração, ele transforma texto não confiável em ação com consequência. E as garantias que existiam na tela — identidade, dono do anúncio, confirmação — teriam que existir no adaptador.”

**Slide 3 · A solução e o fluxo (50 s)**
“Só para situar: o PetHouse é um projeto de quatro integrantes, já evoluído numa disciplina anterior. React no front, Express e TypeScript no back em arquitetura hexagonal, Postgres, login por JWT em cookie e senha com bcrypt. O que a gente fez agora foi um cliente fino dessa API: onze endpoints virados ferramentas, que o agente chama em linguagem natural.
Olhando o caminho: usuário fala, o Claude Desktop escolhe a ferramenta, o servidor MCP chama a API na porta 3333, e a API fala com o banco. O detalhe está na caixa do meio: esse servidor **não tem credencial nenhuma**.
Na tabela de baixo, a comparação que a gente fez questão de deixar explícita: identidade, dono do anúncio, confirmação e a distinção entre dado e comando existiam quando quem usava era uma pessoa na tela — nenhuma delas existe no caminho do agente.”

**Slide 4 · Inventário das 12 ferramentas (70 s)**
“Este é o slide mais denso, então vou guiar vocês por ele. Cada linha é uma ferramenta que o agente vê, o endpoint que ela chama, se aquele endpoint exige login, e o que aconteceu quando a gente executou de verdade.
No topo, o que funciona: listar pets, detalhes de um pet, remover pet e a média de reputação — quatro. O cadastro de anúncio só funciona se vier a foto, porque a coluna no banco não aceita nulo.
No meio, a busca por raça, idade ou palavra-chave: **devolve vazio sempre**, e isso é uma falha silenciosa, não um erro.
E embaixo, cinco ferramentas que retornam erro 500 em toda tentativa: listar usuários, buscar usuário por id, curtir, contar curtidas e denunciar — justamente a parte de interação social do produto.
Fechando a conta: quatro funcionam, uma funciona só com um parâmetro, uma funciona pela metade, uma devolve vazio e cinco são inalcançáveis. Dá doze.
E foi assim que a gente foi verificar isso na prática.” *(passa para P2)*

---

## P2 — slides 5 a 8 (inclui a demo em vídeo) (~4 min)

**Slide 5 · Método (40 s)**
“Antes de acusar o código, a gente precisa mostrar como mediu. Leu os dois repositórios no commit 90b6e86, e leu o que a API realmente faz — rotas, middlewares, repositórios e casos de uso — porque o que a documentação promete não é o que a API devolve.
Depois subiu o sistema inteiro: Postgres 14 com o script de criação do próprio projeto, o backend em Node 18 na porta 3333, e um cliente MCP oficial falando com o servidor por stdio.
O bloco cinza são saídas reais, não exemplo: a busca devolveu vazio com um pug cadastrado; a estatística devolveu zero três vezes com seis posts e cinco usuários no banco; e uma ferramenta devolveu stack trace.
Regra do trabalho: o que a gente chama de observado foi executado. O que é conclusão de leitura de código está marcado no texto, e aqui o ambiente é local — sem proxy, sem WAF, sem cota.”

**Slide 6 · Casos de uso (45 s)**
“Com o sistema na mão, esses são os casos de uso que justificam a existência do projeto.
O primeiro é a busca conversacional: a pessoa descreve o que quer — cão pequeno, dócil, que aceite apartamento — e não precisa dominar filtro de tela. É o caso que dá sentido ao projeto.
Depois, moderação assistida: resumir denúncia, apontar anúncio repetido. Panorama para quem decide, sem abrir banco. E cadastro assistido do adotante, que ataca abandono de cadastro.
E tem um ganho de engenharia que vale para os quatro: como o adaptador é fino, expor uma nova função da API ao agente custa poucas linhas — desde que o contrato dela seja respeitado. É aí que a próxima parte pega.”

**Slide 7 · Caso de uso destaque (45 s)**
“Vamos pegar o caso que mais importa. Deveria ser assim: a pessoa pergunta por um pug dócil, o agente chama a busca com raça igual a Pug, recebe o anúncio da Lulu — pug, doze anos, ‘só dorme’ — e responde com nome, idade e descrição.
O que aconteceu: a ferramenta devolve lista vazia — nas três tentativas, por raça, por descrição e por idade. E aqui está o achado que só apareceu quando a gente foi gravar a demo: o agente costuma **contornar** a ferramenta quebrada. Ele chama a listagem completa, filtra por conta própria e acerta a resposta.
O problema é o preço: para responder ‘tem pug?’ ele joga a base inteira no contexto dele, com os dados do dono de cada anúncio. Ou seja, o defeito é invisível com cinco anúncios e vira custo, privacidade e escala quando a base cresce — e se o agente escolher a ferramenta certa, a resposta é vazia.
É isso que a gente vai mostrar agora, no vídeo.”

---

**Slide 8 · Demo em vídeo (58 s, mudo)**
*Antes de dar play (15 s):* “Vou mostrar isso acontecendo, no Claude Desktop falando com o nosso servidor. Olhem três coisas: o rótulo da ferramenta que ele chama, o que o pedido teve de informar e o que aparece na tela no fim.”
*Durante:* o vídeo é mudo — narre por cima em duas frases: “aqui ele está escolhendo a ferramenta sozinho, é a nossa: Pethouse, listar todos os pets” (aos ~0:40) e “para cadastrar, o pedido levou `ownerId: 1`” (aos ~0:25).
*Depois (20 s):* “Três coisas para levar daqui. Um: quem respondeu foi o nosso servidor — o rótulo na tela é a nossa ferramenta. Dois: para cadastrar, **a identidade foi digitada no chat** — `ownerId: 1` — e o agente confirmou ‘Dono: ID 1 (Eduardo Sereia)’. Ninguém estava logado. Três: na listagem seguinte o payload cru subiu na tela com nome, e-mail, telefone e endereço do dono.
O agente não é o vilão: ele usou o que estava exposto. É o que vem agora.” *(passa para P3)*

---

## P3 — slides 9 a 12 (~3 min)

**Slide 8 · Insucesso 1: contrato (55 s)**
“O primeiro insucesso tem uma causa só, e ela se repete: o adaptador não conhece o contrato da API. A tela documenta uma coisa, a API faz outra.
A API devolve um objeto com a lista dentro do campo body — o adaptador testa se aquilo é uma lista, não é, e cai num retorno vazio. É literalmente a razão de a busca nunca funcionar.
A foto é declarada como opcional para o modelo, mas a coluna é obrigatória no banco: quem não manda foto recebe erro 500.
O cadastro de usuário aceita telefone, endereço e descrição, e o caso de uso **sobrescreve os três** com texto padrão: o dado é descartado em silêncio, e o agente acredita que salvou.
A política de senha não está em lugar nenhum: a API exige de 8 a 16 caracteres com maiúscula, minúscula, número e caractere especial. O modelo não tem como adivinhar — toma 400.
E a última linha é o padrão de manutenção que mais custa: o bug da data de criação foi corrigido no cliente, calculando `createdAt` no relógio da máquina do agente. Ou seja, a regra de negócio migrou para o adaptador — o oposto do que a arquitetura hexagonal do nosso backend propõe.”

**Slide 9 · Insucesso 2: falha silenciosa (50 s)**
“Esse é o meu slide favorito para discutir falha silenciosa. O recurso de estatísticas devolve: zero posts, zero usuários, zero denúncias. No mesmo momento, o banco tinha seis anúncios, cinco usuários e denúncias.
A mecânica: quando a API responde 401 ou 500, o adaptador devolve um dicionário de erro; o código soma ‘tamanho se for lista, senão zero’ — e o erro **vira o número zero**. Dois dos três endpoints falham, e a frase final tem cara de medição.
Na parte de baixo, a prova do diagnóstico: a gente aplicou um patch de duas linhas no filtro e a mesma chamada passou a devolver o pug.
Ou seja: erro de dependência não pode virar valor de negócio. O certo é dizer ‘não foi possível consultar’, nunca ‘zero’. E contrato não se descobre lendo; descobre-se com teste que falha quando a forma da resposta muda.”

**Slide 10 · Insucesso 3: sem identidade (50 s)**
“O terceiro bloco é de identidade, e tem dois lados.
À esquerda, as cinco ferramentas que dependem de login: como o adaptador é um cliente anônimo — ele nunca faz login, não guarda token, não tem usuário — todas retornam erro de autenticação. E isso é do adaptador, não do sistema: a gente testou, a API autentica normalmente; o que ela não aceita é `Authorization: Bearer`, porque o middleware lê só o cookie `jwt`. O agente tenta, recebe stack trace e improvisa uma explicação para o usuário — o defeito de autorização vira afirmação errada na conversa.
À direita, o lado mais delicado: nas rotas públicas, o dono não vem da sessão, vem do parâmetro. O `owner_id` tem valor padrão 1, e a denúncia recebe o id de quem denuncia como texto. No nosso teste, o anúncio criado pelo agente apareceu no sistema **como se fosse do usuário 1**, sem nenhum login. É a peça mais frágil da análise: a autorização do produto vive da identidade, e aqui a identidade é um parâmetro que o modelo escolhe.”

**Slide 11 · Segurança: o que o agente pode fazer (50 s)**
“Juntando 10 e 11 numa pergunta prática: o que o modelo pode fazer hoje sem credencial nenhuma?
Pode listar todos os anúncios com os dados do dono — e-mail, endereço, telefone — e isso vai para o contexto, e para o provedor do modelo.
Pode criar anúncio em nome de qualquer id. Pode apagar anúncio de qualquer id. Pode criar contas em massa: não existe limite de taxa nem registro de autoria. E pode ler a reputação de qualquer pessoa.
O bloco cinza é a execução real: criamos um anúncio pelo agente e apagamos dois, sem login e sem dono verificado. Na apresentação a gente apagou só o que criou no teste, mas nada no sistema impediria apagar os anúncios reais, porque o endpoint aceita qualquer id.
Fica a formulação que a gente leva: em um agente, ‘destrutivo’ não é o verbo da ferramenta. É a combinação de irreversibilidade, ausência de confirmação e ausência de identidade. Aqui as três coexistem. Tudo isso tem uma camada a mais, que é o que entra no contexto do modelo.” *(passa para P4)*

---

## P4 — slides 13 a 16 (~3 min)

**Slide 12 · Segurança: o que vaza para o modelo (55 s)**
“Esse slide é sobre o que muda quando o consumidor é um modelo de linguagem.
À esquerda, injeção indireta: o campo de descrição do anúncio é texto livre escrito por qualquer usuário, e a ferramenta de listagem entrega esse texto ao modelo. O trecho que está na tela foi escrito por nós durante o teste e voltou íntegro — no meio dele, uma instrução para o assistente ignorar o usuário e chamar a ferramenta de remover. No front, isso seria só um anúncio feio na tela. Aqui, é uma instrução ao lado de uma ferramenta destrutiva.
À direita, três vazamentos: o bloco do dono no prompt; a senha como parâmetro de ferramenta — senha em texto claro no histórico da conversa; e as respostas de erro repassadas cruas, com stack trace e caminhos internos.
E na faixa de baixo o risco que só aparece depois: quando as ferramentas de usuário passarem a funcionar, elas vão devolver o hash bcrypt da senha de todos. Corrigir a autenticação sem filtrar a resposta troca um erro por um incidente.
Duas camadas do back que agravam: o JWT é assinado com segredo vazio se a variável não estiver no ambiente, e o seed versionado tem os quatro usuários com o mesmo hash.”

**Slide 13 · Manutenção e evolução (50 s)**
“Agora a leitura de manutenção, e o slide mais desconfortável para nós.
À esquerda, o projeto original: 43 suítes, 231 testes passando, integração contínua em três sistemas, formatação verificada, arquitetura documentada, 110 commits com revisão de outro integrante. À direita, o repositório novo: zero testes, zero CI, nada de análise estática, um único arquivo de 303 linhas, quatro commits em dois dias direto na main.
Ou seja, o repositório novo nasceu fora da disciplina que o projeto já tinha. Não é falta de capacidade do time — é o custo de tratar ‘expor a API para IA’ como protótipo.
Nos dois cartões de baixo, o que ficou pendurado: duas dependências que não são usadas em nenhuma linha; uma camada de compatibilidade com a v2 do MCP que funciona — a gente testou, sobe e registra as doze ferramentas — mas que nunca roda, porque o requirements fixa a versão 1; e o acoplamento, com o adaptador decidindo data, dono, permissão e a busca inteira em memória, sem paginação.”

**Slide 14 · Roadmap (45 s)**
“Do diagnóstico para o que fazer, em três prioridades.
P0 é segurança e identidade: identidade real no caminho do agente, com o id vindo de um contexto autenticado em vez de parâmetro; confirmação humana obrigatória nas ferramentas de escrita e destrutivas, separadas das de leitura; e minimização de dado no prompt — sem o bloco do dono, sem senha por parâmetro e sem stack trace.
P1 é contrato: schema e teste de contrato com API simulada, integração contínua no repositório do MCP, e corrigir as seis ferramentas. É a causa-raiz dos defeitos que mostramos, e o repositório irmão já tem o padrão para copiar.
P2 é operação e higiene: auditoria, limite de taxa, versão, changelog, licença, política de senha documentada e o default de data no servidor, onde ele deveria estar desde o começo.”

**Slide 15 · Fechamento (50 s)**
“Para fechar, cinco frases.
Um: a ideia é boa, a execução não sustenta o caso principal. Dois: o adaptador não conhece o contrato da API — e isso não se resolve lendo, se resolve testando. Três: autenticação não é detalhe de implementação, é a garantia que o agente herdou ou perdeu. Quatro: o risco novo é o fluxo, não a linha de código. E cinco: o repositório novo abandonou a disciplina do original — e a evolução mais barata é reaproveitar o que o time já sabe fazer.
Também vale registrar o que a solução acerta: adaptador fino, uma regra em um lugar só, casos de uso coerentes com o produto, adesão a um padrão que a indústria está adotando e a compatibilidade com as duas versões do MCP, que a gente verificou funcionando.
Embaixo estão os repositórios, o commit analisado, como reproduzir e o limite honesto da análise: o que está marcado como observado foi executado localmente; o resto é leitura de código.
E é isso; ficamos à disposição para as perguntas.”

---

## Perguntas prováveis (quem responde)

| Pergunta | Responde | Resposta curta |
|---|---|---|
| “Se vocês sabem o que está errado, por que não corrigiram?” | P3 | O trabalho da disciplina é análise; o roadmap mostra o caminho, e o fix mais barato é justamente o P1: teste de contrato. |
| “O MCP é inseguro por natureza?” | P4 | Não. MCP é transporte. O que falta é política no adaptador: identidade, confirmação e minimização de dado. |
| “Isso é defeito do backend ou do servidor MCP?” | P3 | Dos dois: a API tem rotas públicas sem dono (herdado do projeto original) e o MCP não autentica nem confirma (defeito novo). |
| “E os erros de autenticação, foram do MCP ou do sistema?” | P3 | Do MCP: ele nunca manda credencial (nem cookie, nem header). A API autentica — login + chamada com cookie devolve 200. Duas coisas do lado da API atrapalham o diagnóstico: responde 500 em vez de 401 e só lê o token do cookie, ignorando `Authorization: Bearer`. |
| “No vídeo o Claude acertou o pug — então a busca funciona?” | P2 | Não: ele acertou **contornando**, baixando a lista completa e filtrando. Chamando a ferramenta de busca, a resposta é `{"result": []}` — está no próprio vídeo. |
| “Como ficaria a confirmação humana na prática?” | P1 ou P4 | Ferramenta destrutiva em duas etapas: o agente propõe, o cliente mostra e só executa com aprovação explícita. Leitura e ação em ferramentas separadas. |
| “E a LGPD?” | P4 | Dado pessoal no prompt é tratamento de dado: minimizar campos na origem, mandar só o necessário e nunca credencial. |
| “Quanto tempo para corrigir?” | P2 | Estimativa: P0 em um a dois dias, P1 em cerca de uma semana com os testes de contrato — é estimativa, não medição. |

## Checklist de ensaio

- [ ] rodar o deck inteiro uma vez com cronômetro: alvo 12–14 min; se passar de 15, corte o slide 4 (Inventário) para 50 s falando só os baldes.
- [ ] cada pessoa ensaia a sua primeira e a sua última frase sem olhar.
- [ ] combinar quem controla a passagem de slide (uma pessoa só, sentada no notebook) e usar a mesma frase de deixa.
- [ ] o vídeo da demo abre no notebook da apresentação **sem depender da internet da sala** (baixe o arquivo); ele é mudo, então ensaie a narração por cima e teste o volume da sala.
- [ ] decidir sobre os dados pessoais que aparecem no vídeo entre 0:47 e 0:52 (nome, e-mail, telefone, endereço do dono): manter como evidência ou tarjar antes de projetar.
- [ ] depois de gravar: apagar o anúncio criado na demo e parar os containers (`docker stop petapi petpg`).
- [ ] **não falar**: dados reais do seed (nomes, e-mails, telefones), valores de commit de outro repositório, nem “o agente errou” — o defeito é do adaptador, não do modelo.
- [ ] números citados sempre com a mesma fonte da apresentação: 12 ferramentas, 6 que não entregam, 231 testes, 110 commits, 6 posts e 5 usuários no banco de teste.
