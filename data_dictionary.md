# Data Dictionary

This document describes the structure and details of the database tables used in the project.

## Table: dim.users

| Field  | Data Type      | Description                         | Constraints                      |
|--------|----------------|-------------------------------------|----------------------------------|
| id     | INT            | Unique identifier for the user      | Primary Key, Auto-increment      |
| name   | VARCHAR(100)   | Name of the user                    | Not Null                         |
| age    | INT            | Age of the user                     | CHECK (age >= 0)                 |
| gender | VARCHAR(10)    | Gender of the user                  |                                  |

## Table: dim.supplements

| Field           | Data Type      | Description                               | Constraints                      |
|-----------------|----------------|-------------------------------------------|----------------------------------|
| id              | INT            | Unique identifier for the supplement      | Primary Key, Auto-increment      |
| supplement_name | VARCHAR(100)   | Name of the supplement                    | Not Null                         |
| manufacturer    | VARCHAR(100)   | Manufacturer of the supplement            |                                  |
| pills_per_bottle| INT            | Number of pills per bottle                | CHECK (pills_per_bottle > 0)     |

## Table: dim.dosage_data

| Field             | Data Type       | Description                                   | Constraints                                   |
|-------------------|-----------------|-----------------------------------------------|-----------------------------------------------|
| id                | INT             | Unique identifier for the dosage record       | Primary Key, Auto-increment                   |
| user_id           | INT             | Foreign key to the users table                | REFERENCES dim.users(id)                      |
| supplement_id     | INT             | Foreign key to the supplements table          | REFERENCES dim.supplements(id)                |
| dosage_per_day    | NUMERIC(5,2)    | Daily dosage amount                           | CHECK (dosage_per_day >= 0)                     |
| reorder_threshold | INT             | Threshold for reorder alert                   | CHECK (reorder_threshold >= 0)                  |
|                   |                 |                                               | UNIQUE(user_id, supplement_id)                |

## Table: fact.missed_doses

| Field         | Data Type | Description                                  | Constraints                          |
|---------------|-----------|----------------------------------------------|--------------------------------------|
| id            | INT       | Unique identifier for the missed dose record  | Primary Key, Auto-increment          |
| user_id       | INT       | Foreign key to the users table               | REFERENCES dim.users(id)             |
| supplement_id | INT       | Foreign key to the supplements table         | REFERENCES dim.supplements(id)       |
| date_missed   | DATE      | Date when the dose was missed                | Not Null                             |

## Table: fact.inventory

| Field         | Data Type  | Description                                      | Constraints                                  |
|---------------|------------|--------------------------------------------------|----------------------------------------------|
| id            | INT        | Unique identifier for the inventory record       | Primary Key, Auto-increment                  |
| user_id       | INT        | Foreign key to the users table                   | REFERENCES dim.users(id)                     |
| supplement_id | INT        | Foreign key to the supplements table             | REFERENCES dim.supplements(id)               |
| qty_remaining | INT        | Remaining quantity in the inventory              | CHECK (qty_remaining >= 0)                   |
| last_updated  | TIMESTAMP  | Timestamp for the last inventory update          | DEFAULT CURRENT_TIMESTAMP                    |

## Additional Notes
The ERD can be viewed [here](database/supp_inv_db_ERD.pdf)

Include any additional information or clarifications regarding the data model, such as relationship diagrams or business rules.