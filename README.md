# mock-data-generator

### request example
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
