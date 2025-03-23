INSERT INTO dim.supplements (supplement_name, manufacturer, pills_per_bottle)
VALUES
    ('Beta Alanine', 'Biogen', 60),
    ('Cod Liver Oil', 'Clicks', 90),
    ('Creatine Monohydrate', 'Machito', 60),
    ('Zinc', 'VitaTech', 30),
    ('Omega 3', 'Wellvita', 120),
    ('Multi Vitamin & Minerals', 'USN', 60),
    ('Magnesium Glycinate', 'Neuro Active', 60);

INSERT INTO dim.users (name, age, gender)
VALUES ('Regan-John Daniels', 28, 'Male');

INSERT INTO dim.dosage_data (user_id, supplement_id, dosage_per_day, reorder_threshold)
VALUES
    (1, 1, 2, 7),
    (1, 2, 2, 7),
    (1, 3, 2, 7),
    (1, 4, 1, 7),
    (1, 5, 1, 7),
    (1, 6, 1, 7),
    (1, 7, 1, 7);

INSERT INTO fact.inventory (user_id, supplement_id, qty_remaining, last_updated)
VALUES
    (1, 1, 60, '2025-03-20'),
    (1, 2, 90, '2025-03-20'),
    (1, 3, 60, '2025-03-20'),
    (1, 4, 30, '2025-03-20'),
    (1, 5, 120, '2025-03-20'),
    (1, 6, 60, '2025-03-20'),
    (1, 7, 60, '2025-03-20');