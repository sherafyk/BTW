import os
from celery import Celery
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup

from .database import SessionLocal
from .models import Article

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery('worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery_app.task
def process_article(article_id: int):
    db: Session = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        db.close()
        return
    try:
        article.status = "fetching"
        db.commit()
        # Simple extraction using requests + BeautifulSoup
        resp = requests.get(article.url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string if soup.title else ''
        article.title = title
        article.content = soup.get_text()[:1000]  # stub
        article.status = "extracted"
        db.commit()
        # Further AI steps would go here
        article.summary = f"Summary of {title}..."  # placeholder
        article.status = "summarized"
        db.commit()
        article.outline = "Outline..."  # placeholder
        article.status = "outlined"
        db.commit()
        article.draft = "Draft article..."  # placeholder
        article.status = "drafted"
        db.commit()
    finally:
        db.close()
