from src.storage.base import BaseRepository
from src.schemas.experiment import ExperimentCreate
from src.schemas.mru import MRUSchema

class ExperimentRepository(BaseRepository):
    
    def create_mru_experiment(self, exp_data: ExperimentCreate, physics_data: dict):
        # 1. Insertar en la tabla maestra 'experimentos'
        res_exp = self.client.table("experimentos").insert({
            "nombre": exp_data.nombre,
            "tipo": "MRU"
        }).execute()
        
        if not res_exp.data:
            self._handle_error("Insert Experimento", "No se pudo crear el maestro")
            
        # 2. Obtener el ID generado (El ID heredado)
        new_id = res_exp.data[0]["id"]
        
        # 3. Insertar en la tabla hija 'ensayos_mru' con su PROPIO ID autoincremental
        # y la relación experimento_id
        res_physics = self.client.table("ensayos_mru").insert({
            "experimento_id": new_id,
            "distancia": physics_data["distancia"],
            "velocidad": physics_data["velocidad"],
            "tiempo": physics_data["tiempo"]
        }).execute()
        
        return {"maestro": res_exp.data[0], "detalle": res_physics.data[0]}
    
    def create_mrua_experiment(self, nombre: str, datos: dict):
        # 1. Crear el registro maestro
        res_exp = self.client.table("experimentos").insert({
            "nombre": nombre,
            "tipo": "MRUA"
        }).execute()
        
        new_id = res_exp.data[0]["id"]
        
        # 2. Crear el detalle de física vinculado al id maestro
        datos["experimento_id"] = new_id
        res_physics = self.client.table("ensayos_mrua").insert(datos).execute()
        
        return {"id": new_id, "detalle": res_physics.data[0]}

    def get_all_experiments(self):
        """Consulta que une las tablas para mostrar resultados."""
        return self.client.table("experimentos").select("*, ensayos_mru(*), ensayos_mrua(*)").execute()