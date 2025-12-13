from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Setup admin user and populate database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up demo data...')

        # Create or update admin user
        admin_username = 'admin'
        admin_password = 'admin123'
        admin_email = 'admin@ecommerce.com'

        try:
            admin = User.objects.get(username=admin_username)
            admin.set_password(admin_password)
            admin.is_staff = True
            admin.is_superuser = True
            admin.email = admin_email
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Updated admin user: {admin_username}'))
        except User.DoesNotExist:
            admin = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_username}'))

        self.stdout.write(f'Admin credentials: username={admin_username}, password={admin_password}')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Electronic devices and accessories'},
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'slug': 'books', 'description': 'Books and publications'},
            {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Home and garden products'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and accessories'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            categories[cat_data['slug']] = category
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'{status} category: {category.name}')

        # Create products
        products_data = [
            # Electronics
            {
                'category': 'electronics',
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'description': 'High-quality wireless headphones with noise cancellation',
                'price': Decimal('79.99'),
                'stock': 50,
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
                'featured': True
            },
            {
                'category': 'electronics',
                'name': 'Smart Watch',
                'slug': 'smart-watch',
                'description': 'Fitness tracking smartwatch with heart rate monitor',
                'price': Decimal('199.99'),
                'stock': 30,
                'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500',
                'featured': True
            },
            {
                'category': 'electronics',
                'name': 'Laptop Stand',
                'slug': 'laptop-stand',
                'description': 'Ergonomic aluminum laptop stand',
                'price': Decimal('29.99'),
                'stock': 100,
                'image': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500',
                'featured': False
            },
            # Clothing
            {
                'category': 'clothing',
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-tshirt',
                'description': 'Comfortable 100% cotton t-shirt',
                'price': Decimal('19.99'),
                'stock': 200,
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500',
                'featured': False
            },
            {
                'category': 'clothing',
                'name': 'Denim Jeans',
                'slug': 'denim-jeans',
                'description': 'Classic blue denim jeans',
                'price': Decimal('49.99'),
                'stock': 150,
                'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500',
                'featured': True
            },
            {
                'category': 'clothing',
                'name': 'Hoodie',
                'slug': 'hoodie',
                'description': 'Warm and comfortable hoodie',
                'price': Decimal('39.99'),
                'stock': 80,
                'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500',
                'featured': False
            },
            # Books
            {
                'category': 'books',
                'name': 'Python Programming Guide',
                'slug': 'python-programming',
                'description': 'Complete guide to Python programming',
                'price': Decimal('34.99'),
                'stock': 60,
                'image': 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500',
                'featured': True
            },
            {
                'category': 'books',
                'name': 'Web Development Handbook',
                'slug': 'web-dev-handbook',
                'description': 'Modern web development techniques',
                'price': Decimal('29.99'),
                'stock': 45,
                'image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=500',
                'featured': False
            },
            # Home & Garden
            {
                'category': 'home-garden',
                'name': 'Indoor Plant Pot',
                'slug': 'indoor-plant-pot',
                'description': 'Ceramic pot for indoor plants',
                'price': Decimal('15.99'),
                'stock': 120,
                'image': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=500',
                'featured': False
            },
            {
                'category': 'home-garden',
                'name': 'LED Desk Lamp',
                'slug': 'led-desk-lamp',
                'description': 'Adjustable LED desk lamp',
                'price': Decimal('24.99'),
                'stock': 90,
                'image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500',
                'featured': True
            },
            # Sports
            {
                'category': 'sports',
                'name': 'Yoga Mat',
                'slug': 'yoga-mat',
                'description': 'Non-slip yoga mat with carrying strap',
                'price': Decimal('25.99'),
                'stock': 75,
                'image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500',
                'featured': False
            },
            {
                'category': 'sports',
                'name': 'Running Shoes',
                'slug': 'running-shoes',
                'description': 'Lightweight running shoes',
                'price': Decimal('89.99'),
                'stock': 65,
                'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500',
                'featured': True
            },
        ]

        for product_data in products_data:
            category_slug = product_data.pop('category')
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': categories[category_slug]
                }
            )
            if not created:
                # Update existing product
                for key, value in product_data.items():
                    setattr(product, key, value)
                product.category = categories[category_slug]
                product.save()

            status = 'Created' if created else 'Updated'
            self.stdout.write(f'{status} product: {product.name}')

        self.stdout.write(self.style.SUCCESS('\nDemo data setup complete!'))
        self.stdout.write(self.style.SUCCESS(f'\nAdmin Login:'))
        self.stdout.write(self.style.SUCCESS(f'  Username: {admin_username}'))
        self.stdout.write(self.style.SUCCESS(f'  Password: {admin_password}'))
        self.stdout.write(self.style.SUCCESS(f'  Admin URL: http://localhost:8000/admin/'))
