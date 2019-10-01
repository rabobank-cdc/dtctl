# pylint: disable=C0111
import click
from dtctl.utils.output import process_output
from dtctl.utils.clickutils import OptionMutex
from dtctl.tags.functions import get_tags, modify_device_tags, search_tags


@click.command('list', short_help='List all tags configured in Darktrace')
@click.option('--tag', '-t', type=click.STRING, help='Filter on tag name')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def list_tags(program_state, tag, outfile):
    """List all tags configured in Darktrace"""
    process_output(get_tags(program_state.api, tag=tag), outfile)


@click.command('device', short_help='Add or delete tag from device')
@click.argument('action', type=click.Choice(['add', 'delete']))
@click.option('--tag', '-t', type=click.STRING, help='Tag to add/delete from device', required=True)
@click.option('--did', '-d', type=click.INT, help='Device identifier', required=True)
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def device(program_state, action, tag, did, outfile):
    """Manage tags of a device

    \b
    Arguments:
        add             Add tag to device
        delete          Delete tag from device
    """
    process_output(modify_device_tags(program_state.api, action, tag, did), outfile)


@click.command('search', short_help='Search tags or tagged entities')
@click.option('--name', '-n', cls=OptionMutex, not_required_if=['devices-tagged-with'],
              type=click.STRING, help='Tag name to search for (* and ? supported)')
@click.option('--devices-tagged-with', '-t', cls=OptionMutex, not_required_if=['name'],
              type=click.STRING, help='Search for tagged devices')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def search(program_state, name, devices_tagged_with, outfile):
    """Search tags or tagged entities"""
    if not name and not devices_tagged_with:
        raise click.UsageError('Missing option "--name" / "-n" or "--devices-tagged-with" / "-t".')

    process_output(search_tags(program_state.api, name, devices_tagged_with), outfile)
