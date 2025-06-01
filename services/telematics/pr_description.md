# Telematics Service Core Setup

## Overview
This PR implements the core foundation for the Telematics service, establishing the essential infrastructure for vehicle telemetry data collection and processing. The implementation includes JWT-based authentication, database models, and comprehensive test coverage.

## Changes Made
- ✅ Created telematics service with FastAPI framework
- ✅ Implemented JWT-based authentication with proper status codes
- ✅ Set up database models and Alembic migrations
- ✅ Added comprehensive test suite with 100% coverage for auth flows
- ✅ Fixed status code mismatches in JWT authentication
- ✅ Added CI/CD pipeline with GitHub Actions
- ✅ Updated documentation and added PR template

## Testing
All tests are passing, covering:
- Valid token access (200 OK)
- Invalid token handling (401 Unauthorized)
- Missing token handling (401 Unauthorized)
- Expired token handling (401 Unauthorized)

## Checklist
- [x] All tests pass
- [x] Documentation updated
- [x] Authentication implemented
- [x] Database migrations ready
- [x] CI/CD pipeline configured

## Reviewers
- @Evens (Tech Lead)
- @Kenny (Co-Tech Lead)
- @Bruce (PM/PO)

## Notes
- Added JWT token generation utilities for testing
- Adhering to REST best practices for status codes
- CI pipeline will run on all PRs and pushes to dev/feature branches 