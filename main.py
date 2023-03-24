from fastapi import FastAPI

from api.routers import gallery

app = FastAPI()

# models.Base.metadata.create_all(engine)

app.include_router(gallery.router)
