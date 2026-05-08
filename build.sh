#!/bin/bash
# Build script for Szoftverfejlesztes Vizsgagyakarlo
# Output: dist/SzoftverfejlesztesVizsgagyakarlo.app  (macOS .app bundle)
#         dist/SzoftverfejlesztesVizsgagyakarlo       (single binary, --onefile)

set -e
cd "$(dirname "$0")"

echo "Building macOS app bundle..."

pyinstaller \
    --noconfirm \
    --onefile \
    --windowed \
    --name "SzoftverfejlesztesVizsgagyakarlo" \
    --add-data "data/questions.json:data" \
    --collect-data customtkinter \
    main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Build successful!"
    echo "Executable: $(pwd)/dist/SzoftverfejlesztesVizsgagyakarlo"
    echo ""
    echo "Note: stats.json will be created next to the binary on first run."
else
    echo "Build FAILED"
    exit 1
fi
