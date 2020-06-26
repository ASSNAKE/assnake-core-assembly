import click, glob, os
import assnake.api.loaders
import assnake
from assnake.core.sample_set import generic_command_dict_of_sample_sets, prepare_sample_set_tsv_and_get_results
from assnake.cli.cli_utils import sample_set_construction_options, add_options


@click.command('megahit', short_help='Ultra-fast and memory-efficient NGS assembler')
@add_options(sample_set_construction_options)

@click.option('--params', help='Parameters for Megahit', default='def')
@click.option('--min-len','-l', help='Minimum length of contigs', default=1000)
@click.option('--overwrite', is_flag=True, help='Overwrite existing sample_set.tsv files', default=True)

@click.pass_obj

def megahit_invocation(config, params, min_len,overwrite, **kwargs):
    # load sample sets     
    sample_sets = generic_command_dict_of_sample_sets(config,   **kwargs)

    sample_set_dir_wc = '{fs_prefix}/{df}/assembly/{sample_set}/'
    result_wc = '{fs_prefix}/{df}/assembly/{sample_set}/megahit__v1.2.9__{params}/final_contigs__{min_len}.fa'
    res_list = prepare_sample_set_tsv_and_get_results(sample_set_dir_wc, result_wc, df = kwargs['df'], sample_sets = sample_sets, min_len = min_len, params = params, overwrite = overwrite)

    config['requests'] += res_list

