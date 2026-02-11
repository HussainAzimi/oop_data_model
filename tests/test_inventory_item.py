import pytest
from decimal import Decimal
from src.models import Quantity, InventoryItem, InsufficientInventoryError

def sample_item():
    return InventoryItem("WIDGET-101", Quantity(Decimal("50"), "count"))

def test_on_hand_type_validation():
    with pytest.raises(TypeError):
        InventoryItem("SKU-1", "10 units")
