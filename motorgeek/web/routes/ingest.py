"""Web routes for agentic ingestion — paste, review, chat, save."""

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from motorgeek.core.database import get_session as db_session
from motorgeek.core.ingest import (
    create_session,
    get_session_by_id,
    process_session,
    respond_to_session,
    save_session,
    transition,
)
from motorgeek.core.models import IngestSessions
from motorgeek.web.app import templates


def _render_review(request: Request, session_obj: IngestSessions) -> HTMLResponse:
    """Render the full review page with current session state."""
    return templates.TemplateResponse(request, "ingest/review.html", {
        "session": session_obj,
        "parsed": session_obj.parsed_data or {},
        "messages": session_obj.agent_messages or [],
        "can_respond": session_obj.status in ("awaiting_response", "enriched"),
    })


async def ingest_page(request: Request) -> HTMLResponse:
    """GET /ingest — paste form."""
    return templates.TemplateResponse(request, "ingest/paste.html")


async def ingest_create(request: Request) -> HTMLResponse:
    """POST /ingest — create session, run agent, redirect to review (or return HTMX partial)."""
    form = await request.form()
    raw_paste = form.get("raw_paste", "").strip()
    if not raw_paste:
        return templates.TemplateResponse(request, "ingest/paste.html", {
            "error": "Please paste some car data first.",
        })

    source_url = form.get("source_url", "").strip() or None
    source_site = form.get("source_site", "").strip() or None
    family = form.get("family", "").strip() or None
    is_htmx = request.headers.get("HX-Request") == "true"

    db = db_session()
    try:
        session_obj = create_session(db, raw_paste, source_url=source_url, source_site=source_site)
        process_session(db, session_obj.id, family=family)
        if is_htmx:
            return templates.TemplateResponse(request, "ingest/_result.html", {
                "session": session_obj,
                "parsed": session_obj.parsed_data or {},
                "messages": session_obj.agent_messages or [],
            })
        return RedirectResponse(url=f"/ingest/{session_obj.id}", status_code=303)
    except Exception as e:
        if is_htmx:
            return HTMLResponse(f'<div class="ingest-result" style="border-color: #f85149;"><strong>Error:</strong> {e}</div>')
        return templates.TemplateResponse(request, "ingest/paste.html", {
            "error": f"Agent processing failed: {e}",
        })


async def ingest_review(request: Request, session_id: int) -> HTMLResponse:
    """GET /ingest/{id} — review page."""
    db = db_session()
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        return HTMLResponse("Session not found", status_code=404)
    return _render_review(request, session_obj)


async def ingest_message(request: Request, session_id: int) -> HTMLResponse:
    """POST /ingest/{id}/message — send a message to the agent (HTMX)."""
    form = await request.form()
    message = form.get("message", "").strip()
    if not message:
        return HTMLResponse("")

    db = db_session()
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        return HTMLResponse("Session not found", status_code=404)

    try:
        session_obj = respond_to_session(db, session_id, message)
    except Exception as e:
        # Show error in chat
        session_obj.agent_messages = (session_obj.agent_messages or []) + [
            {"role": "agent", "text": f"Error: {e}", "timestamp": ""}
        ]
        db.add(session_obj)
        db.commit()
        db.refresh(session_obj)

    # Return just the chat partial for HTMX swap
    return templates.TemplateResponse(request, "ingest/_chat.html", {
        "session_id": session_id,
        "messages": session_obj.agent_messages or [],
        "can_respond": session_obj.status in ("awaiting_response", "enriched"),
    })


async def ingest_save(request: Request, session_id: int) -> HTMLResponse:
    """POST /ingest/{id}/save — save to DB, redirect to car detail."""
    db = db_session()
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        return HTMLResponse("Session not found", status_code=404)

    try:
        car_id = save_session(db, session_id)
        return RedirectResponse(url=f"/cars/{car_id}", status_code=303)
    except Exception as e:
        session_obj.agent_messages = (session_obj.agent_messages or []) + [
            {"role": "agent", "text": f"Save failed: {e}", "timestamp": ""}
        ]
        db.add(session_obj)
        db.commit()
        return _render_review(request, session_obj)


async def ingest_discard(request: Request, session_id: int) -> HTMLResponse:
    """POST /ingest/{id}/discard — abandon the session."""
    db = db_session()
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        return HTMLResponse("Session not found", status_code=404)

    try:
        transition(session_obj, "discarded", db)
    except ValueError:
        pass  # already discarded

    return RedirectResponse(url="/ingest", status_code=303)
