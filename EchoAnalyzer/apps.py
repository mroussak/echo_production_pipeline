from django.apps import AppConfig
import sys
import os
from decouple import config
# Pipeline imports:

from Pipeline import ProductionPipeline



class EchoanalyzerConfig(AppConfig):
    name = 'EchoAnalyzer'

    # def ready(self):
    #     ModelsPipeline.main()