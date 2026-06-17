[app]

# (str) Title of your application
title = Opataz AI

# (str) Package name
package.name = opatazai

# (str) Package domain (needed for android packaging)
package.domain = org.opataz

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,csv

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# ध्यान दें: यहाँ kivymd और pillow दोनों को सही तरीके से जोड़ दिया गया है
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, hostpython3

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# =============================================================================
# Android specific configurations
# =============================================================================

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
# मोड 2 में CSV फ़ाइल लोड करने के लिए स्टोरेज परमिशन ज़रूरी है
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android NDK directory (leave empty to download automatically)
android.ndk_path =

# (str) Android SDK directory (leave empty to download automatically)
android.sdk_path =

# (str) ANT directory (leave empty to download automatically)
android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) The Android architectural targets to build for
android.archs = armeabi-v7a, arm64-v8a

# (bool) Allow root execution for buildozer
buildozer.allow_root = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and outputs)
# गिटहब पर एरर को साफ़ देखने के लिए इसे 2 पर रखा गया है
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
