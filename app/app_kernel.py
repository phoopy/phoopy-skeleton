import sys
import os

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, '..'))

from phoopy.kernel import Kernel # noqa
from phoopy.http.http_bundle import HttpBundle # noqa
from src.app_bundle import AppBundle # noqa


class AppKernel(Kernel):
    def register_bundles(self):
        template_folder = os.path.realpath(os.path.join(
            self.get_root_dir(),
            'src',
            'app_bundle',
            'resources',
            'views'
        ))

        config = {
            'MAX_CONTENT_LENGTH': 128 * 1024 * 1024, # 128Mb
        }

        bundles = [
            AppBundle(),
            HttpBundle(template_folder=template_folder, config=config)
        ]

        return bundles
