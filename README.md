# 📸 Casamento Izabella & Anderson

Aplicação web simples para compartilhamento de fotos durante o casamento de **Izabella & Anderson**.

A ideia é permitir que os convidados, pelo celular, acessem a aplicação através de um QR Code, tirem ou selecionem uma foto e enviem para o servidor. As fotos ficam armazenadas no computador que está executando a aplicação.

A aplicação foi pensada para ser simples, leve e funcionar durante o evento sem necessidade de aplicativo mobile, banco externo ou infraestrutura complexa.

---

## 💍 Evento

**Izabella & Anderson**

📅 **3 de outubro de 2026**  
📍 **Belo Horizonte - Minas Gerais - Brasil**

---

# 🏗️ Arquitetura

A aplicação utiliza:

- **Python**
- **Flask**
- **SQLite**
- **HTML + CSS + JavaScript**
- **Pillow**
- **pillow-heif**
- **Cloudflare Quick Tunnel**
- Sistema de arquivos local para armazenamento das fotos

Estrutura simplificada:

```text
celular do convidado
        │
        │ HTTPS
        ▼
Cloudflare Quick Tunnel
        │
        ▼
Flask
        │
        ├── SQLite
        │     └── casamento.db
        │
        └── Fotos
              └── uploads/
```

---

# 📁 Estrutura do projeto

```text
casamento/
│
├── app.py
├── casamento.db
├── cloudflared.exe
├── iniciar_casamento.sh
├── uploads/
│
└── venv/
```

### `app.py`

Arquivo principal da aplicação Flask.

É responsável por:

- receber fotos;
- salvar os dados no SQLite;
- armazenar os arquivos;
- exibir a galeria;
- exibir a galeria especial;
- disponibilizar a área administrativa;
- converter fotos HEIC/HEIF para JPEG.

### `casamento.db`

Banco SQLite contendo os registros das fotos enviadas.

Tabela principal:

```text
fotos
├── id
├── nome
├── local
├── arquivo
└── data_hora
```

### `uploads/`

Diretório onde as fotos enviadas pelos convidados são armazenadas.

### `venv/`

Ambiente virtual Python do projeto.

### `cloudflared.exe`

Executável do Cloudflare Tunnel usado para disponibilizar a aplicação local através de HTTPS.

### `iniciar_casamento.sh`

Script de inicialização automática do projeto.

---

# 🚀 Primeiro uso / preparação

Abra o **Git Bash** e entre na pasta do projeto:

```bash
cd ~/eclipse-workspace/casamento
```

Ative o ambiente virtual:

```bash
source venv/Scripts/activate
```

Instale as dependências:

```bash
pip install flask pillow pillow-heif
```

Depois execute:

```bash
python app.py
```

A aplicação ficará disponível localmente em:

```text
http://localhost:8080
```

---

# ▶️ Inicialização simplificada

Depois que tudo estiver instalado, pode ser utilizado o script:

```bash
./iniciar_casamento.sh
```

O script:

1. entra na pasta do projeto;
2. ativa o ambiente virtual;
3. atualiza o `pip`;
4. verifica/instala Flask;
5. verifica/instala Pillow;
6. verifica/instala pillow-heif;
7. inicia o Flask.

O terminal deve permanecer aberto enquanto o servidor estiver sendo utilizado.

---

# 🌐 Acesso pelo celular

O Flask roda localmente no notebook.

Para que convidados possam acessar a aplicação pela internet, é utilizado o **Cloudflare Quick Tunnel**.

Em uma segunda janela do Git Bash:

```bash
cd ~/eclipse-workspace/casamento
./cloudflared.exe tunnel --url http://localhost:8080
```

O Cloudflare exibirá uma URL parecida com:

```text
https://alguma-coisa.trycloudflare.com
```

Essa é a URL que deve ser utilizada pelos convidados.

## ⚠️ Importante

O endereço do Quick Tunnel é temporário.

Se o `cloudflared` for encerrado e iniciado novamente, uma nova URL poderá ser criada.

Por isso, o QR Code deve ser gerado utilizando a URL do túnel que estiver ativo no momento do evento.

