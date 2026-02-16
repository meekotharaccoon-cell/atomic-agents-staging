import os
import uuid
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from models.cerebras_client import CerebrasClient, Message
from core.safety import SystemSafety

class AgentState(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    SAFETY_BLOCKED = "safety_blocked"

@dataclass
class ConversationMessage:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

class AIChatbot:
    def __init__(self, agent_id: Optional[str] = None, system_prompt: Optional[str] = None):
        self.agent_id = agent_id or os.getenv("AGENT_ID", f"agent_{uuid.uuid4().hex[:8]}")
        self.system_prompt = system_prompt or "You are a helpful AI assistant."
        self.safety = SystemSafety()
        self.state = AgentState.IDLE
        self.conversation_history = [ConversationMessage(role="system", content=self.system_prompt)]
    
    async def process(self, user_input: str) -> Dict[str, Any]:
        self.state = AgentState.PROCESSING
        
        try:
            safety_result = self.safety.check(user_input, "input")
            if not safety_result["allowed"]:
                self.state = AgentState.SAFETY_BLOCKED
                return {"success": False, "error": "Safety violation", "agent_id": self.agent_id}
            
            self.conversation_history.append(ConversationMessage(role="user", content=user_input))
            messages = [Message(role=m.role, content=m.content) for m in self.conversation_history[-10:]]
            
            async with CerebrasClient() as client:
                response = await client.complete(messages)
            
            safety_result = self.safety.check(response.content, "output")
            if not safety_result["allowed"]:
                self.state = AgentState.SAFETY_BLOCKED
                return {"success": False, "error": "Output safety violation", "agent_id": self.agent_id}
            
            self.conversation_history.append(ConversationMessage(role="assistant", content=response.content))
            self.state = AgentState.IDLE
            
            return {
                "success": True,
                "response": response.content,
                "agent_id": self.agent_id,
                "safety_score": safety_result["risk_score"]
            }
            
        except Exception as e:
            self.state = AgentState.ERROR
            return {"success": False, "error": str(e), "agent_id": self.agent_id}
