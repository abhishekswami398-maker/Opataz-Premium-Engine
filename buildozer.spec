[app]
title = Opataz AI
package.name = opatazai
package.domain = org.opataz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,csv
version = 1.0.0
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, hostpython3
orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.logcat_filters = *:S python:D
android.archs = armeabi-v7a, arm64-v8a
buildozer.allow_root = 1

[buildozer]
log_level = 2
warn_on_root = 0
