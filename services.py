import shutil
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from starlette.background import BackgroundTasks

from models import Video
from schemas import UploadVideo


async def save_video(file: UploadFile,
                     user_id: int,
                     background_tasks: BackgroundTasks,
                     title: str,
                     description: str):

    file_name = f'media/{user_id}_{uuid4()}.mp4'
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")

    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user_id, **info.dict())


def write_video(file_name: str, file: UploadFile):
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
