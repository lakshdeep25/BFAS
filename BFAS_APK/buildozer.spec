[app]
# (str) Title of your application
title = BFAS

# (str) Package name
package.name = bfas

# (str) Package domain (used for package name)
package.domain = org.bfas

# (str) Source code directory (typically '.')
source.dir = .

# (str) Application versioning
version = 1.0

# (list) List of requirements
requirements = python3,kivy,kivymd

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Presplash image filename (no path)
presplash.filename = %(source.dir)s/images/presplash.png

# (str) Icon filename (no path)
icon.filename = %(source.dir)s/images/icon.png

# (str) Supported platforms
android.ndk = 19b
android.api = 29
android.minapi = 21
android.sdk = 28

[buildozer]
log_level = 2
warn_on_root = 1
