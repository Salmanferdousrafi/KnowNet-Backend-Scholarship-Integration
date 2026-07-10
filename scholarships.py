"""
Scholarship router: list, match, admin trigger.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user, require_admin
from app.schemas.user import UserInDB
from app.schemas.scholarship import (
    ScholarshipOut, ScholarshipListParams, ScholarshipMatchOut, ScholarshipCreate
)
from app.services.scholarship_service import (
    get_scholarship_by_id,
    list_scholarships,
    match_scholarships_for_user,
    create_scholarship,
)
from app.scheduler.collector import run_collection_cycle

router = APIRouter(prefix="/scholarships", tags=["scholarships"])

@router.get("", response_model=List[ScholarshipOut])
async def list_scholarships_endpoint(
    params: ScholarshipListParams = Depends(),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """List scholarships with filtering and sorting by deadline."""
    return list_scholarships(db, params)

@router.get("/match", response_model=List[ScholarshipMatchOut])
async def match_scholarships(
    top_k: int = 50,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """
    AI-powered scholarship matching for the current user.
    Scores: 60% semantic similarity + 25% rule-based eligibility + 15% deadline urgency.
    """
    # Ensure user profile is complete enough for matching
    if not current_user.bio and not current_user.field_of_study:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your profile (bio, field of study, country, education level) to get personalized matches."
        )
    return match_scholarships_for_user(db, current_user, top_k=top_k)

@router.get("/{scholarship_id}", response_model=ScholarshipOut)
async def get_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    sch = get_scholarship_by_id(db, scholarship_id)
    if not sch:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return sch

@router.post("/demo-seed", response_model=List[ScholarshipOut], status_code=status.HTTP_201_CREATED)
async def seed_demo_scholarships(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Seed demo scholarships for testing. Only works if table is empty."""
    existing = list_scholarships(db, ScholarshipListParams(page_size=1))
    if existing:
        raise HTTPException(status_code=400, detail="Scholarships already exist. Skipping demo seed.")

    demo_data = [
        ScholarshipCreate(
            title="Google Generation Scholarship",
            provider="Google",
            source_url="https://buildyourfuture.withgoogle.com/scholarships/generation-scholarship",
            deadline="2026-12-15T23:59:00+00:00",
            amount="$10,000 USD",
            eligibility_raw="Undergraduate students in computer science or related fields. Must demonstrate financial need and academic excellence.",
            field_tags=["computer_science", "software_engineering", "data_science"],
            country_scope=["global"],
            education_levels=["bachelor"],
        ),
        ScholarshipCreate(
            title="Rhodes Scholarship",
            provider="Rhodes Trust",
            source_url="https://www.rhodeshouse.ox.ac.uk/",
            deadline="2026-10-01T23:59:00+00:00",
            amount="Full tuition + stipend",
            eligibility_raw="Outstanding students aged 18-24 with demonstrated leadership and academic excellence. All fields accepted.",
            field_tags=["all_fields"],
            country_scope=["global"],
            education_levels=["master", "phd"],
        ),
        ScholarshipCreate(
            title="Fulbright Foreign Student Program",
            provider="U.S. Department of State",
            source_url="https://foreign.fulbrightonline.org/",
            deadline="2026-05-15T23:59:00+00:00",
            amount="Varies by country",
            eligibility_raw="International students seeking to study in the USA. Graduate-level research or study. Varies by home country.",
            field_tags=["all_fields"],
            country_scope=["global"],
            education_levels=["master", "phd"],
        ),
        ScholarshipCreate(
            title="Microsoft AI Scholarship",
            provider="Microsoft",
            source_url="https://www.microsoft.com/en-us/research/careers/",
            deadline="2026-11-30T23:59:00+00:00",
            amount="$15,000 + internship",
            eligibility_raw="Students in AI, machine learning, or NLP. Must be enrolled in a graduate program. US or Canada preferred.",
            field_tags=["artificial_intelligence", "machine_learning", "nlp"],
            country_scope=["US", "Canada"],
            education_levels=["master", "phd"],
        ),
        ScholarshipCreate(
            title="ETH Zurich Excellence Scholarship",
            provider="ETH Zurich",
            source_url="https://ethz.ch/studies/application/master/entry-requirements/excellence-scholarship-opportunity-programme.html",
            deadline="2026-03-15T23:59:00+00:00",
            amount="Full tuition + living expenses",
            eligibility_raw="Outstanding students applying for a Master's program at ETH Zurich. All STEM fields.",
            field_tags=["stem", "engineering", "computer_science", "physics"],
            country_scope=["global"],
            education_levels=["master"],
        ),
        ScholarshipCreate(
            title="Commonwealth Scholarship",
            provider="Commonwealth Scholarship Commission",
            source_url="https://cscuk.fcdo.gov.uk/",
            deadline="2026-09-01T23:59:00+00:00",
            amount="Full funding",
            eligibility_raw="Citizens of Commonwealth countries. Master's or PhD study in the UK. Demonstrated academic merit and development impact.",
            field_tags=["all_fields"],
            country_scope=["Commonwealth"],
            education_levels=["master", "phd"],
        ),
    ]

    created = []
    for sch_in in demo_data:
        created.append(create_scholarship(db, sch_in))
    return created
