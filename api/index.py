import os
import sys

# Pastiin package `generator` di root repo bisa di-import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.main import app  # noqa: E402  <- ini ASGI app yang diserve Vercel