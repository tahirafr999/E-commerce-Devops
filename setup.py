#!/usr/bin/env python
"""
Complete Setup Script for E-Commerce Django Application
This script will install all dependencies and set up the application ready to use.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description=""):
    """Run shell command and handle errors"""
    print(f"\n=> {description}")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print("SUCCESS:", result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def install_dependencies():
    """Install required Python packages"""
    packages = [
        "Django==5.0.0",
        "python-dotenv==1.0.0",
        "dj-database-url==2.1.0",
        "django-environ==0.11.2"
    ]

    print("\n[INSTALLING DEPENDENCIES]")

    for package in packages:
        success = run_command(f"python -m pip install {package}", f"Installing {package}")
        if not success:
            print(f"WARNING: Failed to install {package}, continuing...")

    # Try to install Pillow (for image handling)
    print("\n[INSTALLING IMAGE SUPPORT]")
    pillow_success = run_command("python -m pip install Pillow", "Installing Pillow")
    if not pillow_success:
        print("WARNING: Pillow installation failed. Using CharField for images instead.")
        return False
    return True

def setup_database():
    """Set up the database and run migrations"""
    print("\n[SETTING UP DATABASE]")

    # Make migrations
    success = run_command("python manage.py makemigrations", "Creating migrations")
    if not success:
        return False

    # Apply migrations
    success = run_command("python manage.py migrate", "Applying migrations")
    if not success:
        return False

    return True

def create_superuser():
    """Create a superuser account"""
    print("\n[CREATING ADMIN USER]")

    # Set environment variables for non-interactive superuser creation
    env = os.environ.copy()
    env['DJANGO_SUPERUSER_USERNAME'] = 'admin'
    env['DJANGO_SUPERUSER_EMAIL'] = 'admin@example.com'
    env['DJANGO_SUPERUSER_PASSWORD'] = 'admin123'

    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'createsuperuser', '--noinput'
        ], env=env, capture_output=True, text=True)

        if result.returncode == 0:
            print("SUCCESS: Superuser created!")
            print("Admin credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@example.com")
            return True
        else:
            print("WARNING: Superuser creation failed or user already exists")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def populate_sample_data():
    """Add sample data to the database"""
    print("\n[ADDING SAMPLE DATA]")

    # Django setup
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    django.setup()

    from shop.models import Category, Product

    try:
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Latest gadgets and electronic devices'},
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel for all ages'},
            {'name': 'Books', 'slug': 'books', 'description': 'Educational and entertainment books'},
            {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Everything for your home and garden'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and accessories'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                print(f"Created category: {category.name}")

        # Create products
        products_data = [
            {
                'name': 'Smartphone Pro Max',
                'slug': 'smartphone-pro-max',
                'category': 'electronics',
                'description': 'Latest smartphone with advanced features, high-resolution camera, and long battery life.',
                'price': 999.99,
                'stock': 50,
                'featured': True
            },
            {
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'category': 'electronics',
                'description': 'Premium wireless headphones with noise cancellation and superior sound quality.',
                'price': 199.99,
                'stock': 30,
                'featured': True
            },
            {
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-t-shirt',
                'category': 'clothing',
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors and sizes.',
                'price': 29.99,
                'stock': 100,
                'featured': False
            },
            {
                'name': 'Python Programming Guide',
                'slug': 'python-programming-guide',
                'category': 'books',
                'description': 'Comprehensive guide to Python programming for beginners and advanced users.',
                'price': 49.99,
                'stock': 25,
                'featured': True
            },
            {
                'name': 'Coffee Maker Deluxe',
                'slug': 'coffee-maker-deluxe',
                'category': 'home-garden',
                'description': 'Premium coffee maker with programmable settings and thermal carafe.',
                'price': 149.99,
                'stock': 20,
                'featured': False
            },
            {
                'name': 'Yoga Mat Pro',
                'slug': 'yoga-mat-pro',
                'category': 'sports',
                'description': 'Professional yoga mat with superior grip and cushioning for all yoga styles.',
                'price': 79.99,
                'stock': 40,
                'featured': True
            }
        ]

        for prod_data in products_data:
            category = Category.objects.get(slug=prod_data['category'])
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    'name': prod_data['name'],
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'featured': prod_data['featured'],
                    'available': True
                }
            )
            if created:
                print(f"Created product: {product.name}")

        print(f"\nDatabase populated with:")
        print(f"   - {Category.objects.count()} categories")
        print(f"   - {Product.objects.count()} products")
        print(f"   - {Product.objects.filter(featured=True).count()} featured products")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

def create_static_directory():
    """Create static files directory"""
    static_dir = Path("static")
    if not static_dir.exists():
        static_dir.mkdir()
        print("Created static directory")

    # Create JS file directory
    js_dir = Path("shop/static/shop/js")
    js_dir.mkdir(parents=True, exist_ok=True)
    print("Created JavaScript directory")

def main():
    """Main setup function"""
    print("STARTING E-COMMERCE APPLICATION SETUP")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("ERROR: manage.py not found. Please run this script from the project directory.")
        sys.exit(1)

    # Create necessary directories
    create_static_directory()

    # Install dependencies
    pillow_installed = install_dependencies()

    # Setup database
    if not setup_database():
        print("ERROR: Database setup failed!")
        sys.exit(1)

    # Create superuser
    create_superuser()

    # Populate with sample data
    if not populate_sample_data():
        print("WARNING: Sample data population failed, but continuing...")

    # Final success message
    print("\n" + "=" * 50)
    print("SETUP COMPLETE!")
    print("=" * 50)
    print("\nYour E-Commerce Application is Ready!")
    print("\nQuick Start:")
    print("   1. Run: python manage.py runserver")
    print("   2. Visit: http://127.0.0.1:8000/")
    print("   3. Admin: http://127.0.0.1:8000/admin/")
    print("\nAdmin Login:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\nProject includes:")
    print("   - Product catalog with categories")
    print("   - Shopping cart functionality")
    print("   - User authentication")
    print("   - Order management")
    print("   - Responsive design with Tailwind CSS")
    print("   - Sample products and categories")

    if not pillow_installed:
        print("\nNote: Pillow not installed - images will use URL fields instead")

    print("\nTo connect Neon PostgreSQL:")
    print("   1. Update DATABASE_URL in .env file")
    print("   2. Install: pip install psycopg2-binary")
    print("   3. Run: python manage.py migrate")

    print("\nEnjoy your new e-commerce store!")

if __name__ == "__main__":
    main()