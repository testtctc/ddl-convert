# 数仓开发便利工具

## 简介
数仓开发小工具，减少重复的的复制粘贴

## 技术
python flask + react + typescript

## 用途
- 支持自动转换mysql ddl 到hive/flink/doris ddl
- 支持产生自动填充doris 日期分区
- 支持生成自动解析json的代码

## 启动
#### 调试
python app.py 

#### 生产

gunicorn --workers=4  --bind=0.0.0.0 --port=8085

## 开发

### 编译前端
#### 必备：安装 nodejs

cd webddl && npm install && npm run build

### 后端测试
pytest