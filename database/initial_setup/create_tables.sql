-- USERS table
CREATE TABLE dim.users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),
    gender VARCHAR(10)
);

-- SUPPLEMENTS table
CREATE TABLE dim.supplements (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplement_name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    pills_per_bottle INT CHECK (pills_per_bottle > 0)
);

-- DOSAGE DATA table
CREATE TABLE dim.dosage_data (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT REFERENCES dim.users(id),
    supplement_id INT REFERENCES dim.supplements(id),
    dosage_per_day NUMERIC(5,2) CHECK (dosage_per_day >= 0),
    reorder_threshold INT CHECK (reorder_threshold >= 0),
    UNIQUE(user_id, supplement_id)
);

-- MISSED DOSES table
CREATE TABLE fact.missed_doses (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT REFERENCES dim.users(id),
    supplement_id INT REFERENCES dim.supplements(id),
    date_missed DATE NOT NULL
);

CREATE INDEX idx_missed_doses_user_supp_date
    ON fact.missed_doses (user_id, supplement_id, date_missed);

-- INVENTORY table
CREATE TABLE fact.inventory (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT REFERENCES dim.users(id),
    supplement_id INT REFERENCES dim.supplements(id),
    qty_remaining INT CHECK (qty_remaining >= 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);  

CREATE TABLE fact.inventory_adjustments (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT REFERENCES dim.users(id),          -- Who made the adjustment
    supplement_id INT REFERENCES dim.supplements(id),-- Which supplement was adjusted
    change_amount INT NOT NULL,                      -- Positive for additions, negative for subtractions
    adjustment_type VARCHAR(50) NOT NULL,            -- e.g., 'purchase', 'loss', 'manual_adjustment'
    adjustment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the adjustment was made
    remarks TEXT                                     -- Optional: additional information about the adjustment
);