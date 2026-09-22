#!/usr/bin/env python3
"""
CLI para compartir recursos técnicos en Slack (#guild-engineering).

Genera el mensaje formateado y lo copia al portapapeles (si `pyperclip` está
disponible) para pegarlo directamente en el canal.

Modo interactivo (uso normal):
  python3 tools/guild_post.py

Modo no interactivo (pensado para invocarse desde un agente/script; ver
tools/README.md para el detalle del formato):
  python3 tools/guild_post.py \\
    --title "Título del recurso" \\
    --url "https://..." \\
    --category "Backend & APIs" \\
    --tldr "Primer punto clave" --tldr "Segundo punto clave" \\
    --impact "Por qué esto le importa a R&D"
"""

import argparse
import sys

# Categorías sugeridas
CATEGORIES = [
    "AI & Machine Learning",
    "Backend & APIs",
    "Cloud & Infrastructure",
    "DevOps & CI/CD",
    "Database & Data",
    "Architecture & Patterns",
    "Frontend & UI",
    "Security",
]


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val if val else default


def ask_required(prompt: str) -> str:
    val = ask(prompt)
    while not val:
        print("⚠️ Este campo es obligatorio.")
        val = ask(prompt)
    return val


def select_category() -> str:
    print("\nSelecciona la temática:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  [{i}] {cat}")
    print(f"  [{len(CATEGORIES) + 1}] Otra (personalizada)")

    choice = ask(f"Opción (1-{len(CATEGORIES) + 1})", "1")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(CATEGORIES):
            return CATEGORIES[idx]
        elif idx == len(CATEGORIES):
            return ask_required("Escribe la categoría personalizada")
    except ValueError:
        pass
    return CATEGORIES[0]


def format_message(title: str, url: str, category: str, tldr_bullets: list, impact: str) -> str:
    tldr_block = "\n".join(f"• {b}" for b in tldr_bullets)
    return (
        f"💡 *[Tech Share] · {title}*\n"
        f"🔗 *Enlace:* {url}\n"
        f"🏷️ *Temática:* `{category}`\n\n"
        f"🎯 *TL;DR:*\n{tldr_block}\n\n"
        f"💬 *¿Por qué nos importa en R&D?*\n{impact}\n\n"
        f"🧵 _Debatimos en el hilo._"
    )


def build_message_interactive() -> str:
    print("\n===========================================")
    print("  🚀 Gremio de R&D · Compartir Tech Share")
    print("===========================================\n")

    title = ask_required("📌 Título del recurso / artículo")

    url = ask_required("🔗 Enlace (URL)")
    if not url.startswith(("http://", "https://")):
        print("⚠️ La URL no parece válida (debería empezar con http:// o https://), se usará igual.")

    category = select_category()

    print("\n💡 TL;DR (puntos clave, uno por línea; Enter en blanco para terminar):")
    bullets = []
    while True:
        bullet = ask(f"  • Punto {len(bullets) + 1}")
        if not bullet:
            if bullets:
                break
            print("⚠️ Agrega al menos un punto.")
            continue
        bullets.append(bullet)

    print("\n💬 ¿Por qué nos importa en R&D? / Pregunta disparadora:")
    impact = ask_required("  Impacto o debate")

    return format_message(title, url, category, bullets, impact)


def copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip

        pyperclip.copy(text)
        return True
    except ImportError:
        return False
    except Exception:
        # pyperclip puede fallar si no hay backend de portapapeles disponible
        # (p. ej. en un entorno headless sin xclip/xsel instalado).
        return False


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genera un mensaje de Tech Share para #guild-engineering.",
    )
    parser.add_argument("--title", help="Título del recurso / artículo")
    parser.add_argument("--url", help="Enlace (URL) del recurso")
    parser.add_argument(
        "--category",
        help=f"Temática. Sugeridas: {', '.join(CATEGORIES)} (o cualquier otra libre)",
    )
    parser.add_argument(
        "--tldr",
        action="append",
        metavar="BULLET",
        help="Punto clave del TL;DR. Repite la opción para agregar varios puntos.",
    )
    parser.add_argument("--impact", help="Por qué le importa esto a R&D / disparador de debate")
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="No intentar copiar el mensaje al portapapeles.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    non_interactive_fields = (args.title, args.url, args.tldr, args.impact)

    if any(non_interactive_fields):
        if not all(non_interactive_fields):
            print("⚠️ Para modo no interactivo se requieren --title, --url, --tldr (al menos uno) y --impact.")
            sys.exit(1)
        message = format_message(
            args.title,
            args.url,
            args.category or CATEGORIES[0],
            args.tldr,
            args.impact,
        )
    else:
        try:
            message = build_message_interactive()
        except (KeyboardInterrupt, EOFError):
            print("\n\n✋ Cancelado.")
            sys.exit(1)

    print("\n" + "-" * 50)
    print(message)
    print("-" * 50 + "\n")

    if args.no_clipboard:
        return

    if copy_to_clipboard(message):
        print("📋 ¡Copiado automáticamente al portapapeles! Pégalo en el canal #guild-engineering.")
    else:
        print("💡 Copia el texto delimitado arriba y pégalo en el canal #guild-engineering.")


if __name__ == "__main__":
    main()
