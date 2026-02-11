from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Union

class InsufficientInventoryError(Exception):
   """Raised when attempting to ship/adjust below zero."""
   pass

class Measurable(ABC):
    """
    Abstract base class defining the behavior expected
    of Measurable-like value objects.
    """

    @abstractmethod
    def __add__(self, other: object):
        pass

    @abstractmethod
    def __sub__(self, other: object):
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    def is_zero(self) -> bool:
        """
        Default implementation.
        Subclasses may override if necessary.
        """
        return False


@total_ordering
@dataclass(frozen=True)
class Quantity(Measurable):
    amount: Decimal
    unit: str
    def __post_init__(self) -> None:
          
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))

        if self.amount < 0:
            raise ValueError(f"Amount must be non-negative, {self.amount}")
        
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ValueError("Unit must be a non-empty string")
        
        object.__setattr__(self, 'unit', self.unit.lower().strip())

    def __repr__(self) -> str:
        return f"Quantity(amount={self.amount!r}, unit={self.unit!r})"

    def __str__(self) -> str:
        return f"{self.amount} {self.unit}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.amount == other.amount and self.unit == other.unit

    def __hash__(self) -> int:
        return hash((self.amount, self.unit))
    
    def __lt__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.unit != other.unit:
            raise ValueError(f"Cannot compare units {self.unit} and {other.unit}")
        return self.amount < other.amount
    
    def __add__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.unit != other.unit:
            raise ValueError("Cannot add quantities with different units")
        return Quantity(self.amount + other.amount, self.unit)

    def __sub__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.unit != other.unit:
            raise ValueError("Cannot subtract quantities with different units")
        return Quantity(self.amount - other.amount, self.unit)
    
    def __mul__(self, other: Union[int, Decimal]):
        if not isinstance(other, (int, Decimal)):
            return NotImplemented
        return Quantity(self.amount * Decimal(str(other)), self.unit)
    
    def __rmul__(self, other: Union[int, Decimal]):
        return self.__mul__(other)

    def is_zero(self) -> bool:
        return self.amount == Decimal("0")
    

class InventoryItem:
    def __init__(self, sku: str, on_hand: Quantity) -> None:
        self._validate(sku, on_hand)
        self.sku = sku
        self.on_hand = on_hand
        
    # Explicitly make the class unhashable
    __hash__ = None

    def _validate(self, sku: str, on_hand: Quantity) -> None:
        if not isinstance(sku, str):
            raise ValueError(f"SKU must be a string, {type(sku).__name__}")
        
        if not isinstance(on_hand, Quantity):
            raise TypeError(
                f"on_hand must be a Quantity instance, {type(on_hand).__name__}"
            )

    def _check_unit(self, qty: Quantity):
        if qty.unit != self.on_hand.unit:
            raise ValueError(f"Unit mismatch: cannot operate {qty.unit} on {self.on_hand.unit}")
           
    def receive(self, qty: Quantity)-> None:
        self._check_unit(qty)

        self.on_hand += qty

    def ship(self, qty: Quantity)-> None:
        self._check_unit(qty)
        if qty.amount > self.on_hand.amount:
            raise InsufficientInventoryError(
                f"Cannot ship {qty.amount}, only {self.on_hand.amount} available."
            )      
        self.on_hand -= qty

    def adjust(self, qty: Quantity) -> None:
        self._check_unit(qty)
        self.on_hand = qty

    def available(self) -> Quantity:
        return self.on_hand
    
    def __repr__(self) -> str:
        return f"InventoryItem(sku='{self.sku!r}', on_hand={self.on_hand!r})"

    def __str__(self) -> str:
        return f"SKU {self.sku} {self.on_hand.amount} {self.on_hand.unit} on hand"
    
    def __bool__(self) -> bool:
        return self.on_hand.amount > 0