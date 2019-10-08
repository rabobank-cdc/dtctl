# pylint: disable=C0111
import click
from dtctl.utils.output import process_output
from dtctl.utils.clickutils import OptionMutex
from dtctl.intelfeed.functions import get_intelfeed, add_entry_to_intelfeed, delete_entry_from_intelfeed


@click.command('list', short_help='List entries configured in the intelligence feed')
@click.option('--outfile', '-o', help='Full path to the output file', type=click.Path())
@click.pass_obj
def list_intelfeed(program_state, outfile):
    """List entries in Darktrace's intelligence feed (Watchlist)"""
    process_output(get_intelfeed(program_state.api), outfile)


@click.command('add', short_help='Add entries to intelligence feed')
@click.option('--value', '-v', cls=OptionMutex, not_required_if=['infile'],
              help='IP address or domain to add',
              type=click.STRING)
@click.option('--infile', '-i', cls=OptionMutex, not_required_if=['value'],
              help='File with entries to add (one per line)',
              type=click.Path(exists=True))
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def add_entry(program_state, value, infile, outfile):
    """Add entries to Darktrace's intelligence feed (Watchlist)"""
    if not (value or infile):
        raise click.UsageError('Missing option "--value" / "-v" or "--infile" / "-i".')
    process_output(add_entry_to_intelfeed(program_state.api, value, infile), outfile)


@click.command('del', short_help='Delete entries from intelligence feed')
@click.option('--value', '-v', cls=OptionMutex, not_required_if=['infile'],
              help='IP address or domain to delete',
              type=click.STRING)
@click.option('--infile', '-i', cls=OptionMutex, not_required_if=['value'],
              help='File with entries to delete (one per line)',
              type=click.Path(exists=True))
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def del_entry(program_state, value, infile, outfile):
    """Delete entries from Darktrace's intelligence feed (Watchlist)"""
    if not (value or infile):
        raise click.UsageError('Missing option "--value" / "-v" or "--infile" / "-i".')
    process_output(delete_entry_from_intelfeed(program_state.api, value, infile), outfile)
