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
source.include_exts = py,png,jpg,kv,atlas

# (string) Application version
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,numpy,pandas,pillow,materialyoucolor,exceptiongroup,asyncgui

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# =============================================================================
# Android specific configuration
# =============================================================================

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Automatically accept SDK licenses
android.accept_sdk_license = True

# (bool) Use --private data storage for binary instead of app data
android.private_storage = True

# (str) Format used to package the app for the test/environment (apk or aar)
android.archs = armeabi-v7a, arm64-v8a

# (str) The Android arch to build for
android.allow_backup = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug and outputs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
