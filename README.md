# mock-data-generator

### API config
```
git clone git@github.com:luizTavolaro/mock-data-generator.git

virtualenv .venv
.venv/bin/activate

pip install -r requiremets.txt

fastapi dev main.py
```

### Request example
```
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{
    "data_inicio": "2024-10-07",
    "quantidade_dias": 5,
    "lim_inf": [0, 0.7],
    "lim_sup": [0.7, 1.9],
    "var": [0, 0]
  }'
```

### Container config
```
docker build -t mock-data-app
docker run -p 80:80 mock-data-app 
```
