"""Agent loop — conversational agent with tool calling for MotorGeek.
Now with conversation persistence and enhanced tools."""

import json
import time
from datetime import datetime, timezone, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from motorgeek.core.database import get_session as db_session
from motorgeek.core.llm import LLMClient
from motorgeek.core.tools import TOOLS, execute_tool
from motorgeek.core.models import AgentToolCallLog

MAX_TOOL_ROUNDS = 10  # safety limit to prevent infinite loops

# ── Conversation persistence ─────────────────────────────────────────────────

class ConversationManager:
    """Manages multi-turn conversations with memory across queries."""

    def __init__(self, llm: Optional[LLMClient] = None):
        self.llm = llm or LLMClient()
        self._history: list[dict] = []  # full message history
        self._summaries: list[str] = []  # key findings for context window

    def add_exchange(self, user_msg: str, agent_response: str, key_findings: Optional[str] = None) -> None:
        """Record a Q&A pair. Optionally store a summary for context."""
        self._history.append({"role": "user", "content": user_msg})
        self._history.append({"role": "assistant", "content": agent_response[:500]})  # truncate for context
        if key_findings:
            self._summaries.append(key_findings)

    def get_context(self, max_turns: int = 5) -> list[dict]:
        """Return recent conversation for passing to the agent."""
        return self._history[-max_turns * 2:]  # last N turns (user + assistant pairs)

    def get_summary(self) -> str:
        """Return a summary of what we've learned so far."""
        if not self._summaries:
            return "(no previous analysis)"
        return "Previous findings:\n" + "\n".join(f"• {s}" for s in self._summaries[-5:])

    def clear(self) -> None:
        self._history = []
        self._summaries = []


# ── Agent loop ────────────────────────────────────────────────────────────────

class AgentLoop:
    """Manages a conversation with tool-calling capability."""

    def __init__(self, llm: Optional[LLMClient] = None, conversation: Optional[ConversationManager] = None):
        self.llm = llm or LLMClient()
        self.conversation = conversation

    def run(
        self,
        system_prompt: str,
        user_message: str,
        conversation: Optional[list[dict]] = None,
        ingest_session_id: Optional[int] = None,
        db: Optional[Session] = None,
    ) -> dict:
        """Run the agent loop. Returns {"messages": [...], "final_response": str, "summary": str}."""
        if db is None:
            db = db_session()

        messages = [{"role": "system", "content": system_prompt}]

        # Inject conversation history if available
        if self.conversation and self.conversation._history:
            summary = self.conversation.get_summary()
            if summary:
                messages.append({
                    "role": "system",
                    "content": f"[Previous session context]\n{summary}\n[/Previous session context]",
                })

        if conversation:
            messages.extend(conversation)
        messages.append({"role": "user", "content": user_message})

        tool_rounds = 0
        final_text = None

        while tool_rounds < MAX_TOOL_ROUNDS:
            tool_rounds += 1
            response = self.llm.complete_with_tools(messages, TOOLS)

            if response.get("tool_calls"):
                messages.append(response)
                for tc in response["tool_calls"]:
                    tool_name = tc["function"]["name"]
                    try:
                        args = json.loads(tc["function"]["arguments"])
                    except json.JSONDecodeError:
                        args = {}

                    start = time.time()
                    try:
                        result = execute_tool(tool_name, args, db, ingest_session_id)
                        status = "success"
                        error_msg = None
                    except Exception as e:
                        result = {"error": str(e)}
                        status = "error"
                        error_msg = str(e)
                    duration_ms = int((time.time() - start) * 1000)

                    self._log_tool_call(
                        db, tool_name=tool_name, arguments=args, result=result,
                        status=status, error_message=error_msg, duration_ms=duration_ms,
                        session_id=ingest_session_id,
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": json.dumps(result, default=str),
                    })
            else:
                final_text = response.get("content") or ""
                messages.append(response)
                break

        if final_text is None:
            final_text = "I ran out of steps. Try a more specific query."

        # Generate a one-line summary for conversation memory
        summary = self._summarize(user_message, final_text)

        return {
            "messages": messages,
            "final_response": final_text,
            "tool_rounds": tool_rounds,
            "summary": summary,
        }

    def _summarize(self, question: str, answer: str) -> str:
        """Extract a one-line summary for conversation memory."""
        try:
            prompt = f"Summarize this Q&A in ONE sentence (max 80 chars):\nQ: {question}\nA: {answer[:500]}\n\nOne sentence:"
            return self.llm.complete(prompt).strip()
        except Exception:
            return f"Asked: {question[:60]}..."

    def _log_tool_call(
        self, db: Session, tool_name: str, arguments: dict, result: dict,
        status: str, error_message: Optional[str], duration_ms: int,
        session_id: Optional[int] = None,
    ) -> None:
        log = AgentToolCallLog(
            session_id=session_id, tool_name=tool_name,
            arguments=arguments, result=result, status=status,
            error_message=error_message, duration_ms=duration_ms,
        )
        db.add(log)
        db.commit()


