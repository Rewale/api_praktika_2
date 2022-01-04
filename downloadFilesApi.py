import shutil
from typing import List
from uuid import uuid4
import ormar
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse

from models import Video, User
from schemas import UploadVideo, Message, GetVideo
from services import write_video, save_video

video_router = APIRouter()


@video_router.post("/video")
async def create_video(background_tasks: BackgroundTasks,
                       title: str = Form(...),
                       description: str = Form(...),
                       file: UploadFile = File(...)):
    user = await User.objects.first()
    return await save_video(file=file, description=description, title=title, user_id=user.id,
                            background_tasks=background_tasks)


@video_router.get("/video/{id_video}", response_model=GetVideo, responses={404: {"model": Message}})
async def get_video(id_video: int):
    try:
        file: Video = await Video.objects.select_related("user").get(id=id_video)
        file_like = open(file.file, mode='rb')

        return StreamingResponse(file_like, media_type='video/mp4')
    except ormar.exceptions.NoMatch:
        return JSONResponse(status_code=404, content=Message(text="No match entity").dict())
    except FileNotFoundError:
        return JSONResponse(status_code=404, content=Message(text="Video was deleted").dict())



