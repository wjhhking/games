from setuptools import setup
import sys
import os
sys.setrecursionlimit(10000)  # Keep this increased limit

# Get all audio files from the sounds directory
def get_audio_files():
    audio_files = []
    sounds_dir = 'sounds'  # Adjust this to your audio files directory
    if os.path.exists(sounds_dir):
        for file in os.listdir(sounds_dir):
            if file.endswith(('.mp3', '.wav')):
                audio_files.append(os.path.join(sounds_dir, file))
    return [('sounds', audio_files)] if audio_files else []

APP = ['dance_with_me.py']
DATA_FILES = get_audio_files()  # Include audio files in the bundle
OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'mediapipe',
        'cv2',
        'PIL',
        'playsound',
        'pytubefix',
        'numpy',
        'AppKit',  # Add macOS audio support
        'Foundation',  # Add macOS audio support
        'objc',  # Add macOS audio support
        'simpleaudio',  # Add simpleaudio as backup
    ],
    'includes': [
        'PIL._tkinter_finder',
        'numpy.core._methods',
        'numpy.lib.format',
        'playsound',
        'AppKit',
        'Foundation',
        'objc',
        'simpleaudio',
    ],
    'resources': ['sounds'],  # Include sounds directory as a resource
    'excludes': [
        'matplotlib', 'PyQt5', 'pandas', 'notebook',
        'jupyter', 'IPython', 'scipy', 'zmq', 'torch',
        'jax', 'sympy', 'sphinx', 'babel', 'tomli',
        'filelock', 'setuptools', 'pip', 'wheel'
    ],
    'frameworks': ['AVFoundation', 'CoreAudio'],  # Add more audio frameworks
    # 'iconfile': 'app_icon.icns',  # Comment out or remove this line
    'plist': {
        'CFBundleName': 'Dance With Me',
        'CFBundleDisplayName': 'Dance With Me',
        'CFBundleIdentifier': 'com.yourcompany.dancewithme',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSCameraUsageDescription': 'This app needs access to the camera for pose detection.',
        'NSMicrophoneUsageDescription': 'This app needs access to the microphone.',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.games',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 