# 本项目采用用fastapi框架,docker部署
开发python版本:3.9
开发环境:windows11

py启动方法:
pip install -r requirements.txt
python3 main.py

docker启动方法:
docker build -t aiqa:latest .
docker run -d --name aiqa -p 5000:5000 aiqa:latest

项目概述:一个非常简单的问答系统,使用fastapi作为web框架,sqlalchemy作为orm,sqlite作为database。运行端口为5000,没有编写配置文件,配置全部都写死在程序中,需要自行修改。
