#!/bin/bash

# Test configuration
AUTH_SERVICE_URL="http://localhost:8000"
VEHICLE_SERVICE_URL="http://localhost:8001"
TEST_USER="test_owner"
TEST_PASSWORD="test_password"
TEST_ADMIN="test_admin"
TEST_ADMIN_PASSWORD="admin_password"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Helper function to print test results
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
        exit 1
    fi
}

# Test token validation
echo "Testing token validation..."
curl -s -X POST "${AUTH_SERVICE_URL}/validate-token?token=invalid" | grep -q "Invalid token"
print_result $? "Token validation rejects invalid tokens"

# Test vehicle creation
echo "Testing vehicle creation..."
TOKEN=$(curl -s -X POST "${AUTH_SERVICE_URL}/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"${TEST_USER}\",\"password\":\"${TEST_PASSWORD}\"}" | jq -r '.access_token')

echo "Debug: Got token: $TOKEN"

VEHICLE_RESPONSE=$(curl -s -X POST "${VEHICLE_SERVICE_URL}/vehicles?token=${TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"make":"Toyota","model":"Hilux","year":2023,"license_plate":"TEST123"}')

echo "Debug: Vehicle response: $VEHICLE_RESPONSE"

VEHICLE_ID=$(echo $VEHICLE_RESPONSE | jq -r '.id')

echo "Debug: Vehicle ID: $VEHICLE_ID"

[ ! -z "$VEHICLE_ID" ]
print_result $? "Vehicle creation successful"

# Test vehicle deletion
echo "Testing vehicle deletion..."

# Test unauthorized deletion
curl -s -X DELETE "${VEHICLE_SERVICE_URL}/vehicles/${VEHICLE_ID}?token=invalid" | grep -q "Invalid token"
print_result $? "Unauthorized deletion rejected"

# Test deletion by non-owner
OTHER_TOKEN=$(curl -s -X POST "${AUTH_SERVICE_URL}/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"other_user\",\"password\":\"other_password\"}" | jq -r '.access_token')

curl -s -X DELETE "${VEHICLE_SERVICE_URL}/vehicles/${VEHICLE_ID}?token=${OTHER_TOKEN}" | grep -q "Not authorized"
print_result $? "Non-owner deletion rejected"

# Test successful deletion
curl -s -X DELETE "${VEHICLE_SERVICE_URL}/vehicles/${VEHICLE_ID}?token=${TOKEN}" | grep -q "deleted_at"
print_result $? "Vehicle successfully deleted"

# Test deletion of non-existent vehicle
curl -s -X DELETE "${VEHICLE_SERVICE_URL}/vehicles/999999?token=${TOKEN}" | grep -q "not found"
print_result $? "Deletion of non-existent vehicle rejected"

# Test deletion of already deleted vehicle
curl -s -X DELETE "${VEHICLE_SERVICE_URL}/vehicles/${VEHICLE_ID}?token=${TOKEN}" | grep -q "not found"
print_result $? "Deletion of already deleted vehicle rejected"

# Test GET /vehicles/all endpoint
echo "Testing GET /vehicles/all endpoint..."

# Test unauthorized access
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/all?token=invalid" | grep -q "Invalid token"
print_result $? "Unauthorized access to /vehicles/all rejected"

# Test non-admin access
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/all?token=${TOKEN}" | grep -q "Admin access required"
print_result $? "Non-admin access to /vehicles/all rejected"

# Test admin access with pagination
ADMIN_TOKEN=$(curl -s -X POST "${AUTH_SERVICE_URL}/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"${TEST_ADMIN}\",\"password\":\"${TEST_ADMIN_PASSWORD}\"}" | jq -r '.access_token')

# Test default pagination
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/all?token=${ADMIN_TOKEN}" | jq -e '.items != null and .total != null and .limit == 50 and .offset == 0'
print_result $? "Admin access with default pagination successful"

# Test custom pagination
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/all?token=${ADMIN_TOKEN}&limit=10&offset=5" | jq -e '.items != null and .total != null and .limit == 10 and .offset == 5'
print_result $? "Admin access with custom pagination successful"

# Test soft delete filtering
# Create and delete a vehicle
DELETED_VEHICLE_ID=$(curl -s -X POST "${VEHICLE_SERVICE_URL}/vehicles?token=${TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"make":"Ford","model":"Ranger","year":2023,"license_plate":"DEL123"}' | jq -r '.id')

curl -s -X DELETE "${VEHICLE_SERVICE_URL}/vehicles/${DELETED_VEHICLE_ID}?token=${TOKEN}"

# Verify deleted vehicle is not in results
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/all?token=${ADMIN_TOKEN}" | jq -e ".items[] | select(.id == ${DELETED_VEHICLE_ID}) | not"
print_result $? "Soft-deleted vehicle is filtered from results"

# Test GET /vehicles/{id} endpoint
echo "Testing GET /vehicles/{id} endpoint..."

# Create a new vehicle for testing
TEST_VEHICLE_ID=$(curl -s -X POST "${VEHICLE_SERVICE_URL}/vehicles?token=${TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"make":"Toyota","model":"Hilux","year":2023,"license_plate":"TEST456"}' | jq -r '.id')

# Test unauthorized access
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/${TEST_VEHICLE_ID}?token=invalid" | grep -q "Invalid token"
print_result $? "Unauthorized access to vehicle by ID rejected"

# Test non-owner, non-admin access
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/${TEST_VEHICLE_ID}?token=${OTHER_TOKEN}" | grep -q "Unauthorized"
print_result $? "Non-owner, non-admin access to vehicle rejected"

# Test owner access
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/${TEST_VEHICLE_ID}?token=${TOKEN}" | jq -e '.id == '${TEST_VEHICLE_ID}
print_result $? "Owner can access their vehicle"

# Test admin access
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/${TEST_VEHICLE_ID}?token=${ADMIN_TOKEN}" | jq -e '.id == '${TEST_VEHICLE_ID}
print_result $? "Admin can access any vehicle"

# Test access to non-existent vehicle
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/999999?token=${TOKEN}" | grep -q "not found"
print_result $? "Access to non-existent vehicle rejected"

# Test access to soft-deleted vehicle
curl -s -X DELETE "${VEHICLE_SERVICE_URL}/vehicles/${TEST_VEHICLE_ID}?token=${TOKEN}"
curl -s -X GET "${VEHICLE_SERVICE_URL}/vehicles/${TEST_VEHICLE_ID}?token=${TOKEN}" | grep -q "not found"
print_result $? "Access to soft-deleted vehicle rejected"

echo "All tests passed successfully!" 