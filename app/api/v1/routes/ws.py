from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.core.websocket_manager import (
    manager,
)


router = APIRouter(
    tags=["WebSockets"],
)


@router.websocket(
    "/ws/submissions/{submission_id}"
)
async def websocket_submission_updates(
    websocket: WebSocket,
    submission_id: str,
):

    await manager.connect(
        submission_id,
        websocket,
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(
            submission_id,
            websocket,
        )