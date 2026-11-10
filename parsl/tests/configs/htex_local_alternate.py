"""
The aim of this configuration is to run a local htex
in a similar manner to htex_local.py, but with lots of
options different and more complicated than in that
configuration, so that more code paths are executed
than when testing only with htex_local.

It does not matter too much *what* is different in this
configuration; what matters is that the differences
cause significantly different pieces of parsl code to be
run - for example, by turning on monitoring, by allowing
blocks to be started by a strategy, by using a different
set of staging providers, by using timing parameters that
will cause substantially different behaviour on whatever
those timing parameters control.
"""

import os

from parsl.config import Config
from parsl.data_provider.file_noop import NoOpFileStaging
from parsl.data_provider.ftp import FTPInTaskStaging
from parsl.data_provider.http import HTTPInTaskStaging
from parsl.data_provider.zip import ZipFileStaging
from parsl.dataflow.memoization import BasicMemoizer
from parsl.executors import HighThroughputExecutor
from parsl.launchers import SingleNodeLauncher
from parsl.logconfigs.json import JSONLogging
from parsl.monitoring import MonitoringHub
from parsl.providers import LocalProvider

working_dir = os.getcwd() + "/" + "test_htex_alternate"

config = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_local",
            cores_per_worker=1,
            provider=LocalProvider(
                init_blocks=1,
                max_blocks=1,
            ),
        )
    ],
)

# def fresh_config():
#     # return Config(
#     #     executors=[
#     #         HighThroughputExecutor(
#     #             label="htex_local",
#     #             cores_per_worker=1,
#     #             provider=LocalProvider(
#     #                 init_blocks=1,
#     #                 max_blocks=1,
#     #             ),
#     #         )
#     #     ],
#     # )
#     return config

