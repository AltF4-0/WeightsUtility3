# WeightsUtility3
Alvie Farm's utility to automate the creation of spreadsheets and PDFs for record keeping in relation to the weight of loads on vehicles.

Install (Linux):

curl -fsSL https://raw.githubusercontent.com/AltF4-0/WeightsUtility3/main/install.sh | bash

This downloads the latest AppImage from the Releases page and installs it to ~/.local/bin, with a desktop launcher entry and icon set up automatically.

Alternatively, download install.sh from a release and inspect it before running:

chmod +x install.sh
./install.sh

Requirements:

glibc ≥ 2.43
x86_64 Linux

Supported platforms:

Built and tested on Fedora Linux 44 (glibc 2.43). It's likely to run on other modern distributions with a comparable or newer glibc version (e.g. recent Ubuntu, Debian, Arch, openSUSE releases). This isn't actively tested outside Fedora 44, so results elsewhere may vary.

License:

GPL-3.0 (required due to the PyQt6 dependency). See LICENSE.
