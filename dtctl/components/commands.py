# pylint: disable=C0111
# pylint: disable=R0801
import click
from dtctl.components.functions import get_components
from dtctl.utils.output import process_output


@click.command('list', short_help='List Darktrace components')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def list_components(program_state, outfile):
    """List Darktrace components"""
    output = get_components(program_state.api)
    process_output(output, outfile)
