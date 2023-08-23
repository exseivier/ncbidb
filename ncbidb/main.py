from pprint import pprint
import os
import click
import subprocess as sup
import pymods.jsonload as js

@click.group()
def ncbidbrun():
    """
        NCBI proteins, genes and genomes data base manager.
    """

    pass

@click.group()
def show():
    """
        Commands group for showing tasks.
    """
    pass


@click.command()
@click.option('-db', help = 'Path to NCBI database', type = str, required = True)
def database(db):
    """
        Prints on screen organism name and other usefull data from NCBI database.
        Member of commands group for showing tasks.
    """
    data = js.load_json(f'{db}/dataset_catalog.json')
    datal = js.load_json_lines(f'{db}/assembly_data_report.jsonl')
    df = js.load_df(data, datal)
    click.echo(df)

@click.group()
def concatenate():
    """
        Commands group for concatenate databases.
    """
    pass

@click.command()
@click.option('-db1', help = 'Path to NCBI database #1', type = str, required = True)
@click.option('-db2', help = 'Path to NCBI database #2', type = str, required = True)
@click.option('-mv', help = 'Flag option to move files of the databases instead of copy them', is_flag=True)
@click.argument('out-dir')
def two_db(db1, db2, mv, out_dir):
    """
        Concatenates 2 NCBI database if they are of the same molecule type (DNA, RNA or Proteins).
        Where OUT_DIR is the name of the output directory.
    """
    ## ASSERT THAT THESE TWO DATABASE ARE OF THE SAME MOLECULE TYPE.
    ##  CODE HERE. NOT YET.

    data_all = {}
    data1 = js.load_json(f'{db1}/dataset_catalog.json')
    data2 = js.load_json(f'{db2}/dataset_catalog.json')
    data_all.update(data1)
    data_all.update(data2)
    data3 = {"apiVersion" : "V2",
            "assemblies" : [
                {"files" : [
                    {"filePath" : "assembly_data_report.jsonl",
                    "fileType" : "DATA_REPORT"}
                    ]}
                ]}

    for key in data_all.keys():
        data3['assemblies'].append({"accession" : key, "files" : data_all[key]})

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(f'{out_dir}/dataset_catalog.json', 'w+') as FHOUT:
        data3 = js.json.dumps(data3)
        data3 = str(data3)
        FHOUT.write(str(data3))

    if (mv):
        for key in data1.keys():
            sup.call(['mv', f'{db1}/{key}', out_dir])
        for key in data2.keys():
            sup.call(['mv', f'{db2}/{key}', out_dir])
    else:
        for key in data1.keys():
            sup.call(['cp', '-r', f'{db1}/{key}', out_dir])
        for key in data2.keys():
            sup.call(['cp', '-r', f'{db2}/{key}', out_dir])

    with open(f'{out_dir}/assembly_data_report.jsonl', 'w+') as FHOUT:
        p = sup.Popen(['cat', f'{db1}/assembly_data_report.jsonl', f'{db2}/assembly_data_report.jsonl'], stdout = FHOUT)
        out, err = p.communicate()
        if err != None:
            print(err)
        p.kill()
            

show.add_command(database)
concatenate.add_command(two_db)

ncbidbrun.add_command(show)
ncbidbrun.add_command(concatenate)


if __name__ == '__main__':
    ncbidbrun()
