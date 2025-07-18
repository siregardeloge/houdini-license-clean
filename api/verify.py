#!/usr/bin/env python3
"""
Clean Houdini License Server API - No complications!
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """API info endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "service": "Houdini License Server",
            "version": "1.0",
            "status": "active",
            "timestamp": datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """License verification endpoint"""
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Read request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
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
                
                # Check hardware ID (allow 'any' for demo)
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
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "valid": False,
                "error": f"Server error: {str(e)}"
            }
            
            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
