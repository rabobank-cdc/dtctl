# pylint: disable=C0111
import click
from dtctl.system.functions import get_status, get_usage, get_tags, get_info, get_auditlog, \
    get_summary_statistics, get_instances
from dtctl.utils.output import process_output


@click.command('info', short_help='View Darktrace system information')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def info(program_state, outfile):
    """View Darktrace system information such as time and version"""
    process_output(get_info(program_state.api), outfile)


@click.command('status', short_help='Detailed status information of all instances and probes')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def status(program_state, outfile):
    """Detailed status information of all instances and probes"""
    process_output(get_status(program_state.api), outfile)


@click.command('usage', short_help='Short usage information of all instances and probes')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def usage(program_state, outfile):
    """Short usage information of all instances and probes"""
    process_output(get_usage(program_state.api), outfile)


@click.command('tags', short_help='All tags configured in Darktrace')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def tags(program_state, outfile):
    """All tags configured in Darktrace"""
    process_output(get_tags(program_state.api), outfile)


@click.command('summary-statistics', short_help='Summary of Darktrace statistics')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def summary_statistics(program_state, outfile):
    """Summary of Darktrace statistics"""
    process_output(get_summary_statistics(program_state.api), outfile)


@click.command('instances', short_help='View Darktrace instances')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def instances(program_state, outfile):
    """
    View Darktrace instances, their labels, id numbers and potential locations.

    \b
    Note that:
        - Master id numbers are prepended to breach ids.
        - Location is determined by the Master's label. The part before a "-" is
          considered to be the device's location or region.

    """
    process_output(get_instances(program_state.api), outfile)


@click.command('auditlog', short_help='Account audit log')
@click.option('--offset', '-s', help='Offset for auditlog', default=0, show_default=True)
@click.option('--limit', '-l', help='Maximum entries to display for auditlog', default=30, show_default=True)
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def auditlog(program_state, offset, limit, outfile):
    """Account audit log"""
    process_output(get_auditlog(program_state.api, offset=offset, limit=limit), outfile)


@click.command('moo', hidden=True, add_help_option=False)
def moo():
    """Mooooo"""
    print(r"""
              _________
             < Moooooo >
              ---------
                     \   ^__^
                      \  (oo)\_______
                         (__)\       )\/\/
                             ||----w |
                             ||     ||""")
