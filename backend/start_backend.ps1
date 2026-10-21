# ----------------------------------------------------
# backend/start_backend.ps1
# Starts the FastAPI backend using the *active* virtual environment.
# ----------------------------------------------------

# ------------------------------------------------------------
# Step 1 – Verify we are inside a Python virtual environment.
# If the prompt already shows (venv) you can skip activation.
# ------------------------------------------------------------
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found – activate the virtual environment first."
    exit 1
}

# ------------------------------------------------------------
# Step 2 – Add the folder that contains the `app` package to PYTHONPATH.
# This allows `import app.main` to work even when the script is run
# from the project root.
# ------------------------------------------------------------
$backendRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $backendRoot

# ------------------------------------------------------------
# Step 3 – Run uvicorn via the interpreter (ensures the venv's uvicorn).
# ------------------------------------------------------------
python -m uvicorn app.main:app `
    --host 0.0.0.0 `
    --port 8000 `
    --reload