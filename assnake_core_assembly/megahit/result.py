import click, os
from assnake.core.result import Result

result = Result.from_location(name='megahit',
                              description='Ultra-fast and memory-efficient NGS assembler',
                              result_type='assembly',
                              input_type='illumina_sample_set',
                              with_presets=True,
                              additional_inputs=[
                                  click.option('--min-len', '-l', help='Minimum length of contigs', default=1000),
                                  click.option('--overwrite', is_flag=True, help='Overwrite existing sample_set.tsv files', default=False)
                              ],
                              location=os.path.dirname(os.path.abspath(__file__))
                              )
