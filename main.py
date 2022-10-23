import subprocess
import os
import tempfile
import sys
from tkinter.filedialog import askopenfilename
from pathlib import Path

executable = hasattr(sys, 'frozen')

if executable:
    gnucobol_path = Path("./GnuCOBOL/").resolve()
else:
    gnucobol_path = Path("C:\\Program Files (x86)\\OpenCobolIDE\\GnuCOBOL\\").resolve()
gnucobol_config_path = gnucobol_path / "config"
gnucobol_copy_path = gnucobol_path / "copy"
gnucobol_include_path = gnucobol_path / "include"
gnucobol_lib_path = gnucobol_path / "lib"
gnucobol_extras_path = gnucobol_path / "extras"
gnucobol_bin_path = gnucobol_path / "bin"

envs = {
    "COB_MAIN_DIR": str(gnucobol_path),
    "COB_CONFIG_DIR": str(gnucobol_config_path),
    "COB_COPY_DIR": str(gnucobol_copy_path),
    "COB_CFLAGS": f"-I\"{gnucobol_include_path}\"",
    "COB_LDFLAGS": f"-L\"{gnucobol_lib_path}\"",
    "COB_LIBRARY_PATH": str(gnucobol_extras_path),
    "PATH": f"{gnucobol_bin_path};{os.environ['PATH']}"
}

def set_env():
    for key, value in envs.items():
        os.environ[key] = value

def getfile():
    while True:
        filepath = askopenfilename()
        if not filepath:
            continue
        
        return filepath

def main():
    set_env()
    cobol_file = getfile()
    base_file = os.path.basename(cobol_file)
    exe_file = os.path.splitext(base_file)[0] + '.exe'

    # Compile
    subprocess.run([
        "cobc",
        "-x",
        "-free",
        cobol_file,
        "-o",
        exe_file
    ])

    if os.path.exists(exe_file):
        # Run
        subprocess.run([
            exe_file
        ])

        # Delete executable file
        os.remove(exe_file)

        print(f"\n\nProgram '{base_file}' has exited\nPress any key to continue")
        input("")

if __name__ == "__main__":
    main()