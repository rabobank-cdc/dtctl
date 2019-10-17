# pylint: disable=C0111
# pylint: disable=R0913
import datetime as dt
import click
from dtctl.models.functions import get_autoupdatable, get_pending_updates, get_updatable, report_models, \
                                   breach_summary, get_models, get_models_with_changes, get_deleted_models, \
                                   get_new_models, select_models_by_key_values, search_models
from dtctl.models.model_differ import get_update_diffs
from dtctl.utils.output import process_output
from dtctl.utils.timeutils import determine_date_range
from dtctl.utils.clickutils import OptionMutex


@click.command('select', short_help='View models based on top-level key value pairs')
@click.argument('selectors', nargs=-1, required=True)
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def select_model(program_state, selectors, outfile):
    """
    Select models based on top-level key value pairs. Nesting is not possible.

    \b
    Arguments:
        SELECTORS       One or multiple key-value paris

    \b
    Examples:
        dtctl models select active=true
        dtctl models select autoupdate=true version=13
    """
    key_values = {}
    for arg in selectors:
        if '=' not in arg:
            raise click.UsageError('Invalid format for "{0}"\nSELECTORS must be in format "key=value"'.format(arg))
        key, value = arg.split('=')
        key_values[key] = value

    output = select_models_by_key_values(program_state.api, key_values)
    process_output(output, outfile)


@click.command('list', short_help='List models')
@click.option('--enhanced-only', '-e', cls=OptionMutex, not_required_if=['tag'],
              help='Only list models with "*Enhanced*" tags', is_flag=True)
@click.option('--active-only', '-a', help='Only list models that are active', is_flag=True)
@click.option('--with-components', '-w', help='List models and their components', is_flag=True)
@click.option('--tag', '-t', cls=OptionMutex, not_required_if=['enhanced-only'],
              type=click.STRING, help='List models for specified tag (case insensitive). ')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def list_models(program_state, enhanced_only, active_only, with_components, tag, outfile):
    """List all models present within Darktrace"""
    output = get_models(program_state.api, enhanced_only, active_only, with_components, tag)
    process_output(output, outfile)


@click.command('autoupdatable', short_help='Models that have autoupdate configured')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def autoupdatable(program_state, outfile):
    """List all models that have auto-update configured"""
    process_output(get_autoupdatable(program_state.api), outfile)


@click.command('pending-updates', short_help='Models that have pending updates')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def pending_updates(program_state, outfile):
    """List all models that have updates pending"""
    process_output(get_pending_updates(program_state.api), outfile)


@click.command('search', short_help='Case-insensitive search for models')
@click.option('--name', '-n', type=click.STRING, help='Model name to search for (* and ? supported)')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def search_model(program_state, name, outfile):
    """
    Case-insensitive search for models

    \b
    Examples:
        dtctl models search --name *SMB*
        dtctl models search --name Device*
        dtctl models search --name ?evice*
    """
    output = search_models(program_state.api, name)
    process_output(output, outfile)


@click.command('updatable', short_help='Models that can be updated without losing changes')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def updatable(program_state, outfile):
    """List all models that can be updated without losing custom changes"""
    process_output(get_updatable(program_state.api), outfile)


@click.command('update-diff', short_help='Shows changes for models that have pending updates')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def update_diff(program_state, outfile):
    """List models that have updates pending and their respective changes"""
    process_output(get_update_diffs(program_state.api), outfile)


@click.command('input-diff', short_help='Shows new or modified models based on input list')
@click.argument('arg', type=click.Choice(['new', 'deleted', 'changed']))
@click.option('--infile', '-i', help='Full path to file with model names on each line',
              required=True, type=click.Path(exists=True))
@click.option('--days', '-d', default=7, type=click.INT,
              help='Number of days in the past for the start date of modified models.')
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date for modified models date range. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date for modified models date range.')
@click.option('--enhanced-only', '-e', help='Only list models with "*Enhanced*" tags', is_flag=True)
@click.option('--active-only', '-a', help='Only list models that are active', is_flag=True)
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def input_diff(program_state, arg, infile, days, start_date, end_date, enhanced_only, active_only, outfile):
    """
    List differences in models based on a input list. Input list must contain full model names
    with one name per line.

    \b
    Example file contents:
        Anomalous Connection::Data Sent to Rare Domain
        SaaS::AWS::Anonymous S3 File Download

    \b
    Arguments:
        new                 Models present in Darktrace but not in the input list
        deleted             Models present in the input list but not in Darktrace
        changed             Models in the input list that have been modified within date range

    """
    end_date, start_date = determine_date_range(days, end_date, start_date)

    diff_by_type = {
        'new': get_new_models,
        'deleted': get_deleted_models,
        'changed': get_models_with_changes
    }

    output = diff_by_type[arg](program_state.api, enhanced_only, active_only, infile,
                               start_date=start_date, end_date=end_date)
    process_output(output, outfile)


@click.command('report', short_help='Generate Excel report of models')
@click.argument('arg', type=click.Choice(['all', 'breach-summary']))
@click.option('--days', '-d', default=7, type=click.INT,
              help='Number of days in the past for the start date of the report.')
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date of the report. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date of the report.')
@click.option('--active-only', '-a', help='Only list models that are active', is_flag=True)
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file'
                                                         ' Defaults to ./models_arg_%Y-%m-%d_%H.%M.%S.xlsx')
@click.pass_obj
def report(program_state, arg, days, start_date, end_date, active_only, outfile):
    """
    Generate report that lists models or breaches per model

    \b
    Arguments:
        all                 Create Excel report that contains all models within Darktrace
        breach-summary      Create Excel report that contains breach statistics per model
    """
    end_date, start_date = determine_date_range(days, end_date, start_date)

    if not outfile:
        outfile = f'./models_{arg}_{dt.datetime.now():%Y-%m-%d_%H.%M.%S}.xlsx'

    if arg == 'all':
        report_models(program_state.api, active_only=active_only, outfile=outfile)

    if arg == 'breach-summary':
        breach_summary(program_state.api, outfile=outfile, start_date=start_date, end_date=end_date)
