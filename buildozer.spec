[app]
title = Guess the Flag
package.name = guessflag
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*,data/*
version = 0.1

requirements = python3,\
    kivy==2.2.1,\
    pillow

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 23b
android.skip_update = False
android.accept_sdk_license = True
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
