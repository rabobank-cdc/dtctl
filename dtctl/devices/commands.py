# pylint: disable=C0111
# pylint: disable=R0801
import click
from dtctl.devices.functions import get_devices, get_device_info
from dtctl.utils.output import process_output


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
