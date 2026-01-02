"""
URL configuration for babygoods project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings


def home_view(request):
    """Homepage for Baby Goods Dealer"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Baby Goods Dealer - Premium Baby Products</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .feature-card { transition: transform 0.3s; }
            .feature-card:hover { transform: translateY(-5px); }
            .baby-icon { font-size: 3rem; }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand" href="/">🍼 Baby Goods Dealer</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="#products">Products</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#categories">Categories</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/admin/">Admin</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/cms/">CMS</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <section class="hero text-white py-5">
            <div class="container py-5">
                <div class="row align-items-center">
                    <div class="col-lg-6">
                        <h1 class="display-4 fw-bold">Premium Baby Products</h1>
                        <p class="lead">Safe, organic, and certified products for your little ones. Complete e-commerce solution with professional admin management.</p>
                        <div class="d-grid gap-3 d-md-flex justify-content-md-start">
                            <a href="#products" class="btn btn-light btn-lg px-4 me-md-2">🛍️ Shop Products</a>
                            <a href="/admin/" class="btn btn-outline-light btn-lg px-4">🔧 Admin Panel</a>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="text-center">
                            <div class="baby-icon">👶</div>
                            <p class="mt-3">Professional Baby Product Management Platform</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-5" id="products">
            <div class="container">
                <div class="row text-center mb-5">
                    <div class="col">
                        <h2>Featured Categories</h2>
                        <p class="lead">Age-appropriate products for every stage of development</p>
                    </div>
                </div>
                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card feature-card h-100">
                            <div class="card-body text-center">
                                <div class="feature-icon mb-3">🍼</div>
                                <h5 class="card-title">Newborn (0-2 months)</h5>
                                <p class="card-text">Essential products for newborns with safety certifications</p>
                                <a href="/admin/products/product/add/" class="btn btn-primary">Add Products</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card feature-card h-100">
                            <div class="card-body text-center">
                                <div class="feature-icon mb-3">👶</div>
                                <h5 class="card-title">Infant (3-11 months)</h5>
                                <p class="card-text">Developmental toys and feeding supplies</p>
                                <a href="/admin/products/product/add/" class="btn btn-primary">Add Products</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card feature-card h-100">
                            <div class="card-body text-center">
                                <div class="feature-icon mb-3">🧒</div>
                                <h5 class="card-title">Toddler (1-3 years)</h5>
                                <p class="card-text">Educational toys and safety gear</p>
                                <a href="/admin/products/product/add/" class="btn btn-primary">Add Products</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-5 bg-light" id="categories">
            <div class="container">
                <div class="row text-center mb-5">
                    <div class="col">
                        <h2>Management Features</h2>
                        <p class="lead">Professional e-commerce administration</p>
                    </div>
                </div>
                <div class="row g-4">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">🛡️ Safety Certification Tracking</h5>
                                <p class="card-text">Track ASTM, CPSC, and CE safety certifications for all products</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">📦 Inventory Management</h5>
                                <p class="card-text">Real-time stock tracking with low stock alerts</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">⭐ Customer Reviews</h5>
                                <p class="card-text">5-star rating system with moderation</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">🏷️ Product Variants</h5>
                                <p class="card-text">Size, color, and pattern management</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <footer class="py-4 bg-dark text-white">
            <div class="container text-center">
                <p>© 2026 Baby Goods Dealer. Professional E-commerce Platform.</p>
                <div>
                    <a href="/admin/" class="text-white me-3">🔧 Admin</a>
                    <a href="/cms/" class="text-white me-3">📝 CMS</a>
                    <a href="https://github.com/afaye1/babygoodsdealer-wagtail" class="text-white">📦 GitHub</a>
                </div>
            </div>
        </footer>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
]
