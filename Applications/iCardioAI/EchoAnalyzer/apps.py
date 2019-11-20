from django.apps import AppConfig
import sys
import os
from decouple import config
# Pipeline imports:

sys.path.insert(1, config("BASE_DIR") + 'echo_production_pipeline/Pipeline/ProductionPipeline')
from Components.Models import ModelsPipeline
import ProductionPipeline



class EchoanalyzerConfig(AppConfig):
    name = 'EchoAnalyzer'

    # def ready(self):
    #     ModelsPipeline.main()