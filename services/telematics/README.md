# TAMP Telematics Service

[![CI](https://github.com/ONLYBOTAi/TAMP-MVP/actions/workflows/ci.yml/badge.svg)](https://github.com/ONLYBOTAi/TAMP-MVP/actions/workflows/ci.yml)

## Overview
The Telematics Service is responsible for handling vehicle telemetry data ingestion, processing, and storage. It provides real-time monitoring and historical data analysis capabilities for the TAMP platform.

## Features
- Real-time telemetry data ingestion
- Background task processing
- Structured logging
- Vehicle metadata integration
- Integration test suite

## Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

3. Start the service:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation
Once the service is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
