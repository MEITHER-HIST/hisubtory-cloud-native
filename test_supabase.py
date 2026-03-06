import os
import sys
from supabase import create_client

def test():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    print(f"--- Supabase Diagnostic ---")
    print(f"URL: {url}")
    print(f"KEY: {key[:15]}...{key[-5:] if key else ''}")
    
    if not url or not key:
        print("ERROR: Missing URL or KEY")
        return

    try:
        supabase = create_client(url, key)
        # Auth 설정을 확인하기 위한 가벼운 호출
        print("Attempting to fetch auth config...")
        # get_user는 무조건 에러가 나겠지만(토큰이 더미니까), 
        # 키가 틀리면 여기서 'Invalid Key' 에러가 명확히 나옵니다.
        try:
            supabase.auth.get_user("dummy")
        except Exception as auth_e:
            auth_msg = str(auth_e)
            print(f"Auth Response: {auth_msg}")
            
            if "invalid" in auth_msg.lower() and "api key" in auth_msg.lower():
                print("!!! CRITICAL: YOUR SUPABASE_KEY IS INVALID !!!")
            elif "not found" in auth_msg.lower():
                print("URL is wrong or Project is paused.")
            else:
                print("Key seems valid, but 'dummy' token was rejected (Normal).")
                
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    test()
