# Supplement Inventory Management & Alert System

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)


## Project Overview

This personal project was created to help me track my supplement inventory and ensure I never run out of my daily tablets. It helps prevent gaps in my supplement routine by monitoring dosages and remaining quantities, and prompting me via email to replenish the inventory before I run out.

While I have more experience working architecting OLAP (Online Analytical Processing) database designs, I recognised that an OLTP (Online Transaction Processing) framework would be more suitable for this project, as it's primarily handling individual transactions and almost real-time updates of supplement quantities.

## Features

- Automated alerts for low stock or missed dosages
- Scalable architecture using dimensional modeling
- Highly normalised database design to ensure data integrity and reduce redundancy