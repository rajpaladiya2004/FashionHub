# FashioHub - Django E-Commerce Platform

[![CI - Test and Lint](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/ci.yml/badge.svg)](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/ci.yml)
[![CodeQL](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/codeql.yml/badge.svg)](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/codeql.yml)
[![Security Scan](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/security.yml/badge.svg)](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/security.yml)

A modern e-commerce web application built with Django 5.2, featuring product management, shopping cart, wishlist, user authentication, and product reviews with admin approval.

## Features

- **Product Management**: Browse products with categories, ratings, and reviews
- **Shopping Cart**: Add/remove products, update quantities
- **Wishlist**: Save favorite products for later
- **User Authentication**: Register, login, profile management
- **Product Reviews**: User reviews with admin approval workflow
- **Admin Panel**: Full product, review, and content management
- **Responsive Design**: Modern UI with Bootstrap and custom styling
- **Pagination**: 16 products per page for optimal browsing

## Tech Stack

- Django 5.2
- Python 3.x
- SQLite (Development)
- Bootstrap 5
- FontAwesome Icons
- JavaScript (Vanilla)

## Documentation

- [Installation & Setup](#installation)
- [Contributing Guide](CONTRIBUTING.md)
- [GitHub Actions Setup](GITHUB_ACTIONS_GUIDE.md)
- [Render Deployment](RENDER_DEPLOYMENT_GUIDE.md)
- [Razorpay Setup](RAZORPAY_SETUP_GUIDE.md)
- [Category Management](CATEGORY_MANAGEMENT_GUIDE.md)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rajpaladiya2004/FashionHub.git
cd FashionHub
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django pillow
```

4. Run migrations:
```bash
python manage.py makemigrations
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

7. Access the application:
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Project Structure

```
FashioHub/
├── FashioHub/          # Project settings
├── Hub/                # Main app
│   ├── models.py       # Database models
│   ├── views.py        # View functions
│   ├── urls.py         # URL routing
│   ├── admin.py        # Admin configuration
│   ├── templates/      # HTML templates
│   └── static/         # CSS, JS, images
├── media/              # User uploads
└── manage.py           # Django management script
```

## Key Models

- **Product**: Product information with pricing, inventory, categories
- **ProductReview**: User reviews with admin approval
- **Cart**: Shopping cart items
- **Wishlist**: Saved products
- **UserProfile**: Extended user information

## Usage

### For Users:
- Browse products on the shop page
- Add products to cart or wishlist
- Submit reviews (requires login and admin approval)
- Manage profile and orders

### For Admins:
- Manage products, categories, and inventory
- Approve/reject user reviews
- Monitor sales and user activity
- Configure site content (sliders, banners, features)

## CI/CD & Automation

This project uses GitHub Actions for continuous integration and deployment:

- **CI Pipeline**: Automated testing and linting on every push and PR
- **CodeQL Analysis**: Security vulnerability scanning and code quality checks
- **Security Scanning**: Regular dependency and security audits
- **Auto Deployment**: Automatic deployment to Render on main branch updates
- **Issue Management**: Automated greeting and labeling for new issues
- **Stale Management**: Automatic cleanup of inactive issues and PRs

### Workflows

- `ci.yml` - Runs tests, linting, and Django checks
- `codeql.yml` - Security and code quality analysis
- `security.yml` - Dependency vulnerability scanning
- `deploy.yml` - Automated deployment to Render
- `handle-new-issue.yml` - Greets new issue creators
- `pr-labels.yml` - Auto-labels PRs by size and greets first-time contributors
- `stale.yml` - Manages stale issues and PRs

## License

This project is open-source and available for educational purposes.

## Author

Raj Paladiya - [GitHub](https://github.com/rajpaladiya2004)
