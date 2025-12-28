from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any, Optional
from pydantic import BaseModel
from auth_config import auth_instance
import os

router = APIRouter(prefix="/api/auth", tags=["authentication"])

class SignupRequest(BaseModel):
    """
    Request model for user signup
    """
    email: str
    password: str
    name: str
    profile_data: Optional[Dict[str, Any]] = {}

class SigninRequest(BaseModel):
    """
    Request model for user signin
    """
    email: str
    password: str

class SignoutRequest(BaseModel):
    """
    Request model for user signout
    """
    token: str

class UpdateProfileRequest(BaseModel):
    """
    Request model for updating user profile
    """
    software_background: Optional[str] = None
    programming_languages: Optional[list] = None
    ai_ml_experience: Optional[str] = None
    hardware_background: Optional[str] = None
    primary_learning_goal: Optional[str] = None

@router.post("/signup")
async def signup(request: Request, signup_data: SignupRequest):
    """
    Register a new user with background information
    """
    try:
        # Extract profile data
        profile_data = signup_data.profile_data or {}

        # Validate password length for bcrypt (max 72 characters)
        if len(signup_data.password) > 72:
            raise HTTPException(status_code=400, detail="Password must be less than 72 characters")

        # Create user with Better Auth
        user = await auth_instance.create_user(
            email=signup_data.email,
            password=signup_data.password,
            name=signup_data.name,
            # Add custom fields
            software_background=profile_data.get("softwareBackground", "beginner"),
            programming_languages=profile_data.get("programmingLanguages", []),
            ai_ml_experience=profile_data.get("aiMlExperience", "learning"),
            hardware_background=profile_data.get("hardwareBackground", "none"),
            primary_learning_goal=profile_data.get("primaryLearningGoal", ""),
            profile_complete=True  # Set to True if profile is complete
        )

        if not user:
            raise HTTPException(status_code=400, detail="Failed to create user")

        # Sign in the user to get a session
        session = await auth_instance.sign_in_with_email_password(
            email=signup_data.email,
            password=signup_data.password
        )

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "software_background": getattr(user, 'software_background', None),
                "programming_languages": getattr(user, 'programming_languages', []),
                "ai_ml_experience": getattr(user, 'ai_ml_experience', None),
                "hardware_background": getattr(user, 'hardware_background', None),
                "primary_learning_goal": getattr(user, 'primary_learning_goal', None),
                "profile_complete": getattr(user, 'profile_complete', False),
                "created_at": user.created_at.isoformat() if hasattr(user, 'created_at') else None,
                "updated_at": user.updated_at.isoformat() if hasattr(user, 'updated_at') else None
            },
            "session": {
                "token": session.access_token if hasattr(session, 'access_token') else '',
                "type": "Bearer"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@router.post("/signin")
async def signin(request: Request, signin_data: SigninRequest):
    """
    Authenticate an existing user
    """
    try:
        # Validate password length for bcrypt (max 72 characters)
        if len(signin_data.password) > 72:
            raise HTTPException(status_code=400, detail="Password must be less than 72 characters")

        # Sign in with Better Auth
        session = await auth_instance.sign_in_with_email_password(
            email=signin_data.email,
            password=signin_data.password
        )

        if not session or not hasattr(session, 'user'):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = session.user

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "software_background": getattr(user, 'software_background', None),
                "programming_languages": getattr(user, 'programming_languages', []),
                "ai_ml_experience": getattr(user, 'ai_ml_experience', None),
                "hardware_background": getattr(user, 'hardware_background', None),
                "primary_learning_goal": getattr(user, 'primary_learning_goal', None),
                "profile_complete": getattr(user, 'profile_complete', False),
                "created_at": user.created_at.isoformat() if hasattr(user, 'created_at') else None,
                "updated_at": user.updated_at.isoformat() if hasattr(user, 'updated_at') else None
            },
            "session": {
                "token": session.access_token if hasattr(session, 'access_token') else '',
                "type": "Bearer"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signin failed: {str(e)}")

@router.post("/signout")
async def signout(request: Request):
    """
    End the current user's session
    """
    try:
        # For Better Auth, signout is typically handled on the client side
        # This endpoint could invalidate tokens server-side if needed
        return {"success": True, "message": "Successfully signed out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signout failed: {str(e)}")

@router.get("/me")
async def get_current_user(request: Request):
    """
    Get current user's profile information
    """
    try:
        # Get user from session
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = auth_header.split(" ")[1]
        user = await auth_instance.verify_token(token)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "software_background": getattr(user, 'software_background', None),
            "programming_languages": getattr(user, 'programming_languages', []),
            "ai_ml_experience": getattr(user, 'ai_ml_experience', None),
            "hardware_background": getattr(user, 'hardware_background', None),
            "primary_learning_goal": getattr(user, 'primary_learning_goal', None),
            "profile_complete": getattr(user, 'profile_complete', False),
            "created_at": user.created_at.isoformat() if hasattr(user, 'created_at') else None,
            "updated_at": user.updated_at.isoformat() if hasattr(user, 'updated_at') else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

@router.put("/me")
async def update_current_user(request: Request, profile_data: UpdateProfileRequest):
    """
    Update current user's profile information
    """
    try:
        # Get user from session
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = auth_header.split(" ")[1]
        user = await auth_instance.verify_token(token)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Update user profile
        updated_user = await auth_instance.update_user(
            user_id=user.id,
            software_background=profile_data.software_background,
            programming_languages=profile_data.programming_languages,
            ai_ml_experience=profile_data.ai_ml_experience,
            hardware_background=profile_data.hardware_background,
            primary_learning_goal=profile_data.primary_learning_goal
        )

        return {
            "user": {
                "id": updated_user.id,
                "email": updated_user.email,
                "name": updated_user.name,
                "software_background": getattr(updated_user, 'software_background', None),
                "programming_languages": getattr(updated_user, 'programming_languages', []),
                "ai_ml_experience": getattr(updated_user, 'ai_ml_experience', None),
                "hardware_background": getattr(updated_user, 'hardware_background', None),
                "primary_learning_goal": getattr(updated_user, 'primary_learning_goal', None),
                "profile_complete": getattr(updated_user, 'profile_complete', False),
                "created_at": updated_user.created_at.isoformat() if hasattr(updated_user, 'created_at') else None,
                "updated_at": updated_user.updated_at.isoformat() if hasattr(updated_user, 'updated_at') else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")