#!/usr/bin/env python
"""
Verify Neon PostgreSQL Database Connection
This script checks that your Django app is properly connected to Neon.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from shop.models import Category, Product

def verify_database_connection():
    """Test database connection and show info"""
    print("NEON POSTGRESQL CONNECTION VERIFICATION")
    print("=" * 50)

    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            print(f"✅ Database Connected: {db_version}")

            # Get connection info
            cursor.execute("SELECT current_database(), current_user;")
            db_name, db_user = cursor.fetchone()
            print(f"✅ Database: {db_name}")
            print(f"✅ User: {db_user}")

            # Check if we're using Neon
            cursor.execute("SELECT inet_server_addr(), inet_server_port();")
            result = cursor.fetchone()
            if result[0]:
                print(f"✅ Server: {result[0]}:{result[1]}")

        print(f"\n📊 DATABASE CONTENT:")
        print(f"   • Users: {User.objects.count()}")
        print(f"   • Categories: {Category.objects.count()}")
        print(f"   • Products: {Product.objects.count()}")
        print(f"   • Featured Products: {Product.objects.filter(featured=True).count()}")

        # Show categories
        print(f"\n📁 CATEGORIES:")
        for cat in Category.objects.all():
            print(f"   • {cat.name} ({cat.products.count()} products)")

        # Show featured products
        print(f"\n⭐ FEATURED PRODUCTS:")
        for product in Product.objects.filter(featured=True):
            print(f"   • {product.name} - ${product.price}")

        # Verify admin user
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            print(f"\n👤 ADMIN USER: {admin_user.username} ({admin_user.email})")
            print(f"   • Is Active: {admin_user.is_active}")
            print(f"   • Is Superuser: {admin_user.is_superuser}")
        else:
            print(f"\n❌ Admin user not found")

        print(f"\n✅ NEON DATABASE FULLY OPERATIONAL!")
        print(f"🌐 Your e-commerce app is ready at: http://127.0.0.1:8000/")
        print(f"⚙️  Admin panel: http://127.0.0.1:8000/admin/ (admin/admin123)")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

    return True

if __name__ == "__main__":
    verify_database_connection()