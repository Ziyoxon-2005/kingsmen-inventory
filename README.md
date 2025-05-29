# Kingsmen - Clothing Store Inventory Management System

A Django-based inventory management system specifically designed for clothing stores. This system helps manage products, track inventory, handle orders, and manage staff members.

## Features

- **Product Management**
  - Add, edit, and delete products
  - Track product inventory
  - Categorize products (Men, Women, Kids, Accessories)
  - Manage sizes (XS to XXL, plus Universal)
  - Track product colors and prices
  - Upload product images

- **Order Management**
  - Track orders with status (Pending, Delivered, Cancelled)
  - View order history
  - Monitor daily order statistics

- **Staff Management**
  - User authentication and authorization
  - Staff profiles with contact information
  - Role-based access control

- **Dashboard**
  - Daily statistics overview
  - Low stock alerts
  - Visual data representation
  - Quick access to all features

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd kingsmen-inventory
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Technologies Used

- Django 3.1.7
- Bootstrap 4.6
- Chart.js
- SQLite3
- Crispy Forms

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 