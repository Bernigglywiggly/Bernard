"""Preview only: chapters 0-2 of ch2/ep06, so the first takes can be laid out before the rest are voiced."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("ep06_script", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ep06", "script.py"))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
LINES = [ln for ln in _m.LINES if ln["floor"] <= 2]
FLOORS = _m.FLOORS[:3]
SOURCES = _m.SOURCES
