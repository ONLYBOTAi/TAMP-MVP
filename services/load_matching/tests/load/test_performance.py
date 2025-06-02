import asyncio
import time
import httpx
import pytest
from datetime import datetime, timedelta
from typing import List, Dict
import statistics
from services.auth.core.auth import create_access_token

# Test configuration
CONCURRENT_USERS = 1000
REQUESTS_PER_USER = 10
RATE_LIMIT = 100
RATE_LIMIT_PERIOD = 60

# Test data
test_user = {
    "id": "1",
    "email": "test@example.com",
    "is_active": True
}

def generate_test_request() -> Dict:
    """Generate a test match request"""
    return {
        "origin": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "address": "New York, NY"
        },
        "destination": {
            "latitude": 34.0522,
            "longitude": -118.2437,
            "address": "Los Angeles, CA"
        },
        "cargo_type": "general",
        "weight": 1000.0,
        "volume": 10.0,
        "pickup_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "delivery_deadline": (datetime.now() + timedelta(days=2)).isoformat(),
        "special_requirements": ["temperature_control"]
    }

async def make_request(client: httpx.AsyncClient, auth_headers: Dict) -> Dict:
    """Make a single match request"""
    start_time = time.time()
    response = await client.get(
        "http://localhost:8003/api/v1/match",
        params=generate_test_request(),
        headers=auth_headers
    )
    end_time = time.time()
    
    return {
        "status_code": response.status_code,
        "latency": end_time - start_time,
        "rate_limit_remaining": response.headers.get("X-RateLimit-Remaining"),
        "rate_limit_reset": response.headers.get("X-RateLimit-Reset")
    }

async def simulate_user(client: httpx.AsyncClient, auth_headers: Dict) -> List[Dict]:
    """Simulate a single user making multiple requests"""
    results = []
    for _ in range(REQUESTS_PER_USER):
        result = await make_request(client, auth_headers)
        results.append(result)
        # Small delay between requests
        await asyncio.sleep(0.1)
    return results

@pytest.mark.asyncio
async def test_concurrent_load():
    """Test system performance under concurrent load"""
    auth_headers = {"Authorization": f"Bearer {create_access_token(test_user)}"}
    
    async with httpx.AsyncClient() as client:
        # Create tasks for concurrent users
        tasks = [
            simulate_user(client, auth_headers)
            for _ in range(CONCURRENT_USERS)
        ]
        
        # Run all tasks concurrently
        start_time = time.time()
        all_results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Flatten results
        results = [item for sublist in all_results for item in sublist]
        
        # Calculate statistics
        latencies = [r["latency"] for r in results]
        status_codes = [r["status_code"] for r in results]
        
        # Calculate success rate
        success_count = status_codes.count(200)
        total_requests = len(status_codes)
        success_rate = (success_count / total_requests) * 100
        
        # Calculate latency statistics
        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
        p99_latency = statistics.quantiles(latencies, n=100)[98]  # 99th percentile
        
        # Calculate throughput
        total_time = end_time - start_time
        throughput = total_requests / total_time
        
        # Print results
        print("\nLoad Test Results:")
        print(f"Total Requests: {total_requests}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Average Latency: {avg_latency:.3f}s")
        print(f"95th Percentile Latency: {p95_latency:.3f}s")
        print(f"99th Percentile Latency: {p99_latency:.3f}s")
        print(f"Throughput: {throughput:.2f} requests/second")
        
        # Assertions
        assert success_rate >= 95.0, f"Success rate {success_rate}% below threshold 95%"
        assert avg_latency < 1.0, f"Average latency {avg_latency}s above threshold 1s"
        assert p95_latency < 2.0, f"95th percentile latency {p95_latency}s above threshold 2s"
        assert p99_latency < 3.0, f"99th percentile latency {p99_latency}s above threshold 3s"

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting behavior"""
    auth_headers = {"Authorization": f"Bearer {create_access_token(test_user)}"}
    
    async with httpx.AsyncClient() as client:
        # Make requests up to rate limit
        results = []
        for _ in range(RATE_LIMIT + 10):  # Try to exceed rate limit
            result = await make_request(client, auth_headers)
            results.append(result)
            await asyncio.sleep(0.1)  # Small delay between requests
        
        # Check rate limit headers
        rate_limits = [r["rate_limit_remaining"] for r in results if r["rate_limit_remaining"] is not None]
        
        # Verify rate limiting
        assert len(rate_limits) > 0, "No rate limit headers found"
        assert min(rate_limits) == "0", "Rate limit not enforced"
        
        # Check for 429 responses
        status_codes = [r["status_code"] for r in results]
        assert 429 in status_codes, "No 429 responses found when rate limit exceeded"

@pytest.mark.asyncio
async def test_burst_traffic():
    """Test system behavior under burst traffic"""
    auth_headers = {"Authorization": f"Bearer {create_access_token(test_user)}"}
    
    async with httpx.AsyncClient() as client:
        # Create burst of requests
        tasks = [make_request(client, auth_headers) for _ in range(200)]  # Burst size
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Calculate burst statistics
        latencies = [r["latency"] for r in results]
        status_codes = [r["status_code"] for r in results]
        
        # Calculate success rate
        success_count = status_codes.count(200)
        total_requests = len(status_codes)
        success_rate = (success_count / total_requests) * 100
        
        # Calculate burst throughput
        burst_time = end_time - start_time
        burst_throughput = total_requests / burst_time
        
        print("\nBurst Test Results:")
        print(f"Burst Size: {total_requests}")
        print(f"Burst Duration: {burst_time:.3f}s")
        print(f"Burst Throughput: {burst_throughput:.2f} requests/second")
        print(f"Success Rate: {success_rate:.2f}%")
        
        # Assertions
        assert burst_throughput >= 50, f"Burst throughput {burst_throughput} below threshold 50 req/s"
        assert success_rate >= 90, f"Burst success rate {success_rate}% below threshold 90%" 