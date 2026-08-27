# Lista de fiabilidad de RouteKit Lite

Ejecuta esta lista en una copia del juego real antes de publicar una actualización.

## Base automatizada

1. Ejecuta el lint de Ren'Py.
2. Ejecuta la suite de RouteKit.
3. Confirma que pasan los casos de migración, rollback, guardado/carga, cálculos y pantallas.

## Recorridos manuales

1. Inicia una partida, cambia el afecto, retrocede una decisión y confirma que regresan el valor y la etapa anteriores.
2. Guarda con un valor no inicial, vuelve a cambiarlo, carga y confirma que regresa el valor guardado.
3. Haz un guardado rápido, cambia varias veces el afecto, carga rápidamente y confirma que la interfaz coincide con el valor.
4. Alcanza repetidamente el mínimo y el máximo y confirma que el valor nunca sale del rango.
5. Cambia el mínimo, máximo y valor inicial configurados; carga una partida anterior y confirma que se limita correctamente.
6. Elimina el personaje configurado en una copia del proyecto, carga una partida anterior y confirma que el juego abre sin errores.
7. Sustituye un valor guardado por datos inválidos, llama `routekit_migrate_state()` y confirma que se utiliza el valor inicial.
8. Prueba la misma partida en Windows y en otra plataforma prevista para el lanzamiento.

Conserva una copia de cada partida de compatibilidad utilizada en una versión pública.
