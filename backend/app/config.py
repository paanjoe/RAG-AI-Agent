from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str
    supabase_url: str        # The project URL (e.g., https://your-project.supabase.co)
    supabase_service_key: str # The service_role key, not the anon key
    
    class Config:
        env_file = ".env"

settings = Settings()