# ♻️ smartUpCycle

**Empowering individuals to upcycle creatively, reduce their carbon footprints, and build a sustainability-first community.**



---

## 🌱 Overview

smartUpCycle is a full-stack web platform that:
- Suggests upcycling ideas from common waste items
- Analyzes your personal carbon footprint
- Lets users post and showcase their DIY upcycled creations
- Encourages sustainable behavior through community and gamification

---

## 🚀 Live Features

### 🛠 DIY Suggestion Engine
- Accepts description of a waste item
- Suggests creative upcycling ideas using predefined logic
- Displays images and step-by-step guidance

### 🌍 Carbon Footprint Analyzer
- Calculates your estimated CO₂ emissions based on:
  - Monthly electricity usage
  - Weekly non-vegetarian meals
  - Weekly car travel
- Offers actionable eco-alternatives and impact metrics (e.g., trees needed to offset emissions)

### 🛒 Marketplace (EcoBazar)
- Users can post DIY projects
- Upload images, descriptions, and showcase their creativity
- Visual community feed (Facebook-style UI)

### 👥 Dashboard
- Navigate across all modules (Login, DIY, Carbon, Marketplace)
- Simple and clean UX with green/white theme

---

## 💡 Technologies Used

### 🔧 Backend
- Flask (Python)
- REST APIs for DIY, carbon, auth, and marketplace modules
- SQLAlchemy for MySQL-based user authentication
- Custom logic for eco suggestions and emission calculations

### 🧠 AI / ML (optional / removed)
- Original design used OpenAI GPT-3.5 for DIY suggestions
- Replaced with switch-case logic for cost-efficiency and demo stability

### 🌐 Frontend
- HTML, Tailwind CSS, JavaScript
- Responsive, modern UI
- Video backgrounds, drag-and-drop file uploads, dynamic suggestion boxes

### 🧰 Dev & Deployment
- Git + GitHub
- `.gitignore` to avoid tracking sensitive files
- Media stored in `static/media/`
- XAMPP (MySQL) for local database setup

---