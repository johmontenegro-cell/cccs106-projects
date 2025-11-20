# Weather Application - Module 6 Lab

## Student Information
- **Name**: John Renzzo C. Montenegro
- **Student ID**: 231002278
- **Course**: CCCS 106
- **Section**: BSCS - 3A

## Project Overview
This weather app fetches and displays a user input address' current weather forecast, humidity level, and wind flow speed.

## Features Implemented

### Base Features
- [x] City search functionality
- [x] Current weather display
- [x] Temperature, humidity, wind speed
- [x] Weather icons
- [x] Error handling
- [x] Modern UI with Material Design

### Enhanced Features
1. **Search History**
   - Stores the last 5 - 10 searched cities.
   - This feature allows users to quickly access previously searched locations to avoid retyping them.
   - The json file was all over the place when it was first instantiated. Adjusted the main.py file path to read it inside the mod6_labs folder.

2. **Temperature Unit Toggle**
   - Toggles between Celsius / Fahrenheit.
   - This feature allows users to know the exact temperature of the entered location based on the unit they are used to without much hassle.
   - Mislabeled values every conversion. Made own function to not ruin the logic of the display function.

3. **Weather Condition Icons and Colors**
   - Changes background colors based on the weather forecast.
   - This feature makes it visually easier to determine the weather forecast without reading too much data on the screen.
   - Color doesn't change.

## Screenshots
[Add 3-5 screenshots showing different aspects of your app]

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/johmontenegro-cell/cccs106-projects.git
cd cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OpenWeatherMap API key to .env
