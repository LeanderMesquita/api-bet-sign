import re
import random
import string

def adjust_username(email: str) -> str:
    # Split the email to get the part before the @
    username = email.split('@')[0]
    
    # Remove special characters
    username = re.sub(r'[^a-zA-Z0-9]', '', username)
    
    # Generate a random number
    random_number = ''.join(random.choices(string.digits, k=4))
    
    # Combine the cleaned username with the random number
    username_formatted = f"{username}"
    
    return username_formatted
