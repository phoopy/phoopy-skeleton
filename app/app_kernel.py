import sys
import os

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, '..'))

from phoopy import Kernel # noqa
from src.app_bundle import AppBundle # noqa


class AppKernel(Kernel):
    def register_bundles(self):
        bundles = [
            AppBundle()
        ]

        return bundles
