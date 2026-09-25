"""Pulls live numbers for the profile cards.

Every lookup has a fallback, so a flaky API never breaks the build —
the card just keeps its last-known-good value.
"""
import json
import urllib.error
import os
import re
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

USER = "dev048patel"
SITE = "https://gotransitregina.ca"
DMARC_README = f"https://raw.githubusercontent.com/{USER}/dmarc-translate/main/README.md"
TZ = ZoneInfo("America/Regina")

FIX = re.compile(r"\b(fix|fixes|fixed|fixing|bug|bugs|patch|typo|oops|hotfix|tweak)\b", re.I)
BREAK = re.compile(r"\b(revert|reverted|rollback|roll back|broke|broken|hotfix|urgent|emergency)\b", re.I)

DEFAULTS = {
    "gotransit_commits": 116,
    "site_live": True,
    "phase_current": 2,
    "phase_total": 5,
    "phase_name": "report ingestion pipeline",
    "last_push_days": None,
    "commits": [],          # list of "ok" | "fix" | "break", newest first
    "updated": datetime.now(TZ).strftime("%d %b %Y").upper(),
    "live": False,
    # per-project stats; public=False means the repo isn't on GitHub yet
    "repos": {
        "GoTransit": {"public": True, "commits": 116, "days": None},
        "dmarc-translate": {"public": True, "commits": 9, "days": None},
        "AI-Finance": {"public": True, "commits": None, "days": None},
        "AI-generate-code-reviewer": {"public": False, "commits": 0, "days": None},
    },
}


def _req(url, head=False):
    headers = {"User-Agent": f"{USER}-profile-card", "Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {tok}"
    r = urllib.request.Request(url, headers=headers, method="HEAD" if head else "GET")
    return urllib.request.urlopen(r, timeout=15)


def _json(url):
    with _req(url) as r:
        return json.load(r), r.headers


def commit_count(repo):
    _, h = _json(f"https://api.github.com/repos/{USER}/{repo}/commits?per_page=1")
    m = re.search(r'[?&]page=(\d+)>; rel="last"', h.get("Link", ""))
    return int(m.group(1)) if m else 1


def repo_stats(name):
    try:
        info, _ = _json(f"https://api.github.com/repos/{USER}/{name}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"public": False, "commits": 0, "days": None}
        raise
    pushed = datetime.fromisoformat(info["pushed_at"].replace("Z", "+00:00"))
    return {"public": True, "commits": commit_count(name),
            "days": (datetime.now(timezone.utc) - pushed).days}


def site_live():
    for _ in range(3):  # retry so one slow response doesn't flip the card to "down"
        try:
            with _req(SITE, head=True) as r:
                return r.status < 400
        except urllib.error.HTTPError as e:
            if e.code < 500 and e.code != 404:
                return True
        except Exception:
            pass
    return False


def dmarc_phase():
    with _req(DMARC_README) as r:
        text = r.read().decode()
    phases = re.findall(r"- \[( |x|X)\] Phase \d+\s*[—-]\s*(.+)", text)
    done = sum(1 for mark, _ in phases if mark.lower() == "x")
    total = len(phases)
    cur = min(done + 1, total)
    name = re.sub(r"\s*\(.*?\)", "", phases[cur - 1][1]).strip().lower()
    return cur, total, name, done == total


def my_commits(limit=200):
    repos, _ = _json(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    rows = []
    for repo in repos:
        if repo.get("fork") or repo["name"] == USER:
            continue
        for page in (1, 2):
            try:
                batch, _ = _json(f"https://api.github.com/repos/{USER}/{repo['name']}/commits"
                                 f"?author={USER}&per_page=100&page={page}")
            except Exception:
                break
            for c in batch:
                msg = c["commit"]["message"].split("\n")[0]
                when = c["commit"]["author"]["date"]
                kind = "break" if BREAK.search(msg) else "fix" if FIX.search(msg) else "ok"
                rows.append((when, kind))
            if len(batch) < 100:
                break
    rows.sort(reverse=True)
    return [k for _, k in rows[:limit]], (rows[0][0] if rows else None)


def gather():
    d = dict(DEFAULTS)
    if os.environ.get("PROFILE_OFFLINE"):  # local previews without network
        return d
    steps = {
        "gotransit_commits": lambda: commit_count("GoTransit"),
        "site_live": site_live,
    }
    for key, fn in steps.items():
        try:
            d[key] = fn()
            d["live"] = True
        except Exception as e:
            print(f"[live] {key} failed, keeping default: {e}")
    d["repos"] = {k: dict(v) for k, v in DEFAULTS["repos"].items()}
    for name in d["repos"]:
        try:
            d["repos"][name] = repo_stats(name)
        except Exception as e:
            print(f"[live] {name} stats failed, keeping default: {e}")
    try:
        cur, total, name, finished = dmarc_phase()
        d.update(phase_current=cur, phase_total=total, phase_name=name, phase_finished=finished)
    except Exception as e:
        print(f"[live] dmarc phase failed, keeping default: {e}")
    try:
        kinds, newest = my_commits()
        d["commits"] = kinds
        if newest:
            dt = datetime.fromisoformat(newest.replace("Z", "+00:00"))
            d["last_push_days"] = (datetime.now(timezone.utc) - dt).days
    except Exception as e:
        print(f"[live] commit history failed, keeping default: {e}")
    return d


def ago(days):
    if days is None:
        return "recently"
    return "today" if days == 0 else "yesterday" if days == 1 else f"{days} days ago"
