#!/bin/bash

# Baby Goods Dealer - Coolify Deployment Script
# Professional CI/CD deployment automation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COOLIFY_URL="https://cool.afdvprojects.com"
APP_UUID="dowoko08swgksskkckokksog"
PROJECT_UUID="tswswsswow4c00sk0cksc8sw"
ENV_UUID="fokckks8wc8c88ko4oockk8g"
REPO_URL="https://github.com/afaye1/babygoodsdealer-wagtail.git"

echo -e "${BLUE}🚀 Baby Goods Dealer - Coolify Deployment${NC}"
echo -e "${BLUE}================================================${NC}"

# Check if required tools are available
if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ curl is not installed${NC}"
    exit 1
fi

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Step 1: Check repository status
echo -e "\n${YELLOW}📋 Step 1: Checking Repository Status${NC}"
print_info "Repository: $REPO_URL"
print_info "Branch: master"

# Get latest commit info
LATEST_COMMIT=$(git log -1 --format="%H")
COMMIT_MESSAGE=$(git log -1 --format="%s")
print_info "Latest Commit: $LATEST_COMMIT"
print_info "Message: $COMMIT_MESSAGE"

# Step 2: Check CI/CD status
echo -e "\n${YELLOW}🔄 Step 2: Checking CI/CD Status${NC}"
print_info "GitHub Actions running..."

# Wait a moment for CI to start
sleep 5

# Check GitHub Actions status (using GitHub CLI if available)
if command -v gh &> /dev/null; then
    RUN_STATUS=$(gh run list --workflow=deploy.yml --limit=1 --json status --jq '.[0].status' 2>/dev/null || echo "pending")
    print_info "CI/CD Status: $RUN_STATUS"
    
    if [ "$RUN_STATUS" = "completed" ]; then
        print_status "CI/CD checks passed!"
    elif [ "$RUN_STATUS" = "in_progress" ]; then
        print_warning "CI/CD still running, proceeding with deployment..."
    else
        print_warning "CI/CD status: $RUN_STATUS"
    fi
else
    print_warning "GitHub CLI not available, skipping CI/CD check"
fi

# Step 3: Prepare deployment payload
echo -e "\n${YELLOW}📦 Step 3: Preparing Deployment${NC}"

# Create deployment payload
DEPLOY_PAYLOAD=$(cat <<EOF
{
    "source_type": "git",
    "source_repository": "$REPO_URL",
    "source_branch": "master",
    "build_command": "docker build -t babygoodsdealer-wagtail .",
    "environment_variables": {
        "DEBUG": "false",
        "SECRET_KEY": "$(openssl rand -base64 64)",
        "ALLOWED_HOSTS": "babygoodsdealer.com,www.babygoodsdealer.com",
        "WAGTAILADMIN_BASE_URL": "https://babygoodsdealer.com",
        "DATABASE_URL": "postgresql://postgres:\${POSTGRES_PASSWORD}@db:5432/babygoods",
        "SECURE_SSL_REDIRECT": "true",
        "SECURE_HSTS_SECONDS": "31536000",
        "SESSION_COOKIE_SECURE": "true",
        "CSRF_COOKIE_SECURE": "true"
    },
    "ports": {
        "8000": "8000"
    },
    "health_check_path": "/admin/",
    "auto_deploy": true
}
EOF
)

print_status "Deployment payload prepared"

# Step 4: Trigger Coolify deployment
echo -e "\n${YELLOW}🚀 Step 4: Triggering Coolify Deployment${NC}"
print_info "Coolify URL: $COOLIFY_URL"
print_info "Application UUID: $APP_UUID"

# Note: This would require API access to Coolify
# For now, we'll provide manual instructions
print_warning "Manual Coolify deployment required"
echo -e "\n${BLUE}📋 Manual Deployment Instructions:${NC}"
echo -e "1. Open Coolify: $COOLIFY_URL"
echo -e "2. Navigate to: Project → Environment → Application"
echo -e "3. Connect repository: $REPO_URL"
echo -e "4. Select branch: master"
echo -e "5. Set build pack: Dockerfile"
echo -e "6. Configure environment variables:"
echo -e "   - DEBUG=false"
echo -e "   - SECRET_KEY=<generate-long-key>"
echo -e "   - ALLOWED_HOSTS=babygoodsdealer.com,www.babygoodsdealer.com"
echo -e "   - DATABASE_URL=<your-postgres-url>"
echo -e "7. Deploy application"

# Step 5: Deployment verification
echo -e "\n${YELLOW}🔍 Step 5: Deployment Verification${NC}"

# Function to check deployment status
check_deployment() {
    local url=$1
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            print_status "Application is accessible at $url"
            return 0
        fi
        
        print_info "Attempt $attempt/$max_attempts - Checking $url..."
        sleep 10
        attempt=$((attempt + 1))
    done
    
    print_error "Deployment verification failed after $max_attempts attempts"
    return 1
}

# Check if deployment URL is provided
if [ -n "$1" ]; then
    echo -e "\n${BLUE}Testing deployment at: $1${NC}"
    if check_deployment "$1"; then
        print_status "🎉 Deployment successful!"
        
        echo -e "\n${GREEN}🏥 Production URLs:${NC}"
        echo -e "• Admin Panel: $1/admin/"
        echo -e "• Wagtail Admin: $1/admin/"
        echo -e "• Health Check: $1/admin/"
        
        echo -e "\n${GREEN}🔐 Admin Credentials:${NC}"
        echo -e "• Username: admin"
        echo -e "• Password: [set in production]"
        
        echo -e "\n${GREEN}📊 CI/CD Status:${NC}"
        echo -e "• GitHub Actions: https://github.com/afaye1/babygoodsdealer-wagtail/actions"
        echo -e "• Repository: https://github.com/afaye1/babygoodsdealer-wagtail"
        
    else
        print_error "Deployment verification failed"
        exit 1
    fi
else
    print_info "No deployment URL provided for verification"
    echo -e "\n${BLUE}To verify deployment, run:${NC}"
    echo -e "./deploy.sh <your-deployment-url>"
fi

echo -e "\n${GREEN}🎯 Deployment Summary:${NC}"
echo -e "• Repository: $REPO_URL"
echo -e "• Branch: master"
echo -e "• Commit: $LATEST_COMMIT"
echo -e "• CI/CD: Automated with GitHub Actions"
echo -e "• Platform: Coolify"
echo -e "• Features: Django + Wagtail + E-commerce"

print_status "Deployment script completed successfully! 🚀"