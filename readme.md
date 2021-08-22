# facilities for data warehouse development

## component
python flask + react + typescript

## features
- support auto convert mysql ddl to hive/flink/doris ddl
- support auto fill doris date range
- suport auto parse json stirng  and convert it to  table fields

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