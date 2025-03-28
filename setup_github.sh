#!/bin/bash

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: ChemE Analysis Suite"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/ChemE_Analysis_Suite.git

# Push to GitHub
git push -u origin main
