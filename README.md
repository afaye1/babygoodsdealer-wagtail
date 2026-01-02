# Baby Goods Dealer - Wagtail Version

A comprehensive baby products e-commerce platform built with Django, Wagtail CMS, and Django Oscar for e-commerce functionality.

## Features

### Baby Product Management
- **Age-based categorization**: Newborn (0-2m), Infant (3-11m), Toddler (1-3y)
- **Safety certification tracking**: ASTM, CPSC, CE marking support
- **Material transparency**: Track organic materials, BPA-free status
- **Gender variants**: Unisex, Male, Female product options
- **Condition tracking**: New, Like New, Good, Fair conditions

### Advanced Admin Interface
- **Django Admin**: Full-featured product management
- **Safety status indicators**: Real-time compliance checking
- **Low stock alerts**: Automated inventory management
- **Bulk operations**: Mass product updates
- **Review management**: Customer review moderation

### E-commerce Features
- **Product variants**: Size, color, pattern options
- **Inventory management**: Stock tracking with backorder support
- **Pricing flexibility**: Compare pricing, cost tracking
- **Product galleries**: Multiple images with alt text
- **Customer reviews**: 5-star rating system with verification

### CMS Capabilities
- **Wagtail integration**: Rich content management
- **Baby safety guides**: Content blocks for safety information
- **Age-based recommendations**: Dynamic product suggestions
- **Blog functionality**: Parenting tips and care guides

## Quick Start

### Local Development

1. **Clone and setup**:
```bash
git clone <repository-url>
cd babygoodsdealer-wagtail
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Database setup**:
```bash
# Using SQLite (default)
python manage.py migrate

# Or PostgreSQL with Docker
docker-compose up db redis
python manage.py migrate
```

3. **Create superuser**:
```bash
python manage.py createsuperuser
# Or use the pre-created one:
# Username: admin
# Email: admin@babygoodsdealer.com
# Password: admin123
```

4. **Start development server**:
```bash
python manage.py runserver 0.0.0.0:8000
```

5. **Access admin**: http://localhost:8000/admin/
6. **Access Wagtail**: http://localhost:8000/admin/

### Docker Development

```bash
# Full development environment
docker-compose up

# Or build and run manually
docker build -t babygoodsdealer-wagtail .
docker run -p 8000:8000 -e DEBUG=1 babygoodsdealer-wagtail
```

## Deployment Options

### 1. Coolify Deployment (Recommended)

**Prerequisites**: Coolify instance at `cool.afdvprojects.com`

**Steps**:
1. **Push to Git Repository**:
```bash
git add .
git commit -m "Initial Baby Goods Dealer Wagtail setup"
git remote add origin <your-git-repo>
git push -u origin main
```

2. **Coolify Configuration**:
   - Connect your Git repository to Coolify
   - Use "Dockerfile" build pack
   - Set environment variables:
     - `DEBUG=0`
     - `SECRET_KEY=<your-secret-key>`
     - `DATABASE_URL=postgresql://user:pass@host:5432/dbname`
     - `ALLOWED_HOSTS=babygoodsdealer.com,www.babygoodsdealer.com`
     - `WAGTAILADMIN_BASE_URL=https://babygoodsdealer.com`

3. **Health Checks**:
   - Coolify automatically monitors `/admin/` health endpoint
   - Database connection checked via Django health system

### 2. Direct Docker Deployment

```bash
# Build production image
docker build -t babygoodsdealer-wagtail:latest .

# Run with environment variables
docker run -d \
  --name babygoodsdealer \
  -p 8000:8000 \
  -e DEBUG=0 \
  -e SECRET_KEY=your-production-secret-key \
  -e DATABASE_URL=postgresql://user:pass@host:5432/dbname \
  -e ALLOWED_HOSTS=babygoodsdealer.com \
  -v /path/to/media:/app/media \
  babygoodsdealer-wagtail:latest
```

## Product Management

### Adding Products

