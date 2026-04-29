# Luxe Hairs - Premium Hair E-Commerce Platform

Luxe Hairs is a sophisticated, high-end e-commerce platform built with **Django** and **Tailwind CSS**. It is designed to provide a seamless and luxurious shopping experience for premium hair products, featuring personalized user profiling and a tiered loyalty system.

---

## ✨ Key Features

- **🛍️ Dynamic Product Catalog:** Supports categorized products with subtitles, rich descriptions, and high-quality image/video previews.
- **🛒 Complete Shopping Workflow:** Integrated cart system, secure checkout, and real-time order status tracking.
- **🏆 Tiered Loyalty Program:** Automated user membership tiers (Member, Elite, Gold) based on engagement and points.
- **🎭 Personalized Aesthetic Profiles:** Captures user-specific traits like face shape and lustre bias to drive tailored product recommendations.
- **🎨 Premium UI/UX:** A modern, responsive interface built with Tailwind CSS, emphasizing luxury and brand excellence.
- **🛠️ Robust Admin Panel:** Specialized views for managing products, categories, and tracking customer orders.

---

## 🚀 Tech Stack

- **Backend:** Django 5.x (Python)
- **Frontend:** Tailwind CSS, HTML5, JavaScript
- **Database:** SQLite (Development)
- **Environment Management:** `django-environ` for secure configuration.
- **Build Tools:** Node.js/NPM for Tailwind CSS compilation.

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js & NPM (for Tailwind)

### 2. Installation
Clone the repository and set up the virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and configure the following:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Running the Project
Compile Tailwind CSS:
```bash
npm install
npm run dev
```
Start the Django server:
```bash
python manage.py runserver
```

---

## 📂 Project Structure

- `luxehairs/`: Core project configuration.
- `shop/`: Main application containing models, views, and business logic.
- `templates/`: Global and app-specific HTML templates.
- `static/`: CSS, JS, and image assets.
- `media/`: User-uploaded content (product images/videos).

---

## 📜 License
This project is proprietary. All rights reserved.