---

# 📱 Fluxo do convidado

O convidado:

1. escaneia o QR Code;
2. abre a aplicação no celular;
3. informa o nome;
4. escolhe onde a foto aconteceu;
5. tira uma foto ou seleciona uma existente;
6. envia a foto;
7. pode consultar a galeria.

O nome é armazenado no `localStorage` do navegador para facilitar os próximos envios pelo mesmo aparelho.

---

# 📍 Locais disponíveis

A aplicação possui opções pré-definidas:

- 💍 Entrada dos noivos
- ⛪ Cerimônia
- ❤️ Dança dos noivos
- 🎸 Show da banda
- 💃 Pista de dança
- 🥂 Brinde
- 🍰 Bolo
- 😂 Momentos diversos

Também existe a possibilidade de informar um local personalizado.

---

# 🖼️ Galeria

A rota:

```text
/galeria
```

exibe as fotos enviadas pelos convidados.

É possível filtrar as fotos pelo local onde foram tiradas.

A galeria busca os locais diretamente no banco de dados, portanto novos locais cadastrados também aparecem no filtro.

---

# ✨ Galeria especial

A rota:

```text
/galeriaEspecial
```

apresenta as fotos em composições especiais.

Existem cinco formatos:

1. **Mosaico**
2. **Coração**
3. **Polaroids**
4. **Destaques**
5. **Artística**

O botão:

```text
🔄 Ver outra composição
```

alterna entre os cinco formatos.

A sequência é:

```text
Mosaico
   ↓
Coração
   ↓
Polaroids
   ↓
Destaques
   ↓
Artística
   ↓
Mosaico
```

A composição é controlada pelo parâmetro:

```text
?formato=0
?formato=1
?formato=2
?formato=3
?formato=4
```

---

# 📸 Fotos HEIC / HEIF

Celulares, principalmente iPhones, podem enviar imagens no formato:

```text
HEIC
HEIF
```

A aplicação possui suporte para esses formatos através de:

- Pillow
- pillow-heif

Quando uma foto HEIC/HEIF é recebida:

1. o arquivo é aberto;
2. a orientação EXIF é corrigida;
3. a imagem é convertida para RGB;
4. é salva como JPEG;
5. somente o JPEG é mantido no diretório de uploads.

Isso evita problemas de visualização no navegador.

---

# 💾 Banco de dados

O banco utilizado é SQLite.

Não existe necessidade de instalar servidor PostgreSQL, MySQL ou Oracle.

O arquivo:

```text
casamento.db
```

contém os registros das fotos.

As imagens propriamente ditas ficam no diretório:

```text
uploads/
```

Portanto:

```text
casamento.db
```

e

```text
uploads/
```

são as duas partes importantes para preservar os dados do evento.

---

# 💽 Backup

Durante o evento, recomenda-se realizar backup periódico de:

```text
casamento.db
```

e

```text
uploads/
```

Após o evento, copiar toda a pasta do projeto é uma forma simples de preservar a aplicação e os registros.

Se as fotos forem direcionadas para um HD/SSD externo, basta configurar o caminho do diretório de uploads no `app.py`.

Exemplo:

```python
UPLOAD_FOLDER = r"E:\CASAMENTO\fotos"
```

Nesse cenário:

- banco continua no notebook;
- fotos ficam no HD/SSD externo.

---

# 🔐 Área administrativa

A aplicação possui uma área administrativa:

```text
/admin
```

Existe também:

```text
/admin/logout
```

As credenciais atualmente configuradas no projeto são:

```text
Usuário: anderson
Senha: 123
```

> ⚠️ Antes de colocar a aplicação em uso público permanente, recomenda-se trocar essas credenciais e retirar as credenciais diretamente do código. Para o uso controlado durante o evento, elas foram mantidas de forma simples.

---

# 🛑 Como desligar

Para parar o Flask:

```text
CTRL + C
```

Para parar o Cloudflare Tunnel:

```text
CTRL + C
```

Fechar o Git Bash **não apaga**:

- banco de dados;
- fotos;
- código;
- ambiente virtual.

---

