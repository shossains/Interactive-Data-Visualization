#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.pycharm")
use_plugin("python.install_dependencies")

name = "Interactive Data Visualization"

# command 'pyb' will run:
default_task = ["clean", "install_build_dependencies", "verify", "run_unit_tests", "coverage"]


@init
def set_properties(project):
    # Dependencies
    project.build_depends_on("mockito")
    # project.build_depends_on("dash")

    # Plugin settings
    project.set_property("dir_docs", "doc")
    project.set_property("flake8_break_build", True)
    project.set_property("coverage_break_build", True)
