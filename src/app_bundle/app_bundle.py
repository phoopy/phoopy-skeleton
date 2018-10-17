from phoopy import Bundle
from os import path


class AppBundle(Bundle):
    def service_path(self):
        return path.join(self.get_bundle_dir(), 'config', 'services.yml')  # pragma: no cover
