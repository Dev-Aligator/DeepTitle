SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Run main.py using the absolute path
python "$SCRIPT_DIR/main.py" "$@"