# RouteKit Lite — Inicio rápido

RouteKit Lite añade puntos de afecto, etapas de relación, una pantalla visual y condiciones para desbloquear contenido en un proyecto de Ren'Py.

## Requisitos

- Ren'Py 8.5.3 o una versión compatible de Ren'Py 8
- Un proyecto que utilice el sistema estándar de pantallas de Ren'Py

## Instalación

1. Copia `routekit_lite.rpy` en la carpeta `game` de tu proyecto.
2. Copia `routekit_config.rpy` en la misma carpeta.
3. Edita el personaje de `routekit_config.rpy`.
4. Abre el proyecto y ejecuta **Check Script (Lint)** desde Ren'Py.

## Cambiar el afecto

Usa una línea de Python después de una decisión:

```renpy
menu:
    "Apoyarla":
        $ routekit_change("maya", 20)

    "Ignorarla":
        $ routekit_change("maya", -10)
```

Para ocultar la notificación, utiliza `False` como tercer argumento:

```renpy
$ routekit_change("maya", 20, False)
```

## Abrir la pantalla de relaciones

```renpy
call screen routekit_relationship_hub
```

## Desbloquear contenido

```renpy
if routekit_can_unlock("maya", 25):
    jump maya_bonus_scene
else:
    "Necesitas 25 puntos de afecto para desbloquear esta escena."
```

## API principal

- `routekit_value(character_id)` — afecto actual
- `routekit_change(character_id, amount, notify=True)` — suma o resta afecto
- `routekit_set(character_id, value, notify=False)` — establece un valor exacto
- `routekit_stage(character_id)` — nombre de la etapa actual
- `routekit_next_stage(character_id)` — siguiente par `(puntos, nombre)` o `None`
- `routekit_points_to_next_stage(character_id)` — puntos restantes
- `routekit_can_unlock(character_id, threshold)` — condición de desbloqueo
- `routekit_reset(notify=False)` — reinicia el estado de RouteKit
- `routekit_migrate_state()` — normaliza inmediatamente una partida antigua o dañada
- `routekit_validate_config()` — devuelve errores de configuración

## Notas

El estado se guarda en una variable `default` de Ren'Py y está cubierto por pruebas reales de rollback y de guardar/cargar. La versión 0.1.2 registra un callback en `config.after_load_callbacks`; no reemplaza el label `after_load` de tu proyecto. Los valores con formato de Pro, inválidos, fuera de rango o pertenecientes a personajes eliminados se normalizan automáticamente después de cargar. La edición Lite admite un personaje configurado.

Lee `LISTA_DE_FIABILIDAD_ES.md` antes de publicar una actualización que cambie personajes o rangos.

## ¿Necesitas rutas más profundas?

RouteKit Pro está disponible para proyectos que necesitan:

- Personajes configurables ilimitados
- Varias estadísticas como afecto, confianza, rivalidad o corrupción
- Eventos con requisitos combinados
- Un panel para varios personajes
- Una galería persistente para repetir escenas
- Colores y etapas de relación configurables

Tú escribes la historia y las decisiones. RouteKit Pro administra el estado compartido, las pantallas, las reglas de desbloqueo, los valores compatibles con partidas guardadas y las repeticiones persistentes.

Consigue RouteKit Pro: https://samokampo.itch.io/routekit-pro
