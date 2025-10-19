#!/bin/bash

# ==========================
# CONFIGURATION
# ==========================
ENV_NAME="dev"                    # your conda/venv environment
NOTEBOOK_DIR="$PWD/notebooks"
PORT=8888                         # notebook server port
DARK_THEME="oceans16"              # jupyterthemes dark theme

# ==========================
# ACTIVATE ENVIRONMENT
# ==========================
if command -v conda &> /dev/null; then
    echo "Activating conda environment: $ENV_NAME"
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$ENV_NAME"
elif [ -d "$ENV_NAME" ]; then
    echo "Activating venv at $ENV_NAME"
    source "$ENV_NAME/bin/activate"
else
    echo "No environment found. Using current Python environment."
fi

# ==========================
# CREATE NOTEBOOK DIRECTORY
# ==========================
mkdir -p "$NOTEBOOK_DIR"
cd "$NOTEBOOK_DIR" || exit

echo "Applying dark theme: $DARK_THEME"
if command -v jt &> /dev/null; then
    echo "Applying dark theme: $DARK_THEME"
    jt -t "$DARK_THEME" -T -N -kl -f roboto -fs 11 -nf ptsans -tf ptsans -cellw 90% -lineh 170
else
    echo "jupyter-themes not installed, skipping theme."
fi
# ==========================
# START NOTEBOOK
# ==========================
echo "Starting Jupyter Notebook at http://localhost:$PORT ..."
jupyter notebook --no-browser --port=$PORT --ip=0.0.0.0