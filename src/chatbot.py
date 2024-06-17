import panel as pn
import param
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions


class ChatBotForSQL(param.Parameterized):

    def __init__(self, tools, toolkit, **params):
        super().__init__(**params)
        self.panels = []
        self.functions = [format_tool_to_openai_function(f) for f in tools]
        self.model = ChatOpenAI(temperature=0).bind(functions=self.functions)
        self.memory = ConversationBufferMemory(
            return_messages=True, memory_key="chat_history"
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful but sassy assistant"),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        if "top_k" in self.prompt.input_variables:
            self.prompt = self.prompt.partial(top_k=str(10))
        if "dialect" in self.prompt.input_variables:
            self.prompt = self.prompt.partial(dialect=toolkit.dialect)
        self.chain = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: format_to_openai_functions(
                    x["intermediate_steps"]
                )
            )
            | self.prompt
            | self.model
            | OpenAIFunctionsAgentOutputParser()
        )
        self.qa = AgentExecutor(
            agent=self.chain, tools=tools, verbose=False, memory=self.memory
        )

    def convchain(self, query):
        if not query:
            return
        # inp.value = ""
        result = self.qa.invoke({"input": query})
        self.answer = result["output"]
        self.panels.extend(
            [
                pn.Row("User:", pn.pane.Markdown(query, width=450)),
                pn.Row(
                    "ChatBot:",
                    pn.pane.Markdown(
                        self.answer, width=450, styles={"background-color": "#F3F3F3"}
                    ),
                ),
            ]
        )
        return pn.WidgetBox(*self.panels, scroll=False)

    def clr_history(self, count=0):
        self.chat_history = []
        return
