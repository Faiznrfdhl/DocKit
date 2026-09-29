import os
import io
import zipfile
from jinja2 import Environment, FileSystemLoader

class DocKitEngine:
    def __init__(self, templates_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            keep_trailing_newline=True,

            trim_blocks=True, 
            lstrip_blocks=True
        )

    def generate(self, framework: str, options: dict) -> io.BytesIO:
        """
        Merender template dan mengembalikan file ZIP di memori.
        options = { "db_enabled": True, "redis_enabled": False, "project_name": "my_app" }
        """
        memory_file = io.BytesIO()
        template_base_dir = os.path.join(framework, "base")
        template_addons_dir = os.path.join(framework, "addons")

        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 1. Render Base Templates (Wajib ada)
            base_path = os.path.join(self.env.loader.searchpath[0], template_base_dir)
            self._render_and_zip(zipf, base_path, template_base_dir, options)

            # 2. Render Addons (PostgreSQL, Redis, dll)
            if options.get("db_enabled"):
                db_path = os.path.join(self.env.loader.searchpath[0], template_addons_dir, "postgres")
                self._render_and_zip(zipf, db_path, "", options)
                
            if options.get("redis_enabled"):
                redis_path = os.path.join(self.env.loader.searchpath[0], template_addons_dir, "redis")
                self._render_and_zip(zipf, redis_path, "", options)

        memory_file.seek(0)
        return memory_file

    def _render_and_zip(self, zipf: zipfile.ZipFile, folder_path: str, zip_prefix: str, context: dict):
        if not os.path.exists(folder_path): return

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.j2'):
                    # Ambil relative path dari folder template
                    rel_path = os.path.relpath(os.path.join(root, file), self.env.loader.searchpath[0])
                    template = self.env.get_template(rel_path)
                    
                    # Render isi file
                    rendered_content = template.render(**context)
                    
                    # Hapus ekstensi .j2 untuk hasil akhir
                    arcname = rel_path.replace('.j2', '')
                    zipf.writestr(arcname, rendered_content)