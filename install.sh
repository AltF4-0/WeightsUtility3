#!/bin/bash
set -e

APP_NAME="WeightsUtility3"
REPO="AltF4-0/WeightsUtility3"
VERSION="latest"

INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
APPIMAGE_DEST="${INSTALL_DIR}/${APP_NAME}.AppImage"

mkdir -p "$INSTALL_DIR" "$DESKTOP_DIR" "$ICON_DIR"

if [ "$VERSION" = "latest" ]; then
    DOWNLOAD_URL="https://github.com/${REPO}/releases/latest/download/${APP_NAME}-x86_64.AppImage"
else
    DOWNLOAD_URL="https://github.com/${REPO}/releases/download/${VERSION}/${APP_NAME}-x86_64.AppImage"
fi

echo "==> Downloading ${APP_NAME}"
curl -fL "$DOWNLOAD_URL" -o "$APPIMAGE_DEST"
chmod +x "$APPIMAGE_DEST"

echo "==> Extracting embedded desktop file and icon"
TMPDIR=$(mktemp -d)
pushd "$TMPDIR" > /dev/null
"$APPIMAGE_DEST" --appimage-extract > /dev/null
popd > /dev/null

DESKTOP_SRC=$(find "$TMPDIR/squashfs-root" -maxdepth 1 -name "*.desktop" | head -n1)
ICON_SRC=$(find "$TMPDIR/squashfs-root" -maxdepth 1 \( -name "*.png" -o -name "*.svg" \) | head -n1)
ICON_EXT="${ICON_SRC##*.}"

sed \
    -e "s|^Exec=.*|Exec=${APPIMAGE_DEST}|" \
    -e "s|^Icon=.*|Icon=${APP_NAME,,}|" \
    "$DESKTOP_SRC" > "$DESKTOP_DIR/${APP_NAME,,}.desktop"

cp "$ICON_SRC" "$ICON_DIR/${APP_NAME,,}.${ICON_EXT}"

rm -rf "$TMPDIR"

update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

echo "==> Done. ${APP_NAME} installed to ${INSTALL_DIR}"
echo "==> It should now appear in your application launcher."
