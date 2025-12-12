courses-service documentation
============================


Overview
--------
This is the Sphinx documentation for the courses-service microservice, which manages course data for the UMASS platform.

Testing
-------
To run the test suite and generate an HTML test report:

.. code-block:: bash

	pytest --html=docs/source/test_report.html --self-contained-html

Documentation Build
-------------------
To build the Sphinx HTML documentation:

.. code-block:: bash

	cd docs
	make html

Open ``docs/build/html/index.html`` in your browser to view the documentation.


Test Report
-----------
`View the latest test report <test_report.html>`_


API Documentation
-----------------
.. automodule:: api.views
	:members:
	:undoc-members:
	:show-inheritance:
