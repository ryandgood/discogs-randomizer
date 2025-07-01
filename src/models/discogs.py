from typing import List, Optional
from pydantic import BaseModel


class Urls(BaseModel):
    next: Optional[str] = None
    last: Optional[str] = None


class Pagination(BaseModel):
    per_page: int
    pages: int
    page: int
    items: int
    urls: Urls


class Format(BaseModel):
    qty: str
    descriptions: List[str]
    name: str


class Label(BaseModel):
    resource_url: str
    entity_type: str
    catno: str
    id: int
    name: str


class Artist(BaseModel):
    id: int
    name: str
    join: str
    resource_url: str
    anv: str
    tracks: str
    role: str


class BasicInformation(BaseModel):
    id: int
    title: str
    year: int
    resource_url: str
    thumb: str
    cover_image: str
    formats: List[Format]
    labels: List[Label]
    artists: List[Artist]
    genres: List[str]
    styles: List[str]


class Note(BaseModel):
    field_id: Optional[int]
    value: Optional[str]


class Release(BaseModel):
    id: int
    instance_id: int
    folder_id: int
    rating: int
    basic_information: BasicInformation
    notes: List[Note] | None = None


class CollectionResponse(BaseModel):
    pagination: Pagination
    releases: List[Release]
