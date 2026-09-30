"""Shared paths and presentation settings; no network or private machine paths."""
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt

# The project can live anywhere, including inside a larger portfolio repository.
ROOT = Path(__file__).resolve().parent
# Optional overrides are resolved before any output is created.
DATA_DIR = Path(os.environ.get("KLEAGUE_DATA_DIR", ROOT / "data/raw")).resolve()
OUTPUT_DIR = Path(os.environ.get("KLEAGUE_OUTPUT_DIR", ROOT / "outputs")).resolve()
FOCUS_TEAMS = ["Anyang", "Daejeon", "Jeju"]
# Korean strings are source identifiers, not untranslated user-facing labels.
TEAM_NAMES = {"강원":"Gangwon", "광주":"Gwangju", "김천":"Gimcheon", "대전":"Daejeon",
              "부천":"Bucheon", "서울":"Seoul", "안양":"Anyang", "울산":"Ulsan",
              "인천":"Incheon", "전북":"Jeonbuk", "제주":"Jeju", "포항":"Pohang"}
COLORS = {"Anyang":"#4F1B87", "Daejeon":"#008578", "Jeju":"#F36C21"}
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
                     "axes.spines.top":False, "axes.spines.right":False,
                     "figure.facecolor":"white", "axes.facecolor":"white"})

def read_stage(stage, filename):
    """Read an explicit prerequisite; never silently use stale Desktop outputs."""
    path = OUTPUT_DIR / stage / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing {stage}/{filename}. Run the earlier stages first.")
    return pd.read_csv(path)

def save_chart(fig, path):
    """Save a portable PNG and retain a visible plot in executed notebooks."""
    from IPython import get_ipython
    from IPython.display import display
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    if get_ipython() is not None:
        display(fig)
    plt.close(fig)
