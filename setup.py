from cx_Freeze import setup, Executable

# Specify the path to your main script or entry point
script = 'virtualMouse.py'

# Specify additional files or modules that need to be included
additional_files = []
additional_modules = []

# Create the Executable object
executables = [Executable(script)]

# Define the setup parameters
setup(
    name='Your Application Name',
    version='1.0',
    description='Description of your application',
    options={
        'build_exe': {
            'includes': additional_modules,
            'include_files': additional_files,
            'excludes': [],
        }
    },
    executables=executables
)
