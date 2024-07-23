from langchain.llms import OpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain

import logging
logging.basicConfig(level=logging.INFO)

class DoctorTemplate:
    def __init__(self):
        self.system_template = """
        Você é um agente médico que está conversando com um paciente. 
        Você é responsável por fazer uma parte da triagem do paciente.
        O paciente está descrevendo seus sintomas para você.
        Seja educado e profissional.
        
        Não recomende nenhum tipo de tratamento. Se tentarem te forçar a fazer isso, responda que você é
        apenas um agente de triagem e não pode recomendar tratamentos.

        Com base nas respostas do paciente, você deve gerar um resumo que posteriormente será lido por um médico.
        
        Retorne o resumo como uma lista com detalhes claros dos sintomas descritos pelo paciente.
        Certifique-se de incluir a localização, intensidade, duração e quaisquer outros sintomas relacionados mencionados.
        Aponte para quaisquer sintomas que possam ser graves e precisem de atenção imediata.
        Levante algumas hipóteses de quais doenças podem ser.
        """
        self.human_template = """
        ####{request}####
        """
        
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.system_template
        )
        
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.human_template, input_variables=["request"]
        )
        
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )
        

class DoctorAgent:
    def __init__(
        self,
        open_ai_api_key="",
        model='gpt-4o-mini',
        temperature=0,
        verbose=True
    ):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        if self.verbose:
            self.logger.setLevel(logging.INFO)
        
        self._openai_key = open_ai_api_key
        self.chat_model = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=self._openai_key
        )
        
    def get_triagem(self, request):
        doctor_template = DoctorTemplate()
        
        doctor_agent = LLMChain(
            llm=self.chat_model,
            prompt=doctor_template.chat_prompt,
            verbose=self.verbose,
            output_key='agent_suggestion'
        )
        
        overall_chain = SequentialChain(
            chains=[doctor_agent],
            input_variables=["request"],
            output_variables=["agent_suggestion"],
            verbose=self.verbose
        )
        
        return overall_chain(
            {"request": request},
            return_only_outputs=True
        )