# pylint: disable=C0111
# pylint: disable=R0801
import click
from dtctl.devices.functions import get_devices, get_device_info, get_device_info_by_ip
from dtctl.utils.output import process_output
from dtctl.utils.subnetting import is_valid_ipv4_address


@click.command('list', short_help='Returns the list of device identified by Darktrace.')
@click.option('--days', '-d', default=1, type=click.INT, show_default=True,
              help='Devices with activity in the past number of days')
@click.option('--seconds', '-s', type=click.INT,
              help='Devices with activity within the number of seconds. Ignores --days')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def list_devices(program_state, days, seconds, outfile):
    """Returns the list of device identified by Darktrace"""
    output = get_devices(program_state.api, days, seconds)
    process_output(output, outfile)


@click.command('info', short_help='Returns graphable connectivity information for a device.')
@click.argument('did', type=click.INT, required=True)
@click.option('--full-device-details', '-l', is_flag=True, default=False, show_default=True,
              help='Show full device details')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def device_info(program_state, did, full_device_details, outfile):
    """
    Returns graphable connectivity information for a device

    \b
    Arguments:
        DID                     A Device Identifier
    """
    output = get_device_info(program_state.api, did, full_device_details)
    process_output(output, outfile)


@click.command('ip', short_help='Return device data for this IP address')
@click.argument('ip-address', type=click.STRING, required=True)
@click.option('--days', '-d', default=30, type=click.INT, show_default=True,
              help='Device seen since days')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def ip_info(program_state, ip_address, days, outfile):
    """
    Return device data for this IP address

    \b
    Arguments:
        IP_ADDRESS          IP address to search
    """
    if not is_valid_ipv4_address(ip_address):
        raise click.UsageError('not a valid IP address')

    output = get_device_info_by_ip(program_state.api, ip_address, days)
    process_output(output, outfile)
