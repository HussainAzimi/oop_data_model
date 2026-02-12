## Design and implement a small set of domain objects that are Pythonic, semantically defensible,  and safe to use in collections.

 ## Learning Objectives
- Implement special methods to integrate custom objects into Python’s data model.
- Design meaningful __repr__ and __str__ for different audiences.
- mplement equality, ordering, and hashing correctly—especially under mutability
  constraints.
- ustify immutability and hashability decisions for value objects.
- Apply operator overloading responsibly and defensively.
- Use an abstract base class to enforce behavioral contracts.

## Problem Domain: Inventory Pricing & Adjustments

### Implementation Details:

### Abstract class Measurable:
This class defines the **behavior** expected of measurable values.

### Immutable Value Object-(Quantity):
It represents an amount of something in a unit (e.g., 3.5 kg, 12 count, 2.0 L).

### Mutable Aggregate-(InventoryItem):
It models an item in inventory with a SKU and an on-hand quantity.

### Unit Tests:

```
pytest -q tests/test_inventory_item.py
pytest -q tests/test_quantity.py

```

