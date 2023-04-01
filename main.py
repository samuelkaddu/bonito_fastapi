from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import gallery, user, auth, service, upload

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(engine)

app.include_router(gallery.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(service.router)
app.include_router(upload.router)
