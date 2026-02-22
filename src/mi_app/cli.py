from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from .models import EnsayoFisico, MovimientoRectilineoUniforme
from .storage import JSONStorage
from .services import LaboratorioService

from .exceptions import *
app = typer.Typer()
console = Console()

DATA_PATH = Path("data/database.json")

storage = JSONStorage(DATA_PATH)
service = LaboratorioService(storage)

@app.command()
def mru(id: int, nombre: str, velocidad: float, tiempo: float):
    """"""
    try:
        ensayo = MovimientoRectilineoUniforme(
            id = id,
            nombre = nombre,
            tipo = "Movimiento Rectilineo Uniforme",
            velocidad = velocidad,
            tiempo = tiempo
        )

        service.crear_mru(ensayo)

        console.print(f"[bold green]Éxito:[/bold green] Ensayo registrado. Distancia: {ensayo.distancia}m")

    except AppError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@app.command()
def listar():
    """Muestra todos los ensayos guardados en una tabla."""
    ensayos = storage.load()

    if not ensayos:
        console.print(f"[yellow]No hay experimentos registrados.[/yellow]")
        return 
    
    table = Table(title="🔬 Laboratorio de Física - Historial")
    table.add_column("ID", style="cyan")
    table.add_column("Nombre", style="magenta")
    table.add_column("Tipo", style="green")
    table.add_column("Resultado (Distancia/Alcance)", style="yellow")
    table.add_column("Hora Experimento", style="blue")

    for ensayo in ensayos:
        resultado = getattr(ensayo, 'distancia', 'N/A')
        table.add_row(str(ensayo.id), ensayo.nombre, ensayo.tipo, str(resultado), str(ensayo.fecha))

    console.print(table)

if __name__ == "__main__":
    app()
