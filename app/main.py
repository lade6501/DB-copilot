from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

from services.query_service import QueryService
from db.schema_loader import SchemaLoader

app = FastAPI()

service = QueryService()

schema_loader = SchemaLoader(
    db_type="sql",
    config={"db_path": "test.db"}
)


@app.get("/")
def root():
    return {"message": "DB Copilot API running 🚀"}


@app.websocket("/ws/query")
async def websocket_query(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            user_query = payload.get("query")

            schema = schema_loader.load()

            try:
                for step in service.run_stream(user_query, schema):
                    await websocket.send_text(json.dumps(step))

                await websocket.send_text(json.dumps({
                    "step": "done"
                }))

            except Exception as e:
                await websocket.send_text(json.dumps({
                    "step": "error",
                    "message": str(e)
                }))

    except WebSocketDisconnect:
        print("Client disconnected")