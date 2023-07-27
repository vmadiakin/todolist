from dataclasses import dataclass, field
from typing import List, Optional
from marshmallow_dataclass import dataclass as ms_dataclass
from marshmallow import EXCLUDE

@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str
    language_code: Optional[str]

    class Meta:
        unknown = EXCLUDE

@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None

    class Meta:
        unknown = EXCLUDE

@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    text: Optional[str] = None
    date: Optional[int] = None
    entities: Optional[List[dict]] = None

    class Meta:
        unknown = EXCLUDE

@ms_dataclass
class UpdateObj:
    update_id: int
    message: Message

@ms_dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj] = field(default_factory=list)

    class Meta:
        unknown = EXCLUDE

@ms_dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
