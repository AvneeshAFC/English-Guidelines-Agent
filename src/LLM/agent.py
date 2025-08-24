from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import os

# Define the state for our graph
class AgentState(TypedDict):
    """ 
    Class for managing the state of an agent in the English Guidelines Agent application.  
    """
    document_content: str
    guidelines: str
    assessment_report: str
    modification_request: str
    modified_document: str
    error: str

class DocumentAssessorAgent:
    """
    An agent that assesses documents against a set of guidelines and suggests modifications.
    
    This agent uses a language model to analyze text content, evaluate it against provided
    guidelines, and generate modification suggestions to improve the document's adherence
    to those guidelines.
    """
    
    def __init__(self, model_name="llama3.2:3b"):
        # Initialize the Ollama model
        self.llm = ChatOllama(model=model_name, temperature=0.2)
        self.graph = self._build_graph()

    def _build_graph(self):
        # Create a new state graph
        workflow = StateGraph(AgentState)

        # Add nodes to the graph
        workflow.add_node("assess_document", self.assess_document_node)
        workflow.add_node("modify_document", self.modify_document_node)

        # Set the entry point
        workflow.set_entry_point("assess_document")
        workflow.add_edge("assess_document", END)
        workflow.add_edge("modify_document", END)
        
        # Compile the graph
        return workflow.compile()

    def assess_document_node(self, state: AgentState):
        """
        Node to assess the document against guidelines.
        """
        try:
            prompt = ChatPromptTemplate.from_template(
                """As an expert document analyst, please assess the following document based on the provided guidelines.
                Provide a detailed report specifying compliance or violations.

                Guidelines:
                {guidelines}

                Document Content:
                {document_content}

                Assessment Report:
                """
            )
            
            chain = prompt | self.llm | StrOutputParser()
            
            report = chain.invoke({
                "guidelines": state["guidelines"],
                "document_content": state["document_content"]
            })
            
            return {"assessment_report": report}
        except Exception as e:
            return {"error": f"Failed to assess document: {e}"}

    def modify_document_node(self, state: AgentState):
        """
        Node to modify the document based on user request.
        """
        try:
            prompt = ChatPromptTemplate.from_template(
                """As an expert document editor, please modify the following document to comply with the given guidelines,
                taking into account the user's specific request.

                Guidelines:
                {guidelines}

                User's Modification Request:
                {modification_request}

                Original Document Content:
                {document_content}

                Modified Document:
                """
            )
            
            chain = prompt | self.llm | StrOutputParser()
            
            modified_content = chain.invoke({
                "guidelines": state["guidelines"],
                "modification_request": state["modification_request"],
                "document_content": state["document_content"]
            })
            
            return {"modified_document": modified_content}
        except Exception as e:
            return {"error": f"Failed to modify document: {e}"}

    def run_assessment(self, doc_content: str, guidelines: str):
        """
        Run the assessment workflow.
        """
        initial_state = {
            "document_content": doc_content,
            "guidelines": guidelines
        }
        # We need to select the assessment graph path.
        # For simplicity, we create a temporary graph for this specific task.
        workflow = StateGraph(AgentState)
        workflow.add_node("assess", self.assess_document_node)
        workflow.set_entry_point("assess")
        workflow.add_edge("assess", END)
        app = workflow.compile()
        
        final_state = app.invoke(initial_state)
        return final_state

    def run_modification(self, doc_content: str, guidelines: str, request: str):
        """
        Run the modification workflow.
        """
        initial_state = {
            "document_content": doc_content,
            "guidelines": guidelines,
            "modification_request": request
        }
        # We need to select the modification graph path.
        workflow = StateGraph(AgentState)
        workflow.add_node("modify", self.modify_document_node)
        workflow.set_entry_point("modify")
        workflow.add_edge("modify", END)
        app = workflow.compile()

        final_state = app.invoke(initial_state)
        return final_state

# Instantiate the agent
assessor_agent = DocumentAssessorAgent()
