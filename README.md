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
cf push --no-start
cf start bump_hunter
```
