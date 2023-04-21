#!/bin/sh

# Check if the venv directory exists
if [ ! -d "venv" ]; then
    # Create a new virtual environment if it doesn't exist
    python3 -m venv venv
fi

# Activate the virtual environment
if [ "$(uname)" = "Darwin" ] || [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
    # macOS or Linux
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" = "MINGW32_NT" ] || [ "$(expr substr $(uname -s) 1 10)" = "MINGW64_NT" ]; then
    # Windows
    . venv/Scripts/activate
fi

# Update the virtual environment with the latest dependencies from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

