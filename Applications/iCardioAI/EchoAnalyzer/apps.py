from django.apps import AppConfig
import sys
import os

# Pipeline imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline/ProductionPipeline')
from Components.Models import ModelsPipeline
import ProductionPipeline



class EchoanalyzerConfig(AppConfig):
    name = 'EchoAnalyzer'

    # def ready(self):
    #     ModelsPipeline.main()