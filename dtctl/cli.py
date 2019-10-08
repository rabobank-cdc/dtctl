"""dtctl initialization"""
import os
import sys
from pathlib import Path
import click
from dtctl.breaches import commands as breaches_commands
from dtctl.config import commands as config_commands
from dtctl.config.operations import load_config, get_private_key
from dtctl.components import commands as components_commands
from dtctl.details import commands as details_commands
from dtctl.devices import commands as devices_commands
from dtctl.dtapi.api import Api
from dtctl.filters import commands as filters_commands
from dtctl.intelfeed import commands as intelfeed_commands
from dtctl.metrics import commands as metrics_commands
from dtctl.models import commands as models_commands
from dtctl.query import commands as query_commands
from dtctl.subnets import commands as subnets_commands
from dtctl.system import commands as system_commands
from dtctl.tags import commands as tags_commands
from dtctl.utils.state import ProgramState


__author__ = 'Connor Dillon, Daan Wagenaar'
DEFAULT_CONFIG_FILE = os.path.join(str(Path.home()), '.dtctl', 'config.json')


@click.group()
@click.version_option(None, "-v", "--version", message="%(version)s")
@click.option('--host', '-h', help='Host address of the Darktrace API. Include scheme (https://)')
@click.option('--pub-dtkey', '-p', help='Public key for the Darktrace API.')
@click.option('--priv-dtkey', '-s', help='Private key for the Darktrace API. NOT RECOMMENDED')
@click.option('--cacert', '-e', help='Full path to the CA certificate used to issue the Darktrace API certificate.')
@click.option('--insecure', '-i', help='Ignore certificate warnings and connect insecurely.',
              is_flag=True, default=False)
@click.option('--debug', '-d', help='Show debug output', is_flag=True, default=False)
@click.option('--config-file', '-c', help='Location of the dtctl config file', default=DEFAULT_CONFIG_FILE,
              show_default=True)
@click.pass_context
def cli(ctx, host, pub_dtkey, priv_dtkey, cacert, insecure, debug, config_file):
    """Darktrace Command Line Interface"""
    config_dict = load_config(config_file)

    if '--help' in sys.argv:
        return

    # Provide fake values for when config command is given
    # This to pass the api_obj creation and still get a
    # valid ProgramState to the config subcommand
    if ctx.invoked_subcommand == 'config':
        host = '_'
        pub_dtkey = '_'
        priv_dtkey = '_'

    if not host:
        if 'host' in config_dict:
            host = config_dict['host']
        else:
            raise click.UsageError('Host not specified or configured')

    if not pub_dtkey:
        if 'pub-dtkey' in config_dict:
            pub_dtkey = config_dict['pub-dtkey']
        else:
            raise click.UsageError('pub-dtkey not specified or configured')

    if not cacert:
        if 'cacert' in config_dict:
            cacert = config_dict['cacert']

    privkey = get_private_key(priv_dtkey, config_dict)

    api_obj = Api(host, pub_dtkey, privkey, cacert, insecure, debug)
    ctx.obj = ProgramState(api_obj, debug, config_dict, config_file)


@cli.group()
def breaches():
    """Commands for Darktrace model breaches"""


@cli.group()
def components():
    """View Darktrace components"""


@cli.group()
def config():
    """Manage dtctl configurations"""


@cli.group()
def details():
    """View details of entities (represented as commands)"""


@cli.group()
def devices():
    """List active devices identified by Darktrace"""


@cli.group()
def filters():
    """View Darktrace filters"""


@cli.group()
def intelfeed():
    """Manage Darktrace's intelligence feeds"""


@cli.group()
def metrics():
    """View Darktrace metrics"""


@cli.group()
def models():
    """View Darktrace models"""


@cli.group()
def subnets():
    """View information of Darktrace's identified subnets"""


@cli.group()
def system():
    """View internal Darktrace information"""


@cli.group()
def tags():
    """Manage Darktrace tags"""


@cli.group()
def query():
    """Send direct HTTP requests to Darktrace API"""


# Sub-commands for "breach" command
breaches.add_command(breaches_commands.list_breaches)
breaches.add_command(breaches_commands.report)

# sub-commands for "components" command
components.add_command(components_commands.list_components)

# sub-commands for "config" command
config.add_command(config_commands.get_config)
config.add_command(config_commands.set_config)

# sub-commands for "details" command
details.add_command(details_commands.breach_details)
details.add_command(details_commands.connection_details)
details.add_command(details_commands.device_details)
details.add_command(details_commands.endpoint_details)
details.add_command(details_commands.host_details)
details.add_command(details_commands.message_details)

# sub-commands for "devices" command
devices.add_command(devices_commands.list_devices)
devices.add_command(devices_commands.device_info)
devices.add_command(devices_commands.ip_info)

# sub-commands for "filters" command
filters.add_command(filters_commands.list_filters)

# sub-commands for "intelfeed" command
intelfeed.add_command(intelfeed_commands.list_intelfeed)
intelfeed.add_command(intelfeed_commands.add_entry)
intelfeed.add_command(intelfeed_commands.del_entry)

# sub-commands for "metrics" command
metrics.add_command(metrics_commands.list_metrics)

# sub-commands for "models" command
models.add_command(models_commands.autoupdatable)
models.add_command(models_commands.updatable)
models.add_command(models_commands.pending_updates)
models.add_command(models_commands.report)
models.add_command(models_commands.list_models)
models.add_command(models_commands.update_diff)
models.add_command(models_commands.input_diff)
models.add_command(models_commands.select_model)

# sub-commands for "subnets" command
subnets.add_command(subnets_commands.list_subnets)
subnets.add_command(subnets_commands.aggregates)
subnets.add_command(subnets_commands.instances)
subnets.add_command(subnets_commands.unidirectional)
subnets.add_command(subnets_commands.dhcp)
subnets.add_command(subnets_commands.devices)

# sub-commands for "sytem" command
system.add_command(system_commands.info)
system.add_command(system_commands.status)
system.add_command(system_commands.usage)
system.add_command(system_commands.auditlog)
system.add_command(system_commands.summary_statistics)
system.add_command(system_commands.tags)
system.add_command(system_commands.instances)
system.add_command(system_commands.moo)
system.add_command(system_commands.packet_loss)
system.add_command(system_commands.issues)

# sub-commands for "tags" command
tags.add_command(tags_commands.list_tags)
tags.add_command(tags_commands.device)
tags.add_command(tags_commands.search)

# sub-commands for "query" command
query.add_command(query_commands.get)
query.add_command(query_commands.post)
