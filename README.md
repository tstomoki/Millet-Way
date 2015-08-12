# Structure
- bluemix
  bluemixに載せるときのファイル(本番用)
- locals
  ローカル環境で作成するアプリ
- materials
  その他資料等

```
./
├── bluemix
├── locals
└── materials
```

# Deployment
```
cd locals/road_condition_detector
cf push bump_hunter --no-manifest --no-start -b https://github.com/cloudfoundry/python-buildpack -c "sh run.sh"
cf start bump_hunter
```
