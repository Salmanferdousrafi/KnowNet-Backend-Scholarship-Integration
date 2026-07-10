# API Reference

Complete REST API documentation for KnowNet X Backend.

**Base URL:** `https://your-backend.vercel.app/api/v1`

**Authentication:** All endpoints (except `/auth/login` and `/auth/register`) require an `Authorization: Bearer <token>` header.

---

## Authentication

### POST /auth/register
Create a new user account.

**Rate Limit:** 3 requests per minute per IP

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "Alex Chen",
  "field_of_study": "computer_science",
  "country": "US",
  "education_level": "master"
}
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Alex Chen",
  "field_of_study": "computer_science",
  "country": "US",
  "education_level": "master",
  "is_active": true,
  "is_admin": false,
  "created_at": "2026-07-10T12:00:00Z",
  "updated_at": "2026-07-10T12:00:00Z"
}
```

---

### POST /auth/login
Login with email and password. Returns access + refresh tokens.

**Rate Limit:** 5 requests per minute per IP

**Request Body (form-data):**
```
username=user@example.com
password=securepassword123
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### POST /auth/refresh
Rotate refresh token and get a new token pair.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### POST /auth/logout
Revoke the refresh token server-side.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "detail": "Successfully logged out"
}
```

---

## Users

### GET /users/me
Get current authenticated user's profile.

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Alex Chen",
  "field_of_study": "computer_science",
  "country": "US",
  "education_level": "master",
  "bio": "AI researcher passionate about NLP...",
  "bio_embedding": [0.1, 0.2, 0.3, ...],
  "is_active": true,
  "is_admin": false,
  "created_at": "2026-07-10T12:00:00Z",
  "updated_at": "2026-07-10T12:00:00Z"
}
```

---

### PATCH /users/me
Update current user's profile. Bio changes trigger re-embedding.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "full_name": "Alex Chen Updated",
  "field_of_study": "artificial_intelligence",
  "bio": "Updated bio about AI research..."
}
```

**Response (200):** Updated user object

---

## Projects

### GET /projects
List current user's projects. Optionally include public projects from others.

**Query Parameters:**
- `include_public` (boolean, default: false)

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "ML Research Notes",
    "description": "Collection of ML papers",
    "is_public": false,
    "owner_id": 1,
    "created_at": "2026-07-10T12:00:00Z",
    "updated_at": "2026-07-10T12:00:00Z"
  }
]
```

---

### POST /projects
Create a new project.

**Request Body:**
```json
{
  "title": "New Project",
  "description": "Project description",
  "is_public": false
}
```

---

### GET /projects/{project_id}
Get a specific project. Returns 403 if not owner and not public.

---

### PATCH /projects/{project_id}
Update a project. Owner only.

---

### DELETE /projects/{project_id}
Delete a project. Owner only.

---

## Knowledge

### GET /knowledge
List knowledge entries for current user.

**Query Parameters:**
- `project_id` (integer, optional)
- `include_public` (boolean, default: false)

---

### POST /knowledge
Create a new knowledge entry. Auto-generates embedding.

**Request Body:**
```json
{
  "title": "Transformer Architecture",
  "content": "The transformer architecture introduced in 'Attention Is All You Need'...",
  "source_url": "https://arxiv.org/abs/1706.03762",
  "tags": ["ai", "nlp", "deep_learning"],
  "is_public": false,
  "project_id": 1
}
```

---

### POST /knowledge/search
**Semantic AI search** over knowledge entries using Claude embeddings + cosine similarity.

**Request Body:**
```json
{
  "query": "machine learning frameworks for NLP",
  "top_k": 10,
  "project_id": 1
}
```

**Response (200):** List of knowledge entries ranked by semantic relevance

---

## Scholarships

### GET /scholarships
List scholarships with filtering and sorting.

**Query Parameters:**
- `search` (string) — text search in title/provider/eligibility
- `field` (string) — filter by field tag
- `country` (string) — filter by country scope
- `education_level` (string) — filter by education level
- `active_only` (boolean, default: true)
- `sort_by` (string: `deadline`, `created_at`, `relevance`)
- `page` (integer, default: 1)
- `page_size` (integer, default: 20)

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Google Generation Scholarship",
    "provider": "Google",
    "source_url": "https://...",
    "deadline": "2026-12-15T23:59:00Z",
    "amount": "$10,000 USD",
    "eligibility_raw": "Undergraduate students in CS...",
    "field_tags": ["computer_science", "software_engineering"],
    "country_scope": ["global"],
    "education_levels": ["bachelor"],
    "is_active": true,
    "last_verified_at": "2026-07-10T12:00:00Z",
    "created_at": "2026-07-10T12:00:00Z",
    "updated_at": "2026-07-10T12:00:00Z"
  }
]
```

---

### GET /scholarships/match
**AI-powered scholarship matching** for the current authenticated user.

Returns scholarships ranked by composite score:
- **60%** semantic similarity (user bio embedding vs scholarship embedding)
- **25%** rule-based eligibility (field/country/education match)
- **15%** deadline urgency weighting

**Query Parameters:**
- `top_k` (integer, default: 50)

**Response (200):**
```json
[
  {
    "id": 4,
    "title": "Microsoft AI Scholarship",
    "provider": "Microsoft",
    "source_url": "https://...",
    "deadline": "2026-11-30T23:59:00Z",
    "amount": "$15,000 + internship",
    "field_tags": ["artificial_intelligence", "machine_learning"],
    "country_scope": ["US", "Canada"],
    "education_levels": ["master", "phd"],
    "is_active": true,
    "match_score": 0.9234,
    "semantic_score": 0.95,
    "rule_score": 0.85,
    "urgency_score": 0.97,
    "last_verified_at": "2026-07-10T12:00:00Z",
    "created_at": "2026-07-10T12:00:00Z",
    "updated_at": "2026-07-10T12:00:00Z"
  }
]
```

---

### POST /scholarships/demo-seed
Seed demo scholarships for testing. Only works if table is empty.

**Response (201):** List of created scholarships

---

## Admin

### POST /admin/scholarships/trigger-collection
Manually trigger the scholarship collection cycle. **Admin only.**

**Response (200):**
```json
{
  "detail": "Collection cycle completed. 15 scholarships processed.",
  "processed": 15
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes:**
- `400` — Bad Request (validation error)
- `401` — Unauthorized (missing/invalid token)
- `403` — Forbidden (not owner / not admin)
- `404` — Not Found
- `429` — Rate Limit Exceeded
- `500` — Internal Server Error

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `POST /auth/register` | 3/min per IP |
| `POST /auth/login` | 5/min per IP |
| All other endpoints | No limit (protected by auth) |
