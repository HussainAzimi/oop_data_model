import pytest
from decimal import Decimal
from src.models import Quantity, InventoryItem, InsufficientInventoryError

class InsufficientInventoryError(Exception):
    """Raised when shipping more than is on hand."""
    pass

def test_repr_and_str():
    q = Quantity(Decimal("10.5"), "kg")
    assert repr(q) == "Quantity(amount=Decimal('10.5'), unit='kg')"
    assert str(q) == "10.5 kg"


def test_equality_and_hashing():
    q1 = Quantity(Decimal("5"), "count")
    q2 = Quantity(Decimal("5"), "count")
    q3 = Quantity(Decimal("10"), "count")

    assert q1 == q2
    assert hash(q1) == hash(q2)
    assert q1 != q3
    assert hash(q1) != hash(q3)

def unit_mismatch():
    kg = Quantity(Decimal("10"), "kg")
    lbs = Quantity(Decimal("10"), "lbs")
    
    with pytest.raises(ValueError, match="different units"):
        _ = kg + lbs
    with pytest.raises(ValueError, match="different units"):
        _ = kg - lbs
    with pytest.raises(ValueError, match="Cannot compare units"):
        _ = kg < lbs

def unsupported_types():
    q = Quantity(Decimal("10"), "kg")

    with pytest.raises(TypeError):
        _ = q + 5
    with pytest.raises(TypeError):
        _ = q == "10 kg"

def scalar_multiplication():
    q = Quantity(Decimal("5"), "l")
    result = q * 3
    assert result.amount == Decimal("15")
    assert result.unit == "l"
    assert isinstance(3 * q, Quantity)