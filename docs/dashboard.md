# Live run monitor (port 8383)

Read-only web dashboard on Leica: `http://<leica-ip>:8383` (currently `http://10.42.0.226:8383`, reachable from any machine on the same network).

- **Code:** `scripts/dashboard/server.py` (plain python3, no dependencies) and `scripts/dashboard/static/index.html` (plain JS, SVG charts, no CDN, works offline).
- **Start / restart:** `sh scripts/dashboard/run.sh [port]` (detached, safe to repeat; logs in `logs/dashboard/server.out`). It does not survive a Leica reboot; never reboot Leica (D15), then restart it with that command.
- **Data:** rebuilt on every 5 s poll from `logs/*.log` (training lines `[run] epN loss L devCER(greedy) C`) and `results/*/*.json`, plus `nvidia-smi`, `/proc` and `scripts/autopilot_status.py`. Nothing is copied or stored elsewhere: the log files are the archive.
- **Tabs:** Runs (every run, past and present: loss and dev-CER graphs, rings where a checkpoint was saved, the best checkpoint marked with a white ring, best.pt size, final metrics, click a run name for its raw log; filters by block, model, state, name), Noise (CER versus noise severity per noise type, per model, from the noisy test results), Now (live loss and dev-CER curves per running job with a verdict: improving, converging, overfitting?, about to early-stop), Tuning (all 6 model/size searches: progress, every trial, top trials), Results (gate, C3, C2 tables, mean +/- sd over seeds, noisy and independent columns as they appear), Past runs (compare up to 4 learning curves), Logs (live tail of any log).
- **Header:** GPU load, temperature, power, VRAM, CPU load, RAM, free disk, kernel check (must be 6.17.0-22-generic), uptime and the autopilot stage.
- **Safety:** the only file access is `logs/<name>.log` by basename (no path traversal); no write endpoints; binds 0.0.0.0, so anyone on the lab network can read it. It exposes no secrets (logs hold only training lines).
