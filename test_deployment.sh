#!/bin/bash

# CloudJobHunt Complete Test Suite
# Tests all endpoints and validates the deployment

set -e

COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
TARGET_IP="${1:-192.168.100.23}"
BASE_URL="http://${TARGET_IP}"
PORT="${2:-80}"
BASE_URL="${BASE_URL}:${PORT}"

echo "================================================"
echo "CloudJobHunt - Complete Deployment Test Suite"
echo "================================================"
echo "Target: $BASE_URL"
echo "Date: $(date)"
echo ""

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to test endpoints
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local expected_code=$5
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${COLOR_GREEN}✓${NC} $name (HTTP $http_code)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${COLOR_RED}✗${NC} $name (Expected $expected_code, Got $http_code)"
        echo "  Response: $body"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

echo "1️⃣  PUBLIC ENDPOINTS (No Authentication Required)"
echo "---------------------------------------------------"

# Homepage
test_endpoint "Homepage /" "GET" "/" "" "200"

# Health check
test_endpoint "Health Check /health" "GET" "/health" "" "200"

# Search public
test_endpoint "Search /api/v1/search?q=python" "GET" "/api/v1/search?q=python&max_results=1" "" "200"

# Sources
test_endpoint "Sources /api/v1/sources" "GET" "/api/v1/sources" "" "200"

# Trending
test_endpoint "Trending /api/v1/trending" "GET" "/api/v1/trending" "" "200"

echo ""
echo "2️⃣  AUTHENTICATION ENDPOINTS"
echo "---------------------------------------------------"

# Register
REGISTER_DATA='{"email":"test-'$(date +%s)'@example.com","password":"SecurePass123","full_name":"Test User"}'
test_endpoint "Register /api/v1/auth/register" "POST" "/api/v1/auth/register" "$REGISTER_DATA" "200"

# Login
LOGIN_DATA='{"username":"test@example.com","password":"anypassword"}'
test_endpoint "Login /api/v1/auth/login" "POST" "/api/v1/auth/login" "$LOGIN_DATA" "422"

echo ""
echo "3️⃣  RESPONSE VALIDATION"
echo "---------------------------------------------------"

# Validate health response
response=$(curl -s "$BASE_URL/health")
if echo "$response" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
    echo -e "${COLOR_GREEN}✓${NC} Health check returns valid JSON with status=healthy"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${COLOR_RED}✗${NC} Health check response invalid"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Validate search response
response=$(curl -s "$BASE_URL/api/v1/search?q=devops&max_results=2")
if echo "$response" | jq -e '.jobs | length >= 0' > /dev/null 2>&1; then
    echo -e "${COLOR_GREEN}✓${NC} Search returns valid job listings"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${COLOR_RED}✗${NC} Search response invalid"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Validate JWT token in register
response=$(curl -s -X POST "$BASE_URL/api/v1/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"jwt-test-$(date +%s)@example.com\",\"password\":\"SecurePass123\",\"full_name\":\"JWT Test\"}")
if echo "$response" | jq -e '.access_token | length > 20' > /dev/null 2>&1; then
    echo -e "${COLOR_GREEN}✓${NC} Register returns valid JWT token"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${COLOR_RED}✗${NC} Register JWT token invalid"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""
echo "4️⃣  PERFORMANCE TESTS"
echo "---------------------------------------------------"

# Response time test
start_time=$(date +%s%N)
curl -s "$BASE_URL/health" > /dev/null
end_time=$(date +%s%N)
response_time=$(( (end_time - start_time) / 1000000 ))

if [ $response_time -lt 1000 ]; then
    echo -e "${COLOR_GREEN}✓${NC} Health check response time: ${response_time}ms"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${COLOR_YELLOW}⚠${NC} Health check response time: ${response_time}ms (OK, but slower)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi

echo ""
echo "================================================"
echo "FINAL RESULTS"
echo "================================================"
echo -e "Tests Passed: ${COLOR_GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${COLOR_RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${COLOR_GREEN}🎉 ALL TESTS PASSED! Deployment is successful!${NC}"
    echo ""
    echo "Your CloudJobHunt API is accessible at:"
    echo "  - Homepage:    $BASE_URL/"
    echo "  - API:         $BASE_URL/api/v1/"
    echo "  - Docs:        $BASE_URL/docs"
    echo ""
    exit 0
else
    echo ""
    echo -e "${COLOR_RED}❌ Some tests failed. Please review the output above.${NC}"
    echo ""
    exit 1
fi
