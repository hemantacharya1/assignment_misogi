from auth import get_gmail_service

def test_gmail_auth():
    service = get_gmail_service()
    profile = service.users().getProfile(userId='me').execute()
    print(f"Authenticated as: {profile['emailAddress']}")

test_gmail_auth()