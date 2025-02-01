import sys
from pathlib import Path
from llama_index.core.objects import SQLTableSchema, SQLTableNodeMapping, ObjectIndex
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.bridge.pydantic import BaseModel
from dotenv import load_dotenv
sys.path.append(str(Path(__file__).resolve().parent.parent))
from settings import MessageRole,Settings
from database.run import engine, get_db_context
from llama_index.llms.openai import OpenAI
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine
from prompt import REFINE_PROMPT
load_dotenv()
class Message(BaseModel):
    role: str
    content: str
class SQLAgent:
    def __init__(self,setting: Settings):
        company_context = get_db_context("company")
        user_context = get_db_context("user")
        table_infos = {
            "company": "This table give information about a company.\n"
                        "It has column: name.\n"
                        "\n"
                        "Some example rows:\n"
                        f"{company_context}",
            "user": "This table give information about a user.\n"  
                    "It has columns: id, name, company_name.\n"
                    "\n"
                    "Some example rows:\n"
                    f"{user_context}",
        }

        self.setting = setting
        self.sql_database = SQLDatabase(engine,include_tables=["company","user"])
        self.table_node_mapping = SQLTableNodeMapping(self.sql_database)
        self.table_schema_objs = [SQLTableSchema(table_name="company",context_str=table_infos["company"]),
                                  SQLTableSchema(table_name="user",context_str=table_infos["user"])]
        self.obj_index = ObjectIndex.from_objects(
            self.table_schema_objs,
            self.table_node_mapping,
            VectorStoreIndex,
        )
        self.history: list[Message] = []
        llm = self.load_model(
            self.setting.type, self.setting.llm
        )
        self.refine_llm = self.load_model(
            self.setting.type,
            self.setting.llm,
            REFINE_PROMPT.format(num=setting.number_of_msgs),
        )
        self.query_engine = SQLTableRetrieverQueryEngine(
            self.sql_database,
            self.obj_index.as_retriever(similarity_top_k=1),
            llm=llm,
            streaming=True,
        )
    def add_message(self, role: str, content: str):
        if role == MessageRole.system:
            return
        self.history.append(Message(role=role, content=content))

    def get_history(self, num_history: int):
        history = self.history[-num_history:]
        return "\n".join([f"- {msg.role}: {msg.content}" for msg in history])

    def load_model(
        self, model_type: str, model_name: str, system: str = ""
    ) -> FunctionCallingLLM:
        if model_type == "openai":
            return OpenAI(model_name, system_prompt=system)
        else:
            raise ValueError("Model type not supported")
    def refine_question(self, question: str):
        prompt = f"History: {self.get_history(self.setting.number_of_msgs)}\nQuestion: {question}\nYour refined question: "
        response = self.refine_llm.complete(prompt)
        return response.text

    def query(self, question: str) -> str:
        prompt = self.refine_question(question)
        print(prompt)
        response = self.query_engine.query(prompt)
        return response