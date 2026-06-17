[app]
title = Opataz AI
package.name = opatazai
package.domain = org.opataz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# शुद्ध लाइटवेट और सबसे स्थिर आवश्यकताओं की सेटिंग
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

icon.filename = icon.png
orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.private_storage = True
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
