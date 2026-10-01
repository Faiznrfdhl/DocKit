import io
import os
import zipfile

from jinja2 import Environment, FileSystemLoader


class DocKitEngine:
    """Core engine DocKit: render template Jinja2 -> ZIP in memory."""

    # Mapping: nama folder addon -> flag di request
    ADDON_FLAGS = {
        "postgres": "db_enabled",
        "redis": "redis_enabled",
    }

    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            keep_trailing_newline=True,
            trim_blocks=True,    # buang newline setelah block tag Jinja
            lstrip_blocks=True,  # buang indentasi sebelum block tag
        )

    # ---------- Utility ----------
    def list_frameworks(self) -> list[str]:
        """Scan folder templates/ buat daftar framework yang tersedia."""
        if not os.path.exists(self.templates_dir):
            return []
        return sorted(
            name
            for name in os.listdir(self.templates_dir)
            if os.path.isdir(os.path.join(self.templates_dir, name, "base"))  # <- TAMBAHIN "base"
            and not name.startswith(("_", "."))
        )

    def framework_exists(self, framework: str) -> bool:
        return framework in self.list_frameworks()

    # ---------- Core ----------
    def generate(self, framework: str, options: dict) -> io.BytesIO:
        if not self.framework_exists(framework):
            raise ValueError(f"Framework '{framework}' belum tersedia di DocKit.")

        memory_file = io.BytesIO()

        with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            # 1) Base templates (wajib ada)
            base_dir = os.path.join(self.templates_dir, framework, "base")
            self._render_folder(zipf, base_dir, options)

            # 2) Addons (opsional, sesuai checklist user)
            addons_dir = os.path.join(self.templates_dir, framework, "addons")
            for addon, flag in self.ADDON_FLAGS.items():
                if options.get(flag):
                    self._render_folder(zipf, os.path.join(addons_dir, addon), options)

        memory_file.seek(0)
        return memory_file

    def _render_folder(self, zipf: zipfile.ZipFile, folder_path: str, context: dict):
        """Render semua file .j2 di satu folder (rekursif) masuk ke ZIP."""
        if not os.path.exists(folder_path):
            return

        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.endswith(".j2"):
                    continue

                full_path = os.path.join(root, file)

                # Path buat Jinja (relatif terhadap templates/, pakai slash)
                template_path = os.path.relpath(full_path, self.templates_dir).replace("\\", "/")
                # Path di DALAM zip (relatif terhadap folder base/addon itu sendiri)
                arcname = os.path.relpath(full_path, folder_path).replace(".j2", "").replace("\\", "/")

                template = self.env.get_template(template_path)
                zipf.writestr(arcname, template.render(**context))