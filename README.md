# JobFree

### 一、项目部署

### 1.1docker-compose部署

```sh
# docker build
cd 项目目录/
docker build -f ./docker_env/django/DockerfileBuild -t django_docker_img:v1 .
# 镜像保存
docker save -o django_docker_img.tar django_docker_img:v1

# docker build
# 进项目目录
cd project/
docker build -f ./docker_env/web/DockerfileBuild -t vue_web_img:v1 .
# 镜像保存
docker save -o vue_web_img.tar vue_web_img:v1
# 加载离线镜像
docker load -i django_docker_img.tar
docker load -i vue_web_img.tar
 
 
# docker-compose 创建并启动相应服务
cd 项目目录/
docker-compose up -d
```

