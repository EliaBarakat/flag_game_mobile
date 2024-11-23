[app]
title = Guess the Flag
package.name = guesstheflag
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*,data/*
source.exclude_patterns = android_permissions.py
version = 0.1
requirements = python3,kivy==2.2.1,pillow,plyer

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
