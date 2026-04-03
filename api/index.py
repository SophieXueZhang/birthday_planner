"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from web_app import app

# Vercel expects the Flask app as 'app'
