# Infrastructure: machines, access and constraints

Source: `/home/lebi/workspace/networks/dscs-lab/` (README, files 01 to 08, CHANGES), written 2026-10-16. Re-verify anything marked (verify) before relying on it. Nothing on Leica was touched in this project's first session.

## Machines

| | Laptop `rog` | Lab server **Leica** |
|---|---|---|
| Role for this project | development, unit tests, small runs, paper writing | long training runs, seed sweeps, hyperparameter search |
| OS | CachyOS (Arch), shell fish | Ubuntu 24.04.4 LTS |
| GPU | NVIDIA RTX 4050 Mobile, 6 GB | NVIDIA RTX 5070, 12 GB (12,227 MiB), 250 W, compute capability 12.0 (Blackwell, sm_120) |
| CPU / RAM | 15 GB RAM | Intel i7-14700, 20 cores / 28 threads; **15 GiB RAM**; 9.3 GiB swap |
| Disk | about 464 GB free on /home | 477 GB NVMe; ext4 root 331 GB, about 237 GB free after the Docker wipe |
| Python | project venv or Docker (never global pip) | system Python 3.12.3, no conda/uv; no `nvcc` (CUDA runtime libraries present, toolkit not) |
| Access | local | `ssh airoot` (key `~/.ssh/airoot`, user `lebiraja`, host `10.42.0.226`) |

Leica's hostname is `airoot-Altos-P130-F9`; Lebi named it "Leica" on 2026-10-16.

## Network
- Laptop and Leica are joined by a LAN cable: laptop `enp108s0` = `10.42.0.1/24` (NetworkManager connection `lan-share`, `ipv4.method shared`, NAT out through Wi-Fi), Leica `enp0s31f6` = `10.42.0.226` by DHCP (can change; use the `.local` name or reserve the address if it does).
- Link speed is 100 Mbps (downshifted; likely a worn cable). Fine for SSH and small files, slow for large model files. Replace the cable for 1 Gbps.
- Laptop internet comes from a phone hotspot; Lebi's home upload to GitHub is slow (about 36 KB/s per earlier notes). **Keep pushed artifacts small**: results as CSV/JSON, not checkpoints. Move big files laptop to Leica with `scp`/`rsync`, not through GitHub.

## Constraints that shape our plan
1. **VRAM 12 GB / RAM 15 GB.** Our models are 1M to 8M parameters, so VRAM is not the limit; RAM and data loading are. Keep datasets small (the Dakshina Tamil lexicon is about 68k pairs).
2. **The GPU works only on kernel 6.17.0-22.** Leica booted into 7.0.0-34 earlier, which has no matching NVIDIA module, and `nvidia-smi` failed. A one-shot `grub-reboot` brought 6.17.0-22 back. The permanent fix (`GRUB_DEFAULT=saved` plus `grub-set-default`) was **not applied**. Therefore **the next reboot of Leica probably breaks the GPU.** We must not reboot it, and we must ask Lebi before touching GRUB. Always run `uname -r` and `nvidia-smi` before a long job.
3. **Blackwell needs a recent PyTorch.** Use a build with CUDA 12.8 or newer (sm_120 support). Driver is 590.48.01. Verify with `torch.cuda.get_device_capability()` and a small matmul before anything else.
4. **Docker on Leica is empty** (0 images, containers, volumes, build cache after the 2026-10-16 wipe). Whether the NVIDIA container toolkit is still installed is ambiguous in the notes (verify with `docker info | grep -i runtime`). Docker Swarm is still active with 3 dead nodes (do not touch).
5. **Shared machine.** Other work (for example ENDCORE for the "Curiosity Is All You Need" paper) may want Leica. Check `nvidia-smi` for running jobs, run ours in a named container, and do not exceed the memory of a job already running.
6. **No sudo without Lebi.** sudo needs a password; per the global rules Lebi gives it per task and it is never written to files.
7. **Security housekeeping (Lebi's to-do).** Rotate the two passwords shared in chat during the lab session; Leica's SSH password login is still enabled; Apache, LDAP and GNOME Remote Desktop still run. Not our scope, but do not make it worse.

## Compute budget (estimates, to be measured in the first smoke test)
- Literature scale: word-level char models of 2 to 6M parameters train in tens of minutes to about 1.5 h on an RTX 2080 Ti for 279k pairs (Moran and Lignos 2020). Our Dakshina training set is about 68k pairs, so one run should take minutes to tens of minutes on the 5070.
- Rough count (see `experiment-plan.md`): about 120 short hyperparameter trials, about 30 seeds for final C3 models, about 60 seeds for the C2 augmentation matrix, plus noise evaluation (inference only, cheap). This is days of GPU time on one 12 GB card, not weeks. Measure before promising a date.

## Workflow
1. Develop and unit-test on the laptop (RTX 4050 6 GB is enough for small runs).
2. `rsync` the repo (code, configs, small data) to `airoot:~/lab/tamil-translit/`.
3. Run inside Docker or a venv on Leica, under `tmux` or `nohup`, logging to `results/`.
4. Pull back only metrics and logs; commit them.
5. Record every run (git commit hash, config file, seed, date, machine, `nvidia-smi` and `torch` versions) in the results JSON.

## Open items (need Lebi)
- Apply the permanent kernel pin on Leica? (Needs a reboot and sudo; recommended before long jobs.)
- Is the NVIDIA container toolkit present on Leica? (verify)
- Is Leica free of other jobs during our runs?
- Replace the cable to get 1 Gbps (optional).
