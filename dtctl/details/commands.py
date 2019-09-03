# pylint: disable=C0111
# pylint: disable=R0801
import click
from dtctl.details.functions import get_device_details, get_host_details, get_message_details, \
                                    get_breach_details, get_connection_details
from dtctl.utils.timeutils import determine_date_range
from dtctl.utils.output import process_output
from dtctl.utils.subnetting import is_valid_domain, is_valid_hostname


@click.command('device', short_help='Time sorted list of connections and events for a device')
@click.argument('did', type=click.INT, required=True)
@click.option('--days', '-d', default=2, type=click.INT,
              help='Number of days in the past for filter.', show_default=True)
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date for date range filtering. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date for date range filtering.')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def device_details(program_state, did, days, start_date, end_date, outfile):
    """Time sorted list of connections and events for a device"""
    end_date, start_date = determine_date_range(days, end_date, start_date)
    output = get_device_details(program_state.api, did, start_date, end_date)
    process_output(output, outfile)


@click.command('host', short_help='Time sorted list of connections and events for an EXTERNAL host')
@click.argument('hostname', type=click.STRING, required=True)
@click.option('--days', '-d', default=2, type=click.INT,
              help='Number of days in the past for filter.', show_default=True)
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date for date range filtering. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date for date range filtering.')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def host_details(program_state, hostname, days, start_date, end_date, outfile):
    """Time sorted list of connections and events for an EXTERNAL host"""
    if not (is_valid_domain(hostname) or is_valid_hostname(hostname)):
        raise click.UsageError('Hostname contains invalid characters')

    end_date, start_date = determine_date_range(days, end_date, start_date)
    output = get_host_details(program_state.api, hostname, start_date, end_date)
    process_output(output, outfile)


@click.command('msg', short_help='Get notice event details for a specified message')
@click.argument('text', type=click.STRING, required=True)
@click.option('--days', '-d', default=2, type=click.INT,
              help='Number of days in the past for filter.', show_default=True)
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date for date range filtering. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date for date range filtering.')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def message_details(program_state, text, days, start_date, end_date, outfile):
    """
    Get notice event details for a specified message. Typically used to specify user credential strings.

        Example: USER123
    """
    end_date, start_date = determine_date_range(days, end_date, start_date)
    output = get_message_details(program_state.api, text, start_date, end_date)
    process_output(output, outfile)


@click.command('breach', short_help='Time sorted list of connections and events for a breach')
@click.argument('pbid', type=click.INT, required=True)
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def breach_details(program_state, pbid, outfile):
    """Time sorted list of connections and events for a breach"""
    output = get_breach_details(program_state.api, pbid)
    process_output(output, outfile)


@click.command('connection', short_help='Time sorted list of events for a connection')
@click.argument('uid', type=click.STRING, required=True)
@click.option('--days', '-d', default=2, type=click.INT,
              help='Number of days in the past for filter.', show_default=True)
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date for date range filtering. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date for date range filtering.')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def connection_details(program_state, uid, days, start_date, end_date, outfile):
    """
    Time sorted list of events for a connection

    \b
        Example: CcdXo43n8B75cdYyI5
    """
    end_date, start_date = determine_date_range(days, end_date, start_date)
    output = get_connection_details(program_state.api, uid, start_date, end_date)
    process_output(output, outfile)
