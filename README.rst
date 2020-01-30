Phoopy
========

.. image:: https://raw.githubusercontent.com/phoopy/phoopy-installer/master/screenshot.png
  :width: 900
  :alt: Screenshot

`Full Documentation <https://github.com/phoopy/phoopy-skeleton/blob/master/DOCUMENTATION.md>`_

Install:
''''''''

.. code:: bash

   curl https://raw.githubusercontent.com/phoopy/phoopy-installer/master/phoopy-installer -o phoopy-installer
   chmod +x phoopy-installer
   ./phoopy-installer my-project
   cd my-project
   pip install -r requeriments.txt


Run:
''''

.. code:: bash

   bin/console


Run Tests:
''''''''''''

.. code:: bash

   pip install -r requeriments-dev.txt
   phulpy test


.. |Build Status| image:: https://travis-ci.org/phoopy/phoopy-skeleton.svg
   :target: https://travis-ci.org/phoopy/phoopy-skeleton
