#!/usr/bin/env python3
"""Old Bridge Cafe — Today's Special bot.

Zero-token background script (no LLM). Long-polls a Telegram bot; the shop
owner (whitelisted Telegram ID) sends the day's special as a plain message
and this script writes special.json in the site repo and pushes it, so the
marquee on the homepage updates within ~1-2 minutes.

Config: bot/config.json (chmod 600) — {"token": "...", "allowed": [123456],
"setup": true|false}. While "setup" is true, the FIRST sender becomes the
allowed admin and setup flips off.
State: bot/state.json — last processed update_id.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CONFIG = os.path.join(HERE, "config.json")
STATE = os.path.join(HERE, "state.json")
SPECIAL = os.path.join(REPO, "special.json")
LOG = os.path.join(HERE, "bot.log")
MAXLEN = 220


def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + str(msg)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line, flush=True)


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    os.replace(tmp, path)


def api(token, method, **params):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=70) as r:
        return json.loads(r.read().decode("utf-8"))


def reply(token, chat_id, text):
    try:
        api(token, "sendMessage", chat_id=chat_id, text=text)
    except Exception as e:
        log(f"reply failed: {e}")


def publish(text):
    """Write special.json and push it. Returns True on success."""
    save(SPECIAL, {"text": text, "updated": time.strftime("%Y-%m-%d %H:%M")})

    def git(*args):
        return subprocess.run(["git", "-C", REPO] + list(args),
                              capture_output=True, text=True, timeout=120)

    try:
        git("add", "special.json")
        c = git("commit", "-q", "-m", f"Special: {text[:60] or 'off'}")
        if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
            log("commit: " + (c.stdout + c.stderr).strip()[:200])
        p = git("push", "origin", "main")
        if p.returncode != 0:
            git("pull", "--rebase", "origin", "main")
            p = git("push", "origin", "main")
        if p.returncode != 0:
            log("push failed: " + (p.stdout + p.stderr).strip()[:300])
            return False
        return True
    except Exception as e:
        log(f"publish error: {e}")
        return False


HELP = ("ഇന്നത്തെ സ്പെഷ്യൽ ഒരു മെസ്സേജായി അയക്കൂ — 1-2 മിനിറ്റിനകം "
        "വെബ്സൈറ്റിൽ വരും.\n"
        "മാർക്വീ നിർത്താൻ OFF എന്ന് അയക്കൂ.\n"
        "ഇപ്പോഴത്തെ മാർക്വീ കാണാൻ /status അയക്കൂ.\n"
        "ഉദാഹരണം: ചിക്കൻ ബിരിയാണി ₹199 — ഇന്ന് മാത്രം!")


def main():
    cfg = load(CONFIG, None)
    if not cfg or not cfg.get("token"):
        log("No token in config.json — exiting.")
        return
    token = cfg["token"]
    try:
        me = api(token, "getMe")
        log(f"Bot up: @{me['result']['username']}")
    except Exception as e:
        log(f"getMe failed: {e}")
        return

    state = load(STATE, {"offset": 0})
    while True:
        try:
            res = api(token, "getUpdates", offset=state["offset"], timeout=50,
                      allowed_updates=["message"])
        except urllib.error.URLError as e:
            log(f"poll error: {e}")
            time.sleep(10)
            continue
        except Exception as e:
            log(f"poll error: {e}")
            time.sleep(10)
            continue

        for upd in res.get("result", []):
            state["offset"] = upd["update_id"] + 1
            save(STATE, state)
            msg = upd.get("message") or {}
            chat_id = (msg.get("chat") or {}).get("id")
            sender = (msg.get("from") or {}).get("id")
            text = (msg.get("text") or "").strip()
            if chat_id is None or sender is None:
                continue

            cfg = load(CONFIG, cfg)
            allowed = cfg.get("allowed", [])
            if cfg.get("setup") and not allowed:
                allowed = [sender]
                cfg["allowed"] = allowed
                cfg["setup"] = False
                save(CONFIG, cfg)
                log(f"Setup: admin captured id={sender}")
                reply(token, chat_id,
                      "✅ നിങ്ങൾ ഇപ്പോൾ Old Bridge Cafe വെബ്സൈറ്റ് സ്പെഷ്യലിന്റെ "
                      "അഡ്മിൻ ആണ്.\n\n" + HELP)
                continue
            if sender not in allowed:
                log(f"Ignored message from non-admin id={sender}")
                continue
            if not text:
                continue
            if text.startswith("/"):
                if text.lower() == "/status":
                    cur = ""
                    try:
                        with open(SPECIAL, encoding="utf-8") as fh:
                            cur = str(json.load(fh).get("text", "")).strip()
                    except Exception:
                        cur = ""
                    reply(token, chat_id,
                          f"\U0001F4E2 ഇപ്പോഴത്തെ മാർക്വീ:\n{cur}" if cur else
                          "\U0001F6D1 മാർക്വീ ഇപ്പോൾ OFF ആണ് \u2014 വെബ്സൈറ്റിൽ ഒന്നും കാണിക്കുന്നില്ല.")
                else:
                    reply(token, chat_id, HELP)
                continue
            if text.lower() in ("off", "stop", "ഓഫ്"):
                ok = publish("")
                reply(token, chat_id,
                      "✅ മാർക്വീ OFF ചെയ്തു — വെബ്സൈറ്റിൽ ഇനി സ്പെഷ്യൽ കാണിക്കില്ല."
                      if ok else "⚠️ OFF ചെയ്യാൻ പറ്റിയില്ല, കുറച്ച് കഴിഞ്ഞ് വീണ്ടും ശ്രമിക്കൂ.")
                continue
            text = text[:MAXLEN]
            ok = publish(text)
            reply(token, chat_id,
                  f"✅ അപ്ഡേറ്റ് ചെയ്തു! 1-2 മിനിറ്റിനകം വെബ്സൈറ്റിൽ കാണും:\n{text}"
                  if ok else "⚠️ അപ്ഡേറ്റ് ചെയ്യാൻ പറ്റിയില്ല, കുറച്ച് കഴിഞ്ഞ് വീണ്ടും ശ്രമിക്കൂ.")


if __name__ == "__main__":
    main()
