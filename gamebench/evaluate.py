"""Fixed candidate-only evaluation; no inference service, training or live baseline."""
import argparse
import hashlib
import json
import os
import select
import selectors
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from .browser import Game
from .fixtures import cases, labels, verify_assets
from .scoring import aggregate, decisions, validate_report

ACTION_BUDGET = 16


class CandidateError(Exception):
    pass


def run_case(browser, policy, case, image=False):
    game = Game(browser, *case)
    process = subprocess.Popen([sys.executable, "-I", str(policy)], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               start_new_session=True, bufsize=0)
    os.set_blocking(process.stdin.fileno(), False)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    # Read bounded newline records without a readline() hang or unbounded allocation.
    buffer = b""
    deadline = time.monotonic() + 30

    def receive():
        nonlocal buffer
        while b"\n" not in buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not selector.select(remaining):
                raise CandidateError("Candidate deadline exceeded")
            chunk = os.read(process.stdout.fileno(), 4096)
            if not chunk:
                raise CandidateError("Candidate exited before final report")
            buffer += chunk
            if len(buffer) > 65536:
                raise CandidateError("Candidate record exceeds 64 KiB")
        line, buffer = buffer.split(b"\n", 1)
        try:
            return json.loads(line)
        except (ValueError, UnicodeError) as error:
            raise CandidateError("Invalid candidate JSON") from error

    try:
        observation = game.observe(image)
        for step in range(ACTION_BUDGET + 1):
            try:
                payload = (json.dumps({"observation": observation,
                    "remaining_actions": ACTION_BUDGET - step, "requirements": ["line_clear", "score_on_clear"]}) + "\n").encode()
                while payload:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0 or not select.select([], [process.stdin], [], remaining)[1]:
                        raise CandidateError("Candidate input deadline exceeded")
                    try:
                        written = os.write(process.stdin.fileno(), payload)
                    except BlockingIOError:
                        continue
                    payload = payload[written:]
            except BrokenPipeError as error:
                raise CandidateError("Candidate process crashed") from error
            message = receive()
            if not isinstance(message, dict) or len(message) != 1:
                raise CandidateError("Candidate must emit one action or final report")
            if "final" in message:
                try:
                    validate_report(message["final"], game.frame)
                except ValueError as error:
                    raise CandidateError(str(error)) from error
                return decisions(message["final"], labels(case[1]), game.certificates), step
            if "action" not in message or step == ACTION_BUDGET:
                raise CandidateError("Missing final report or action budget exceeded")
            try:
                observation = game.act(message["action"])
                if image:
                    observation = game.observe(True)
            except ValueError as error:
                raise CandidateError(str(error)) from error
    finally:
        selector.close()
        import signal
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        game.close()


def evaluate(policy, split, image=False, limit=None):
    verify_assets()
    if not policy.is_file() or policy.stat().st_size > 1024 * 1024:
        raise CandidateError("Missing policy or policy exceeds 1 MiB")
    selected = cases(split)
    if limit is not None:
        selected = selected[:limit]
    rows, actions = [], 0
    begin = time.monotonic()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        try:
            for i, case in enumerate(selected):
                outcomes, count = run_case(browser, policy, case, image)
                rows.extend(outcomes)
                actions += count
                print(f"Completed {i + 1}/{len(selected)} cases", file=sys.stderr, flush=True)
            result = aggregate(rows)
            result.update({"split": split, "cases": len(selected), "actions": actions,
                           "action_budget": ACTION_BUDGET,
                           "elapsed_seconds": round(time.monotonic() - begin, 3),
                           "browser_version": browser.version,
                           "policy_sha256": hashlib.sha256(policy.read_bytes()).hexdigest(),
                           "official_full_run": split == "judge" and limit is None})
            return result
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--split", choices=("dev", "judge"), default="dev")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--images", action="store_true", help="Add optional board PNGs to the same pixel observations")
    parser.add_argument("--limit", type=int, help="Smoke test only; never an official full score")
    args = parser.parse_args()
    try:
        result = evaluate(args.policy.resolve(), args.split, args.images, args.limit)
    except CandidateError as error:
        result = {"status": "candidate_invalid", "score": None, "reason": str(error)}
    except Exception as error:
        result = {"status": "measurement_unavailable", "score": None, "reason": type(error).__name__ + ": " + str(error)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    return 0 if result["status"] == "scored" else 1


if __name__ == "__main__":
    raise SystemExit(main())
