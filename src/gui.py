import panel as pn  # GUI
import param
from .chatbot import ChatBotForSQL
from .tools import get_tools
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from .config import DATABASE_FILE_PATH

pn.extension()


class ChatApp(param.Parameterized):
    query = param.String(default="")
    response = param.String(default="")

    def __init__(self, **params):
        super().__init__(**params)
        # Initialize langchain toolkit
        db = SQLDatabase.from_uri(f"sqlite:///{DATABASE_FILE_PATH}")
        toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0))
        # Get tools
        tools = get_tools(toolkit)
        # Initialize chatbot instance
        self.chatbot = ChatBotForSQL(tools, toolkit)
        self.panels = []
        self.query_input = pn.widgets.TextInput(name="Enter your query:")
        self.submit_button = pn.widgets.Button(name="Submit")
        self.clear_button = pn.widgets.Button(name="Clear History")
        self.submit_button.on_click(self.on_submit)
        self.clear_button.on_click(self.on_clear)

    @param.depends("response", watch=True)
    def view(self):
        return pn.Column(
            pn.pane.Markdown(self.response, width=600),
            self.query_input,
            self.submit_button,
            self.clear_button,
            *self.panels,
        )

    def on_submit(self, event):
        query = self.query_input.value
        if query:
            result = self.chatbot.convchain(query)
            self.query_input.value = ""
            if result:
                self.panels.append(result)
                self.response = f"Query: {query}\n\nResponse: {self.chatbot.answer}"

    def on_clear(self, event):
        self.panels.clear()
        self.response = ""
        self.chatbot.clr_history()


def create_gui():
    chat_app = ChatApp()
    return pn.Column(chat_app.view)


# Create and serve the GUI
gui = create_gui()
pn.serve(gui)
