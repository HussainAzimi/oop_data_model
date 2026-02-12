## Python Data Model Short Design Reflection.

• Why Quantity is immutable and hashable (or why you chose not to hash it)?
• Why InventoryItem is mutable and not hashable?
• Your unit mismatch strategy (raise vs return NotImplemented vs other)?
• One design choice you considered and rejected?

The Quantity is immutable and hashable because it represents a vlue object (5 , kg) and shouldn't change. it makes the code safer and allows quantity to serve as reliable dictionary keys.
The InventoryItem is an entity. it has a unique indentity (sku) that persists even its state (on_hand) changes over time via shipments.it is inherently unsuitable for hashing by default (as its hash value would change if the state changed), so __hash__ is explicitly set to None to prevent it from being used in hashed collections where it might become 'lost' after a state update.
For unit mismatches, I chose to raise a ValueError for arithmetic and comparisons. While NotImplemented is appropriate for type mismatches, a unit mismatch between two Quantity objects is a logical domain error that should fail loudly and early.
I considered allowing unary negation (e.g., -Quantity) but rejected it. Our business rules strictly forbid negative inventory; keeping the class restricted to non-negative values ensures the domain model maintains its integrity by default.