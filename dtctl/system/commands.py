# pylint: disable=C0111
import click
from dtctl.system.functions import get_status, get_usage, get_tags, get_info, get_auditlog, \
    get_summary_statistics, get_instances, get_packet_loss, get_system_issues
from dtctl.utils.output import process_output
from dtctl.utils.parsing import convert_json_to_log_lines
from dtctl.utils.timeutils import determine_date_range
from dtctl.utils.cef import Cef


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
@click.option('--log', is_flag=True, default=False, show_default=True,
              help='Line based output for logging purposes')
@click.option('--cef', is_flag=True, default=False, show_default=True,
              help='Line based output for CEF logging purposes')
@click.pass_obj
def usage(program_state, outfile, log, cef):
    """Short usage information of all instances and probes"""
    output = get_usage(program_state.api)
    append = False
    to_json = True

    if log or cef:
        append = True
        to_json = False

    if log:
        output = convert_json_to_log_lines(output)

    if cef:
        cef_object = Cef(device_event_class_id=100, name='System Usage')
        output = cef_object.generate_logs(output)

    process_output(output, outfile, append, to_json)


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
@click.option('--show-probes', '-p', is_flag=True, default=False, show_default=True)
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def instances(program_state, show_probes, outfile):
    """
    View Darktrace instances, their labels, id numbers and potential locations.

    \b
    Note that:
        - Master id numbers are prepended to breach ids.
        - Location is determined by the Master's label. The part before a "-" is
          considered to be the device's location or region.
    """
    process_output(get_instances(program_state.api, show_probes), outfile)


@click.command('auditlog', short_help='Account audit log')
@click.option('--offset', '-s', help='Offset for auditlog', default=0, show_default=True)
@click.option('--limit', '-l', help='Maximum entries to display for auditlog', default=30, show_default=True)
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def auditlog(program_state, offset, limit, outfile):
    """Account audit log"""
    process_output(get_auditlog(program_state.api, offset=offset, limit=limit), outfile)


@click.command('packet-loss', short_help='View packet loss information')
@click.option('--days', '-d', default=7, type=click.INT,
              help='Number of days in the past for the start date of the report.')
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date of the report. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date of the report.')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.option('--log', is_flag=True, default=False, show_default=True,
              help='Line based output for logging purposes')
@click.option('--cef', is_flag=True, default=False, show_default=True,
              help='Line based output for CEF logging purposes')
@click.pass_obj
def packet_loss(program_state, days, start_date, end_date, outfile, log, cef):
    """Information about reported packet loss per system"""
    end_date, start_date = determine_date_range(days, end_date, start_date)

    output = get_packet_loss(program_state.api, start_date, end_date)
    append = False
    to_json = True

    if log or cef:
        append = True
        to_json = False

    if log:
        output = convert_json_to_log_lines(output)

    if cef:
        cef_object = Cef(device_event_class_id=110, name='Packet Loss')
        output = cef_object.generate_logs(output)

    process_output(output, outfile, append, to_json)


@click.command('issues', short_help='View Darktrace system issues')
@click.option('--days', '-d', default=7, type=click.INT,
              help='Number of days in the past for the start date of the report.')
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date of the report. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date of the report.')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.option('--log', is_flag=True, default=False, show_default=True,
              help='Line based output for logging purposes')
@click.option('--cef', is_flag=True, default=False, show_default=True,
              help='Line based output for CEF logging purposes')
@click.pass_obj
def issues(program_state, days, start_date, end_date, outfile, log, cef):
    """Information about Darktrace system issues"""
    end_date, start_date = determine_date_range(days, end_date, start_date)

    output = get_system_issues(program_state.api, start_date, end_date)
    append = False
    to_json = True

    if log or cef:
        append = True
        to_json = False

    if log:
        output = convert_json_to_log_lines(output)

    if cef:
        cef_object = Cef(device_event_class_id=130, name='System Issue')
        output = cef_object.generate_logs(output)

    process_output(output, outfile, append, to_json)


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
