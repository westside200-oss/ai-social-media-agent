#!/bin/bash

# Local development setup script
# Creates virtual environment and installs dependencies

echo "Setting up AI Social Media Agent development environment..."

# Backend setup
echo "Setting up backend..."
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Frontend setup
echo "Setting up frontend..."
cd frontend
npm install
cd ..

echo "Development environment setup complete!"
echo "\nNext steps:"
echo "1. Copy .env.example to .env and update with your credentials"
echo "2. Start backend: cd backend && source venv/bin/activate && python app/main.py"
echo "3. Start frontend: cd frontend && npm start"
echo "4. Visit http://localhost:3000"
