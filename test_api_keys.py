#!/usr/bin/env python3

import requests
import json

def test_api_key(api_key, key_name):
    """Test if an API key is working"""
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Generate 1 MCQ about water. Return as JSON array."}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1000,
        }
    }

    try:
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            mcq_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            
            if mcq_text:
                print(f"✅ {key_name}: Working (ends with ...{api_key[-4:]})")
                return True
            else:
                print(f"❌ {key_name}: Empty response")
                return False
        else:
            print(f"❌ {key_name}: Error {response.status_code}")
            if response.status_code == 400:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {key_name}: Exception - {e}")
        return False

def main():
    # Your API keys
    api_keys = [
        ("Key 1", "AIzaSyDZ74bZgJw2U8ACz0ncJ4pxhISeBgoosTw"),
        ("Key 2", "AIzaSyC12_noKxy5jJJfGoLUWpAiWPXHnBxD1-Q"), 
        ("Key 3", "AIzaSyD19bjFIt1fNXI0RQy-3BHtZasX-rdZDqo"),
        ("Key 4", "AIzaSyBaJWfsgTaXwkNy711OXHIcBNe8dV7fF_8"),
        ("Key 5", "AIzaSyCJAus6nrOanNRhWu0rkJJ6Z4CecouJE1E")
    ]
    
    print("🔍 Testing API Keys...")
    print("=" * 40)
    
    working_keys = []
    
    for key_name, api_key in api_keys:
        if test_api_key(api_key, key_name):
            working_keys.append(api_key)
    
    print("\n📊 Summary:")
    print(f"Working keys: {len(working_keys)}/{len(api_keys)}")
    
    if working_keys:
        print("\n✅ Working API Keys:")
        for i, key in enumerate(working_keys, 1):
            print(f"  {i}. ...{key[-4:]}")
    else:
        print("\n❌ No working API keys found!")

if __name__ == "__main__":
    main()