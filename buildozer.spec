[app]

# (string) Title of your application
title = Opataz AI

# (string) Package name
package.name = opatazai

# (string) Package domain (needed for android package name)
package.domain = org.opataz

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,so,cpp,h

# (string) Application version
version = 1.0.0

# (list) Application requirements
# यहाँ hostpython3 और numpy का स्थिर वर्जन जोड़ दिया गया है
requirements = python3,hostpython3,kivy==2.3.0,kivymd==1.2.0,pillow,pandas,numpy==1.26.4

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# =============================================================================
# Android specific configuration
# =============================================================================

fullscreen = 1

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Automatically accept SDK licenses
android.accept_sdk_license = True

android.private_storage = True

android.archs = armeabi-v7a, arm64-v8a

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
