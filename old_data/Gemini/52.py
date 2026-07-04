import os
from typing import Generator, Optional
from fastapi import FastAPI, HTTPException, Request, Response, status, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
import uuid



class User(BaseModel):
    user_id: str
    email: str
    is_authenticated: bool = False

class VideoMetadata(BaseModel):
    video_id: str
    title: str
    owner_id: str
    file_path: str
    content_type: str = "video/mp4"



class IStorageProvider(ABC):
    @abstractmethod
    def get_video_stream(self, file_path: str, start: int, end: int) -> bytes:
        pass

    @abstractmethod
    def get_size(self, file_path: str) -> int:
        pass

class IAuthService(ABC):
    @abstractmethod
    def authenticate_request(self, request: Request) -> User:
        pass



class LocalStorageProvider(IStorageProvider):
    
    def get_size(self, file_path: str) -> int:
        if not os.path.exists(file_path):
            raise FileNotFoundError("Video file not found on disk.")
        return os.path.getsize(file_path)

    def get_video_stream(self, file_path: str, start: int, end: int) -> Generator[bytes, None, None]:
        with open(file_path, "rb") as video_file:
            video_file.seek(start)
            chunk_size = 1024 * 1024  
            remaining = end - start + 1
            while remaining > 0:
                read_size = min(chunk_size, remaining)
                data = video_file.read(read_size)
                if not data:
                    break
                yield data
                remaining -= len(data)

class PasskeyAuthService(IAuthService):
    
    def authenticate_request(self, request: Request) -> User:
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing Authentication")
        return User(user_id="user_123", email="brad@amazon.com", is_authenticated=True)



class VideoStreamingService:
    def __init__(self, storage: IStorageProvider, auth: IAuthService):
        self.storage = storage
        self.auth = auth
        
        self.video_db = {
            "vid_001": VideoMetadata(
                video_id="vid_001", 
                title="System Design at Scale", 
                owner_id="user_123", 
                file_path="sample_video.mp4"
            )
        }

    def get_video_metadata(self, video_id: str) -> VideoMetadata:
        video = self.video_db.get(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video

    def handle_range_request(self, request: Request, video_id: str) -> StreamingResponse:
        video = self.get_video_metadata(video_id)
        file_path = video.file_path
        
        try:
            file_size = self.storage.get_size(file_path)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Video file missing")

        range_header = request.headers.get("Range")
        
        
        start = 0
        end = file_size - 1

        if range_header:
            
            try:
                range_value = range_header.replace("bytes=", "").split("-")
                start = int(range_value[0])
                if range_value[1]:
                    end = int(range_value[1])
            except ValueError:
                raise HTTPException(status_code=416, detail="Requested Range Not Satisfiable")

        
        if start >= file_size or end >= file_size:
            raise HTTPException(status_code=416, detail="Requested Range Not Satisfiable")

        chunk_generator = self.storage.get_video_stream(file_path, start, end)
        
        content_length = end - start + 1
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": video.content_type,
        }

        return StreamingResponse(
            chunk_generator, 
            status_code=status.HTTP_206_PARTIAL_CONTENT, 
            headers=headers
        )



app = FastAPI(title="Amazon-Scale Video Service")


storage_provider = LocalStorageProvider()
auth_service = PasskeyAuthService()
stream_service = VideoStreamingService(storage_provider, auth_service)

@app.get("/health")
async def health_check():
    
    return {"status": "healthy", "region": "us-east-1"}

@app.get("/api/v1/videos/{video_id}/metadata", response_model=VideoMetadata)
async def get_metadata(video_id: str, request: Request):
    
    user = auth_service.authenticate_request(request)
    return stream_service.get_video_metadata(video_id)

@app.get("/api/v1/stream/{video_id}")
async def stream_video(video_id: str, request: Request):
    
    
    
    return stream_service.handle_range_request(request, video_id)

if __name__ == "__main__":
    import uvicorn
    
    
    uvicorn.run(app, host="0.0.0.0", port=8080)