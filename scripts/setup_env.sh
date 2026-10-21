#!/usr/bin/env bash
# Create .venv with CUDA 12.8 PyTorch (needed for Blackwell sm_120 on Leica; also fine on the RTX 4050 laptop).
set -euo pipefail
cd "$(dirname "$0")/.."
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cu128
uv pip install --python .venv/bin/python numpy pydantic pyyaml scipy pandas pytest
.venv/bin/python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
