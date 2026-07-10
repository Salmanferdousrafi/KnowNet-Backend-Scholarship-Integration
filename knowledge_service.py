"""
Knowledge CRUD with semantic search via Claude embeddings.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.knowledge import Knowledge
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate, KnowledgeSearchQuery
from app.services.ai_service import get_embedding, cosine_similarity

def get_knowledge_by_id(db: Session, knowledge_id: int) -> Optional[Knowledge]:
    return db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()

def list_user_knowledge(db: Session, user_id: int, project_id: Optional[int] = None, include_public: bool = False) -> List[Knowledge]:
    query = db.query(Knowledge).filter(Knowledge.owner_id == user_id)
    if project_id is not None:
        query = query.filter(Knowledge.project_id == project_id)
    if include_public:
        query = query.union(
            db.query(Knowledge).filter(Knowledge.is_public == True, Knowledge.owner_id != user_id)
        )
    return query.order_by(Knowledge.updated_at.desc()).all()

def create_knowledge(db: Session, user_id: int, knowledge_in: KnowledgeCreate) -> Knowledge:
    # Generate embedding for the content
    embedding = None
    try:
        text_to_embed = f"{knowledge_in.title}. {knowledge_in.content}"
        embedding = get_embedding(text_to_embed)
    except Exception:
        pass  # Non-fatal; can be re-embedded later

    db_knowledge = Knowledge(
        owner_id=user_id,
        project_id=knowledge_in.project_id,
        title=knowledge_in.title,
        content=knowledge_in.content,
        source_url=knowledge_in.source_url,
        tags=knowledge_in.tags or [],
        embedding=embedding,
        is_public=knowledge_in.is_public,
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

def update_knowledge(db: Session, knowledge: Knowledge, knowledge_in: KnowledgeUpdate) -> Knowledge:
    update_data = knowledge_in.model_dump(exclude_unset=True)

    # Re-embed if title or content changed
    if "title" in update_data or "content" in update_data:
        try:
            text_to_embed = f"{update_data.get('title', knowledge.title)}. {update_data.get('content', knowledge.content)}"
            update_data["embedding"] = get_embedding(text_to_embed)
        except Exception:
            pass

    for field, value in update_data.items():
        setattr(knowledge, field, value)
    db.commit()
    db.refresh(knowledge)
    return knowledge

def delete_knowledge(db: Session, knowledge: Knowledge) -> None:
    db.delete(knowledge)
    db.commit()

def verify_knowledge_owner(knowledge: Knowledge, user_id: int) -> None:
    if knowledge.owner_id != user_id and not knowledge.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this knowledge entry"
        )

def verify_knowledge_owner_write(knowledge: Knowledge, user_id: int) -> None:
    if knowledge.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this knowledge entry"
        )

def semantic_search_knowledge(db: Session, user_id: int, search_query: KnowledgeSearchQuery) -> List[Knowledge]:
    """
    Semantic search: embed query, compute cosine similarity against all accessible knowledge entries.
    Returns top_k results sorted by similarity.
    """
    # Get all accessible knowledge (owned + public)
    query = db.query(Knowledge).filter(
        or_(Knowledge.owner_id == user_id, Knowledge.is_public == True)
    )
    if search_query.project_id is not None:
        query = query.filter(Knowledge.project_id == search_query.project_id)

    entries = query.all()

    if not entries:
        return []

    # Embed the search query
    try:
        query_embedding = get_embedding(search_query.query)
    except Exception:
        # Fallback to basic text search if embedding fails
        return [e for e in entries if search_query.query.lower() in (e.title + e.content).lower()][:search_query.top_k]

    # Score each entry by cosine similarity
    scored = []
    for entry in entries:
        if entry.embedding:
            score = cosine_similarity(query_embedding, entry.embedding)
        else:
            # Fallback: simple text overlap score
            text = (entry.title + " " + entry.content).lower()
            query_words = set(search_query.query.lower().split())
            text_words = set(text.split())
            overlap = len(query_words & text_words)
            score = overlap / max(len(query_words), 1) * 0.5  # Cap fallback at 0.5
        scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:search_query.top_k]]
