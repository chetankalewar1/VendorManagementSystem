# Vendor Management System

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [APIs](#apis)

## Overview
This system handles vendor profiles, track purchase orders, and calculate vendor performance
metrics.

## Features

List the key features of your Django project:

- Vendor Profile Management
- Purchase Order Tracking
- Vendor Performance Evaluation:

## Installation

Provide instructions on how to install your Django project. Include any dependencies and specific versions if necessary. You can also include code snippets for commands.

-   **Libraries used:**
    1.  Django
    2.  DRF
    3. OpenApi / **`drf-yasg`**
    

-   **Install Dependencies**
    
    1.  IDE Pycharm
    2.  Run ‘`pip install -r requirements.txt’` to install the remaining necessary packages.
    
  
## Usage

-   **Run Migrations**
	1. `python manage.py makemigrations`
	2. `python manage.py migrate`


-   **Start Server**
	1. `python manage.py runserver`


-   **Create Dummy/Test Data**
	1. `python manage.py shell`
	2. `from vms.ots import create_dummy_po`
	3. `create_dummy_po()`


## APIs
For Api Documentation please refer : "http://localhost:8000/swagger/" or "http://localhost:8000/redoc/"

