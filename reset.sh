
ALT="/var/lib/alternatives"
ALT_CONFIG="${ALT}config"  # Config
ALT_DIR="${ALT}sym/"  # Intermediate location of symlinks

echo 'Removing alternative directory'
rm -rf $ALT

