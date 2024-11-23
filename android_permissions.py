"""
This file is only used when building for Android.
It will be ignored during development.
"""
from kivy.utils import platform

# type: ignore
if platform == 'android':
    from android.permissions import request_permissions, Permission  # type: ignore
    
    def request_android_permissions():
        request_permissions([
            Permission.INTERNET,  # type: ignore
            Permission.READ_EXTERNAL_STORAGE,  # type: ignore
            Permission.WRITE_EXTERNAL_STORAGE  # type: ignore
        ])
