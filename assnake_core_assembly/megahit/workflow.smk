import shutil
import os
import pandas as pd
import assnake

assnake_db = config['assnake_db']
fna_db_dir = config['fna_db_dir']

def megahit_input_from_table(wildcards):
    """
    Reads table with samples, returns dict with reads
    """
    print('start with table')

    table_wc = '{fs_prefix}/{df}/assembly/{sample_set}/sample_set.tsv'
    r_wc_str = '{fs_prefix}/{df}/reads/{preproc}/{sample}_{strand}.fastq.gz'
    
    table = pd.read_csv(table_wc.format(fs_prefix = wildcards.fs_prefix,
                                        df = wildcards.df,
                                        # preset = wildcards.preset,
                                        sample_set = wildcards.sample_set),
                        sep = '\t')
    print(table)
    rr1 = []
    rr2 = []                        
    for s in table.to_dict(orient='records'):     
        rr1.append(r_wc_str.format(fs_prefix=wildcards.fs_prefix,
                                    df=s['df'], 
                                    preproc=s['preproc'],
                                    sample=s['df_sample'],
                                    strand='R1'))
        rr2.append(r_wc_str.format(fs_prefix=wildcards.fs_prefix,
                                    df=s['df'], 
                                    preproc=s['preproc'],
                                    sample=s['df_sample'],
                                    strand='R2'))
    print('done with table')
    return {'F': rr1, 'R': rr2}

rule megahit_from_table:
    input:
        unpack(megahit_input_from_table),
        table      = '{fs_prefix}/{df}/assembly/{sample_set}/sample_set.tsv',
        preset = os.path.join(config['assnake_db'], "presets/megahit/{preset}.json")
    output:
        out_fa     = '{fs_prefix}/{df}/assembly/{sample_set}/megahit__v1.2.9__{preset}/final_contigs.fa',
        preset     = '{fs_prefix}/{df}/assembly/{sample_set}/megahit__v1.2.9__{preset}/preset.json',
    params:
        out_folder = '{fs_prefix}/{df}/assembly/{sample_set}/megahit__v1.2.9__{preset}/assembly/'
    threads: 8
    wildcard_constraints:    
        df="[\w\d_-]+",
        # sample_set = "[\w\d_-]+"
    log: '{fs_prefix}/{df}/assembly/{sample_set}/megahit__v1.2.9__{preset}/log.txt'
    conda: 'megahit_env_v1.2.9.yaml'
    wrapper: "file://"+os.path.join(config['assnake-core-assembly']['install_dir'], 'megahit/megahit_wrapper.py')

def get_ref(wildcards):
    fs_prefix = assnake.Dataset(wildcards.df).fs_prefix
    return '{fs_prefix}/{df}/assembly/{sample_set}/megahit__v1.2.9__{preset}/final_contigs.fa'.format(
            fs_prefix = fs_prefix, 
            df = wildcards.df,
            sample_set = wildcards.sample_set,
            preset = wildcards.preset)

rule refine_assemb_results_cross:
    input: 
        ref = '{fs_prefix}/{df}/assembly/{sample_set}/{assembler}__{assembler_version}__{preset}/final_contigs.fa'
    output: 
        fa =         '{fs_prefix}/{df}/assembly/{sample_set}/{assembler}__{assembler_version}__{preset}/final_contigs__{min_len}.fa',
    log: 
        names = '{fs_prefix}/{df}/assembly/{sample_set}/{assembler}__{assembler_version}__{preset}/final_contigs__{min_len}.txt',
        ll    = '{fs_prefix}/{df}/assembly/{sample_set}/{assembler}__{assembler_version}__{preset}/final_contigs__{min_len}.log'
    wildcard_constraints:
        min_len="[\d_-]+"
    conda: 'anvi_minimal_env.yaml'
    shell: ("anvi-script-reformat-fasta {input.ref} -o {output.fa} --prefix {wildcards.sample_set} --min-len {wildcards.min_len} --simplify-names --report {log.names} > {log.ll} 2>&1")
