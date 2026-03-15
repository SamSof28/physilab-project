# Arquitectura

Esta seccion describe las decisiones de diseno que estructuran el proyecto.

## Uso de src layout

El codigo fuente vive bajo `src/mi_app`, evitando importaciones accidentales desde la raiz del repositorio y mejorando la separacion entre codigo, pruebas y configuracion.

Beneficios:

- imports mas confiables en desarrollo y CI;
- estructura clara para empaquetado;
- menor acoplamiento con scripts externos.

## Separacion por capas

El proyecto esta organizado en capas con responsabilidades explicitas:

- `cli.py`: adaptador de entrada/salida para linea de comandos.
- `services.py`: logica de negocio y formulas fisicas.
- `models/`: entidades de dominio y validaciones en dataclasses.
- `storage.py`: persistencia JSON desacoplada por protocolo.

Flujo tipico:

1. CLI recibe argumentos.
2. Se construye un modelo de dominio.
3. El servicio valida y calcula datos faltantes.
4. Storage persiste y recupera los ensayos.

## Principios de codigo limpio aplicados

- Responsabilidad unica: cada modulo tiene una funcion dominante.
- Bajo acoplamiento: servicio depende de abstraccion de storage.
- Nombres de dominio: metodos y clases expresan conceptos fisicos.
- Validacion temprana: modelos y servicios detectan datos invalidos pronto.
- Excepciones de dominio: errores con significado especifico para el problema.

## Escalabilidad

El diseno actual permite crecer en dos direcciones:

- nuevos modelos fisicos (por ejemplo, tiro parabolico) sin modificar la CLI existente de forma invasiva;
- nuevas implementaciones de persistencia (SQL, API remota) respetando la misma interfaz.
