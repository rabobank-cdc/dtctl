# pylint: disable=C0111
# pylint: disable=R0801
import click
from dtctl.filters.functions import get_filters
from dtctl.utils.output import process_output


@click.command('list', short_help='List Darktrace component filters')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def list_filters(program_state, outfile):
    """List Darktrace component filters"""
    output = get_filters(program_state.api)
    process_output(output, outfile)