# 🔄 Como iniciar novamente

Depois de fechar tudo, abrir o Git Bash.

### Terminal 1

```bash
cd ~/eclipse-workspace/casamento
./iniciar_casamento.sh
```

Aguardar o Flask iniciar.

### Terminal 2

Abrir outro Git Bash:

```bash
cd ~/eclipse-workspace/casamento
./cloudflared.exe tunnel --url http://localhost:8080
```

Copiar a URL:

```text
https://xxxxx.trycloudflare.com
```

Essa será a URL pública do evento.

---

# 🧪 Teste antes do casamento

Antes do evento, recomenda-se testar:

### 1. Servidor

Abrir:

```text
http://localhost:8080
```

### 2. Cloudflare

Iniciar:

```bash
./cloudflared.exe tunnel --url http://localhost:8080
```

### 3. Android

Abrir a URL `https://...trycloudflare.com`.

### 4. iPhone

Abrir a mesma URL pelo Safari.

### 5. Upload

Testar:

- foto comum;
- foto tirada diretamente pelo celular;
- foto existente na galeria;
- foto HEIC de iPhone.

### 6. Galeria

Verificar:

```text
/galeria
```

### 7. Galeria especial

Verificar:

```text
/galeriaEspecial
```

e navegar pelos cinco formatos.

---

# 📡 Internet

A aplicação foi projetada para utilizar o notebook como servidor durante o evento.

A conexão utilizada pode ser:

- internet residencial durante testes;
- 5G durante o evento;
- outra conexão com acesso à internet.

O Cloudflare Tunnel cria a conexão HTTPS entre a internet e o Flask local.

O celular do convidado não precisa estar na mesma rede Wi-Fi do notebook.

---

# ⚠️ Pontos importantes para o dia do casamento

## Não fechar o Flask

A janela onde o comando abaixo estiver executando precisa permanecer aberta:

```bash
./iniciar_casamento.sh
```

## Não fechar o Cloudflare

A segunda janela também precisa permanecer aberta:

```bash
./cloudflared.exe tunnel --url http://localhost:8080
```

## Não deixar o notebook dormir

Desabilitar temporariamente:

- suspensão automática;
- hibernação;
- desligamento automático da tela, se necessário.

O notebook precisa permanecer ligado durante o evento.

## Energia

Manter o notebook conectado à energia durante todo o evento.

---

# 🧰 Comandos rápidos

### Entrar no projeto

```bash
cd ~/eclipse-workspace/casamento
```

### Ativar ambiente virtual

```bash
source venv/Scripts/activate
```

### Iniciar Flask

```bash
python app.py
```

### Iniciar pelo script

```bash
./iniciar_casamento.sh
```

### Iniciar Cloudflare

```bash
./cloudflared.exe tunnel --url http://localhost:8080
```

### Parar qualquer processo

```text
CTRL + C
```

---

# 🧠 Resumo operacional

No dia:

```text
1. Ligar notebook
       ↓
2. Abrir Git Bash
       ↓
3. ./iniciar_casamento.sh
       ↓
4. Abrir segundo Git Bash
       ↓
5. ./cloudflared.exe tunnel --url http://localhost:8080
       ↓
6. Copiar URL HTTPS
       ↓
7. Gerar/usar QR Code com essa URL
       ↓
8. Colocar QR Codes no casamento
       ↓
9. Convidados enviam fotos
       ↓
10. Galeria recebe tudo
       ↓
11. Curtir o caos fotográfico 🍾📸
```

---

# 🏁 Estado final do projeto

O projeto foi concebido para ser uma solução simples e temporária para o casamento, evitando:

- desenvolvimento de aplicativo Android/iOS;
- publicação em lojas;
- servidor dedicado;
- banco de dados externo;
- hospedagem permanente;
- domínio próprio;
- infraestrutura complexa.

A aplicação roda localmente no notebook e utiliza o Cloudflare Quick Tunnel apenas para fornecer acesso HTTPS aos celulares durante o evento.

**Izabella & Anderson · 03/10/2026 · Belo Horizonte/MG 🇧🇷**

📸 Que venham as fotos.
