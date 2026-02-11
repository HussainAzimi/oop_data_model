import pytest
from decimal import Decimal
from src.models import InventoryItem, InsufficientInventoryError

class InsufficientInventoryError(Exception):
    """Raised when shipping more than is on hand."""
    pass