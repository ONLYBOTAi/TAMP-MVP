# **TAMP — Tech‑Lead Command Charter**

> **Audience**  Tech Lead **Evens** (Facilitator & Project Manager) | Tech Lead **Kenny**\
> **Version 1.3 · 23 Jun 2025**\
> **Purpose**  A reusable prompt‑sheet that both Tech Leads read at the **start of every work session**. It cements alignment on goals, GitHub workflow, quality gates, and communication rituals so the **Project TAMP** code‑base stays consistent, traceable, and defect‑free.\
> **Scope**  Rules apply **only** to the TAMP monorepo and its microservices.

---

## 1 · Mission Objectives

| ID      | Objective                                                 | Success Criteria                                                          |
| ------- | --------------------------------------------------------- | ------------------------------------------------------------------------- |
| **O‑1** | Deliver TAMP roadmap increments **on sprint commitments** | All planned stories closed & demo passes with **zero High‑severity bugs** |
| **O‑2** | Maintain **one deploy‑ready truth** (`main`)              | `main` CI always green; can tag & deploy anytime                          |
| **O‑3** | **Lead from the front**—coach, unblock, review            | MR review latency ≤ 24 h; blockers triaged ≤ 2 h                          |
| **O‑4** | Keep docs & metrics **current**                           | Sprint summary committed at review; GitHub Insights updated               |

---

## 2 · Cadence & Rituals

> **Sprint Duration**  Default **1 week**. Tech Leads may extend/shorten to fit BRS roadmap but must lock before planning.

| Event                     | Participants                  | Timing                  | Agenda                                                            | Artefact                                   |
| ------------------------- | ----------------------------- | ----------------------- | ----------------------------------------------------------------- | ------------------------------------------ |
| **Pre‑Sprint Planning**   | Evens + Kenny (+ Senior Devs) | Day‑0                   | ‑ Confirm sprint length & scope‑ Assign issues, labels, milestone | Milestone `YYYY‑WW` created/updated        |
| **Daily Sync**            | Evens ⇄ Kenny                 | Async thread in ``      | ‑ Progress‑ Blockers‑ Review queue                                | Slack thread link in issue `TL‑LOG‑<date>` |
| **Stand‑Up (Pre‑Review)** | TLs + Senior Devs             | Last day, morning       | ‑ Present *SPRINT\_SUMMARY.md* draft                              | Draft committed for review                 |
| **Sprint Review**         | TLs + Senior Devs             | Last day, afternoon     | ‑ Demo features‑ Accept/Reject stories                            | Merge & tag release                        |
| **Retro & Re‑Plan**       | Evens (facilitator) + Kenny   | Immediately post‑review | ‑ Retrospective‑ Draft next sprint                                | Retro notes committed                      |

> **Stand‑Up Content**  Each stand‑up references the **latest commit hash** for every completed story and lists open blockers.

---

## 3 · GitHub Workflow (Non‑Negotiable)

1. **Branching (Trunk‑Based)**
   ```text
   main                                  # protected & deploy‑ready
   feat/<service>/TAMP‑123‑slug          # feature work
   fix/<service>/TAMP‑123‑slug           # bug‑fix
   hotfix/TAMP‑xyz‑slug                  # prod hot‑fix
   ```
2. **Protections**
   - `main` requires ✅ **CI green** + **≥ 1 review** (other TL or CODEOWNER).
   - Feature branches **auto‑deleted** after merge (nightly bot); branches > 14 days or > 50 commits behind deleted.
3. **Issue → PR Lifecycle**
   - Labels: `feat`, `bug`, `chore`, `infra`, `docs`, `high‑blocker`.
   - Conventional Commits (`feat(vehicle): add VIN check`).
   - Milestones == sprint ID (`2025‑26`).
   - Each PR links its issue and fills PR template (context, tests, rollout).
4. **CI Gates** (GitHub Actions)
   - **Lint + Type‑Check** → Ruff & MyPy **zero warnings**.
   - **Unit + Integration Tests** → coverage **≥ 85 %** else fail.
   - **Smoke** → `bootstrap.sh` then `health_check.sh` full Compose stack.
5. **Release Tagging & Hot‑Fixes**
   - Merge of final PR auto‑tags: `v0.<sprint>.<0>` (e.g. `v0.10.0`).
   - Hot‑fix flows: branch from tag, patch, tag `v0.<sprint>.<patch>`; PR back to `main`.
6. **Documentation Hooks**
   - `/docs/sprints/YYYY‑WW/SPRINT_SUMMARY.md` committed before review ends.
   - `/docs/retro/YYYY‑WW/RETRO.md` committed after retro.

---

## 4 · Quality‑Assurance Doctrine

| Metric              | Source          | Threshold     | Action if Breached           |
| ------------------- | --------------- | ------------- | ---------------------------- |
| **Lead‑Time**       | GitHub Insights | > 3 d avg     | Open *Process‑Improve* issue |
| **MTTR**            | GitHub Insights | > 1 d         | Escalate risk issue          |
| **Coverage**        | Pytest --cov    | < 85 %        | Block merge                  |
| **Static Analysis** | Ruff + MyPy     | Any warning   | Block merge                  |
| **Manual QA**       | Playwright      | Critical fail | Revert or hot‑fix before tag |
| **Sprint Summary**  | Docs commit     | Missing       | Sprint incomplete            |

---

## 5 · Cursor IDE Oversight

| Limitation               | Mitigation                                                        |
| ------------------------ | ----------------------------------------------------------------- |
| \~8 k token context      | Limit prompts to ≤ 1 service or ≤ 400 LOC; chunk work             |
| Staging drift            | Pre‑commit hook aborts if staged ≠ working‑tree                   |
| Import/env hallucination | Follow `docs/STYLE_GUIDE.md`; CI fails unknown keys               |
| No runtime               | CI smoke run is single source of truth; red → TL opens fix prompt |

**Prompt Scaffold** (paste into Cursor Chat):

```
Project: TAMP · Service: <service>
Goal: <short goal> (TAMP‑###)
⚙  Build context: repo root
🗄  Follow STYLE_GUIDE for imports, async DB, env keys
🔐  Use .env.example; do NOT add keys
✅  Run `pytest -q && ruff .` locally; confirm green
📄  Stage ONLY intended files
💬  Commit message: <type(scope): summary>
```

---

## 6 · Escalation Path & Risk Log

- **Blocker > 2 h** → label `high‑blocker`, mention `@tech‑lead‑escalation` in Slack.
- **CI red > 4 h** → open *CI‑BLOCKER* issue, assign both TLs.
- **Risk Register** → GitHub Project **Risk‑Log**.

---

## 7 · Daily Command Checklist

| ✔ | Task                                        |
| - | ------------------------------------------- |
| ☐ | Review `high‑blocker` & `CI‑BLOCKER` issues |
| ☐ | Clear PR review queue ≤ 24 h                |
| ☐ | Verify `main` CI green                      |
| ☐ | Check GitHub Insights lead‑time & MTTR      |
| ☐ | Update daily thread in `#tamp‑sync`         |

---

## 8 · Sprint Close Checklist

1. All milestone issues **Done** & closed.
2. Merge remaining PRs; tag release.
3. Commit **SPRINT\_SUMMARY.md**.
4. Run retro; commit **RETRO.md**.
5. Prune stale branches; close milestone.

---

> **Lead the standard.**  When Tech Leads follow these rules openly and consistently, the entire TAMP team mirrors the discipline—ensuring predictable delivery and uncompromising quality.

