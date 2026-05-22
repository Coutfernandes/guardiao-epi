# 🛡️ Guardiao EPI

Sistema inteligente de monitoramento de Equipamentos de Proteção Individual (EPIs) utilizando Visão Computacional com YOLOv8.

> Trabalho de Conclusão de Curso (TCC) — 2026

---

## 🌐 URLs do Sistema

| Serviço | URL |
|---------|-----|
| Frontend | https://guardiao-epi.vercel.app |
| Backend API | 
| Admin Django | 

---

## 📋 Sobre o Projeto

O Guardiao EPI monitora em tempo real o uso correto de EPIs por trabalhadores em ambientes industriais. Através de câmeras IP, o sistema detecta automaticamente se os equipamentos obrigatórios estão sendo utilizados e gera alertas quando não conformidades são identificadas.

---

## 🏗️ Arquitetura

```
Camera Intelbras (RTSP local)
        ↓
Agente Local (Notebook)
  - OpenCV captura frames
  - YOLOv8n detecta pessoas
  - epi_detector.pt detecta EPIs
  - Serve stream MJPEG na porta 8080
  - Envia alertas via HTTPS
        ↓
VPS Hostinger (Docker)
  - Django REST Framework
  - PostgreSQL
  - Nginx + SSL (Let's Encrypt)
        ↓
Vercel (Frontend React)
  - Dashboard em tempo real
  - Gestão de alertas
  - Relatórios em PDF
```

---

## 🛠️ Stack Tecnológica

### Backend
- Python 3.12
- Django 6.0.3
- Django REST Framework
- PostgreSQL 15
- Docker + Docker Compose
- Nginx + Certbot (SSL)
- APScheduler

### Frontend
- React 18
- Vite
- Axios
- React Router DOM
- Lucide React

### Inteligência Artificial
- YOLOv8n (detecção de pessoas)
- Modelo customizado epi_detector.pt (mAP50: 83.8%)
- OpenCV
- PyTorch

### Infraestrutura
- VPS Hostinger (4GB RAM, Ubuntu 22.04)
- Vercel (Frontend)
- DuckDNS (domínio gratuito)
- Ngrok (tunelamento do stream)

---

## 🚀 Como Executar Localmente

### Requisitos
- Python 3.12+
- Node.js 22+
- Docker Desktop

### Backend

```bash
# Clonar repositório
git clone https://github.com/Coutfernandes/guardiao-epi.git
cd guardiao-epi

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Agente Local

```bash
# Instalar dependências
pip install ultralytics opencv-python requests

# Executar
python agente_guardiao.py --rtsp "rtsp://usuario:senha@IP_CAMERA:554/..." --django "http://localhost:8000/api/deteccao/receber/" --camera-id 1
```

---

## 🐳 Deploy com Docker

```bash
# Configurar variáveis de ambiente
cp .env.example .env

# Subir containers
docker compose up --build -d

# Aplicar migrações
docker compose exec web python manage.py migrate

# Criar superusuário
docker compose exec web python manage.py createsuperuser
```

---

## 📦 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DEBUG=False
SECRET_KEY=sua-secret-key-aqui
DATABASE_URL=postgresql://usuario:senha@localhost:5432/guardiao_epi
```

---

## 🤖 Modelo de IA

| Atributo | Valor |
|----------|-------|
| Dataset | PPEKit (Roboflow) |
| Imagens | 1079 |
| Épocas | 30 |
| mAP50 | 83.8% |
| Classes | 10 |

### Classes detectadas
- `helmet` / `no helmet` — Capacete
- `gloves` / `no gloves` — Luvas
- `goggles` / `no goggles` — Óculos
- `vest` / `no vest` — Colete
- `shoes` / `no shoes` — Botina

---

## 📊 Funcionalidades

- ✅ Monitoramento em tempo real via câmera IP
- ✅ Detecção de pessoas com YOLOv8n
- ✅ Detecção de EPIs com modelo customizado
- ✅ Stream ao vivo com bounding boxes
- ✅ Sistema de alertas com cooldown de 2 minutos
- ✅ Dashboard com indicadores de conformidade
- ✅ Relatórios em PDF para download
- ✅ Configuração de EPIs por câmera
- ✅ RBAC com perfis Administrador e Supervisor
- ✅ Log de auditoria de ações
- ✅ Arquitetura distribuída (Edge Computing)

---

## 📁 Estrutura do Projeto

```
guardiao-epi/
├── apps/
│   ├── authentication/   # JWT, Usuários, Auditoria
│   ├── cameras/          # Câmeras, Stream MJPEG
│   └── deteccao/         # Ocorrências, Alertas, YOLOv8
├── config/               # Settings, URLs
├── frontend/             # React + Vite
├── agente_guardiao.py    # Agente de borda local
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 👥 Autor

Matheus Coutinho — [@Coutfernandes](https://github.com/Coutfernandes)

---

## 📄 Licença

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC).
