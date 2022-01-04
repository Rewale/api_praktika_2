from typing import List

from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


class Message(BaseModel):
    text: str


class User(BaseModel):
    id: int
    username: str


class GetVideo(BaseModel):
    user: User
    title: str
    description: str
