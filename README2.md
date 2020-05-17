# Guiıes das Sessıes Laboratoriais


---
## FinalizaÁ„o

ConcluÌda a realizaÁ„o dos guiıes das sessıes laboratoriais, devem proceder ‡ **arrumaÁ„o** do repositÛrio contendo uma nova directoria para a vers„o final da aplicaÁ„o "Cliente/Servidor", que incorpore eventuais melhoramentos sobre as implementaÁıes dos v·rios guiıes. Relembra-se ainda a necessidade de incluir informaÁ„o no ficheiro `Readme.md` de todos os melhoramentos dnos guiıes adicionados depois do prazo previsto.

```
+-- Readme.md: ficheiro se apresenta o conte˙do do repositÛrio, dando nota dos guiıes que sofreram alteraÁıes/melhoramentos
|              depois do prazo previsto.
+-- Guiao1
|        +-- Readme.md: notas sobre a realizaÁ„o do gui„o da semana 3 (justificaÁ„o das opÁıes
|        |              tomadas; instruÁıes de uso; dificuldades encontradas; etc.)
|        +-- ...
|
...
|
+-- CliServ
         +-- Readme.md: notas sobre a aplicaÁ„o Cliente/Servidor final (dever· corresponder
         |              essencialmente a uma vers„o eventualmente melhorada do gui„o do gui„o 10).
         +-- ...
```

