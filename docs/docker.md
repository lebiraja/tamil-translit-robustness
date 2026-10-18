# Docker and environment (planned; nothing built yet)

Rules from the user's global conventions: app services and their dependencies run in Docker; Python deps in Docker or a venv, never global `pip`; pin versions in requirements files; `env_file:` for config, no hardcoded credentials; add healthchecks where a service exists. This project has no long-running service, only a trainer container, so healthchecks do not apply; a smoke-test command serves as the check.

## Image plan
- Base: an official PyTorch CUDA image with CUDA 12.8 or newer (needed for the RTX 5070, Blackwell sm_120). Pin the exact image tag and the `torch` version in `requirements.txt`. Verify support before building: run `torch.cuda.get_device_capability()` and a small matmul on the target GPU.
- Laptop (RTX 4050) works with the same image for development.
- System packages: `git`, `rsync`, a TeX distribution is NOT in the image (the paper is built locally with the existing TeX Live and Texpile).
- Python packages (pin all): torch, numpy, pandas, pydantic, pyyaml, pytest, scipy, tqdm, matplotlib. Add `fairseq`-based IndicXlit only in a separate image if the A3 generator needs it.

## Compose sketch
```yaml
services:
  trainer:
    build: .
    env_file: .env            # not committed; contains only local settings
    volumes:
      - ./:/workspace
      - ./data:/workspace/data
    working_dir: /workspace
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
    command: ["python", "scripts/run_experiment.py", "--config", "configs/baseline.yaml"]
```
Run tests with `docker compose run --rm trainer pytest`.

## Leica specifics
- Docker on Leica is empty after the 2026-10-16 wipe. Whether the NVIDIA container toolkit is installed must be checked (`docker info | grep -i runtime`). If it is missing, either install it with Lebi's sudo approval or use a venv instead of Docker for GPU runs.
- Do not touch Swarm, GRUB or the kernel. Check `uname -r` equals 6.17.0-22-generic and `nvidia-smi` works before each long job.
- Use a named container (`tamil-translit-*`) so it is identifiable next to other work, and limit memory so it cannot starve the 15 GB machine.

## Secrets
- No credentials in the repo. `.env` is gitignored. The Hugging Face token Lebi shared in chat was not needed and must not be stored; if a gated model is ever needed, pass it as `HF_TOKEN` for that one command only.
