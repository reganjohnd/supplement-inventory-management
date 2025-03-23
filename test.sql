SELECT * FROM fact.inventory;

DELETE FROM fact.inventory
WHERE id > 14;

UPDATE fact.inventory
SET qty_remaining = 8
WHERE id = 14;