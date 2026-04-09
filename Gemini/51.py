import os
from typing import Optional, Generator, Tuple
from fastapi import FastAPI, HTTPException, Header, Request, Response, Depends, status
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel, Field
import uvicorn
from abc import ABC, abstractmethod
import logging
import time




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamingService")



class DeviceProfile(BaseModel):
    device_id: str
    device_type: str  
    capabilities: list[str] = ["h264", "aac"]
    last_authenticated: float = Field(default_factory=time.time)

class VideoMetadata(BaseModel):
    video_id: str
    title: str
    file_path: str
    content_type: str = "video/mp4"
    size_bytes: int



class StorageProvider(ABC):
    @abstractmethod
    def get_video_stream(self, path: str, start: int, end: int) -> Generator[bytes, None, None]:
        pass

    @abstractmethod
    def get_file_size(self, path: str) -> int:
        pass

class LocalStorageProvider(StorageProvider):
    
    def get_file_size(self, path: str) -> int:
        return os.path.getsize(path)

    def get_video_stream(self, path: str, start: int, end: int) -> Generator[bytes, None, None]:
        with open(path, "rb") as video:
            video.seek(start)
            remaining = end - start + 1
            chunk_size = 1024 * 1024  
            while remaining > 0:
                read_size = min(chunk_size, remaining)
                data = video.read(read_size)
                if not data:
                    break
                yield data
                remaining -= len(data)



class DeviceAuthenticator:
    
    def __init__(self):
        self.registered_devices = {}

    async def validate_request(self, x_device_id: Optional[str] = Header(None)):
        if not x_device_id:
            raise HTTPException(status_code=401, detail="Device identity missing")
        
        return x_device_id



class StreamingEngine:
    def __init__(self, storage: StorageProvider):
        self.storage = storage

    def parse_range_header(self, range_header: str, file_size: int) -> Tuple[int, int]:
        
        try:
            range_str = range_header.replace("bytes=", "")
            start_str, end_str = range_str.split("-")
            start = int(start_str)
            end = int(end_str) if end_str else file_size - 1
            return start, min(end, file_size - 1)
        except ValueError:
            return 0, file_size - 1



app = FastAPI(title="Amazon-Scale Video Service")
storage = LocalStorageProvider()
engine = StreamingEngine(storage)
auth = DeviceAuthenticator()


VIDEO_CATALOG = {
    "vid-001": VideoMetadata(
        video_id="vid-001",
        title="Sample Stream",
        file_path="movie.mp4", 
        size_bytes=0 
    )
}

@app.on_event("startup")
def verify_assets():
    for vid in VIDEO_CATALOG.values():
        if os.path.exists(vid.file_path):
            vid.size_bytes = os.path.getsize(vid.file_path)



@app.get("/", response_class=HTMLResponse)
async def index():
    
    return 

@app.get("/stream/{video_id}")
async def stream_video(
    video_id: str,
    request: Request,
    range: Optional[str] = Header(None),
    device_id: str = Depends(auth.validate_request)
):
    
    video = VIDEO_CATALOG.get(video_id)
    if not video or not os.path.exists(video.file_path):
        raise HTTPException(status_code=404, detail="Video not found")

    file_size = video.size_bytes
    start, end = engine.parse_range_header(range if range else "bytes=0-", file_size)
    
    content_length = end - start + 1
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": video.content_type,
    }

    logger.info(f"Streaming {video_id} to device {device_id}: {start}-{end}")

    return StreamingResponse(
        engine.storage.get_video_stream(video.file_path, start, end),
        status_code=206,
        headers=headers
    )

@app.post("/register-device")
async def register_device(profile: DeviceProfile):
    
    
    return {"status": "success", "device_id": profile.device_id, "linked": True}

if __name__ == "__main__":
    
    if not os.path.exists("movie.mp4"):
        with open("movie.mp4", "wb") as f:
            f.write(os.urandom(1024 * 1024 * 10)) 
    
    uvicorn.run(app, host="0.0.0.0", port=8000)