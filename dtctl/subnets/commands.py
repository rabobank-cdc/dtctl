# pylint: disable=C0111
import click
from dtctl.subnets.functions import get_subnet_list, get_aggregates, get_subnets_per_instances, \
                                    get_dhcp_stats, get_unidirectional_traffic, list_devices
from dtctl.utils.output import process_output
from dtctl.utils.parsing import convert_json_to_log_lines
from dtctl.utils.cef import Cef
from dtctl.utils.clickutils import OptionMutex


@click.command('list', short_help='Lists all subnets without their meta data (IPv4 only)')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def list_subnets(program_state, outfile):
    """List all subnets without their meta data (IPv4 only)"""
    process_output(get_subnet_list(program_state.api), outfile)


@click.command('aggregates', short_help='Lists the CIDR merged subnets without their meta data (IPv4 only)')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def aggregates(program_state, outfile):
    """Lists the CIDR merged subnets without their meta data (IPv4 only)"""
    process_output(get_aggregates(program_state.api), outfile)


@click.command('instances', short_help='Lists subnets seen per Darktrace instance (IPv4 only)')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def instances(program_state, outfile):
    """Lists subnets seen per Darktrace instance (IPv4 only)"""
    process_output(get_subnets_per_instances(program_state.api), outfile)


@click.command('dhcp', short_help='Metrics for DHCP tracking')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.option('--log', is_flag=True, default=False, show_default=True,
              cls=OptionMutex, not_required_if=['cef'],
              help='Line based output for logging purposes')
@click.option('--cef', is_flag=True, default=False, show_default=True,
              cls=OptionMutex, not_required_if=['log'],
              help='Line based output for CEF logging purposes')
@click.pass_obj
def dhcp(program_state, outfile, log, cef):
    """Metrics for DHCP tracking"""
    output = get_dhcp_stats(program_state.api)
    append = False
    to_json = True

    if log or cef:
        append = True
        to_json = False

    if log:
        output = convert_json_to_log_lines(output)

    if cef:
        cef_object = Cef(device_event_class_id=120, name='DHCP Quality')
        output = cef_object.generate_logs(output)

    process_output(output, outfile, append, to_json)


@click.command('unidirectional', short_help='Metrics for unidirectional traffic')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def unidirectional(program_state, outfile):
    """Metrics for unidirectional traffic"""
    process_output(get_unidirectional_traffic(program_state.api), outfile)


@click.command('devices', short_help='Nr of devices seen by Darktrace')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def devices(program_state, outfile):
    """Nr of devices seen by Darktrace"""
    process_output(list_devices(program_state.api), outfile)
