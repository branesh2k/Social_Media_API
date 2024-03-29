from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(
        models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={id} not found")
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def new_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    newpost = models.Posts(owner_id=current_user.id, **post.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Requested action not authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_post_query = db.query(models.Posts).filter(models.Posts.id == id)
    updated_post = updated_post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={id} not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Requested action not authorized")

    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post
