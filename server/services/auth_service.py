from server.services.supabase_service import supabase
from sqlalchemy.orm import Session
from server.model import Profile


def register_user(
    db: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
):
    response = supabase.auth.sign_up({"email": email, "password": password})
    if response.user is None:
        raise ValueError("Supabase did not return a user")
    
    profile= Profile(
        id=str(response.user.id),
        first_name=first_name,
        last_name=last_name
    )
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    return response, profile


def login_user(email: str, password: str):
    response = supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )

    return response
