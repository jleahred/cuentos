#!/usr/bin/env bash
# Genera un manuscrito concatenado a partir de los capítulos.
#
# Uso:
#   ./build.sh                     -> manuscrito.md con los capítulos 1-5
#   ./build.sh --propuesta         -> manuscrito.md con 1-5 + propuesta/6-9
#   ./build.sh /tmp/lectura.md     -> escribe en /tmp/lectura.md
#
set -euo pipefail

cd "$(dirname "$0")"

salida="manuscrito.md"
incluir_propuesta=0

for arg in "$@"; do
  case "$arg" in
    --propuesta) incluir_propuesta=1 ;;
    -*) echo "Opción desconocida: $arg" >&2; exit 1 ;;
    *) salida="$arg" ;;
  esac
done

capitulos=(
  "1 triunfador.md"
  "2 fallo.md"
  "3 colapso.md"
  "4 fondo.md"
  "5 calma.md"
)

if [[ $incluir_propuesta -eq 1 ]]; then
  capitulos+=(
    "propuesta/6 territorio neutral.md"
    "propuesta/7 el soplo.md"
    "propuesta/8 riesgo.md"
    "propuesta/9 genio.md"
  )
fi

: > "$salida"
for cap in "${capitulos[@]}"; do
  [[ -f "$cap" ]] || { echo "Falta: $cap" >&2; exit 1; }
  cat "$cap" >> "$salida"
  printf '\n\n' >> "$salida"
done

echo "Escrito: $salida"
