import shutil
from typing import List

import ormar
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse

from models import Video, User
from schemas import UploadVideo, Message, GetVideo
from services import write_video

video_router = APIRouter()


@video_router.post("/video")
async def create_video(background_tasks: BackgroundTasks,
                       title: str = Form(...),
                       description: str = Form(...),
                       file: UploadFile = File(...)):
    file_name = f'media/{file.filename}'
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")

    info = UploadVideo(title=title, description=description)
    user = await User.objects.first()
    return await Video.objects.create(file=file_name, user=user, **info.dict())


@video_router.get("/video/{id_video}", response_model=GetVideo, responses={404: {"model": Message}})
async def get_video(id_video: int):
    try:
        return await Video.objects.select_related("user").get(id=id_video)
    except ormar.exceptions.NoMatch:
        return JSONResponse(status_code=404, content=Message(text="No match entity").dict())
