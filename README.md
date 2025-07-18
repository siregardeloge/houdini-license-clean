# Houdini License Server

Simple and clean license verification API for Houdini plugins.

## Features

- License key validation
- Hardware ID verification  
- CORS enabled for web requests
- Demo licenses included for testing

## API Endpoints

### GET /api/verify
Returns server status and info.

### POST /api/verify
Validates license keys.

**Request:**
```json
{
  "license_key": "HBSP-1234-5678-90AB-1C67",
  "hardware_id": "96a21eafc331fec9"
}
```

**Response:**
```json
{
  "valid": true,
  "expires": "2025-12-31T23:59:59",
  "message": "License verified successfully",
  "user": "Demo User"
}
```

## Demo Licenses

- `HBSP-1234-5678-90AB-1C67` - Specific hardware ID
- `HBSP-DEMO-TEST-ABCD-EF12` - Any hardware ID (for testing)

## Deployment

Deploy to Vercel by connecting this repository. No configuration needed!

**Last updated:** 2025-07-18 14:40
