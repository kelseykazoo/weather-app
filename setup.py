from setuptools import setup

APP = ['main.py']
DATA_FILES = ['config.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'weather.icns',  
    'packages': ['requests'],
    'plist': {
        'CFBundleName': 'Weather App',
        'CFBundleDisplayName': 'Weather App',
        'CFBundleIdentifier': 'com.kelseykazoo.weatherapp',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
