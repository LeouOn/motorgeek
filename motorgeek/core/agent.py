"""Agent loop — conversational agent with tool calling for MotorGeek."""

import json
import time
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from motorgeek.core.database import get_session as db_session
from motorgeek.core.llm import LLMClient
from motorgeek.core.tools import TOOLS, execute_tool
from motorgeek.core.models import AgentToolCallLog

MAX_TOOL_ROUNDS = 10  # safety limit to prevent infinite loops


class AgentLoop:
    """Manages a conversation with tool-calling capability."""

    def __init__(self, llm: Optional[LLMClient] = None):
        self.llm = llm or LLMClient()

    def run(
        self,
        system_prompt: str,
        user_message: str,
        conversation: Optional[list[dict]] = None,
        ingest_session_id: Optional[int] = None,
        db: Optional[Session] = None,
    ) -> dict:
        """Run the agent loop. Returns {"messages": [...], "final_response": str}."""
        if db is None:
            db = db_session()

        messages = [{"role": "system", "content": system_prompt}]
        if conversation:
            messages.extend(conversation)
        messages.append({"role": "user", "content": user_message})

        tool_rounds = 0
        final_text = None

        while tool_rounds < MAX_TOOL_ROUNDS:
            tool_rounds += 1
            response = self.llm.complete_with_tools(messages, TOOLS)

            if response.get("tool_calls"):
                # LLM wants to call tools
                messages.append(response)  # assistant's tool_call message

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

                    # Log the tool call
                    self._log_tool_call(
                        db,
                        tool_name=tool_name,
                        arguments=args,
                        result=result,
                        status=status,
                        error_message=error_msg,
                        duration_ms=duration_ms,
                        session_id=ingest_session_id,
                    )

                    # Feed the result back as a tool response message
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "content": json.dumps(result, default=str),
                        }
                    )
            else:
                # LLM responded with text — done
                final_text = response.get("content") or ""
                messages.append(response)
                break

        if final_text is None:
            final_text = "I ran out of steps trying to answer your question. Please try again with a more specific query."

        return {
            "messages": messages,
            "final_response": final_text,
            "tool_rounds": tool_rounds,
        }

    def _log_tool_call(
        self,
        db: Session,
        tool_name: str,
        arguments: dict,
        result: dict,
        status: str,
        error_message: Optional[str],
        duration_ms: int,
        session_id: Optional[int] = None,
    ) -> None:
        """Record a tool call in the database."""
        log = AgentToolCallLog(
            session_id=session_id,
            tool_name=tool_name,
            arguments=arguments,
            result=result,
            status=status,
            error_message=error_message,
            duration_ms=duration_ms,
        )
        db.add(log)
        db.commit()
