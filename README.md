<div align="center">

# ✨ AI Generator 2

**A Next-Generation Social Media Asset Generator powered by Stable Diffusion XL**

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*An intelligent, highly scalable web application designed to instantly generate, edit, and distribute high-quality graphical post assets for hotels, events, and marketing campaigns.*

</div>

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Configuration](#environment-configuration)
  - [Docker Installation (Recommended)](#docker-installation-recommended)
  - [Local Installation](#local-installation)
- [Usage Guide](#-usage-guide)
- [Contributing](#-contributing)

---

## 🚀 Overview
**AI Generator 2** empowers marketing professionals to cut their graphic design turnaround time from hours to seconds. By simply inputting a brand name and a marketing occasion, the application seamlessly interfaces with Hugging Face's serverless endpoints to spin up beautiful, context-aware imagery using `stabilityai/stable-diffusion-xl-base-1.0`.

## ⚡ Key Features
- **Prompt-to-Image Synthesis:** Leverage the Stable Diffusion XL API to generate hyper-realistic, high-fidelity promotional pictures without GPU overhead.
- **Dynamic Image Refinement:** Iteratively edit and refine outputs dynamically by appending natural language adjustments (e.g. *"Make the lighting softer"*).
- **Frictionless Social Sharing:** One-click OAuth integrations to immediately push final image blocks to Twitter, Facebook, LinkedIn, and Instagram.
- **Robust Abstractions:** Fully containerized backend designed explicitly for cloud-native deployment.
- **Security-First Environment:** Built with strict `.env` loading protocols isolating all cryptographic signatures and inference tokens away from the codebase.

## 🛠 Architecture & Tech Stack
| Component | Technology | Description |
|-----------|------------|-------------|
| **Core Framework** | Django | High-level Python web framework enforcing MVC patterns. |
| **Generative SDK** | `huggingface_hub` | Official SDK bridging user inputs to the Nscale generation routers. |
| **Containerization**| Docker | Self-contained local environments using `python:3.11-slim`. |
| **Frontend** | HTML5 / Vanilla CSS | Lightweight, reactive, and responsive raw asset rendering. |

---

## 🚦 Getting Started

### Prerequisites
Before starting, ensure you have the following installed on your machine:
- [Git](https://git-scm.com/)
- [Docker Engine](https://www.docker.com/) (If deploying via containers)
- A **Hugging Face API Token** (Ensure `Make calls to Inference Providers` permission is enabled).

### Environment Configuration
At the root of the project (inside the `ai_post_generator` directory), create a file named exactly `.env`. Populate it strictly without any quotation marks:

```ini
HUGGINGFACE_API_KEY=hf_your_inference_token
SECRET_KEY=your_django_production_secret
```

### Docker Installation (Recommended)
Containerization is heavily recommended as it bypasses local OS dependency constraints.

```bash
# 1. Clone the repository
git clone https://github.com/WAKE-UP-TO-REALITY/marchcohort.git
cd marchcohort/ai_post_generator

# 2. Build the Docker Image
docker build -t ai-generator-2 .

# 3. Spin up the Container
docker run -p 8000:8000 --env-file .env ai-generator-2
```
*Your application is now live at `http://localhost:8000`.*

### Local Installation
For manual development, native Python initialization is required:

```bash
# 1. Initialize a secure virtual environment
python -m venv venv
source venv/bin/activate  # (Use `venv\Scripts\activate` on Windows)

# 2. Install dependencies mapping
pip install -r requirements.txt

# 3. Commit migrations and run the local ASGI/WSGI interface
python manage.py migrate
python manage.py runserver
```

---

## 🎨 Usage Guide
1. **Initialize Request:** Navigate to the web UI and enter the targeted **Hotel Name** (The focal subject) and the **Occasion** (The atmospheric theme).
2. **Generation:** Click **Generate Post**. The backend securely streams your structured request to Hugging Face and saves the resultant SDXL file.
3. **Refinement Pipeline:** If unsatisfied, utilize the *Edit Image* secondary prompt box to refine attributes interactively.
4. **Distribution:** Click any of the platform icons underneath the image to instantly share the asset.

---

<div align="center">
<i>Built with ❤️ by asish111</i>
</div>
