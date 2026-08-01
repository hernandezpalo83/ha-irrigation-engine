"""Release exporter tool for Home Assistant.

Compiles the current registry, generates the Home Assistant package YAML,
and creates a clean zip file in release/ ready for deployment into Home Assistant config.
"""

import os
import shutil
import zipfile
from pathlib import Path

from src.build.generator import PackageGenerator


def export_release() -> Path:
    """Build package and bundle into release zip file.

    Returns:
        Path to generated release zip archive.
    """
    project_root = Path(__file__).resolve().parent.parent.parent
    registry_path = project_root / "registry"
    output_package = project_root / "packages" / "ha_irrigation_engine.yaml"
    release_dir = project_root / "release"
    zip_path = release_dir / "ha_irrigation_engine_release.zip"

    # Step 1: Generate Package YAML
    generator = PackageGenerator(registry_dir=registry_path, output_file=output_package)
    generator.generate()

    # Step 2: Prepare Release Zip
    release_dir.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add generated package
        zip_file.write(output_package, arcname="packages/ha_irrigation_engine.yaml")
        # Add automations
        watchdog_path = project_root / "automations" / "watchdog.yaml"
        if watchdog_path.exists():
            zip_file.write(watchdog_path, arcname="automations/watchdog.yaml")

    return zip_path


def main() -> None:
    """CLI Entrypoint."""
    zip_out = export_release()
    print(f"✅ Release package generated successfully: {zip_out}")


if __name__ == "__main__":
    main()
