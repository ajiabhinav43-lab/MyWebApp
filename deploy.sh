#!/bin/bash

echo "=============================="
echo "🚀 Starting Deployment"
echo "=============================="

cd /home/ubuntu/MyWebApp || exit

echo "📥 Pulling latest code..."
git pull origin main

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "🔄 Restarting application..."
sudo systemctl restart mywebapp

echo "=============================="
echo "✅ Deployment Completed Successfully"
echo "=============================="
