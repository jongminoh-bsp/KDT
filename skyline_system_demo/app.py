#!/usr/bin/env python3
"""
Skyline System Demo Application
간단한 Flask 웹 애플리케이션
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Skyline System Demo",
        "status": "running",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "demo")
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# Updated
