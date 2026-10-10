"""Greedy, non-rotating visual baseline. Uses only the documented observation API."""
import json
import sys

plan = []
previous = None
report = {r: {"status": "unverified", "frames": []} for r in ("line_clear", "score_on_clear")}


def occupied(obs):
    # Samples are rendered cell centers. Ghost outlines/blended cells are dimmer.
    return [[max(rgb) > 125 for rgb in row] for row in obs["board_rgb"]]


def placement(board):
    active = [(x, y) for y in range(6) for x in range(10) if board[y][x]]
    if not active:
        return [{"wait_ms": 800}]
    left = min(x for x, y in active)
    right = max(x for x, y in active)
    locked = [row[:] for row in board]
    for x, y in active:
        locked[y][x] = False
    best = None
    for dx in range(-left, 10 - right):
        dy = 0
        while all(y + dy + 1 < 20 and not locked[y + dy + 1][x + dx] for x, y in active):
            dy += 1
        grid = [row[:] for row in locked]
        for x, y in active:
            grid[y + dy][x + dx] = True
        cleared = sum(all(row) for row in grid)
        rest = [row for row in grid if not all(row)]
        rest = [[False] * 10 for _ in range(20 - len(rest))] + rest
        heights, holes = [], 0
        for x in range(10):
            top = next((y for y in range(20) if rest[y][x]), 20)
            heights.append(20 - top)
            holes += sum(not rest[y][x] for y in range(top, 20))
        value = 12 * cleared - 5 * holes - sum(heights) - sum(abs(a - b) for a, b in zip(heights, heights[1:]))
        item = (value, -abs(dx), dx, dy)
        if best is None or item > best:
            best = item
    dx, dy = best[2:]
    return [{"key": "ArrowRight" if dx > 0 else "ArrowLeft"} for _ in range(abs(dx))] + [{"key": "Space", "expected_drop_points": dy * 2}]


for line in sys.stdin:
    request = json.loads(line)
    obs = request["observation"]
    if previous is not None and previous.get("drop"):
        before = previous["observation"]
        if obs["lines"] > before["lines"]:
            evidence = [before["frame"], obs["frame"]]
            report["line_clear"] = {"status": "passed", "frames": evidence}
            report["score_on_clear"] = {"status": "passed" if obs["score"] - before["score"] > previous["drop_points"] else "failed", "frames": evidence}
        elif any(all(row) for row in occupied(obs)):
            report["line_clear"] = {"status": "failed", "frames": [before["frame"], obs["frame"]]}
    if report["line_clear"]["status"] != "unverified" or request["remaining_actions"] == 0:
        print(json.dumps({"final": report}), flush=True)
        break
    if obs["overlay_visible"]:
        action = {"key": "Enter"}
        plan = []
    else:
        if not plan:
            plan = placement(occupied(obs))
        action = plan.pop(0)
    points = action.pop("expected_drop_points", 0)
    previous = {"observation": obs, "drop": action.get("key") == "Space", "drop_points": points}
    print(json.dumps({"action": action}), flush=True)
