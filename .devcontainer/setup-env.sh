#!/bin/bash
set -e

# Use project-local Micromamba root
export MAMBA_ROOT_PREFIX="$(pwd)/.micromamba"
ENV_NAME="dev"

# Create environment from environment.yml (stored under .micromamba/envs/dev)
micromamba create -y -n "$ENV_NAME" -f ./environment.yml

# Clean cache to keep .micromamba small
micromamba clean -a -y

# Register Jupyter kernel using micromamba run
micromamba run -n "$ENV_NAME" python -m ipykernel install \
    --user \
    --name "$ENV_NAME" \
    --display-name "Python ($ENV_NAME)"

# Add MAMBA_ROOT_PREFIX if not already in bashrc
if ! grep -qxF "export MAMBA_ROOT_PREFIX=\"$MAMBA_ROOT_PREFIX\"" ~/.bashrc; then
    echo "export MAMBA_ROOT_PREFIX=\"$MAMBA_ROOT_PREFIX\"" >> ~/.bashrc
fi

# Add Micromamba initialization (if missing)
if ! grep -qxF 'eval "$(micromamba shell hook -s bash)"' ~/.bashrc; then
    echo 'eval "$(micromamba shell hook -s bash)"' >> ~/.bashrc
fi

# Add environment auto-activation for this workspace only
if ! grep -qxF "micromamba activate $ENV_NAME" ~/.bashrc; then
    echo "micromamba activate $ENV_NAME" >> ~/.bashrc
fi