"""
courses_data.py - Centralized course data and contact information.
Easy to modify, extend, or replace with a database in the future.
"""

CONTACT_INFO = {
    "organization": "CodeCraft Academy",
    "email": "support@codecraftacademy.com",
    "phone": "+1 (800) 555-0199",
    "telegram_support": "@CodeCraftSupportBot",
    "website": "https://codecraftacademy.example.com",
    "hours": "Monday - Friday: 9:00 AM - 6:00 PM (EST)",
    "address": "100 Tech Innovation Way, Suite 400, San Francisco, CA"
}

COURSES = {
    "python_fullstack": {
        "id": "python_fullstack",
        "title": "Python & Django Full-Stack Bootcamp",
        "badge": "🔥 Most Popular",
        "level": "Beginner to Advanced",
        "duration": "12 Weeks (approx. 72 live class hours)",
        "schedule": "Mon, Wed, Fri • 7:00 PM – 9:00 PM (EST)",
        "pricing": {
            "regular": "$350",
            "discounted": "$295",
            "installments": "2 monthly payments of $155",
            "offer": "Early Bird: 15% OFF for next batch!"
        },
        "overview": (
            "Master Python programming from the ground up to full-stack web applications. "
            "You will build real-world SaaS projects, REST APIs, and deploy production-ready code."
        ),
        "modules": [
            "Module 1: Python Core, Data Structures & Object-Oriented Programming (OOP)",
            "Module 2: Relational Databases, SQL & PostgreSQL Mastery",
            "Module 3: Django Web Framework & MVC Architecture",
            "Module 4: Building REST APIs with Django REST Framework (DRF)",
            "Module 5: Frontend Integration (HTML5, Tailwind CSS, Alpine.js / React basics)",
            "Module 6: Authentication, Security, Testing & Celery Background Tasks",
            "Module 7: Docker, CI/CD & Cloud Deployment (AWS / DigitalOcean)",
            "Module 8: Final Capstone Project & Portfolio / Resume Review"
        ],
        "prerequisites": "No prior coding experience required. Just basic computer literacy.",
        "certification": "Verified Certificate of Completion upon Capstone defense."
    },
    "data_science_ai": {
        "id": "data_science_ai",
        "title": "Data Science & Applied Machine Learning",
        "badge": "⭐ High Demand",
        "level": "Intermediate",
        "duration": "14 Weeks (approx. 84 live class hours)",
        "schedule": "Tue, Thu, Sat • 6:30 PM – 8:30 PM (EST)",
        "pricing": {
            "regular": "$420",
            "discounted": "$360",
            "installments": "3 monthly payments of $130",
            "offer": "Bundle Discount: Save $80 when registering this week!"
        },
        "overview": (
            "Transform raw data into actionable insights and build predictive AI models. "
            "Includes hands-on exposure to Pandas, Scikit-Learn, PyTorch, and generative AI basics."
        ),
        "modules": [
            "Module 1: Python for Data Science (NumPy, Pandas, Vectorized Ops)",
            "Module 2: Exploratory Data Analysis (EDA) & Data Visualization (Matplotlib, Seaborn)",
            "Module 3: Statistics, Probability & Hypothesis Testing for Analysts",
            "Module 4: Supervised Learning (Regression, Classification, Ensembles)",
            "Module 5: Unsupervised Learning (Clustering, PCA, Anomaly Detection)",
            "Module 6: Neural Networks & Deep Learning with PyTorch",
            "Module 7: Introduction to NLP & LLM Fine-Tuning basics",
            "Module 8: MLOps: Model Deployment via FastAPI & Docker"
        ],
        "prerequisites": "Basic understanding of Python and high school mathematics.",
        "certification": "Verified Certificate of Completion + GitHub Project Showcase."
    },
    "frontend_react": {
        "id": "frontend_react",
        "title": "Modern Frontend Development with React & Next.js",
        "badge": "🚀 Fast-Track",
        "level": "Beginner to Intermediate",
        "duration": "10 Weeks (approx. 60 live class hours)",
        "schedule": "Tue, Thu • 7:00 PM – 9:30 PM (EST)",
        "pricing": {
            "regular": "$280",
            "discounted": "$235",
            "installments": "2 monthly payments of $125",
            "offer": "Student Discount: 10% extra off with valid student ID."
        },
        "overview": (
            "Build lightning-fast, reactive web user interfaces. Learn modern JavaScript (ES6+), "
            "TypeScript, React hooks, state management, and server-side rendering with Next.js 14."
        ),
        "modules": [
            "Module 1: Advanced HTML5, Semantic Web & Responsive Design",
            "Module 2: Modern CSS, Flexbox/Grid, and Tailwind CSS",
            "Module 3: JavaScript ES6+, Asynchronous JS & Fetch API",
            "Module 4: TypeScript Fundamentals for Frontend Devs",
            "Module 5: React Core: Components, Props, State & Custom Hooks",
            "Module 6: Global State Management (Zustand / Redux Toolkit)",
            "Module 7: Next.js App Router, SSR, SSG & Server Actions",
            "Module 8: Capstone: Production SaaS Dashboard with Authentication"
        ],
        "prerequisites": "Basic knowledge of how the web works. No previous framework experience needed.",
        "certification": "Verified Certificate of Completion."
    },
    "devops_cloud": {
        "id": "devops_cloud",
        "title": "DevOps & Cloud Engineering Bootcamp",
        "badge": "🛠️ Career Accelerator",
        "level": "Intermediate to Advanced",
        "duration": "8 Weeks (approx. 48 live class hours)",
        "schedule": "Saturdays & Sundays • 10:00 AM – 1:00 PM (EST)",
        "pricing": {
            "regular": "$380",
            "discounted": "$320",
            "installments": "2 monthly payments of $170",
            "offer": "Corporate sponsorship available."
        },
        "overview": (
            "Automate, scale, and manage enterprise infrastructure. Master Linux, Git, Docker, "
            "Kubernetes, GitHub Actions CI/CD, and AWS Cloud architecture."
        ),
        "modules": [
            "Module 1: Linux Administration & Bash Shell Scripting",
            "Module 2: Git Version Control & Collaborative Git Workflows",
            "Module 3: Containerization with Docker & Multi-stage Builds",
            "Module 4: Container Orchestration with Kubernetes (K8s)",
            "Module 5: CI/CD Pipelines with GitHub Actions & Automated Testing",
            "Module 6: Infrastructure as Code (IaC) with Terraform",
            "Module 7: AWS Core Services (EC2, S3, RDS, VPC, IAM)",
            "Module 8: Monitoring & Logging (Prometheus, Grafana & CloudWatch)"
        ],
        "prerequisites": "Familiarity with any programming language and command line basics.",
        "certification": "Verified Certificate of Completion + AWS Certification Prep."
    }
}

