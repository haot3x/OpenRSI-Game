"""Benchmark-owned controlled interventions, not historical natural game runs."""
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_MANIFEST = ROOT / "assets/manifest.json"
VARIANTS = ("working", "no_clear", "no_reward")
REQUIREMENTS = ("line_clear", "score_on_clear")


def verify_assets():
    for game in json.loads(ASSET_MANIFEST.read_text())["games"]:
        for record in game["files"]:
            if hashlib.sha256((ROOT / record["path"]).read_bytes()).hexdigest() != record["sha256"]:
                raise ValueError("Frozen game asset digest mismatch")


def cases(split):
    if split != "dev":
        raise ValueError("Local prototype: full Judge fixtures not yet authored")
    seeds = range(10, 18)
    result = [(family, variant, seed) for family in ("a", "b")
              for variant in VARIANTS for seed in seeds]
    random.Random(901 if split == "dev" else 902).shuffle(result)
    return result


def labels(variant):
    # Score-on-clear has no eligible event if removal itself is disabled.
    return {"line_clear": "failed" if variant == "no_clear" else "passed",
            "score_on_clear": None if variant == "no_clear" else
            ("failed" if variant == "no_reward" else "passed")}


def starting_board(seed, family):
    # Local feasibility pilot: board geometry is fixed before policy controls.
    payload = json.loads((ROOT / "assets/challenges-pilot.json").read_text())
    matches = [r for r in payload["boards"] if r["family"] == family and r["seed"] == seed]
    if len(matches) != 1:
        raise ValueError("This local prototype has development fixtures only")
    return matches[0]["board"]


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError("Game adaptation anchor mismatch")
    return source.replace(old, new, 1)


def document(family, variant, seed, probe=False):
    directory = ROOT / "assets/games" / family
    html = (directory / "index.html").read_text()
    if family == "a":
        js = (directory / "game.js").read_text()
        html = html.replace('<link rel="stylesheet" href="style.css">',
                            '<style>' + (directory / "style.css").read_text() + '</style>')
        # Exact tag checked below to avoid silently loading an external script.
        import re
        html, count = re.subn(r'<script src="game.js"[^>]*></script>', '<!-- GAME_SCRIPT -->', html)
        if count != 1:
            raise ValueError("Missing game script tag")
        grid = "board"
        anchor = "const remain=board.filter(r=>r.some(v=>!v)),count=20-remain.length;"
        js = replace_once(js, anchor, "window.__events.push({rows:board.filter(r=>r.every(Boolean)).length,scoreBefore:score,linesBefore:lines});" + anchor)
        if variant == "no_clear":
            js = replace_once(js, "const remain=board.filter(r=>r.some(v=>!v))", "const remain=board.slice()")
        if variant == "no_reward":
            js = replace_once(js, "score+=[0,100,300,500,800][count]*level", "score+=0")
        js = replace_once(js, "$('overlay').hidden=true;$('pause').disabled=false;",
                          "board=window.__startingBoard.map(r=>r.slice());$('overlay').hidden=true;$('pause').disabled=false;")
        if probe:
            js = replace_once(js, "function take(){", "function take(){return window.__sequence.shift()||'O';")
        tail = "})();"
    else:
        start = html.index("  <script>")
        js_start = html.index("  (() => {", start)
        end = html.index("  </script>", js_start)
        js = html[js_start:end]
        html = html[:start] + "<!-- GAME_SCRIPT -->" + html[end + len("  </script>"):]
        grid = "grid"
        js = replace_once(js, "let cleared=0;", "window.__events.push({rows:grid.filter(r=>r.every(Boolean)).length,scoreBefore:score,linesBefore:lines});let cleared=0;")
        if variant == "no_clear":
            js = replace_once(js, "if(grid[y].every(Boolean))", "if(false && grid[y].every(Boolean))")
        if variant == "no_reward":
            js = replace_once(js, "score += [0,100,300,500,800][cleared]*level", "score += 0")
        js = replace_once(js, "overlay.hidden=true;pauseButton.textContent='Pause';updateStats();spawn();draw();",
                          "grid=window.__startingBoard.map(r=>r.slice());overlay.hidden=true;pauseButton.textContent='Pause';updateStats();spawn();draw();")
        if probe:
            js = replace_once(js, "function takeType(){", "function takeType(){return window.__sequence.shift()||'O';")
        tail = "  })();"
    # Private instrumentation certifies actual row-completion events and the
    # reward generated inside lock(), excluding hard/soft-drop points.
    hook = f"""
const originalLock=lock;
lock=function(){{
  const n=window.__events.length; originalLock();
  if(window.__events.length>n){{
    const e=window.__events[window.__events.length-1];
    e.linesAfter=lines; e.scoreAfter=score;
    e.fullRowsAfter={grid}.filter(r=>r.every(Boolean)).length;
  }}
}};
"""
    js = replace_once(js, tail, hook + tail)
    setup = {"board": [[None] * 10 for _ in range(20)] if probe else starting_board(seed, family),
             "seed": seed, "sequence": ["I", "J", "L"] if probe else []}
    bootstrap = """
window.__events=[];
window.__startingBoard=SETUP.board; window.__sequence=SETUP.sequence;
let rng=SETUP.seed>>>0;
Math.random=()=>{rng=(Math.imul(1664525,rng)+1013904223)>>>0;return rng/4294967296;};
window.__sim={time:0,callbacks:[],advance(ms){
  for(let remaining=ms;remaining>0;){const delta=Math.min(16,remaining);
    this.time+=delta;remaining-=delta;const queue=this.callbacks.splice(0);
    for(const fn of queue)fn(this.time);}
}};
performance.now=()=>window.__sim.time;
window.requestAnimationFrame=fn=>{window.__sim.callbacks.push(fn);return window.__sim.callbacks.length;};
""".replace("SETUP", json.dumps(setup, separators=(",", ":")))
    return html.replace("<!-- GAME_SCRIPT -->", "<script>" + bootstrap + js + "</script>")
