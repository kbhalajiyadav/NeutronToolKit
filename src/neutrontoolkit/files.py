"""Strict loading of reduced one-dimensional Q, I(Q), dI, optional dQ ASCII files."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import re
import numpy as np

EXTENSIONS = {".dat", ".txt", ".csv", ".iq"}

@dataclass(frozen=True)
class Curve:
    path: Path
    q: np.ndarray
    intensity: np.ndarray
    di: np.ndarray | None
    dq: np.ndarray | None

    def sha256(self):
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

def discover(folder):
    root = Path(folder).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Directory does not exist: {root}")
    return sorted((p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS),
                  key=lambda p: str(p).lower())

def load(path):
    path = Path(path).expanduser().resolve()
    if path.suffix.lower() not in EXTENSIONS:
        raise ValueError(f"Not reduced 1D ASCII: {path}")
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith(("#", "%", ";", "//")):
            continue
        fields = re.split(r"[,\s]+", line)
        try:
            values = [float(v) for v in fields]
        except ValueError:
            if rows:
                raise ValueError(f"{path}:{n}: invalid row inside data") from None
            continue
        if len(values) not in (2, 3, 4):
            raise ValueError(f"{path}:{n}: expected 2–4 numeric columns, found {len(values)}")
        if rows and len(values) != len(rows[0]):
            raise ValueError(f"{path}:{n}: inconsistent columns")
        rows.append(values)
    if not rows:
        raise ValueError(f"No numeric data in {path}")
    data = np.asarray(rows, dtype=float)
    if not np.all(np.isfinite(data)):
        raise ValueError("Nonfinite data")
    if np.any(data[:, 0] <= 0) or np.any(np.diff(data[:, 0]) <= 0):
        raise ValueError("Q must be positive and strictly increasing")
    di = data[:, 2] if data.shape[1] > 2 else None
    dq = data[:, 3] if data.shape[1] > 3 else None
    if di is not None and np.any(di <= 0):
        raise ValueError("dI must be positive")
    if dq is not None and np.any(dq < 0):
        raise ValueError("dQ must be nonnegative")
    return Curve(path, data[:, 0], data[:, 1], di, dq)

def quality(curve):
    return {
        "file": str(curve.path), "sha256": curve.sha256(), "points": len(curve.q),
        "q_min_A_inv": float(curve.q[0]), "q_max_A_inv": float(curve.q[-1]),
        "nonpositive_intensity": int(np.sum(curve.intensity <= 0)),
        "has_dI": curve.di is not None, "has_dQ": curve.dq is not None,
        "warning": "ASCII validation cannot establish reduction quality, absolute scale, or physical model",
    }
