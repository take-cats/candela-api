import os

if os.system("docker --version") == 1:
    print("Docker is not installed. Please install Docker.")
    exit(1)

# Windows
if os.name == "nt":
    os.system("wsl python3 scripts/docker/build.py")
else:
    os.system("docker build -t candela-api .")
