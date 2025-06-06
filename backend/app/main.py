from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, SessionLocal
from .tasks import process_article

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI News Pipeline")
app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit", response_model=schemas.ArticleOut)
async def submit_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = models.article.Article(url=article.url)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    process_article.delay(db_article.id)
    return db_article

@app.get("/articles", response_model=list[schemas.ArticleOut])
async def list_articles(db: Session = Depends(get_db)):
    return db.query(models.article.Article).all()
