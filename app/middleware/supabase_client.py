from fastapi import HTTPException
from fastapi import UploadFile
from datetime import datetime
from mimetypes import guess_type

from app.core.config import settings

import httpx
import logging
import re
import uuid

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        self.supabase_url = settings.supabase_url
        self.supabase_key = settings.supabase_key
        self.bucket_name = settings.supabase_bucket
        self.clint = httpx.Client()

    def sanitize_filename(self, filename: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

    def build_path(self, folder: str, filename: str) -> str:
        today = datetime.now().strftime("%Y/%m/%d")
        sanatized_filename = self.sanitize_filename(filename)
        unique_filename = f"{uuid.uuid4()}_{sanatized_filename}"

        full_path = f"{folder}/{today}/{unique_filename}"
        return full_path
        
    def upload_to_supabase(self, file: UploadFile, folder: str="uploads") -> str:
        try:
            # sanatized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)
            # unique_filename = f"{uuid.uuid4()}_{sanatized_filename}"
            file_path = self.build_path(folder, file.filename)
            content_type = guess_type(file.filename)[0] or "application/octet-stream"
            file_bytes = file.file.read()
            
            upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{file_path}"
            headers = {
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": content_type,
                "Cache-Control": "3600"
            }

            response = self.clint.put(upload_url, headers=headers, content=file_bytes)

            if response.status_code != 200 and response.status_code != 201:
                logger.error(f"Error uploading file to Supabase: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error uploading file to Supabase: {response.text}"
                )
            
            public_url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{file_path}"
            logger.info(f"File uploaded to Supabase: {public_url}")
            return public_url    

        except Exception as e:
            logger.error(f"Unexpected error uploading file to Supabase: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error uploading file to Supabase: {str(e)}"
            )

