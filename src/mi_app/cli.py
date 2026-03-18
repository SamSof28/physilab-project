"""Interfaz de línea de comandos para PhysiLab."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .exceptions import ErrorAplicacion
from .models.mru import MovimientoRectilineoUniforme
from .services import ServicioLaboratorio
from .storage import AlmacenamientoJson

app = typer.Typer()
consola = Console()

RUTA_DATOS = Path("data/database.json")

almacenamiento = AlmacenamientoJson(RUTA_DATOS)
servicio = ServicioLaboratorio(almacenamiento)


@app.command()
def mru(
    id: int = typer.Option(..., help="ID único del experimento"),
    nombre: str = typer.Option(..., help="Nombre descriptivo"),
    velocidad: float = typer.Option(None, help="Velocidad en m/s"),
    tiempo: float = typer.Option(None, help="Tiempo en segundos"),
    distancia: float = typer.Option(None, help="Distancia en metros"),
) -> None:
    """Crea un ensayo de Movimiento Rectilíneo Uniforme (MRU)."""
    try:
        ensayo = MovimientoRectilineoUniforme(
            id=id,
            nombre=nombre,
            tipo="Movimiento Rectilineo Uniforme",
            velocidad=velocidad,
            tiempo=tiempo,
            distancia=distancia,
        )

        servicio.calcular_mru(ensayo)

        consola.print("[bold green]✔[/bold green] Ensayo registrado.")
        consola.print(
            f"Resultados: V={ensayo.velocidad} m/s, T={ensayo.tiempo} s, D={ensayo.distancia} m"
        )

    except ErrorAplicacion as error:
        consola.print(f"[bold red]Error:[/bold red] {error}")


@app.command()
def listar() -> None:
    """Lista todos los ensayos almacenados en una tabla formateada."""
    ensayos = almacenamiento.cargar()

    if not ensayos:
        consola.print("[yellow]No hay experimentos registrados.[/yellow]")
        return

    tabla = Table(title="Laboratorio de Fisica - Historial")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Tipo", style="green")
    tabla.add_column("Resultado (Distancia/Alcance)", style="yellow")
    tabla.add_column("Hora Experimento", style="blue")

    for ensayo in ensayos:
        resultado = getattr(ensayo, "distancia", "N/A")
        tabla.add_row(str(ensayo.id), ensayo.nombre, ensayo.tipo, str(resultado), str(ensayo.fecha))

    consola.print(tabla)


@app.command()
def eliminar(id: int = typer.Option(..., help="ID del experimento a eliminar")) -> None:
    """Elimina un ensayo por su identificador."""
    try:
        servicio.eliminar_ensayo(id)
        consola.print(f"[bold green]✔[/bold green] Ensayo {id} borrado")
    except ErrorAplicacion as error:
        consola.print(f"[bold red]Error:[/bold red] {error}")


if __name__ == "__main__":
    app()
