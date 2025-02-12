Welcome to LineaPy!
===================

.. _intro:

What is LineaPy?
----------------

LineaPy is a Python package for capturing, analyzing, and automating data science workflows.
At a high level, LineaPy traces the sequence of code execution to form a comprehensive understanding
of the code and its context. This understanding allows LineaPy to provide a set of tools that help
data scientists bring their work to production more quickly and easily, with just *two lines* of code.

Why Use LineaPy?
----------------

Going from data science development to production is full of friction. The engineering process to make messy development code production-ready is manual and
time-consuming. LineaPy creates a frictionless path for taking your data science work from development to production with just *two lines* of code.

Use Case 1: Cleaning Messy Notebooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When working in a Jupyter notebook day after day, it's easy to write messy code --- You might execute cells out of order, execute the same cell repeatedly, and edit or delete cells until you've acquired good results, especially when generating tables, models, and charts. This highly dynamic and interactive notebook use, however, can introduce some issues. Our colleagues may not be able to reproduce our results by rerunning our notebook, and worse still, we ourselves may forget the steps required to produce our previous results.

One way to avoid this problem is to keep the notebook in sequential order by constantly re-executing
the entire notebook during development. This approach, however, interrupts our natural workflows and stream of
thoughts, decreasing our productivity. Therefore, it is much more common to clean up the notebook after development. This is a time-consuming process that is not immune from the reproducibility issues caused by deleted cells and out-of-order cell executions.

.. note::

    To see how LineaPy can help here, check out `cleaning up a messy notebook <https://github.com/LineaLabs/lineapy/blob/v0.2.x/.colab/clean_up_a_messy_notebook/clean_up_a_messy_notebook.ipynb>`_ demo.

Use Case 2: Revisiting Previous Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data science is often a team effort where one person's work relies on results from another's. For example, a data scientist building a model may use features engineered by other colleagues. When using results generated by other people, we may encounter data quality issues including missing values, suspicious numbers, and unintelligible variable names. When we encounter these issues, we may need to check how these results came into being in the first place. Often, this means tracing back the code that was used to generate the result in question. In practice, this can be a challenging task because we may not know who produced the result. Even if we know who to ask, that person might not remember where the exact version of the code is stored, or worse, may have overwritten the code without version control. Additionally, the person may no longer be at the organization and may not have handed over the relevant knowledge. In any of these cases, it becomes extremely difficult to identify the root any issues, rendering the result unreliable and even unusable.

.. note::

    To see how LineaPy can help here, check out `discovering and tracing past work <https://github.com/LineaLabs/lineapy/blob/v0.2.x/.colab/discover_and_trace_past_work/discover_and_trace_past_work.ipynb>`_ demo.

Use Case 3: Building Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As our notebooks become more mature, we may use them like pipelines. For example, our notebook might process the latest data to update a dashboard, or pre-process data and dump it into the file system for downstream model development. To keep our results up-to-date, we might be expected to re-execute these processes on a regular basis. Running notebooks manually is a brittle process that's prone to errors, so we may want to set up proper pipelines for production. If relevant engineering support is not available, we need to clean up and refactor our notebook code so that it can be used in orchestration systems or job schedulers, such as cron, Apache Airflow, or Prefect. Of course, this assumes that we already know how these tools work and how to use them --- If not, we need to spend time learning about them in the first place! All this operational work is time-consuming, and detracts from the time that we can spend on our core duties as a data scientist.

.. note::

    To see how LineaPy can help here, check out `creating pipelines <https://github.com/LineaLabs/lineapy/blob/v0.2.x/.colab/create_a_simple_pipeline/create_a_simple_pipeline.ipynb>`_ demo.


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Quickstart

   tutorials/00_lineapy_quickstart


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Concepts

   concepts/artifact
   concepts/artifact-store
   concepts/pipeline


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Tutorials

   tutorials/01_using_artifacts
   tutorials/02_pipeline_building


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Guides

   guides/installation
   guides/configuration/index
   guides/interfaces
   guides/code-cleanup
   guides/package-annotation
   guides/artifact-reuse
   guides/pipeline-building
   guides/pipeline-parametrization
   guides/pipeline-testing
   guides/contribute/index
   guides/troubleshoot
   guides/support


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: References

   references/api_reference
