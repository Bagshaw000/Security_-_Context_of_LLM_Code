import os
from typing import Generator, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel



class DeviceRegistration(BaseModel):
    device_id: str
    device_type: str
    passkey_public_key: Optional[str] = None

class VideoMetadata(BaseModel):
    video_id: str
    title: str
    file_path: str
    is_premium: bool = False



class VideoStreamingManager:
    
    def __init__(self, chunk_size: int = 1024 * 1024):
        self.chunk_size = chunk_size

    def get_video_range(self, file_path: str, range_header: Optional[str]) -> tuple:
        if not os.path.exists(file_path):
            raise FileNotFoundError("Video asset not found in storage.")

        file_size = os.path.getsize(file_path)
        start, end = 0, file_size - 1

        if range_header:
            
            range_parts = range_header.replace("bytes=", "").split("-")
            start = int(range_parts[0])
            if range_parts[1]:
                end = int(range_parts[1])

        return start, end, file_size

    def stream_generator(self, file_path: str, start: int, end: int) -> Generator[bytes, None, None]:
        with open(file_path, "rb") as video_file:
            video_file.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = video_file.read(min(self.chunk_size, remaining))
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)



class DeviceAuthService:
    
    def __init__(self):
        self.registered_devices = {}

    def provision_remote_key(self, registration: DeviceRegistration):
        
        self.registered_devices[registration.device_id] = {
            "status": "active",
            "auth_method": "passkey" if registration.passkey_public_key else "standard",
            "linked_account": "amazon_user_7782"
        }
        return {"status": "provisioned", "device_id": registration.device_id}

    def verify_session(self, request: Request):
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Device not authenticated")
        return True



app = FastAPI(title="Amazon-Scale Video Streaming Backend")
stream_manager = VideoStreamingManager()
auth_service = DeviceAuthService()


VIDEO_DB = {
    "vid001": VideoMetadata(video_id="vid001", title="System Architecture 101", file_path="assets/demo.mp4"),
    "vid002": VideoMetadata(video_id="vid002", title="Distributed Systems at Scale", file_path="assets/scale.mp4")
}

@app.get("/", response_class=HTMLResponse)
async def index():
    
    return 

@app.post("/device/register", status_code=status.HTTP_201_CREATED)
async def register_device(reg: DeviceRegistration):
    
    return auth_service.provision_remote_key(reg)

@app.get("/stream/{video_id}")
async def stream_video(video_id: str, request: Request):
    
    video = VIDEO_DB.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    try:
        range_header = request.headers.get("range")
        start, end, file_size = stream_manager.get_video_range(video.file_path, range_header)
        
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": "video/mp4",
        }

        return StreamingResponse(
            stream_manager.stream_generator(video.file_path, start, end),
            status_code=206,
            headers=headers
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Physical video file missing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")