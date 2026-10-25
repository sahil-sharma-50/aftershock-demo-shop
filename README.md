# Demo Shop

A small shop app (FastAPI + Postgres backend, React frontend behind nginx) with
a dashboard, product catalogue/editing, stock adjustment and orders.

## Run

    docker compose up --build

Then open http://localhost:8080. The browser only calls relative `/api/...`
URLs; nginx proxies them to the API container.
