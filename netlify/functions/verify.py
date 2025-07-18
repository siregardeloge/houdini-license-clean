#!/usr/bin/env python3
"""
Netlify Function for Houdini License Server
"""

import json
from datetime import datetime

def handler(event, context):
    """Netlify function handler"""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS (CORS preflight)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Handle GET - API info
    if event['httpMethod'] == 'GET':
        response = {
            "service": "Houdini License Server",
            "version": "1.0",
            "status": "active",
            "timestamp": datetime.now().isoformat()
        }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
    
    # Handle POST - License verification
    if event['httpMethod'] == 'POST':
        try:
            data = json.loads(event['body'])
            license_key = data.get('license_key', '')
            hardware_id = data.get('hardware_id', '')
            
            # Demo license database
            valid_licenses = {
                "HBSP-1234-5678-90AB-1C67": {
                    "expires": "2025-12-31T23:59:59",
                    "hardware_id": "96a21eafc331fec9",
                    "user": "Demo User"
                },
                "HBSP-DEMO-TEST-ABCD-EF12": {
                    "expires": "2025-12-31T23:59:59", 
                    "hardware_id": "any",
                    "user": "Test User"
                }
            }
            
            # Validate license
            if license_key in valid_licenses:
                license_info = valid_licenses[license_key]
                
                if license_info["hardware_id"] == "any" or license_info["hardware_id"] == hardware_id:
                    response = {
                        "valid": True,
                        "expires": license_info["expires"],
                        "message": "License verified successfully",
                        "user": license_info["user"]
                    }
                else:
                    response = {
                        "valid": False,
                        "error": "Hardware ID mismatch"
                    }
            else:
                response = {
                    "valid": False,
                    "error": "Invalid license key"
                }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    "valid": False,
                    "error": f"Server error: {str(e)}"
                })
            }
    
    # Method not allowed
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({"error": "Method not allowed"})
    }
