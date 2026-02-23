"""Interfaz de línea de comandos para PhysiLab.

Define comandos Typer para crear, listar y eliminar ensayos físicos.
"""

from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from .models import MovimientoRectilineoUniforme
from .storage import JSONStorage
from .services import LaboratorioService

from .exceptions import AppError

app = typer.Typer()
console = Console()

DATA_PATH = Path("data/database.json")

storage = JSONStorage(DATA_PATH)
service = LaboratorioService(storage)


@app.command()
def mru(
    id: int = typer.Option(..., help="ID único del experimento"),
    nombre: str = typer.Option(..., help="Nombre descriptivo"),
    velocidad: float = typer.Option(None, help="Velocidad en m/s"),
    tiempo: float = typer.Option(None, help="Tiempo en segundos"),
    distancia: float = typer.Option(None, help="Distancia en metros"),
) -> None:
    """Crear un ensayo de Movimiento Rectilíneo Uniforme (MRU).

    Exactly one of `velocidad`, `tiempo` o `distancia` may be omitted; el
    servicio calculará la variable faltante y persistirá el ensayo.

    Args:
        id: Identificador único del ensayo.
        nombre: Nombre descriptivo del ensayo.
        velocidad: Velocidad en m/s (opcional).
        tiempo: Tiempo en segundos (opcional).
        distancia: Distancia en metros (opcional).
    """

    try:
        ensayo = MovimientoRectilineoUniforme(
            id=id,
            nombre=nombre,
            tipo="Movimiento Rectilineo Uniforme",
            velocidad=velocidad,
            tiempo=tiempo,
            distancia=distancia,
        )

        service.calcular_mru(ensayo)

        console.print("[bold green]✔[/bold green] Ensayo registrado.")
        console.print(f"Resultados: V={ensayo.velocidad}, T={ensayo.tiempo}, D={ensayo.distancia}")

    except AppError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@app.command()
def listar() -> None:
    """Listar todos los ensayos almacenados en una tabla formateada.

    No toma argumentos; muestra ID, nombre, tipo, resultado y marca temporal.
    """
    ensayos = storage.load()

    if not ensayos:
        console.print("[yellow]No hay experimentos registrados.[/yellow]")
        return

    table = Table(title="🔬 Laboratorio de Física - Historial")
    table.add_column("ID", style="cyan")
    table.add_column("Nombre", style="magenta")
    table.add_column("Tipo", style="green")
    table.add_column("Resultado (Distancia/Alcance)", style="yellow")
    table.add_column("Hora Experimento", style="blue")

    for ensayo in ensayos:
        resultado = getattr(ensayo, "distancia", "N/A")
        table.add_row(str(ensayo.id), ensayo.nombre, ensayo.tipo, str(resultado), str(ensayo.fecha))

    console.print(table)


@app.command()
def eliminar(id: int) -> None:
    """Eliminar un ensayo por su identificador.

    Args:
        id: Identificador del ensayo a eliminar.

    Raises:
        AppError: Si ocurre un error manejado por la capa de servicios.
    """
    try:
        service.eliminar_ensayo(id)
        console.print(f"[bold green]✔[/bold green] Ensayo {id} borrado")
    except AppError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    app()
