#!/bin/bash

# Check if GOOGLE_API_KEY is set
if [ -z "${GOOGLE_API_KEY}" ]; then
    echo "Error: GOOGLE_API_KEY environment variable is not set"
    exit 1
fi

# Start the Streamlit app
streamlit run main.py