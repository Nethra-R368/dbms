import os
import zipfile
import shutil
from pathlib import Path

def create_submission_zip():
    base_dir = Path(__file__).resolve().parent
    zip_name = "B12_TEAM12_SMARTHOSTEL.zip"
    zip_path = base_dir / zip_name
    downloads_zip_path = Path(r"C:\Users\Nethra R\Downloads") / zip_name

    # Exclusions
    exclude_dirs = {
        '.git', 'venv', 'node_modules', '__pycache__', '.pytest_cache', 
        'db_data', '.vscode', 'dist', '.github'
    }
    exclude_files = {
        '.env', 'cloudflared.exe', 'ngrok.exe'
    }
    exclude_extensions = {
        '.pyc', '.pyo'
    }

    print(f"Packaging submission ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]

            for file in files:
                if file in exclude_files:
                    continue
                if file.startswith('~$'):
                    continue
                if file.endswith('.zip'):
                    continue
                if any(file.endswith(ext) for ext in exclude_extensions):
                    continue

                full_path = Path(root) / file
                rel_path = full_path.relative_to(base_dir)
                
                # We place contents under a top-level root folder matching the name convention: B12_TEAM12_SMARTHOSTEL/
                archive_name = Path("B12_TEAM12_SMARTHOSTEL") / rel_path
                zipf.write(full_path, arcname=str(archive_name))

    print(f"Created {zip_path} ({zip_path.stat().st_size / (1024*1024):.2f} MB)")
    
    # Copy to Downloads
    shutil.copy2(zip_path, downloads_zip_path)
    print(f"Copied to {downloads_zip_path}")
    
    # Also create alias B12_G12_SMARTHOSTEL.zip for maximum compatibility
    alias_path = Path(r"C:\Users\Nethra R\Downloads\B12_G12_SMARTHOSTEL.zip")
    shutil.copy2(zip_path, alias_path)
    print(f"Copied alias to {alias_path}")

if __name__ == "__main__":
    create_submission_zip()
