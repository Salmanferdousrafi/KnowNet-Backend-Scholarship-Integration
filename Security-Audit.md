# Security Audit & Architecture Gaps

This document tracks all security fixes applied and remaining gaps to address.

---

## ✅ Fixed Vulnerabilities

### 1. Broken Authentication (OWASP A07)
**Before:** Token accepted as plain function parameter or query string.
**After:** `OAuth2PasswordBearer` with `Authorization: Bearer <token>` header via FastAPI `Depends()`.

**File:** `app/core/deps.py`
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    # ... validation
```

---

### 2. Insecure Direct Object References (IDOR) (OWASP A01)
**Before:** Any authenticated user could access any project/knowledge by guessing IDs.
**After:** Every read/write verifies `resource.owner_id == current_user.id` before returning data.

**File:** `app/services/project_service.py`
```python
def verify_project_owner_write(project: Project, user_id: int) -> None:
    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to modify this project")
```

---

### 3. Hardcoded Secrets (OWASP A05)
**Before:** `JWT_SECRET = "dev-secret-123"` fallback in code.
**After:** App refuses to boot if `JWT_SECRET` or `DATABASE_URL` is missing from environment.

**File:** `app/core/config.py`
```python
if not settings.jwt_secret or len(settings.jwt_secret) < 32:
    raise RuntimeError("FATAL: JWT_SECRET must be at least 32 characters")
```

---

### 4. Missing Session Management
**Before:** Single long-lived JWT token.
**After:** Short-lived access tokens (30 min) + revocable refresh tokens (7 days) stored as SHA-256 hashes.

**File:** `app/services/auth_service.py`
```python
def issue_token_pair(db: Session, user: User):
    access_token = create_access_token({"sub": user.email})
    raw_refresh, token_hash = create_refresh_token({"sub": user.email})
    # Store hash in DB for revocation
    db_token = RefreshToken(user_id=user.id, token_hash=token_hash, ...)
```

---

### 5. Missing Rate Limiting (OWASP A07)
**Before:** No rate limits on auth endpoints.
**After:** `slowapi` limits: `/login` 5/min, `/register` 3/min per IP.

**File:** `app/routers/auth.py`
```python
@router.post("/register")
@limiter.limit(get_settings().rate_limit_register)  # 3/minute
async def register(...):
```

---

### 6. Insecure Search (SQL Injection Risk)
**Before:** Plain SQL `ILIKE` text search.
**After:** Semantic search via Claude embeddings + cosine similarity ranking.

**File:** `app/services/knowledge_service.py`
```python
def semantic_search_knowledge(db, user_id, search_query):
    query_embedding = get_embedding(search_query.query)
    scored = [(cosine_similarity(query_embedding, entry.embedding), entry) 
              for entry in accessible_entries]
    return sorted(scored, key=lambda x: x[0], reverse=True)[:search_query.top_k]
```

---

## ⚠️ Remaining Gaps (Action Required)

### Gap 1: Embedding Provider
**Risk:** Current `get_embedding()` uses deterministic fallback, not real semantic vectors.
**Fix:** Integrate Voyage AI or OpenAI embeddings for production.
**Priority:** HIGH
**Effort:** 2 hours

### Gap 2: HTTPS Enforcement
**Risk:** No redirect from HTTP to HTTPS.
**Fix:** Add `TrustedHostMiddleware` and HSTS headers.
**Priority:** MEDIUM
**Effort:** 30 minutes

### Gap 3: Input Sanitization
**Risk:** Raw HTML in knowledge content not sanitized before storage.
**Fix:** Add `bleach` library to strip dangerous tags.
**Priority:** MEDIUM
**Effort:** 1 hour

### Gap 4: Missing Email Verification
**Risk:** Anyone can register with any email.
**Fix:** Add SendGrid/Resend integration for verification emails.
**Priority:** LOW
**Effort:** 4 hours

### Gap 5: Missing Password Reset
**Risk:** Users cannot recover forgotten passwords.
**Fix:** Add secure token-based password reset flow.
**Priority:** LOW
**Effort:** 3 hours

### Gap 6: No Audit Logging
**Risk:** No record of who accessed what data.
**Fix:** Add middleware to log all auth'd requests.
**Priority:** LOW
**Effort:** 2 hours

### Gap 7: File Uploads Not Covered
**Risk:** If existing app has file uploads, no virus scanning or size limits.
**Fix:** Add ClamAV integration and S3 presigned URLs.
**Priority:** LOW (if no uploads)
**Effort:** 4 hours

### Gap 8: No Backup Strategy
**Risk:** Database loss = total data loss.
**Fix:** Enable Supabase automated backups (already included in free tier).
**Priority:** MEDIUM
**Effort:** 5 minutes (toggle in dashboard)

---

## Security Checklist

- [x] OAuth2PasswordBearer with Bearer header
- [x] Resource ownership verification (IDOR fix)
- [x] Environment-only secrets with hard fail
- [x] Short-lived access + revocable refresh tokens
- [x] Rate limiting on auth endpoints
- [x] Semantic search (no SQL injection)
- [x] CORS configured for specific origins
- [x] Password hashing with bcrypt
- [x] JWT minimum secret length (32 chars)
- [ ] HTTPS redirect middleware
- [ ] Input sanitization (bleach)
- [ ] Email verification
- [ ] Password reset
- [ ] Audit logging
- [ ] Automated DB backups enabled
- [ ] Real embedding provider (Voyage AI)
