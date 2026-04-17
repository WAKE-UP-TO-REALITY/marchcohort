# AI Generator 2 🤖✨

AI Generator 2 is a modern Django-based web application that leverages the power of Hugging Face's inference API (Stable Diffusion XL) to instantly create high-quality, professional social media posts for hotels and marketing campaigns.

## 🌟 Features
- **Prompt-to-Image AI:** Instantly generate stunning, high-quality promotional posts by simply entering a hotel name and an occasion.
- **Image Editing:** Fine-tune the generated images by specifying additional prompts (e.g., "add balloons", "make it more sunny").
- **1-Click Social Sharing:** Out-of-the-box integration to instantly share generated content to Instagram, Facebook, Twitter, and LinkedIn.
- **Dockerized:** Fully containerized for easy and replicable deployments anywhere.

## 🛠 Tech Stack
- **Backend Framework:** Django (Python)
- **AI Integration:** Hugging Face Hub (Stable Diffusion XL API)
- **Frontend:** HTML5, Vanilla CSS, Vanilla JavaScript
- **Deployment:** Docker

---

## ⚙️ Prerequisites
To run this project, make sure you have the following installed on your machine:
- [Docker & Docker Desktop](https://www.docker.com/products/docker-desktop/) 
- A [Hugging Face](https://huggingface.co/) free account and an **Inference API Token**

## 🔐 Environment Variables (.env)
You will need to create a `.env` file in the `ai_post_generator` root directory with the following variables. Do NOT use quotation marks around the values.

```env
HUGGINGFACE_API_KEY=your_hugging_face_token_here
SECRET_KEY=a_randomly_generated_django_secret_key_here
```

---

## 🐳 Quickstart: Docker (Recommended)

Running the app via Docker is the easiest method and guarantees it works on any operating system without installing Python modules locally.

**1. Clone the repository and navigate into the app folder**
```bash
git clone https://github.com/your-username/marchcohort.git
cd marchcohort/ai_post_generator
```

**2. Build the Docker image**
```bash
docker build -t ai-generator-2 .
```

**3. Run the container**
```bash
docker run -p 8000:8000 --env-file .env ai-generator-2
```
The server will now be running. You can access it in your browser at `http://localhost:8000`.

---

## 💻 Local Setup (Without Docker)

If you prefer to run the project natively using Python on your machine:

**1. Create & activate a Virtual Environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Apply Migrations & Start Server**
```bash
python manage.py migrate
python manage.py runserver
```

---

## 📷 Usage
1. Open the web app interface.
2. Type in a **Hotel Name** (e.g. "Sunset Resort").
3. Type in the **Occasion** (e.g. "Summer Launch Party").
4. Click **Generate** and let the AI do its magic!
5. Easily share your newly minted graphic to your social timelines. 
