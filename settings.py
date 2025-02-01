import os
import enum
from dotenv import load_dotenv
from llama_index.core.bridge.pydantic import BaseModel, Field

load_dotenv()


class MessageRole(enum.Enum):
    user = "user"
    system = "system"


class Settings(BaseModel):
    type: str = Field(
        description="Type of llm",
        default="openai",
    )

    llm: str = Field(description="Default LLM to use", default="gpt-4o-mini")

    database_url: str = Field(
        default=os.getenv("DATABASE_URL"),
        description="Database URL to connect to",
    )   
    db_verbose: bool = Field(
        default=True,
        description="Verbose mode for database connection",
    )
    number_of_msgs: int = Field(
        default=2,
        description="Number of history messages to be used to refine",
    )


setting = Settings()
