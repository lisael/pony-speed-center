import glob
import os

HERE = os.path.abspath(os.path.dirname(__file__))
REPO = os.path.abspath(HERE + "/../ponyc/")
BRANCHES = ["master"]
STARTING_REVISIONS = {
    "master": "5a70dfd685179ee127e815ffd81ae9d223c2600f"
    #"master": "a9e8a0ef8ad3297380d91a2cfa97fcbced413491"
}
LLVM_VERSIONS = ["3.6", "3.8"]
BENCHS = glob.glob(os.path.abspath(HERE + "/../suite/*"))
ENVIRONMENT = "lisael-laptop"
PROJECT_NAME = "ponyc"
CODESPEED_URL = "http://codespeed.lxc:8000/"
