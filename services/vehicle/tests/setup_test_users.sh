#!/bin/bash

# Test configuration
AUTH_SERVICE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Helper function to print results
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
        exit 1
    fi
}

# Register test owner
echo "Registering test owner..."
curl -s -X POST "${AUTH_SERVICE_URL}/register" \
    -H "Content-Type: application/json" \
    -d '{"username":"test_owner","password":"test_password","role":"truck_owner"}' | jq -e '.access_token != null'
print_result $? "Test owner registered"

# Register test admin
echo "Registering test admin..."
curl -s -X POST "${AUTH_SERVICE_URL}/register" \
    -H "Content-Type: application/json" \
    -d '{"username":"test_admin","password":"admin_password","role":"admin"}' | jq -e '.access_token != null'
print_result $? "Test admin registered"

# Register other user
echo "Registering other user..."
curl -s -X POST "${AUTH_SERVICE_URL}/register" \
    -H "Content-Type: application/json" \
    -d '{"username":"other_user","password":"other_password","role":"user"}' | jq -e '.access_token != null'
print_result $? "Other user registered"

echo "All test users registered successfully!" 