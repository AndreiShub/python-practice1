import enum
import json
from dataclasses import dataclass
from abc import ABC, abstractmethod

class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    username: str
    text: str
    timestamp: str

class MessageParser(ABC):
    @abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage:
        pass


class TelegramParser(MessageParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        data = json.loads(message.payload)
        return ParsedMessage(
            username=data["from"]["username"],
            text=data["text"],
            timestamp=data["date"],
        )


class MattermostParser(MessageParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        data = json.loads(message.payload)
        return ParsedMessage(
            username=data["user_name"],
            text=data["post"]["message"],
            timestamp=data["post"]["create_at"],
        )


class SlackParser(MessageParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        data = json.loads(message.payload)
        return ParsedMessage(
            username=data["user"],
            text=data["text"],
            timestamp=data["ts"],
        )


class ParserFactory:
    _parsers = {
        MessageType.TELEGRAM: TelegramParser(),
        MessageType.MATTERMOST: MattermostParser(),
        MessageType.SLACK: SlackParser(),
    }

    @classmethod
    def get_parser(cls, message_type: MessageType) -> MessageParser:
        try:
            return cls._parsers[message_type]
        except KeyError:
            raise ValueError(f"No parser found for message type {message_type}")
