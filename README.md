# 🛡️ Guardiao EPI

<div align="center">

![Guardiao EPI](https://img.shields.io/badge/Guardiao-EPI-003050?style=for-the-badge&logo=shield&logoColor=white)

**Sistema inteligente de monitoramento de EPIs com Visao Computacional em tempo real**

[![MIT License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0.3-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-mAP50%3A83.8%25-FF6B35?style=flat-square)](https://ultralytics.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)

[🌐 Demo ao Vivo](https://guardiao-epi.vercel.app) · [🐛 Reportar Bug](https://github.com/Coutfernandes/guardiao-epi/issues) · [💡 Solicitar Feature](https://github.com/Coutfernandes/guardiao-epi/issues)

</div>

---

## 📋 Sobre o Projeto

O **Guardiao EPI** e um sistema distribuido de monitoramento de seguranca do trabalho que utiliza **Inteligencia Artificial** para detectar automaticamente se trabalhadores estao usando os Equipamentos de Protecao Individual (EPIs) obrigatorios em ambientes industriais.

O sistema captura video em tempo real via cameras IP, processa os frames localmente com o modelo **YOLOv8** treinado para detectar 10 classes de EPIs, e envia os resultados para um servidor na nuvem que gera alertas automaticos e relatorios gerenciais.

> 💡 Projeto desenvolvido como **Trabalho de Conclusao de Curso (TCC) — 2026**

---

## ✨ Principais Funcionalidades

- 🎯 **Deteccao em Tempo Real** — YOLOv8 detecta pessoas e EPIs com mAP50 de 83.8%
- 📷 **Stream ao Vivo** — visualize o video com bounding boxes diretamente no dashboard
- 🚨 **Alertas Automaticos** — notificacoes instantaneas quando EPIs estao ausentes
- 📊 **Dashboard Interativo** — indicadores de conformidade e status das cameras em tempo real
- 📄 **Relatorios em PDF** — exportacao de dados de ocorrencias com um clique
- ⚙️ **Configuracao por Camera** — defina quais EPIs sao obrigatorios por setor
- 🔒 **RBAC** — controle de acesso com perfis Administrador e Supervisor
- 📝 **Log de Auditoria** — rastreamento completo de acoes dos usuarios
- 🌐 **Edge Computing** — processamento de IA local, dados na nuvem
- 🐳 **Deploy com Docker** — containerizado com PostgreSQL e Nginx

---

## 🌐 URLs do Sistema

| Servico | URL |
|---------|-----|
| 🖥️ Frontend (Dashboard) | https://guardiao-epi.vercel.app |
| 🔌 Backend (API REST) | https://guardiao-epi.duckdns.org/api |
| ⚙️ Admin Django |  |

---

## 🛠️ Tecnologias Utilizadas

### Backend
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.3-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-3.17-FF1709?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=flat-square&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat-square&logo=jsonwebtokens)

### Frontend
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8.0-646CFF?style=flat-square&logo=vite&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-Latest-5A29E4?style=flat-square)
![Lucide](https://img.shields.io/badge/Lucide_React-0.383-F56565?style=flat-square)

### Inteligencia Artificial
![YOLOv8](https://img.shields.io/badge/YOLOv8n-Ultralytics-FF6B35?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)

### Infraestrutura
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-1.18-009639?style=flat-square&logo=nginx&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Hobby-000000?style=flat-square&logo=vercel&logoColor=white)
![Let's Encrypt](https://img.shields.io/badge/SSL-Let's_Encrypt-003A70?style=flat-square)

---

## 🏗️ Arquitetura do Sistema

```
Camera Intelbras (RTSP local)
        ↓
agente_guardiao.py (notebook local)
  ├── Thread 1: Captura RTSP
  ├── Thread 2: YOLOv8 (deteccao de pessoas e EPIs)
  ├── Thread 3: Envio HTTPS POST para Django
  └── Thread 4: Stream MJPEG porta 8080
        ↓ HTTPS POST (JSON + Base64)        ↓ Ngrok (stream)
VPS Hostinger (Docker)                  Dashboard (Vercel)
  ├── Django REST Framework    ←——————  React 18 + Vite
  ├── PostgreSQL 15
  ├── Nginx + SSL (Let's Encrypt)
  └── DuckDNS (guardiao-epi.duckdns.org)
```

---

## 🤖 Modelo de IA

| Atributo | Valor |
|----------|-------|
| Modelo base | YOLOv8n (nano) |
| Dataset | PPEKit — [Roboflow](https://universe.roboflow.com/tprashant1729/ppekit) |
| Total de imagens | 1079 |
| Epocas de treinamento | 30 |
| **mAP50** | **83.8%** |
| Precisao (Box P) | 89.0% |
| Recall (R) | 76.7% |

### Classes Detectadas

| ID | Classe | Traducao |
|----|--------|----------|
| 0 | gloves | Luvas presentes ✅ |
| 1 | goggles | Oculos presentes ✅ |
| 2 | helmet | Capacete presente ✅ |
| 3 | no gloves | Sem luvas ❌ |
| 4 | no goggles | Sem oculos ❌ |
| 5 | no helmet | Sem capacete ❌ |
| 6 | no shoes | Sem botina ❌ |
| 7 | no vest | Sem colete ❌ |
| 8 | shoes | Botina presente ✅ |
| 9 | vest | Colete presente ✅ |

---

## 🚀 Comecando

### 📦 Pre-requisitos

- [Python 3.12+](https://python.org/downloads/)
- [Node.js 22+](https://nodejs.org/)
- [Docker Desktop](https://docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

### 💻 Instalacao

**1. Clone o repositorio**

```bash
git clone https://github.com/Coutfernandes/guardiao-epi.git
cd guardiao-epi
```

**2. Configure o ambiente virtual**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

**3. Instale as dependencias do backend**

```bash
pip install -r requirements.txt
```

**4. Configure as variaveis de ambiente**

```bash
cp .env.example .env
```

Edite o `.env`:

```env
DEBUG=True
SECRET_KEY=sua-secret-key-aqui
DATABASE_URL=sqlite:///db.sqlite3
```

**5. Execute as migracoes e inicie o servidor**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**6. Instale e inicie o frontend**

```bash
cd frontend
npm install
npm run dev
```

**7. Acesse no navegador**

```
http://localhost:5173
```

### 🐳 Deploy com Docker

```bash
# Suba os containers
docker compose up --build -d

# Aplique as migracoes
docker compose exec web python manage.py migrate

# Crie o superusuario
docker compose exec web python manage.py createsuperuser
```

---

## 🤖 Agente Local

O agente e um script independente que roda no notebook com acesso a camera:

### Instalacao do Agente

```bash
# Instale as dependencias
pip install ultralytics opencv-python requests

# Baixe o script
curl -o agente_guardiao.py https://raw.githubusercontent.com/Coutfernandes/guardiao-epi/main/agente_guardiao.py

# Crie a pasta de modelos e copie o epi_detector.pt
mkdir models
# Copie o epi_detector.pt para a pasta models/
```

### Execucao do Agente

```bash
python agente_guardiao.py \
  --rtsp "rtsp://admin:senha@192.168.0.14:554/cam/realmonitor?channel=1&subtype=1" \
  --django "https://guardiao-epi.duckdns.org/api/deteccao/receber/" \
  --camera-id 1
```

### Stream ao Vivo (Ngrok)

```bash
# Configure o token do Ngrok
ngrok config add-authtoken SEU_TOKEN

# Exponha o stream
ngrok http 8080
```

---

## 🗂️ Estrutura de Pastas

```
📦 guardiao-epi
├── 📁 apps/
│   ├── 📁 authentication/    # JWT, Usuarios, Log de Auditoria
│   ├── 📁 cameras/           # Cameras, Stream MJPEG, Config EPI
│   └── 📁 deteccao/          # Ocorrencias, Alertas, Pipeline YOLOv8
├── 📁 config/                # settings.py, urls.py
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 components/    # Layout, Sidebar
│   │   ├── 📁 context/       # AuthContext (JWT)
│   │   ├── 📁 pages/         # Dashboard, Cameras, Alertas, Relatorios
│   │   └── 📁 services/      # api.js (Axios)
│   └── 📄 vercel.json        # Rewrites React Router
├── 📄 agente_guardiao.py     # Agente de borda local (4 threads)
├── 📄 Dockerfile
├── 📄 docker-compose.yml
├── 📄 requirements.txt       # Completo (com YOLOv8)
└── 📄 requirements-server.txt # Sem YOLOv8 (deploy VPS)
```

---

## 🔌 API REST

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| POST | `/api/auth/login/` | Login — retorna tokens JWT |
| POST | `/api/auth/logout/` | Logout — invalida refresh token |
| GET | `/api/cameras/` | Listar cameras |
| POST | `/api/cameras/{id}/verificar/` | Verificar status RTSP |
| GET | `/api/cameras/{id}/stream/` | Stream MJPEG ao vivo |
| GET | `/api/deteccao/ocorrencias/` | Listar ocorrencias |
| GET | `/api/deteccao/alertas/` | Listar alertas |
| PATCH | `/api/deteccao/alertas/{id}/reconhecer/` | Reconhecer alerta |
| POST | `/api/deteccao/receber/` | Receber dados do agente (publico) |
| GET | `/api/deteccao/relatorio/pdf/` | Gerar relatorio PDF |

---

## 👥 Equipe

| Nome | Matricula | Funcao |
|------|-----------|--------|
| Matheus Fernandes Coutinho | 2408725 | Desenvolvedor Fullstack |
| Daniel Barbosa Figueiredo | 2422527 | Redes e Camera IP |
| Adailton Gustavo Paixao dos Santos | 2403879 | Documentacao |
| Levi Gustavo Coelho Maciel | 2408845 | Documentacao |
| Alex Gonhi Ribeiro Junior | 2394569 | Documentacao |

---

## 📄 Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Matheus Fernandes Coutinho**

- GitHub: [@Coutfernandes](https://github.com/Coutfernandes)

---

##  Agradecimentos

- Dataset [PPEKit](https://universe.roboflow.com/tprashant1729/ppekit) disponibilizado no Roboflow Universe
- [Ultralytics YOLOv8](https://ultralytics.com) pelo framework de deteccao de objetos
- [DuckDNS](https://www.duckdns.org) pelo dominio gratuito
- [Let's Encrypt](https://letsencrypt.org) pelo certificado SSL gratuito
- Icones por [Lucide Icons](https://lucide.dev)

---

<div align="center">

⭐ Se este projeto foi util, considere dar uma estrela!


</div>
