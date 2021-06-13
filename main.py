from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4

app = FastAPI()