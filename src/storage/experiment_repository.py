from src.storage.base import BaseRepository
from src.schemas.experiment import ExperimentCreate
from src.core.exceptions import StorageError

class ExperimentRepository(BaseRepository):
    
    def create_mru_experiment(self, exp_data: ExperimentCreate, physics_data: dict):
        try:
            # 1. Insertar en la tabla maestra 'experimentos'
            res_exp = self.client.table("experimentos").insert({
                "nombre": exp_data.nombre,
                "tipo": exp_data.tipo
            }).execute()
            
            if not res_exp.data:
                raise StorageError("Insert", "No se pudo crear el experimento maestro")
            
            # Obtener el ID que Supabase generó automáticamente
            nuevo_id = res_exp.data[0]["id"]
            
            # 2. Insertar en 'ensayos_mru' usando ese ID como LLAVE FORÁNEA
            physics_data["experimento_id"] = nuevo_id
            res_physics = self.client.table("ensayos_mru").insert(physics_data).execute()
            
            return {
                "id": nuevo_id,
                "nombre": exp_data.nombre,
                "detalle": res_physics.data[0]
            }
        except Exception as e:
            self._handle_error("create_mru_experiment", str(e))

    def create_mrua_experiment(self, exp_data: ExperimentCreate, physics_data: dict):
        try:
            # Repetimos el proceso para MRUA
            res_exp = self.client.table("experimentos").insert({
                "nombre": exp_data.nombre,
                "tipo": exp_data.tipo
            }).execute()
            
            nuevo_id = res_exp.data[0]["id"]
            
            physics_data["experimento_id"] = nuevo_id
            res_physics = self.client.table("ensayos_mrua").insert(physics_data).execute()
            
            return {
                "id": nuevo_id,
                "nombre": exp_data.nombre,
                "detalle": res_physics.data[0]
            }
        except Exception as e:
            self._handle_error("create_mrua_experiment", str(e))

    def get_all(self) -> list:
        response = self.client.table("experimentos").select("*").execute()
        return response.data

    def get_by_id(self, exp_id: int) -> dict | None:
        response = self.client.table("experimentos").select("*").eq("id", exp_id).execute()
        if not response.data:
            return None
        
        exp = response.data[0]
        # Traemos el detalle correspondiente de manera limpia
        if exp["tipo"] == "MRU":
            det = self.client.table("ensayos_mru").select("*").eq("experimento_id", exp_id).execute()
        else:
            det = self.client.table("ensayos_mrua").select("*").eq("experimento_id", exp_id).execute()
            
        exp["detalle"] = det.data[0] if det.data else {}
        return exp

    def delete(self, exp_id: int) -> bool:
        response = self.client.table("experimentos").delete().eq("id", exp_id).execute()
        return len(response.data) > 0