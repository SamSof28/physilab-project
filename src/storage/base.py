from supabase import create_client, Client
from src.core.config import settings
from src.core.exceptions import StorageError

class BaseRepository:
    """Clase base para todos los repositorios de Supabase."""
    
    def __init__(self) -> None:
        try:
            # Inicializa el cliente usando el Singleton de settings
            self.client: Client = create_client(
                settings.supabase_url, 
                settings.supabase_key
            )
        except Exception as e:
            raise StorageError("Conexión", str(e))

    def _handle_error(self, operation: str, error_detail: str):
        """Centraliza el manejo de errores de la base de datos."""
        raise StorageError(operation, error_detail)