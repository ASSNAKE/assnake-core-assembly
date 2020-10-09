import os, assnake

import assnake_core_assembly.megahit.result as megahit


snake_module = assnake.SnakeModule(name='assnake-core-assembly',
                                   install_dir=os.path.dirname(os.path.abspath(__file__)),
                                #    results = [megahit]
                                   )