Como melhoramento ao pedido nos guiıes, sugere-se a geraÁ„o dos certificados utilizados pela aplicaÁ„o. Para tal pode
usar qualquer das v·rias sugestıes de software livre disponÌvies para o efeito - uma escolha Ûbvia È naturalmente
o `openssl` a que j· recorremos antes, mas preferindo podem utilizar uma soluÁ„o de mais alto nÌvel, como a [EJBCA](https://www.ejbca.org).

Alguns apontadores:
 * http://pki-tutorial.readthedocs.io/en/latest/expert/
 * https://jamielinux.com/docs/openssl-certificate-authority/index-full.html
 * https://roll.urown.net/ca/ca_intermed_setup.html

---
## Gui„o 9

### FinalizaÁ„o do protocolo StS usando certificados

No gui„o desta semana vamos concluir a implementaÁ„o do protocolo _Station_to_Station_ fazendo uso de certificados X509. Para tal vamos incorporar a funcionalidade explorada no ˙ltimo gui„o (validaÁ„o dos certificados), por forma a assegurar a cada um dos intervenientes que fazem uso da chave p˙blica correcta na verificaÁ„o da assinatura.

Concretamente, o protocolo a implementar ir· ser ent„o:
1. Alice ? Bob : g<sup>x</sup>
1. Bob ? Alice : g<sup>y</sup>, Sig<sub>B</sub>(g<sup>x</sup>, g<sup>y</sup>), Cert<sub>B</sub>
1. Alice ? Bob :  Sig<sub>A</sub>(g<sup>x</sup>, g<sup>y</sup>), Cert<sub>A</sub>
1. Alice, Bob : K = g<sup>(x*y)</sup>

Note que os pares de chave a utilizar neste gui„o s„o os fornecidas nas _keystores_ PKCS12 fornecidos no gui„o 8.

Alguns apontadores:
 * Biblioteca [PyOpenSSL](https://www.pyopenssl.org/en/stable/), em particular os mÈtodos:
    * [load_certificate](https://www.pyopenssl.org/en/stable/api/crypto.html#OpenSSL.crypto.load_certificate) e [dump_certificate](https://www.pyopenssl.org/en/stable/api/crypto.html#OpenSSL.crypto.dump_certificate)
    * [load_pkcs12](https://www.pyopenssl.org/en/stable/api/crypto.html#OpenSSL.crypto.load_pkcs12) e os v·rios mÈtodos da classe [PKCS12](https://www.pyopenssl.org/en/stable/api/crypto.html#pkcs12-objects)
    * os v·rios mÈtodos da classe [X509Store](https://www.pyopenssl.org/en/stable/api/crypto.html#x509store-objects) (em particular, o [verify_certificate](https://www.pyopenssl.org/en/stable/api/crypto.html#OpenSSL.crypto.X509StoreContext.verify_certificate]))
    
---
## Gui„o 8

### ManipulaÁ„o de Certificados X509

O objectivo nesta semana È o de se investigar formas de validar _cadeias de certificados_ em _Python_. A ideia È que, mais tarde, esses certificados ser„o incorporados na aplicaÁ„o clente-servidor que temos vindo a implementar - mas neste gui„o o objectivo È forcar no aspecto da _validaÁ„o_ desses certificados.

Como ponto de partida, disponibiliza-se:

 1. Uma _keystore_ PKCS12 contendo o Certificado (e respectiva chave privada) para o rervidor: [Servidor.p12](Servidor.p12)
 1. Uma _keystore_ PKCS12 contendo o Certificado (e respectiva chave privada) para o cliente: [Cliente1.p12](Cliente1.p12) 
 1. O Certificado (em formato DER) da CA utilizada: [CA.cer](CA.cer)

Para aceder ao conte˙do das `Keystores` devem utilizar a password "1234", quer para carregar a `keystore`, quer para aceder ‡ entrada respectiva (o `alias` È `Cliente1` e `Servidor` para as keystores `Cliente1.p12` e `Servidor.p12` respectivamente).

Numa primeira fase, utilizaremos ferramentas de domÌnio p˙blico directamente na linha-de-comando. Concretamente, utilizaremos o [openSSL](https://www.openssl.org), e em particular os sub-comandos (ver respectiva documentaÁ„o):
 - [`x509`](https://www.openssl.org/docs/manmaster/man1/openssl-x509.html);
 - [`pkcs12`](https://www.openssl.org/docs/manmaster/man1/openssl-pkcs12.html);
 - [`verify`](https://www.openssl.org/docs/manmaster/man1/verify.html).

Uma vez ultrapassado esse passo, vamos considerar como transpor esse mÈtodo de validaÁ„o para o _Python_, por forma a ser us·vel na aplicaÁ„o cliente-servidor. A dificuldade È que as bibliotecas que temos vindo a utilizar n„o dispıe dessa funcionalidade, pelo que se sugere a instalaÁ„o/utilizaÁ„o da biblioteca [PyOpenSSL](https://pyopenssl.org/en/stable/index.html).

ReferÍncias adicionais:
 - http://www.yothenberg.com/validate-x509-certificate-in-python/
 - http://aviadas.com/blog/2015/06/18/verifying-x509-certificate-chain-of-trust-in-python/
 - https://stackoverflow.com/questions/6345786/python-reading-a-pkcs12-certificate-with-pyopenssl-crypto
 
 obs [21/11/19]: actualizados certificados

---
## Gui„o 7

### Protocolo *Station-to-Station* simplificado

Pretende-se complementar o programa com o acordo de chaves *Diffie-Hellman* para incluir a funcionalidade
an·loga ‡ do protocolo *Station-to-Station*. Recorde que nesse protocolo È adicionado uma troca de assinaturas:

1. Alice ? Bob : g<sup>x</sup>
1. Bob ? Alice : g<sup>y</sup>, Sig<sub>B</sub>(g<sup>x</sup>, g<sup>y</sup>)
1. Alice ? Bob :  Sig<sub>A</sub>(g<sup>x</sup>, g<sup>y</sup>)
1. Alice, Bob : K = g<sup>(x*y)</sup>

De notar que um requisito adicional neste protocolo È a manipulaÁ„o de pares de chaves assimÈtricas para realizar as assinaturas digitais (e.g. RSA). Para tal deve produzir um pequeno programa que gere os pares de chaves para cada um dos intervenientes e os guarde em ficheiros que ser„o lidos pela aplicaÁ„o Cliente/Servidor.

Sugest„o: comece por isolar as "novidades" requeridas pelo gui„o, nomeadamente:
  1. criaÁ„o do par de chaves para a assinatura e utilizaÁ„o dos mÈtodos para ''assinar'' e ''verificar''

  1. gravar as chaves p˙blicas/privadas em ficheiro
  
  1. integrar as assinaturas no protocolo _Diffie-Hellman_

---
## Gui„o 6

### Protocolo *Diffie-Hellman*

Relembre o protocolo de acordo de chaves _Diffie\_Hellman_:

 1. Alice ? Bob : g<sup>x</sup>
 1. Bob ? Alice : g<sup>y</sup>
 1. Alice, Bob : K = g<sup>(x*y)</sup>

Onde `g` È um gerador de um grupo cÌclico de ordem prima `p`, `x` e `y` s„o elementos aleatÛrios do grupo, e `K` È o segredo estabelecido pelo protocolo. Todas as operaÁes s„o realizadas mÛdulo `p`.

Pretende-se implementar o protocolo de acordo de chaves *Diffie-Hellman* fazendo uso da funcionalidade oferecida pela biblioteca `cryptography`. Em concreto, utilizando a classe [`dh`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/).

Algumas observaÁıes:
 * Se pretender, pode fixar os par‚metros do grupo utilizando por exemplo:
 ```
P = 99494096650139337106186933977618513974146274831566768179581759037259788798151499814653951492724365471316253651463342255785311748602922458795201382445323499931625451272600173180136123245441204133515800495917242011863558721723303661523372572477211620144038809673692512025566673746993593384600667047373692203583
G = 44157404837960328768872680677686802650999163226766694797650810379076416463147265401084491113667624054557335394761604876882446924929840681990106974314935015501571333024773172440352475358750668213444607353872754650805031912866692119819377041901642732455911509867728218394542745330014071040326856846990119719675
```
 * A documentaÁ„o da biblioteca n„o È muito clara na forma como se pode comunicar as chaves p˙blicas DH, tal como requerido pelo protocolo. Na pr·tica, existem duas alternativas:
     - Aceder ao valor (inteiro) da chave p˙blica atravÈs da classe `DHPublicNumbers`
     - Utilizar as facilidades de serializaÁ„o da chave p˙blica oferecidas pela biblioteca (acessÌvel a partir do mÈtodo `public_bytes` da classe `DHPublicKey`).

---
## Gui„o 5


### ComunicaÁ„o entre cliente-servidor

As scripts [Client.py](scripts/Client.py) e
[Server.py](scripts/Server.py) constituem uma implementaÁ„o muito
b·sica de uma aplicaÁ„o que permite a um n˙mero arbitr·rio de
clientes comunicar com um servidor que escuta num dado port
(e.g. 8888). O servidor atribui um n˙mero de ordem a cada cliente, e
simplesmente faz o _dump_ do texto enviado por eese cliente
(prefixando cada linha com o respectivo n˙mero de ordem). Quando um
cliente fecha a ligaÁ„o, o servidor assinala o facto (e.g. imprimindo
[n], onde _n_ È o n˙mero do cliente).

Exemplo da execuÁ„o do servidor (que comunica com 3 clientes):


```bash
$ python3 Servidor.py
1 : daskj djdhs slfghfjs askj
1 : asdkdh fdhss
1 : sjd
2 : iidhs
2 : asdjhf sdga
2 : sadjjd d dhhsj
3 : djsh
1 : sh dh d   d
3 : jdhd kasjdh as
2 : dsaj dasjh
3 : asdj dhdhsjsh
[3]
2 : sjdh
1 : dhgd ss
[1]
2 : djdj
[2]
```

Pretende-se:

 * Modificar as respectivas classes por forma a garantir a
   _confidencialidade_ e _integridade_ nas comunicaÁıes
   estabelecidas.
 * Para garantir a confidencialidade, dever· considerar uma cifra por
   blocos no modo que considerar mais apropriado.
 * Na resoluÁ„o deste gui„o, vamos desvalorizar as questıes relativas
   ‡ protecÁ„o da(s) chave(s) requeridas (e.g. podemos considerar
   chaves fixas no prÛprio cÛdigo). A ideia È que iremos abordar esse
   problema mais tarde.
 * obs: nas implementaÁıes fornecidas das classes `Client` e
   `ServerWorker`, n„o dever· ser necess·rio "mexer" muito para alÈm
   do mÈtodo `process`.

---
## Gui„o 4

### AnimaÁ„o de modelos de seguranÁa

Pretende-se animar em _Python_ os "jogos" que servem de base aos modelos de seguranÁa
adoptados na formalizaÁ„o das provas de seguranÁa. Especificamente,
sugere-se ilustrar ataque(s) ‡ confidencialidade das cifras, recorrende ‡ definiÁ„o de
**IND-CPA** (_indistinguibilidade na presenÁa
de ataques de texto-limpo escolhido_). Recorda-se que o jogo `IND-CPA` È definido
como (apresentado numa sintaxe que pretende facilitar a transposiÁ„o para a respectiva
codificaÁ„o em _Python_).

```
IND_CPA(C,A) =
  k = C.keygen()
  enc_oracle = lambda ptxt: C.enc(k,ptxt)
  m[0], m[1] = A.choose(enc_oracle)
  b = random_bit()
  c = C.enc(k,m[b])
  b' = A.guess(enc_oracle, c)
  return b==b'
```

Obs: `m[0]` e `m[1]` devem ser mensagens com um tamanho fixo prÈ-determinado; assume-se
ainda que o advers·rio `A` dispıe de "vari·veis de inst‚ncia" que armazena o estado
a preservar entre as duas chamadas.

A seguranÁa È estabelecida quando, para qualquer advers·rio, a sua **vantagem** definida
como `2 * | Pr[IND_CPA(C,A)=1] - 1/2 |` È negligÍnci·vel. Naturalmente que verificar a
seguranÁa de uma cifra concreta `C` estar· fora do alcance de uma "animaÁ„o" do jogo
`IND-CPA`, mas pode servir para ilustrar **ataques** instanciando um advers·rio que
permita um desvio significativo na probabilidade de sucesso do jogo.

Sugestıes:
 * O mecanismo de classes do _Python_ È particularmente ˙til na parametrizaÁ„o dos jogos;
 * Uma cifra claramente insegura, como a cifra `Identidade` (onde as operaÁıes de cifrar
 e decifrar s„o a funÁ„o identidade) pode ser ˙til para ilustrar os conceitos.
 * Alguns exemplos de ataques mencionados nas aulas que podem ser ilustrados: inseguranÁa
 das cifras determinÌsticas; do mecanismo _encrypt\_and\_mac_; modo ECB numa cifra por
 blocos; etc.
 
 ValorizaÁ„o:
  * Considere jogos para outros modelos mencionados na aula (e.g. IND-CCA, INT-PTXT, INT-CTXT)

---
## Gui„o 3
### ImplementaÁ„o de Cifra Autenticada

Tem-se vindo a fazer uso da cifra autenticada `Fernet` que
garante simultaneamente ('i') a confidencialidade dos dados e ('ii') a
integridade da informaÁ„o. Neste curso interessa-nos perceber como È que
essas propriedades podem ser estabelecidas a partir das v·rias tÈcnicas
criptogr·ficas disponÌveis, pelo que nesta semana iremos realizar a mesma
funcionalidade recorrendo directamente de uma _cifra simÈtrica_ e de um
_MAC_. A quest„o que surge È como combinar essas primitivas, sendo que È concebÌvel considerar as seguintes soluÁıes:

 * **encrypt and MAC**: onde tanto cifra como o MAC s„o aplicados sobre o texto limpo;
 * **encrypt then MAC**: onde o texto limpo passa originalmente pela cifra, e o MAC È calculado j· sobre o criptograma;
 * **MAC then encrypt**: onde È primeiro calculado o MAC sobre o texto limpo, e sÛ depois È cifrado (texto limpo e _tag_ de autenticaÁ„o).

Pretende-se ent„o substituir a cirfra `Fernet` do programa de cifra por cada uma das trÍs versıes referidas. Sugere-se a utilizaÁ„o de `ChaCha20` como cifra, e de `HMAC-Sha256` como MAC.

---
## Gui„o 2
### ProtecÁ„o de Segredos Criptogr·ficos

No gui„o da semana passada fez-se uso da cifra autenticada `Fernet`
que garante simultaneamente ('i') a confidencialidade dos dados e
('ii') a integridade da informaÁ„o. No entanto, e do ponto de vista de
seguranÁa, o aspecto mais crÌtico na resoluÁ„o do gui„o È o tratamento
dado aos segredos criptogr·ficos utilizados. De facto, e para alÈm de
se certificar que se recorre sempre a um **gerador de n˙meros
aletÛrios seguro**, È em geral desaconselhado armazenar segredos
criptogr·ficos em ficheiros sem qualquer protecÁ„o.

Existem duas estratÈgias para evitar a utilizaÁ„o desses ficheiros
desprotegidos:

 1. *Evitar a necessidade de se armazenar a chave*. Para isso, considera-se
 um mecanismo seguro que permita gerar um segredo criptogr·fico a partir
 de uma _password_ ou _passphrase_ (que naturalmente n„o podem ser utilizadas
 directamente como chaves criptogr·ficas). Para o efeito faz-se uso das
 designadas _Password Based Key Derivation Functions (PBKDF)_.
 1. Armazenar o ficheiro de forma protegida, no que se designa
 habitualmente por *KeyStore*. Na realidade, esta estratÈgia acaba por
 partilhar muitos dos requisitos da apresentada antes, porque para
 protegermos a 'KeyStore' ir· ter de (internamente) usar uma cifra
 autenticada, e para isso de um novo segredo. Mas, tal como no ponto
 anterior, esse segredo È geralmente gerado a partir de uma
 _password_. [**OBS:** na verdade, È muito raro utilizar-se
 _KeyStores_ para armazenar chaves simÈtricas -- as _KeyStores_ s„o
 normalmente utilizadas para armazenar secregdos de "longo-prazo", que
 n„o È o caso de chaves simÈtricas que se recomenda que sejam
 utilizadas uma ˙nica vez (chaves de sess„o)].
 
Pretende-se assim adicionar ‡ funcionalidade pedida no gui„o anterior
a protecÁ„o dos segredos de acordo com ambas as estratÈgias
apresentadas. 

Sugestıes:

 * Como mecanismo de PBKDF na primeiro abordagem, sugere-se a itilizaÁ„o da primitiva [`PBKDF2`](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC);
 * Na inicializaÁ„o do mecanismo PBKDF, ir· recorrer a um _salt_ aleatÛrio. Esse valor deve ser armazenado juntamente com o criptograma;
 * Para a leitura da _passphrase_, sugere-se a utilizaÁ„o do mÛdulo [`getpass`](https://docs.python.org/3.7/library/getpass.html), da biblioteca standard Python;
  * A cifra [`Fernet`](https://cryptography.io/en/stable/fernet/) adopta um formato para a chave com a codificaÁ„o `base64`. Para converter a _byte_string_ derivada pela KDF numa chave nesse formato, pode recorrer ao mÛdulo da biblioteca `base64` do `Python`, especificamente o mÈtodo [base64.urlsafe_b64encode](https://docs.python.org/2/library/base64.html#base64.urlsafe_b64encode);
 * Na segunda abordagem, recomenda-se o uso da PBKDF [`Scrypt`](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.scrypt.Scrypt), j· que adiciona protecÁ„o adicional a ataques de dicion·rio.


---

## Gui„o 1
### O Ambiente de Desenvolvimento

Esta primeira aula pretende essencialmente garantir uma utilizaÁ„o fluida do ambiente de trabalho adoptado
na UC. Isso pressupıe a utilizaÁ„o do `github` (em particular, do repositÛrio atribuÌdo ao grupo de trabalho), e
do ambiente `Python` (vers„o 3). 

#### InstalaÁ„o de bibliotecas de suporte

##### Cryptography - https://cryptography.io/en/latest/

A biblioteca criptogr·fica que iremos usar maioritariamente no curso È `cryptography`. Trata-se de uma biblioteca
para a linguagem Python bem desenhada e bem documentada que oferece uma API de alto nÌvel a diferentes
ìServiÁos Criptogr·ficosî (_recipes_). No entanto, e no ‚mbito concreto deste curso, iremos fazer um uso
"menos standard" dessa biblioteca, na medida em que iremos recorrer directamente ‡ funcionalidade de baixo nÌvel.

InstalaÁ„o:

Sugere-se o mÈtodo de instalaÁ„o baseado no `pip` (ver https://cryptography.io/en/latest/installation/).

```
pip3 install --upgrade pip
pip3 install cryptography
```

##### [opcional] Jupiter - https://jupyter.readthedocs.io/

`Jupyter` È um sistema de 'notebooks' para o Python que possibilita a
interaÁ„o com a linguagem por intermÈdio de um simples
'browser'. Esses ¥notebooks¥ permitem que, para alÈm cÈlulas contendo
cÛdigo Python e as respectivas respostas, existam elementos contendo
texto formatado, figuras, fÛrmulas matem·ticas (escritas em LaTeX),
etc.  A ideia da utilizaÁ„o desses ¥notebooks¥ ent„o a de permitir a
produÁ„o de documentos informativos contendo, para alÈm do cÛdigo
Python, todos os aspectos considerados relevantes (assumpÁıes, opÁıes
de desenho, limitaÁıes assumidas, etc.).

InstalaÁ„o:

Sugere-se o mÈtodo de instalaÁ„o baseado no `pip` (ver https://jupyter.readthedocs.io/en/latest/install.html)

```
pip3 install jupyter
```


### AplicaÁ„o de exemplo: Cifra autenticada de Ficheiro

Pretende-se cifrar o conte˙do de um ficheiro, assegurando a
*confidencialidade* e *integridade* dos dados l· armazenados.

 * Para o efeito deve o mecanismo de cifra autenticada _Fernet_,
disponibilizada pela biblioteca _cryptography_.
 * Emule o efeito de um 'ataque' ‡ integridade do criptograma. Verifique
o impacto na utilizaÁ„o do seu programa.

---

## ORGANIZA«√O DO REPOSIT”RIO

### ArrumaÁ„o do repositÛrio

Por forma a permitir um acesso ao repositÛrio mais efectivo, devem proceder ‡ seguinte organizaÁ„o de directorias:

```
+-- Readme.md: ficheiro contendo: (i) composiÁ„o do grupo (n˙mero, nome e login github de cada
|              membro); (ii) aspectos que entenderem relevante salientar (e.g. dar nota de
|              algum gui„o que tenha ficado por realizar ou incompleto; um ou outro gui„o
|              que tenha sido realizado apenas por um dos membros do grupo; etc.)
+-- Guioes
|        |
|        +-- G1
|        |    +-- Readme.md: notas sobre a realizaÁ„o do gui„o 1 (justificaÁ„o das opÁıes
|        |    |              tomadas; instruÁıes de uso; dificuldades encontradas; etc.)
|        |    +-- ...
|        |
|        +-- G2
|        |   ...
...      ...
|
+-- Projs
|       |
|       +-- A88888: projeecto individual do aluno ...
|       ...
|
...
```


---
