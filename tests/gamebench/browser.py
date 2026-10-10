"""Task-owned browser. A candidate receives rendered pixels and visible counters."""
import base64
from .fixtures import document

ALLOWED_KEYS = {"Enter", "ArrowLeft", "ArrowRight", "ArrowDown", "ArrowUp", "Space"}


class Game:
    def __init__(self, browser, family, variant, seed, probe=False):
        self.context = browser.new_context(viewport={"width": 1280, "height": 900},
                                           device_scale_factor=1, service_workers="block")
        self.context.route("**/*", lambda route: route.abort())
        self.page = self.context.new_page()
        self.page.set_content(document(family, variant, seed, probe))
        self.frame = 0
        self.certificates = {}
        self.page.evaluate("window.__sim.advance(32)")

    def observe(self, include_image=False):
        observation = self.page.evaluate("""() => {
          const canvas=document.querySelector('#board'),ctx=canvas.getContext('2d');
          const rgb=Array.from({length:20},(_,y)=>Array.from({length:10},(_,x)=>
            Array.from(ctx.getImageData(x*30+15,y*30+15,1,1).data).slice(0,3)));
          return {board_rgb:rgb,score:Number(document.querySelector('#score').textContent),
            lines:Number(document.querySelector('#lines').textContent),
            overlay_visible:!document.querySelector('#overlay').hidden,
            overlay_text:document.querySelector('#overlay').innerText};
        }""")
        observation["frame"] = self.frame
        if include_image:
            observation["board_png_base64"] = base64.b64encode(
                self.page.locator("#board").screenshot()).decode()
        return observation

    def act(self, action):
        if not isinstance(action, dict):
            raise ValueError("Action must be an object")
        if set(action) == {"key"} and isinstance(action["key"], str) and action["key"] in ALLOWED_KEYS:
            self.page.keyboard.press(action["key"])
            duration = 32
        elif set(action) == {"wait_ms"} and type(action["wait_ms"]) is int and 16 <= action["wait_ms"] <= 2000:
            duration = action["wait_ms"]
        else:
            raise ValueError("Illegal action; only one bounded key or wait is allowed")
        self.page.evaluate("ms => window.__sim.advance(ms)", duration)
        events = self.page.evaluate("window.__events.splice(0)")
        self.frame += 1
        for e in events:
            if e["rows"] <= 0:
                continue
            cert = {"line_clear": "passed" if e["linesAfter"] > e["linesBefore"] and e["fullRowsAfter"] == 0 else "failed"}
            if cert["line_clear"] == "passed":
                cert["score_on_clear"] = "passed" if e["scoreAfter"] > e["scoreBefore"] else "failed"
            self.certificates[self.frame] = cert
        return self.observe()

    def close(self):
        self.context.close()
