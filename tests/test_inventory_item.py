import pytest
from decimal import Decimal
from src.models import Quantity, InventoryItem, InsufficientInventoryError

@pytest.fixture
def sample_item():
    return InventoryItem("WIDGET-101", Quantity(Decimal("50"), "count"))

def test_on_hand_type_validation():
    with pytest.raises(TypeError):
        InventoryItem("SKU-1", "10 units")

def test_receive_stock(sample_item):
    add_qty = Quantity(Decimal("25"), "count")
    sample_item.receive(add_qty)
    assert sample_item.on_hand.amount == Decimal("75")

def test_ship_stock_success(sample_item):
    ship_qty = Quantity(Decimal("20"), "count")
    sample_item.ship(ship_qty)
    assert sample_item.on_hand.amount == Decimal("30")

def test_unit_mismatch(sample_item):
    wrong_unit = Quantity(Decimal("10"), "kg")
    with pytest.raises(ValueError, match="Unit mismatch"):
        sample_item.receive(wrong_unit)

def test_inventory_item_unhashable(sample_item):
    with pytest.raises(TypeError, match="unhashable type"):
        hash(sample_item)