1. **Navigate to Admin**: http://yoursite.com/admin/
2. **Add Categories**: Create product categories first
3. **Add Safety Certifications**: Define required safety standards
4. **Add Age Groups**: Set up age ranges (0-3m, 3-6m, 6-12m, etc.)
5. **Add Products**: Complete product information with:
   - Basic info, pricing, inventory
   - Baby-specific attributes (age groups, materials)
   - Safety certifications
   - Product images and variants

### Safety Certification Management

```python
# Example of required certifications
required_certs = [
    "ASTM F963-17",  # Toy Safety Standard
    "CPSC Certified",   # Consumer Product Safety
    "CE Marking",       # European Conformity
]
```

### Inventory Management

- **Low stock alerts**: Automatically highlighted below threshold
- **Backorder support**: Optional for out-of-stock items
- **Stock tracking**: Real-time inventory updates
- **Bulk operations**: Mass stock updates via admin

## API Endpoints

### Product API (Future Enhancement)
```python
# Product endpoints (when REST API is added)
/api/products/                    # List all products
/api/products/{id}/               # Product details
/api/products/by-category/{slug}/  # Products by category
/api/products/by-age/{group}/       # Products by age group
```

## Security Features

### Product Safety
- **Mandatory certifications**: Required safety standards
- **Compliance checking**: Real-time status verification
- **Age-appropriate filtering**: Automatic age group validation
- **Material tracking**: BPA-free, organic verification

### Platform Security
- **CSRF protection**: Django built-in protection
- **SQL injection prevention**: Django ORM protection
- **XSS protection**: Django template auto-escaping
- **Secure file uploads**: Wagtail media validation

## Performance Optimization

### Database
- **Optimized queries**: Select_related/prefetch_related
- **Database indexes**: Strategic index placement
- **Query optimization**: Efficient admin list views

### Caching
- **Static file caching**: Whitenoise compression
- **Database caching**: Redis integration available
- **CDN ready**: Static files CDN compatible

## Content Management

### Wagtail Features
- **Rich text editing**: Advanced content editor
- **Image management**: Optimized image handling
- **Page hierarchy**: Nested content structure
- **Content blocks**: Custom baby product blocks

### Content Types
- **Product pages**: Detailed product information
- **Category pages**: Product groupings
- **Safety guides**: Educational content
- **Blog posts**: Parenting advice and tips

## Migration from Next.js

### Data Migration Strategy

1. **Phase 1**: Set up Wagtail alongside Next.js
2. **Phase 2**: Migrate product data to Django models
3. **Phase 3**: Switch frontend to Wagtail templates
4. **Phase 4**: Decommission Next.js (optional)

### SEO Preservation
```python
# URL structure compatibility
# Next.js: /products/[id]
# Wagtail: /products/{slug}/
```

## Development Workflow

### Adding New Features

1. **Create Django app**:
```bash
python manage.py startapp feature_name
```

2. **Add to INSTALLED_APPS** in settings.py

3. **Create models**: Define database structure

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create admin interface**: Register models in admin.py

### Testing

```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check --deploy
```

## Environment Variables

```bash
# Production settings
DEBUG=0
SECRET_KEY=your-very-long-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=babygoodsdealer.com,www.babygoodsdealer.com
WAGTAILADMIN_BASE_URL=https://babygoodsdealer.com
```

## Monitoring and Maintenance

### Health Checks
- **Database connectivity**: Django health check
- **File system access**: Media file verification
- **Application health**: HTTP endpoint monitoring

### Backup Strategy
- **Database backups**: Regular pg_dump exports
- **Media backups**: File system synchronization
- **Configuration backup**: Git version control

## Support

### Documentation
- **Django documentation**: https://docs.djangoproject.com/
- **Wagtail docs**: https://docs.wagtail.io/
- **Django Oscar docs**: https://django-oscar.readthedocs.io/

### Common Issues

1. **Static files not loading**: Run `collectstatic` command
2. **Database connection errors**: Check DATABASE_URL format
3. **Permission denied**: Ensure correct file permissions
4. **Admin 404 errors**: Check ALLOWED_HOSTS setting

## License

Private - All rights reserved.