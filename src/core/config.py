from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Supabase ──────────────────────────────────────────────────────────────
    supabase_url: str
    supabase_key: str
    # ── FastAPI (Personalizado para PhysiLab) ─────────────────────────────────
    api_base_url: str = "http://localhost:8000"
    api_title: str = "PhysiLab API - Laboratorio de Física"
    api_version: str = "1.0.0"

    # ── Entorno ───────────────────────────────────────────────────────────────
    debug: bool = True  # Activado para desarrollo

settings = Settings()