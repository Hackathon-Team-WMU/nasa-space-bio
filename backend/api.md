# API Usage
Health Check Command
```
curl http://localhost:2121/api/health
```

Query Command
```
curl -X POST http://localhost:2121/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test question"}'
```