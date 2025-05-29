#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚚 Starting Vehicle Service Tests..."

# Test 1: Register a new user
echo -e "\n${GREEN}Test 1: Registering new user${NC}"
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testowner", "password": "testpass123", "role": "truck_owner"}')
echo "Response: $REGISTER_RESPONSE"

# Test 2: Login with the user
echo -e "\n${GREEN}Test 2: Logging in${NC}"
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testowner", "password": "testpass123", "role": "truck_owner"}')
echo "Response: $LOGIN_RESPONSE"

# Extract token from login response
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Failed to get token${NC}"
    exit 1
fi

# Test 3: Create a vehicle with valid token
echo -e "\n${GREEN}Test 3: Creating vehicle with valid token${NC}"
CREATE_RESPONSE=$(curl -s -X POST "http://localhost:8001/vehicles?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "Hilux", "year": 2023, "license_plate": "ABC123"}')
echo "Response: $CREATE_RESPONSE"

# Test 4: Create vehicle with invalid token
echo -e "\n${GREEN}Test 4: Creating vehicle with invalid token${NC}"
INVALID_RESPONSE=$(curl -s -X POST "http://localhost:8001/vehicles?token=invalid_token" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "Hilux", "year": 2023, "license_plate": "ABC123"}')
echo "Response: $INVALID_RESPONSE"

# Test 5: Create vehicle without token
echo -e "\n${GREEN}Test 5: Creating vehicle without token${NC}"
NO_TOKEN_RESPONSE=$(curl -s -X POST "http://localhost:8001/vehicles" \
  -H "Content-Type: application/json" \
  -d '{"make": "Toyota", "model": "Hilux", "year": 2023, "license_plate": "ABC123"}')
echo "Response: $NO_TOKEN_RESPONSE"

echo -e "\n${GREEN}Tests completed!${NC}" 