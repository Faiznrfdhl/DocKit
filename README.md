# 🚀 DocKit

> **Docker Development Kit**  
> Generate production-ready project boilerplates in seconds. Build your next project before writing your first line of code.

DocKit adalah *project generator* yang dirancang untuk menghilangkan rasa sakit saat setup project dari nol. Cukup pilih framework, database, cache, dan fitur yang kamu butuhkan, DocKit akan menghasilkan struktur folder, konfigurasi Docker, dan boilerplate kode yang rapi, terstandarisasi, dan siap untuk dikembangkan.

*(Catatan: DocKit adalah singkatan dari **Docker Development Kit**, bukan Documentation Kit).*

---

## ✨ Fitur Utama

- ⚡ **Instan**: Hasilkan project lengkap dalam hitungan detik.
- 🐳 **Docker-Ready**: `Dockerfile` dan `docker-compose.yml` yang sudah terkonfigurasi otomatis sesuai pilihan stack.
- 🧩 **Modular**: Tambahkan PostgreSQL, Redis, Celery, JWT, atau GitHub Actions hanya dengan satu klik/centang.
- 🏗️ **Clean Architecture**: Opsi struktur folder yang mengikuti best practice (misal: Hexagonal Architecture untuk FastAPI).
- 🛠️ **Developer Experience (DX)**: Sudah termasuk `.gitignore`, `.env.example`, pre-commit hooks, dan linter (Ruff/Black) yang siap pakai.

---

## 🛠️ Tech Stack

- **Generator Engine**: Python, FastAPI, Jinja2
- **Frontend (Web UI)**: Next.js, Tailwind CSS, shadcn/ui *(Coming Soon)*
- **CLI**: Python `click` / `typer` *(Coming Soon)*
- **Target Output**: Docker, Docker Compose, Git, CI/CD

---

## 🚀 Quick Start (Generator API)

Untuk menjalankan engine generator secara lokal:

1. Clone repository ini:
   ```bash
   git clone https://github.com/Faiznrfdhl/dockit.git
   cd dockit