# ── Enhanced tools ────────────────────────────────────────────────────────────

def get_qualitative_analysis(db: Session, car_id: Optional[int] = None, keyword: Optional[str] = None) -> dict:
    """Retrieve stored qualitative analysis (LLMAnalyses, HistoricalContext) for a car or keyword search."""
    from motorgeek.core.models import LLMAnalyses, HistoricalContext, Car

    results = []

    if car_id:
        analyses = db.query(LLMAnalyses).filter(LLMAnalyses.car_id == car_id).all()
        for a in analyses:
            try:
                data = json.loads(a.generated_text) if isinstance(a.generated_text, str) else a.generated_text
                results.append({
                    "car_id": car_id,
                    "dimension": a.dimension,
                    "model": a.model_used,
                    "data": data,
                })
            except Exception:
                results.append({"car_id": car_id, "dimension": a.dimension, "raw": str(a.generated_text)[:500]})

        hist = db.query(HistoricalContext).filter(HistoricalContext.car_id == car_id).first()
        if hist:
            ctx = {}
            if hist.design_philosophy: ctx["design_philosophy"] = hist.design_philosophy
            if hist.cultural_significance: ctx["cultural_significance"] = hist.cultural_significance
            if hist.innovations: ctx["innovations"] = hist.innovations
            if ctx:
                results.append({"car_id": car_id, "type": "historical_context", "data": ctx})

    if keyword:
        # Search all LLMAnalyses for keyword
        all_analyses = db.query(LLMAnalyses).all()
        for a in all_analyses:
            text = a.generated_text or ""
            if keyword.lower() in text.lower():
                try:
                    data = json.loads(text) if isinstance(text, str) else text
                    results.append({
                        "car_id": a.car_id,
                        "dimension": a.dimension,
                        "model": a.model_used,
                        "matched_keyword": keyword,
                        "data": data,
                    })
                except Exception:
                    pass

    return {"results": results, "count": len(results)}


def check_market_freshness(db: Session) -> dict:
    """Audit market data freshness. Flag stale prices and missing data."""
    from motorgeek.core.models import MarketHistory, Car

    markets = db.query(MarketHistory).all()
    now = datetime.now(timezone.utc)
    stale = []
    fresh = []
    missing = []

    cars_with_market = set()
    for m in markets:
        cars_with_market.add(m.car_id)
        age_days = (now - m.date_recorded.replace(tzinfo=timezone.utc)).days if m.date_recorded else 999
        entry = {
            "car_id": m.car_id,
            "source": m.source_site,
            "price_low": m.price_low,
            "price_high": m.price_high,
            "age_days": age_days,
        }
        if age_days > 180:
            stale.append(entry)
        else:
            fresh.append(entry)

    all_cars = db.query(Car).all()
    for car in all_cars:
        if car.id not in cars_with_market:
            missing.append({"car_id": car.id, "name": f"{car.make} {car.model}"})

    return {
        "total_entries": len(markets),
        "fresh": len(fresh),
        "stale": len(stale),
        "missing": len(missing),
        "stale_entries": stale[:10],
        "missing_cars": missing[:10],
        "recommendation": f"{len(stale)} prices are >6 months old. {len(missing)} cars have no market data. Consider updating for accurate comparisons.",
    }


# ── Global conversation manager (shared across web requests) ─────────────────

_global_conversation = ConversationManager()

def get_global_conversation() -> ConversationManager:
    """Return the singleton conversation manager."""
    return _global_conversation

def reset_global_conversation() -> None:
    """Clear the global conversation."""
    global _global_conversation
    _global_conversation = ConversationManager()
