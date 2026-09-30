import httpx

BASE = "http://127.0.0.1:8000"

variants = {
    "demo-full": {
        "framework": "fastapi",
        "project_name": "demo_full",
        "db_enabled": True,
        "redis_enabled": True,
    },
    "demo-min": {
        "framework": "fastapi",
        "project_name": "demo_min",
        "db_enabled": False,
        "redis_enabled": False,
    },
}

for name, payload in variants.items():
    r = httpx.post(f"{BASE}/generate", json=payload)
    if r.status_code != 200:
        print(f"{name} GAGAL:", r.status_code, r.text)
        continue
    with open(f"{name}.zip", "wb") as f:
        f.write(r.content)
    print(f"{name} OK, {len(r.content)} bytes")