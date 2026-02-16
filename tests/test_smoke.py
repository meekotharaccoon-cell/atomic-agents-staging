import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.main import GumroadManual
from core.safety import SystemSafety


def test_gumroad_generate_product():
    g = GumroadManual().generate_product("freelance client tracker")
    assert "name" in g and "description" in g and "price" in g


def test_system_safety_blocks_credentials():
    safety = SystemSafety()
    res = safety.check("password=supersecret", "input")
    assert res["allowed"] is False
