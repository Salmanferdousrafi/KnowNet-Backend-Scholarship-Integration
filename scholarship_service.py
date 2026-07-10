"""
Scholarship CRUD, matching, and scoring logic.
"""
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from fastapi import HTTPException, status

from app.models.scholarship import Scholarship
from app.models.user import User
from app.schemas.scholarship import (
    ScholarshipCreate, ScholarshipUpdate, ScholarshipListParams, ScholarshipMatchOut
)
from app.services.ai_service import get_embedding, cosine_similarity

def get_scholarship_by_id(db: Session, scholarship_id: int) -> Optional[Scholarship]:
    return db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()

def list_scholarships(db: Session, params: ScholarshipListParams) -> List[Scholarship]:
    query = db.query(Scholarship)

    if params.active_only:
        query = query.filter(Scholarship.is_active == True)

    if params.search:
        search_term = f"%{params.search}%"
        query = query.filter(
            or_(
                Scholarship.title.ilike(search_term),
                Scholarship.provider.ilike(search_term),
                Scholarship.eligibility_raw.ilike(search_term),
            )
        )

    if params.field:
        query = query.filter(Scholarship.field_tags.any(params.field))

    if params.country:
        query = query.filter(
            or_(
                Scholarship.country_scope.any(params.country),
                Scholarship.country_scope.any("global")
            )
        )

    if params.education_level:
        query = query.filter(Scholarship.education_levels.any(params.education_level))

    # Sorting
    if params.sort_by == "deadline":
        query = query.order_by(
            func.coalesce(Scholarship.deadline, datetime.max.replace(tzinfo=timezone.utc)).asc()
        )
    elif params.sort_by == "created_at":
        query = query.order_by(Scholarship.created_at.desc())
    else:
        query = query.order_by(Scholarship.updated_at.desc())

    offset = (params.page - 1) * params.page_size
    return query.offset(offset).limit(params.page_size).all()

def create_scholarship(db: Session, scholarship_in: ScholarshipCreate) -> Scholarship:
    # Generate embedding from title + eligibility
    embedding = None
    try:
        text = f"{scholarship_in.title}. {scholarship_in.eligibility_raw or ''}"
        embedding = get_embedding(text)
    except Exception:
        pass

    db_scholarship = Scholarship(
        title=scholarship_in.title,
        provider=scholarship_in.provider,
        source_url=scholarship_in.source_url,
        deadline=scholarship_in.deadline,
        amount=scholarship_in.amount,
        eligibility_raw=scholarship_in.eligibility_raw,
        field_tags=scholarship_in.field_tags or [],
        country_scope=scholarship_in.country_scope or [],
        education_levels=scholarship_in.education_levels or [],
        embedding=embedding,
        external_id=scholarship_in.external_id,
        source_feed=scholarship_in.source_feed,
    )
    db.add(db_scholarship)
    db.commit()
    db.refresh(db_scholarship)
    return db_scholarship

def upsert_scholarship_by_url(db: Session, scholarship_in: ScholarshipCreate) -> Scholarship:
    """Update existing scholarship by source_url or create new."""
    existing = db.query(Scholarship).filter(Scholarship.source_url == scholarship_in.source_url).first()
    if existing:
        # Update fields
        for field in ["title", "provider", "deadline", "amount", "eligibility_raw", 
                      "field_tags", "country_scope", "education_levels", "external_id", "source_feed"]:
            val = getattr(scholarship_in, field, None)
            if val is not None:
                setattr(existing, field, val)
        existing.is_active = True
        existing.last_verified_at = datetime.now(timezone.utc)

        # Re-embed
        try:
            text = f"{existing.title}. {existing.eligibility_raw or ''}"
            existing.embedding = get_embedding(text)
        except Exception:
            pass

        db.commit()
        db.refresh(existing)
        return existing
    else:
        return create_scholarship(db, scholarship_in)

def update_scholarship(db: Session, scholarship: Scholarship, scholarship_in: ScholarshipUpdate) -> Scholarship:
    update_data = scholarship_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scholarship, field, value)
    db.commit()
    db.refresh(scholarship)
    return scholarship

def delete_scholarship(db: Session, scholarship: Scholarship) -> None:
    db.delete(scholarship)
    db.commit()

def match_scholarships_for_user(db: Session, user: User, top_k: int = 50) -> List[ScholarshipMatchOut]:
    """
    Rank active scholarships for a user using:
    - 60% semantic similarity (user bio_embedding vs scholarship embedding)
    - 25% rule-based eligibility (field/country/education level match)
    - 15% deadline urgency weighting
    """
    scholarships = db.query(Scholarship).filter(Scholarship.is_active == True).all()
    if not scholarships:
        return []

    now = datetime.now(timezone.utc)
    results = []

    for sch in scholarships:
        # 1. Semantic score (60%)
        semantic_score = 0.0
        if user.bio_embedding and sch.embedding:
            semantic_score = cosine_similarity(user.bio_embedding, sch.embedding)
        elif user.bio and sch.embedding:
            # Fallback: embed user bio on the fly
            try:
                user_emb = get_embedding(user.bio)
                semantic_score = cosine_similarity(user_emb, sch.embedding)
            except Exception:
                semantic_score = 0.0
        semantic_score = max(0.0, min(1.0, semantic_score))

        # 2. Rule-based score (25%)
        rule_score = 0.0
        matches = 0
        total_rules = 0

        # Field match
        if user.field_of_study and sch.field_tags:
            total_rules += 1
            user_field = user.field_of_study.lower()
            if any(user_field in tag.lower() or tag.lower() in user_field for tag in sch.field_tags):
                matches += 1

        # Country match
        if user.country and sch.country_scope:
            total_rules += 1
            user_country = user.country.lower()
            if any(user_country in c.lower() or c.lower() == "global" for c in sch.country_scope):
                matches += 1

        # Education level match
        if user.education_level and sch.education_levels:
            total_rules += 1
            user_level = user.education_level.lower()
            if any(user_level in lvl.lower() for lvl in sch.education_levels):
                matches += 1

        if total_rules > 0:
            rule_score = matches / total_rules

        # 3. Urgency score (15%)
        urgency_score = 0.0
        if sch.deadline:
            days_until = (sch.deadline - now).total_seconds() / 86400
            if days_until < 0:
                urgency_score = 0.0  # Expired
            elif days_until <= 7:
                urgency_score = 1.0
            elif days_until <= 30:
                urgency_score = 0.7
            elif days_until <= 90:
                urgency_score = 0.4
            else:
                urgency_score = 0.2
        else:
            urgency_score = 0.5  # No deadline = moderate urgency

        # Weighted composite
        match_score = (0.60 * semantic_score) + (0.25 * rule_score) + (0.15 * urgency_score)

        match_out = ScholarshipMatchOut(
            id=sch.id,
            title=sch.title,
            provider=sch.provider,
            source_url=sch.source_url,
            deadline=sch.deadline,
            amount=sch.amount,
            eligibility_raw=sch.eligibility_raw,
            field_tags=sch.field_tags,
            country_scope=sch.country_scope,
            education_levels=sch.education_levels,
            is_active=sch.is_active,
            last_verified_at=sch.last_verified_at,
            created_at=sch.created_at,
            updated_at=sch.updated_at,
            source_feed=sch.source_feed,
            external_id=sch.external_id,
            match_score=round(match_score, 4),
            semantic_score=round(semantic_score, 4),
            rule_score=round(rule_score, 4),
            urgency_score=round(urgency_score, 4),
        )
        results.append(match_out)

    # Sort by match score descending
    results.sort(key=lambda x: x.match_score, reverse=True)
    return results[:top_k]
