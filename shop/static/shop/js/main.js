// Main JavaScript for E-Commerce Store

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initializeTabs();
    initializeCartUpdates();
    initializeFormValidation();
    initializeImageZoom();
    initializeNotifications();
    initializeMobileMenu();
});

// Mobile menu functionality
function initializeMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isMenuOpen = !mobileMenu.classList.contains('hidden');

            if (isMenuOpen) {
                // Close menu
                mobileMenu.classList.add('hidden');
                menuIcon.classList.remove('hidden');
                closeIcon.classList.add('hidden');
            } else {
                // Open menu
                mobileMenu.classList.remove('hidden');
                menuIcon.classList.add('hidden');
                closeIcon.classList.remove('hidden');
            }
        });

        // Close mobile menu when clicking on a link
        const mobileMenuLinks = mobileMenu.querySelectorAll('a');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
                menuIcon.classList.remove('hidden');
                closeIcon.classList.add('hidden');
            });
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenuButton.contains(event.target) && !mobileMenu.contains(event.target)) {
                mobileMenu.classList.add('hidden');
                menuIcon.classList.remove('hidden');
                closeIcon.classList.add('hidden');
            }
        });

        // Close mobile menu on window resize (for responsive behavior)
        window.addEventListener('resize', function() {
            if (window.innerWidth >= 768) { // md breakpoint
                mobileMenu.classList.add('hidden');
                menuIcon.classList.remove('hidden');
                closeIcon.classList.add('hidden');
            }
        });
    }
}

// Tab functionality for product detail page
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.id.replace('-tab', '-content');

            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => {
                btn.classList.remove('active', 'border-primary', 'text-primary');
                btn.classList.add('border-transparent', 'text-gray-500');
            });

            tabContents.forEach(content => {
                content.classList.add('hidden');
            });

            // Add active class to clicked button and show target content
            this.classList.add('active', 'border-primary', 'text-primary');
            this.classList.remove('border-transparent', 'text-gray-500');

            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.remove('hidden');
            }
        });
    });
}

// Cart quantity updates
function initializeCartUpdates() {
    // Add loading state to cart update forms
    const cartForms = document.querySelectorAll('form[action*="cart_add"]');

    cartForms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.textContent;
                submitButton.textContent = 'Adding...';
                submitButton.disabled = true;

                // Re-enable after a short delay (in case of quick redirect)
                setTimeout(() => {
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                }, 2000);
            }
        });
    });

    // Quantity selector enhancements
    const quantitySelects = document.querySelectorAll('select[name="quantity"]');
    quantitySelects.forEach(select => {
        select.addEventListener('change', function() {
            // Add visual feedback for quantity changes
            this.style.backgroundColor = '#e5f3ff';
            setTimeout(() => {
                this.style.backgroundColor = '';
            }, 1000);
        });
    });
}

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], select[required]');

        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                // Remove error styling while typing
                this.classList.remove('border-red-500', 'bg-red-50');
            });
        });

        form.addEventListener('submit', function(e) {
            let isValid = true;

            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = form.querySelector('.border-red-500');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

function validateField(field) {
    if (field.hasAttribute('required') && !field.value.trim()) {
        showFieldError(field, 'This field is required');
        return false;
    }

    if (field.type === 'email' && field.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }

    clearFieldError(field);
    return true;
}

function showFieldError(field, message) {
    field.classList.add('border-red-500', 'bg-red-50');

    // Remove existing error message
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }

    // Add new error message
    const errorDiv = document.createElement('p');
    errorDiv.className = 'field-error text-red-600 text-sm mt-1';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('border-red-500', 'bg-red-50');
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Image zoom functionality for product images
function initializeImageZoom() {
    const productImages = document.querySelectorAll('img[src*="products"]');

    productImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.3s ease';
        });

        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });

        // Add cursor pointer to suggest clickability
        img.style.cursor = 'zoom-in';

        // Click to view full size (basic modal)
        img.addEventListener('click', function() {
            showImageModal(this.src, this.alt);
        });
    });
}

function showImageModal(src, alt) {
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50';
    overlay.style.cursor = 'zoom-out';

    // Create image container
    const imgContainer = document.createElement('div');
    imgContainer.className = 'max-w-4xl max-h-4xl p-4';

    // Create image
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    img.className = 'w-full h-full object-contain';

    imgContainer.appendChild(img);
    overlay.appendChild(imgContainer);

    // Add to body
    document.body.appendChild(overlay);

    // Close on click
    overlay.addEventListener('click', function() {
        document.body.removeChild(overlay);
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (document.body.contains(overlay)) {
                document.body.removeChild(overlay);
            }
        }
    });
}

// Auto-hide notifications
function initializeNotifications() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Add close button
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.className = 'float-right text-xl font-bold ml-4 hover:opacity-70';
        closeButton.addEventListener('click', function() {
            alert.style.display = 'none';
        });
        alert.appendChild(closeButton);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.style.display = 'none';
                    }
                }, 500);
            }
        }, 5000);
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Search functionality (if search input exists)
const searchInput = document.querySelector('input[type="search"]');
if (searchInput) {
    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.toLowerCase();

        searchTimeout = setTimeout(() => {
            if (query.length > 2) {
                performSearch(query);
            }
        }, 300);
    });
}

function performSearch(query) {
    // Basic client-side search for product names (can be enhanced with server-side search)
    const products = document.querySelectorAll('.product-card, [class*="product"]');

    products.forEach(product => {
        const productName = product.querySelector('h3, h2, .product-name');
        if (productName) {
            const text = productName.textContent.toLowerCase();
            const productElement = product.closest('.grid > div, .product-item');

            if (productElement) {
                if (text.includes(query)) {
                    productElement.style.display = '';
                } else {
                    productElement.style.display = 'none';
                }
            }
        }
    });
}

// Add to cart animation
function animateAddToCart(button) {
    const originalText = button.textContent;
    button.textContent = '✓ Added!';
    button.classList.add('bg-green-500');
    button.classList.remove('bg-primary');

    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('bg-green-500');
        button.classList.add('bg-primary');
    }, 2000);
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}