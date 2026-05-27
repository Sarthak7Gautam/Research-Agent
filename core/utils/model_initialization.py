from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
import os

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from custom_logging.custom_logging import CustomLogging
import yaml

from langchain_openai import ChatOpenAI


log = CustomLogging().custom_logger()


class LLMInitialization:
    def __init__(self):

        load_dotenv()
        self.REQUIRED_KEYS = ["GROQ_API_KEY", "HF_TOKEN"]

        self.api_keys = {}
        self.hf_token = {}
        for key in self.REQUIRED_KEYS:
            if key == "GROQ_API_KEY":
                self.api_keys[key] = os.getenv(key)
                log.info("API keys loaded successfully")

        for key in self.REQUIRED_KEYS:
            if key == "HF_TOKEN":
                self.hf_token[key] = os.getenv(key)
                log.info("HuggingFace Token loaded successfully")

    def load_config(self):

        base = Path(__file__).resolve().parents[2]
        config_path = base / "config" / "config.yml"

        with open(config_path, "r") as f:
            log.info("Config file read successfully")
            file = yaml.safe_load(f)

        return file

    def load_groq_llm(self):

        file = self.load_config()

        llm_config = file.get("llm", {})
        llm_data = llm_config.get("groq", {})

        llm_provider = llm_data.get("provider", {})
        model_name = llm_data.get("model_name", {})
        max_tokens = llm_data.get("max_output_tokens", {})
        temperature = llm_data.get("temperature", {})

        if llm_provider == "groq":
            model = ChatGroq(
                api_key=str(self.api_keys["GROQ_API_KEY"]),
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            log.info("Chat Model Initialized Successfully")

            return model

    def load_deepseek_llm(self):
        file = self.load_config()

        llm_config = file.get("llm", {})

        ds_openai_llm_data = llm_config.get("openai", {})
        openai_llm_provider = ds_openai_llm_data.get("provider", {})
        ds_model_name = ds_openai_llm_data.get("model", {})
        ds_model_base_url = ds_openai_llm_data.get("base_url", {})
        ds_temperature = ds_openai_llm_data.get("temperature", {})
        ds_max_tokens = ds_openai_llm_data.get("max_output_tokens", {})

        if openai_llm_provider == "openai":
            model = ChatOpenAI(
                model=ds_model_name,
                api_key=str(self.hf_token.get("HF_TOKEN")),
                base_url=ds_model_base_url,
                max_completion_tokens=ds_max_tokens,
                temperature=ds_temperature,
            )

            log.info("Deep Seek Model Initialized Successfully")

            return model

    def load_nvidia_llm(self):
        file = self.load_config()

        llm_config = file.get("llm", {})

        nvidia_openai_llm_data = llm_config.get("openai", {})
        openai_llm_provider = nvidia_openai_llm_data.get("provider", {})
        nvidia_model_name = nvidia_openai_llm_data.get("model", {})
        nvidia_model_base_url = nvidia_openai_llm_data.get("base_url", {})
        nvidia_temperature = nvidia_openai_llm_data.get("temperature", {})
        nvidia_max_tokens = nvidia_openai_llm_data.get("max_output_tokens", {})

        if openai_llm_provider == "openai":
            model = ChatOpenAI(
                model=nvidia_model_name,
                api_key=str(self.hf_token.get("HF_TOKEN")),
                base_url=nvidia_model_base_url,
                max_completion_tokens=nvidia_max_tokens,
                temperature=nvidia_temperature,
            )

            log.info("Deep Seek Model Initialized Successfully")

            return model
        
