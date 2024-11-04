import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_google_api():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Debug: Print API key status (but not the actual key)
    print(f"\nAPI Key exists: {'Yes' if api_key else 'No'}")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Test the API with a simple prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say 'Hello, API is working!'")
        
        print("\nAPI Test Result:")
        print("✅ API connection successful!")
        print(f"Model Response: {response.text}")
        
    except Exception as e:
        print("\nAPI Test Result:")
        print("❌ API connection failed!")
        print(f"Error: {str(e)}")
        
        # Additional debugging information
        print("\nDebugging Information:")
        print(f"Current Working Directory: {os.getcwd()}")
        print("Environment Variables:", {k: v for k, v in os.environ.items() if 'api' in k.lower()})

if __name__ == "__main__":
    print("Starting Google API Test...")
    test_google_api()