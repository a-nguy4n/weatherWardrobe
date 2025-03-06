import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uuid
from typing import Dict
from contextlib import asynccontextmanager

from database import (
    setup_database,
    get_user_by_username,
    get_user_by_id,
    create_session,
    get_session,
    delete_session,
)



# TODO: 1. create your own user
INIT_USERS = {"alice": "pass123", "bob": "pass456", "michael": "testtest1232"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for managing application startup and shutdown.
    Handles database setup and cleanup in a more structured way.
    """
    # Startup: Setup resources
    try:
        await setup_database(INIT_USERS)  # Make sure setup_database is async
        print("Database setup completed")
        yield
    finally:
        print("Shutdown completed")


# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Static file helpers
def read_html(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def get_error_html(username: str) -> str:
    error_html = read_html("./templates/error.html")
    return error_html.replace("{username}", username)


@app.get("/")
async def root():
    """Redirect users to /login"""
    # TODO: 2. Implement this route
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Show login if not logged in, or redirect to profile page"""
    # TODO: 3. check if sessionId is in attached cookies and validate it
    # if all valid, redirect to /user/{username}
    # if not, show login page
    sessionId = await get_session(request.cookies.get("sessionId"))
    if sessionId:
        user = await get_user_by_id(sessionId["user_id"])
        username = user["usernameLog"]
        return RedirectResponse(url=f"/user/{username}")
    # return HTMLResponse(content=read_html("./templates/loginPage.html"))
    return templates.TemplateResponse("/loginPage.html", {"request": request})


@app.post("/login")
async def login(request: Request):
    """Validate credentials and create a new session if valid"""
    # TODO: 4. Get username and password from form data
    username = (await request.form()).get("usernameLog")
    print(username)
    password = (await request.form()).get("passwordLog")
    # TODO: 5. Check if username exists and password matches
    checkUser = await get_user_by_username(username)
    if not checkUser or checkUser["password"] != password:
        return HTMLResponse(get_error_html(username))
    # TODO: 6. Create a new session
    sessionId = str(uuid.uuid4())
    await create_session(checkUser["id"], sessionId)
    # TODO: 7. Create response with:
    #   - redirect to /user/{username}
    #   - set cookie with session ID
    #   - return the response
    response = RedirectResponse(url=f"/user/{username}", status_code=303)
    response.set_cookie(key="sessionId", value=sessionId)
    return response


@app.post("/logout")
async def logout():
    """Clear session and redirect to login page"""
    # TODO: 8. Create redirect response to /login
    redirect = RedirectResponse(url="/login", status_code=302)
    # TODO: 9. Delete sessionId cookie
    redirect.delete_cookie(key="sessionId")
    # TODO: 10. Return response
    return redirect


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    
    return HTMLResponse(content=read_html("./templates/signUpPage.html"))

@app.get("/user/{username}", response_class=HTMLResponse)
async def user_page(username: str, request: Request):
    """Show user profile if authenticated, error if not"""
    # TODO: 11. Get sessionId from cookies
    sessionId = request.cookies.get("sessionId")
    # TODO: 12. Check if sessionId exists and is valid
    #   - if not, redirect to /login
    session = await get_session(sessionId)
    if not session:
        return RedirectResponse("/login")
    # TODO: 13. Check if session username matches URL username
    #   - if not, return error page using get_error_html with 403 status
    getUser = await get_user_by_id(session["user_id"])
    if getUser is None or getUser["username"] != username:
        return HTMLResponse(content=get_error_html(username), status_code=403)
    # TODO: 14. If all valid, show profile page
    else:
        profile = read_html("./templates/dashboard.html")
        return HTMLResponse(content=profile.replace("{username}", username))


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
