# pylint: disable=C0111
import click
from dtctl.utils.output import process_output
from dtctl.intelfeed.functions import get_intelfeed, add_entry_to_intelfeed


@click.command('list', short_help='List entries configured in the intelligence feed')
@click.option('--outfile', '-o', help='Full path to the output file', type=click.Path())
@click.pass_obj
def list_intelfeed(program_state, outfile):
    """List entries in Darktrace's intelligence feed (Watchlist)"""
    process_output(get_intelfeed(program_state.api), outfile)


@click.command('add', short_help='Add single entry to intelligence feed')
@click.argument('entry', type=click.STRING)
@click.pass_obj
def add_entry(program_state, entry):
    """
    Add an entry to Darktrace's intelligence feed (Watchlist)

    \b
    Arguments:
        ENTRY       Hostname or IP address
    """
    process_output(add_entry_to_intelfeed(program_state.api, entry), None)
