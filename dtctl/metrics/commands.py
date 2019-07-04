# pylint: disable=C0111
# pylint: disable=R0801
import click
from dtctl.metrics.functions import get_metrics
from dtctl.utils.output import process_output


@click.command('list', short_help='List Darktrace metrics')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def list_metrics(program_state, outfile):
    """List Darktrace metrics"""
    output = get_metrics(program_state.api)
    process_output(output, outfile)
