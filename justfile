import? 'adamghill.justfile'
import? '../dotfiles/just/justfile'

# List commands
_default:
    just --list --unsorted --justfile {{ justfile() }} --list-heading $'Available commands:\n'

# Grab default `adamghill.justfile` from GitHub
fetch:
  curl https://raw.githubusercontent.com/adamghill/dotfiles/master/just/justfile > adamghill.justfile

serve port='8024':
  uv run --all-extras coltrane play --port {{ port }}

serve-js:
  uv run --all-extras coltrane play --port 8024

serve-css:
  uv run --all-extras coltrane play --port 8025
