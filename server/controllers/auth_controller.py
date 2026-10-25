from fastapi import APIRouter, HTTPException, Depends
from server.Schemas.auth_schema import RegisterRequest, LoginRequest
from server.services.auth_service import register_user, login_user
from sqlalchemy.orm import Session
from server.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        response, profile = register_user(
            db=db,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
        )

        return {
            "message": "Registration request processed successfully",
            "user_id": response.user.id if response.user else None,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "email_confirmation_required": response.session is None,
        }

    except HTTPException:
        raise

    except Exception as exc:
        db.rollback()

        print(
            f"Registration error: {type(exc).__name__}: {exc}"
        )

        raise HTTPException(
            status_code=400,
            detail="Registration failed. Check the backend terminal for details.",
        )


@router.post("/login")
def login(data: LoginRequest):
    try:
        response = login_user(data.email, data.password)

        if response.session is None:
            raise HTTPException(
                status_code=401,
                detail="Login did not return an active session.",
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user_id": str(response.user.id),
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials or login failed.",
        )
