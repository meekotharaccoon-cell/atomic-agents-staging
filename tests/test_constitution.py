import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from mycelium.constitution import RootSystem


def test_register_and_profit_distribution(tmp_path):
    root = RootSystem()

    # Register a new hypha with small capital
    resp = root.register_hypha("crypto_1", "crypto", 10)
    assert resp.get("approved") is True
    assert "crypto_1" in root.hyphae_registry

    # Record profit and ensure network capital increases by compounded amount
    before = root.network_capital
    result = root.record_profit("crypto_1", 100)
    assert result["compounded_back"] == 50.0
    assert root.network_capital == before + 50.0


def test_consecutive_losses_trigger_growth_halt():
    root = RootSystem()
    root.register_hypha("stock_1", "stock", 10)

    # Trigger losses
    for i in range(3):
        res = root.record_loss("stock_1", 1)

    assert res.get("growth_halt") is True
