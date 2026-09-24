# Tools

Utilidades de línea de comandos para el gremio de R&D.

## `guild_post.py` — Compartir un Tech Share en Slack

Genera un mensaje formateado para publicar un recurso técnico (artículo, RFC,
librería, paper, etc.) en el canal `#guild-engineering`, y lo copia al
portapapeles automáticamente si `pyperclip` está instalado (`pip install
pyperclip`). No tiene dependencias obligatorias: si `pyperclip` no está
disponible, simplemente imprime el texto para copiarlo manualmente.

El script **no envía nada a Slack directamente** — solo genera el texto. Vos
(o un agente) lo pega en el canal.

### Formato del mensaje

Todo Tech Share sigue esta misma estructura, con 5 campos:

| Campo | Descripción |
|---|---|
| **Título** | Nombre del recurso o artículo que estás compartiendo. |
| **Enlace (URL)** | Link directo al recurso. |
| **Temática** | Categoría del recurso (ver lista sugerida en `CATEGORIES` dentro del script, o una libre). |
| **TL;DR** | *("Too Long; Didn't Read")*: 1 o más bullets muy breves con los puntos clave del recurso — lo mínimo que alguien necesita leer para decidir si le interesa entrar al link. |
| **Impacto / disparador de debate** | Por qué esto le importa al equipo de R&D, o una pregunta para arrancar la conversación en el hilo. |

El mensaje final que se genera (y que se pega en Slack) tiene esta forma:

```
💡 *[Tech Share] · <Título>*
🔗 *Enlace:* <URL>
🏷️ *Temática:* `<Temática>`

🎯 *TL;DR:*
• <bullet 1>
• <bullet 2 (opcional, pueden ser más)>

💬 *¿Por qué nos importa en R&D?*
<Impacto o pregunta disparadora>

🧵 _Debatimos en el hilo._
```

### Uso interactivo

Pensado para una persona ejecutándolo en su terminal: el script pregunta cada
campo uno por uno.

```bash
python3 tools/guild_post.py
```

### Uso no interactivo (para invocar desde un agente o script)

Si ya tenés los 5 campos resueltos (por ejemplo, un agente que acaba de leer
un artículo y armó el resumen), podés pasarlos todos por flags y el script
genera el mensaje sin hacer ninguna pregunta:

```bash
python3 tools/guild_post.py \
  --title "Structured Outputs en Claude" \
  --url "https://docs.claude.com/structured-outputs" \
  --category "Backend & APIs" \
  --tldr "Permite forzar JSON schema en la respuesta" \
  --tldr "Reduce parsing errors en integraciones" \
  --impact "Podríamos usarlo en el pipeline de ingesta" \
  --no-clipboard
```

- `--tldr` se puede repetir tantas veces como bullets quieras (al menos uno es obligatorio).
- `--category` es libre: podés usar una de las sugeridas en el script o cualquier otra.
- `--no-clipboard` evita que intente copiar al portapapeles (recomendado en entornos sin sesión gráfica, como el de un agente).

El modo no interactivo se activa apenas se pasa cualquiera de `--title`,
`--url`, `--tldr` o `--impact`; en ese caso los cuatro pasan a ser
obligatorios (si falta alguno, el script avisa y termina sin generar nada).

En ambos modos, el mensaje final se imprime en la terminal delimitado por
líneas `---`, listo para copiar y pegar en `#guild-engineering`.
