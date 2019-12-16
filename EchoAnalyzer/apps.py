from django.apps import AppConfig
import sys
import os
from decouple import config
# Pipeline imports:

sys.path.insert(1, '/echo_pipeline/Pipeline/')
import ProductionPipeline



class EchoanalyzerConfig(AppConfig):
    name = 'EchoAnalyzer'

    # def ready(self):
    #     ModelsPipeline.main()