import os
import assnake
from assnake_core_assembly.megahit.cmd_megahit import megahit_invocation
from assnake.utils import read_yaml

this_dir = os.path.dirname(os.path.abspath(__file__))
snake_module = assnake.SnakeModule(name = 'assnake-core-assembly', 
                           install_dir = this_dir,
                           snakefiles = ['./megahit/megahit.py', './metaspades/metaspades.py'],
                           invocation_commands = [megahit_invocation],
                           wc_configs = []
                            )
