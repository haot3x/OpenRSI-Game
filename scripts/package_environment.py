"""Create a deterministic, auditable build context for the RSI task environment."""
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package():
    # These trusted evaluator copies are injected only into Judge at /tests.
    judge_package = ROOT / "tests/gamebench"
    judge_package.mkdir(exist_ok=True)
    for source in (ROOT / "gamebench").glob("*.py"):
        (judge_package / source.name).write_bytes(source.read_bytes())
    (ROOT / "tests/assets-manifest.json").write_bytes((ROOT / "assets/manifest.json").read_bytes())
    paths = []
    for directory in ("assets", "gamebench", "reference", "docs", "reports"):
        paths += [p for p in (ROOT / directory).rglob("*") if p.is_file() and
                  "__pycache__" not in p.parts and p.suffix != ".pyc"]
    paths += [ROOT / name for name in ("instruction.md", "README.md", "task.toml", "LICENSE", "NOTICE")]
    manifest = []
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for path in sorted(paths):
            name = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = len(data), 0o644, 0
            archive.addfile(info, io.BytesIO(data))
            manifest.append({"path": name, "sha256": hashlib.sha256(data).hexdigest()})
        data = (ROOT / "reference/policy.py").read_bytes()
        info = tarfile.TarInfo("candidate/policy.py")
        info.size, info.mode, info.mtime = len(data), 0o644, 0
        archive.addfile(info, io.BytesIO(data))
    target = ROOT / "environment/task-source.tar.gz"
    with target.open("wb") as output:
        with gzip.GzipFile(filename="", fileobj=output, mode="wb", mtime=0) as compressed:
            compressed.write(raw.getvalue())
    (ROOT / "environment/source-manifest.json").write_text(json.dumps({
        "archive_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "files": manifest, "candidate": "Exact copy of reference/policy.py"}, indent=2) + "\n")


if __name__ == "__main__":
    package()
