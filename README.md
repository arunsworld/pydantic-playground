# Pydantic AI playground

# Setup

```
pip install -r requirements.txt
cp .env.example .env               (then modify it)
```

# Running multi-agent service

```
APP_PORT=9010 python -m multi-agent.main
```

# Running mcp server

```
python mcp-auth/server.py 8910      (node 1)
python mcp-auth/server.py 8911      (node 2)
```

# Running mcp client (CLI)

```
python mcp-auth/client.py
```

# Running mcp client (AG-UI)

```
python mcp-auth-agui/client.py 9010     (node 1)
python mcp-auth-agui/client.py 9011     (node 2)
```

# Load Balancing

* See ```load-balancer``` directory

# Performance testing

```
./load-tester/agui_perf_testing -endpoint="http://localhost:1961" -c=10
```