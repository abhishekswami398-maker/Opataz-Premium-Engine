[app]

# (str) Title of your application
title = Opataz AI

# (str) Package name
package.name = opatazai

# (str) Package domain (needed for android packaging)
package.domain = org.opataz

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,csv

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, hostpython3

# (str) Supported orientations
orientation = portrait

# =============================================================================
# Android specific configurations
# =============================================================================

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions (सिर्फ ज़रूरी ताकि बिल्ड टूल्स में गड़बड़ न हो)
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) The Android architectural targets to build for
android.archs = arm64-v8a

# (bool) Allow root execution for buildozer
buildozer.allow_root = 1

[buildozer]

# (int) Log level (इसे 1 कर दिया है ताकि विशालकाय लॉग्स न बनें और ट्रंकेट एरर न आए)
log_level = 1

# (int) Display warning if buildozer is run as root
warn_on_root = 0
