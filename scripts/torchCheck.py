# Quick GPU / torch diagnostics
import subprocess

print("--- GPU diagnostics ---")
# lightweight torch import for device checks; if not installed, install a CUDA-enabled build
try:
    import torch
except Exception:
    torch = None

try:
    out = subprocess.run(["nvidia-smi"], capture_output=True, text=True, check=True)
    print(out.stdout.splitlines()[:10])
except Exception as e:
    print("nvidia-smi not available or failed:", e)

if torch is not None:
    print("torch.__version__:", torch.__version__)
    print("torch.cuda.is_available():", torch.cuda.is_available())
    print("torch.cuda.device_count():", torch.cuda.device_count())
    if torch.cuda.is_available() and torch.cuda.device_count() > 0:
        try:
            print("device 0 name:", torch.cuda.get_device_name(0))
        except Exception:
            pass
else:
    print(
        "torch not installed in this environment. Install a CUDA-enabled torch if you want GPU execution."
    )
