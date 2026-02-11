from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from abc import ABC, abstractmethod
from functools import total_ordering

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
        # TODO: validate amount is Decimal, amount >= 0, unit lowercase and non-empty   
        if not isinstance(self.amount, Decimal):
            object.__setatt__(self, 'amount', Decimal(self.amount))

        if self.amount < 0:
            raise ValueError(f"Amount must be non-negative, {self.amount}")
        
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ValueError("Unit must be a non-empty string")
        
        object.__setattr__(self, 'unit', set.unit.lower().strip())

    def __repr__(self) -> str:
        return f"Amount(amount={self.amount!r}, unit={self.unit!r})"

    def __str__(self) -> str:
        return f"{self.unit} {self.amount}"

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
            raise ValueError("Cannot compare quantities with different units")
        return self.amount < other.amount
    
    def __add__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.unit != other.unit:
            raise ValueError("Cannot add unit values with different unit")
        return Quantity(self.amount + other.amount, self.unit)

    def __sub__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.unit != other.unit:
            raise ValueError("Cannot subtract unit values with different unit")
        return Quantity(self.amount - other.amount, self.unit)

    def is_zero(self) -> bool:
        return self.amount == Decimal("0")
    

class InventoryItem:
    def __init__(self, sku: str, on_hand: Quantity) -> None:
        self._validate(sku, on_hand)
        self.sku = sku
        self.on_hand = on_hand

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
        new_amount = self.on_hand.amount + qty.amount
        self.on_hand = Quantity(new_amount, self.on_hand.unit)

    def ship(self, qty: Quantity)-> None:
        self._check_unit(qty)
        if qty.amount > self.on_hand.amount:
            raise ValueError(f"Insufficient stock to ship {qty.amount}")
        new_amount = self.on_hand.amount - qty.amount
        self.on_hand = Quantity(new_amount, self.on_hand.unit)

    def adjust(self, qty: Quantity) -> None:
        self._check_unit(qty)
        self.on_hand = qty

    @property
    def available(self) -> bool:
        return self.on_hand.amount > 0
    
    def __repr__(self) -> str:
        return f"InventoryItem(sku='{self.sku}', on_hand={self.on_hand})"
    def __str__(self) -> str:
        return f"SKU {self.sku} {self.amount} count on hand"
    
    def __bool__(self) -> bool:
        return self.available