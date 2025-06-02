# Load Testing Suite

This directory contains the load testing infrastructure for the Load Matching Service.

## Overview

The load testing suite is designed to validate the service's performance under various conditions:
- Concurrent user load
- Rate limiting behavior
- Burst traffic handling
- Response time consistency

## Prerequisites

- Python 3.11+
- pytest
- pytest-asyncio
- httpx
- statistics

## Running Tests

### 1. Local Development

```bash
# Run all load tests
pytest tests/load/test_performance.py -v

# Run specific test
pytest tests/load/test_performance.py::test_concurrent_load -v
```

### 2. Docker Environment

```bash
# Build and run in Docker
docker build -t load-matching-tests .
docker run load-matching-tests pytest tests/load/test_performance.py -v
```

## Test Scenarios

### 1. Concurrent Load Test
- Simulates 1000 concurrent users
- Each user makes 10 requests
- Validates success rate and latency thresholds

### 2. Rate Limiting Test
- Tests rate limit enforcement
- Validates rate limit headers
- Checks 429 response handling

### 3. Burst Traffic Test
- Simulates sudden traffic spikes
- Measures system stability
- Validates throughput under load

## Configuration

Test parameters can be adjusted in `test_performance.py`:
```python
CONCURRENT_USERS = 1000
REQUESTS_PER_USER = 10
RATE_LIMIT = 100
RATE_LIMIT_PERIOD = 60
```

## Results

Test results are documented in `docs/load_test_results.md` and include:
- Success rates
- Latency metrics
- Throughput measurements
- Performance bottlenecks
- Recommendations

## Adding New Tests

1. Create new test file in `tests/load/`
2. Import required dependencies
3. Define test functions with `@pytest.mark.asyncio`
4. Add assertions for expected behavior
5. Update documentation with new test details

## Troubleshooting

Common issues and solutions:

1. **Connection Errors**
   - Verify service is running
   - Check network connectivity
   - Validate service URLs

2. **Rate Limit Issues**
   - Confirm rate limit configuration
   - Check rate limit headers
   - Verify burst handling

3. **Performance Issues**
   - Monitor system resources
   - Check service logs
   - Validate test parameters

## Contributing

1. Follow existing test patterns
2. Add appropriate documentation
3. Include performance thresholds
4. Update results documentation 