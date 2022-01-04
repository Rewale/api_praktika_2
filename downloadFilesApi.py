import shutil
from typing import List
from uuid import uuid4
import ormar
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from models import Video, User
from schemas import UploadVideo, Message, GetVideo, GetListVideo
from services import write_video, save_video, open_file

video_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@video_router.post("/video")
async def create_video(background_tasks: BackgroundTasks,
                       title: str = Form(...),
                       description: str = Form(...),
                       file: UploadFile = File(...)):
    user = await User.objects.first()
    return await save_video(file=file, description=description, title=title, user_id=user.id,
                            background_tasks=background_tasks)


# @video_router.get("/video/{id_video}", response_model=GetVideo, responses={404: {"model": Message}})
# async def get_video(id_video: int):
#     try:
#         file: Video = await Video.objects.select_related("user").get(id=id_video)
#         file_like = open(file.file, mode='rb')
#
#         return StreamingResponse(file_like, media_type='video/mp4')
#     except ormar.exceptions.NoMatch:
#         return JSONResponse(status_code=404, content=Message(text="No match entity").dict())
#     except FileNotFoundError:
#         return JSONResponse(status_code=404, content=Message(text="Video was deleted").dict())


@video_router.get("/video/user/{user_id}", response_model=List[GetListVideo])
async def get_user_video(user_id: int):
    return await Video.objects.filter(user=user_id).all()


@video_router.get("/index/{video_pk}", response_class=HTMLResponse)
async def get_video(req: Request,
                    video_pk: int):
    return templates.TemplateResponse("videoplayer.html", {'request': req, "path": video_pk,
                                                           "title": "TemplateResponse"})


@video_router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response




