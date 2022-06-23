import cx_Freeze

arquivo = [cx_Freeze.Executable(
    script = "Main.py", icon = "data/tetris-img.ico"
)]

cx_Freeze.setup(
    name = "Tetris",
    options = {"build_exe": {"packages": [
        "pygame"] , "include_files":["data"] }},
    executables = arquivo

)