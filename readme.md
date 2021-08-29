# facilities for data warehouse development


## introduction
To make life easier and less hard coding, I develop this project to help those sql boys/girls
## component
python flask + react + typescript

## features
- support auto convert mysql ddl to hive/flink/doris ddl
- support auto fill doris date range
- support auto parse json stirng  and convert it to  table fields
- support auto parse json stirng  and convert it to  from_json argument
- support auto parse json stirng  and convert it to  hive ddl
- support json format
- list common paramters in hive/flink/spark

## run the project
### debug
python app.py 

### production

gunicorn --workers=4  --bind=0.0.0.0 --port=8085

## development

### compily ts code

####you have to install nodejs first

cd webddl && npm install && npm run build

## test
pytest