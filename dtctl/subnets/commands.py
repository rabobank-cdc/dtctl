# pylint: disable=C0111
import click
from dtctl.subnets.functions import get_subnet_list, get_aggregates, get_subnets_per_instances, \
                                    get_dhcp_stats, get_unidirectional_traffic, list_devices
from dtctl.utils.output import process_output


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
@click.pass_obj
def dhcp(program_state, outfile):
    """Metrics for DHCP tracking"""
    process_output(get_dhcp_stats(program_state.api), outfile)


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
