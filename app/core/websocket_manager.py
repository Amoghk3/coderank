from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.active_connections = (
            defaultdict(list)
        )

    async def connect(
        self,
        submission_id: str,
        websocket: WebSocket,
    ):

        await websocket.accept()

        self.active_connections[
            submission_id
        ].append(websocket)

    def disconnect(
        self,
        submission_id: str,
        websocket: WebSocket,
    ):

        if (
            websocket
            in
            self.active_connections[
                submission_id
            ]
        ):

            self.active_connections[
                submission_id
            ].remove(websocket)

    async def send_submission_update(
        self,
        submission_id: str,
        data: dict,
    ):

        for websocket in (
            self.active_connections[
                submission_id
            ]
        ):

            await websocket.send_json(data)


manager = ConnectionManager()