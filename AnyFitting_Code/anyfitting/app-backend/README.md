# Configuration for Virtual-tryon
Pull the docker to local

```
sudo docker pull ccr.ccs.tencentyun.com/hugoycj/csc4001
sudo docker tag ccr.ccs.tencentyun.com/hugoycj/csc4001 tryon
```

# Run deploy scripts
```bash
sh deploy.sh
```

or

```
nvidia-docker run -it -v $pwd:/workspace -p 8009:8009 --name tryon tryon /bin/bash /workspace/run.sh
```

# File structure

├── api_fake.py

├── api.py

├── demo.py # Algorithm testing demo

├── vton.py # Flask backend code

├── Database # Database to store image

├── models # Model file

├── parser # Mysql and COS database API

├── parser # Parsing algorithm api

├── vton -> # Virtural try-on algorithm api

└── remove_api.py # Cloth background remove api
