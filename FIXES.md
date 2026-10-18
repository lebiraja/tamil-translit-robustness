# FIXES

Prepend an entry for each real bug or documentation error fixed: symptom, root cause, fix with `file:line`, verification. Newest on top. No code exists yet, so these are documentation and process fixes.

## F2 · 2026-10-18 · Leftover "laptop RTX 5070" in D10
- **Symptom:** `DECISIONS.md` row D10 still said the laptop was an RTX 5070 after F1 had been applied elsewhere.
- **Root cause:** F1 corrected D7, `CLAUDE.md` and `HANDOVER.md` but D10 was missed.
- **Fix:** `DECISIONS.md` D10 changed to "laptop RTX 4050 for development" (commit `7522579`); the later rewrite of `DECISIONS.md` keeps the correct values in D7 and D10.
- **Verification:** `grep -rn "laptop.*5070" .` over the docs finds only the sentences that describe the mistake itself.

## F1 · 2026-10-18 · Wrong GPU attributed to the laptop
- **Symptom:** early docs said the laptop has an RTX 5070 (12 GB, Blackwell) and planned PyTorch for it.
- **Root cause:** Lebi pasted the 5070 spec while saying "my lab system"; it was recorded as the laptop's GPU without checking. The lab docs (`/home/lebi/workspace/networks/dscs-lab/`, README and file 08) show the laptop `rog` has an RTX 4050 6 GB and the lab server Leica has the RTX 5070 12 GB.
- **Fix:** `DECISIONS.md` D7, `CLAUDE.md` rules, `HANDOVER.md` next steps rewritten to the correct split (laptop dev, Leica long runs); `docs/infrastructure.md` created with the verified specs and the Leica constraints.
- **Verification:** compared against `dscs-lab/README.md` ("Laptop RTX 4050 6 GB", "Leica RTX 5070 12 GB") and file 08 context section.

## Process notes (not bugs, recorded for the next session)
- Two dataset agents hit "No response from API" timeouts mid-task; fixed by resuming with a narrower brief and writing docs in small pieces. One doc had already been written before the timeout.
- Overlapping scope between the two dataset agents (both downloaded informal sets) was resolved by splitting ownership explicitly (pair sets versus informal sets).
- Idle and duplicate agent notifications were relayed to Lebi and confused them; relay only actionable news.
