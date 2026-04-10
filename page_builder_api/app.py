from fastapi import FastAPI

from page_builder_api.routers import auth, projects, users

app = FastAPI()

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(auth.router)
