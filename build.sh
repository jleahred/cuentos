#!/usr/bin/env bash
# Genera un manuscrito concatenado a partir de los capítulos.
#
# Uso:
#   ./build.sh                     -> manuscrito.md con los capítulos escritos (1-9)
#   ./build.sh --esbozos           -> añade los capítulos posteriores que existan
#   ./build.sh /tmp/lectura.md     -> escribe en /tmp/lectura.md
#
set -euo pipefail

cd "$(dirname "$0")"

salida="manuscrito.md"
incluir_esbozos=0

for arg in "$@"; do
  case "$arg" in
    --esbozos|--propuesta) incluir_esbozos=1 ;;
    -*) echo "Opción desconocida: $arg" >&2; exit 1 ;;
    *) salida="$arg" ;;
  esac
done

capitulos=(
  "1 triunfador.md"
  "2 fallo.md"
  "3 colapso.md"
  "4 fondo.md"
  "5 vecinos.md"
  "6 calma.md"
  "7 cena.md"
  "8 agravamiento.md"
  "9 panico.md"
  "10 caos.md"
  "11 inaplazable.md"
  "12 cambio.md"
  "13 comienzo.md"
)

if [[ $incluir_esbozos -eq 1 ]]; then
  for cap in "10 "*.md "11 "*.md "12 "*.md "13 "*.md "14 "*.md "15 "*.md; do
    [[ -e "$cap" ]] && capitulos+=("$cap")
  done
fi

: > "$salida"
for cap in "${capitulos[@]}"; do
  [[ -f "$cap" ]] || { echo "Falta: $cap" >&2; exit 1; }
  cat "$cap" >> "$salida"
  printf '\n\n' >> "$salida"
done

echo "Escrito: $salida ($(wc -w < "$salida") palabras)"
