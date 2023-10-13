nvidia-docker rm tryon
nvidia-docker run -it -v /deployment/virtual-tryon:/workspace -p 8009:8008 --name tryon tryon /bin/bash /workspace/run.sh
