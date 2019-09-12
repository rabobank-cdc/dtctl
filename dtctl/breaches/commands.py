# pylint: disable=C0111
# pylint: disable=R0801
import datetime as dt
import click
from dtctl.breaches.functions import report_breaches, get_breaches
from dtctl.utils.timeutils import determine_date_range
from dtctl.utils.output import process_output
from dtctl.utils.clickutils import OptionMutex


@click.command('list', short_help='List Darktrace model breaches')
@click.option('--acknowledged', '-a', is_flag=True, default=False, show_default=True,
              help='Show only acknowledged breaches')
@click.option('--tag', '-t', 'tags', type=click.STRING, multiple=True, cls=OptionMutex, not_required_if=['minimal'],
              help='Filter model breaches based on tag (option reusable)')
@click.option('--minimal', '-m', type=click.STRING, is_flag=True, default=False, show_default=True,
              cls=OptionMutex, not_required_if=['tag'], help='Only show minimal breach details')
@click.option('--minscore', '-s', type=click.FLOAT, default=0.0, show_default=True,
              help='Filter model breaches based on score (1.0 = 100%)')
@click.option('--days', '-d', default=7, type=click.INT,
              help='Number of days in the past for the start date of the report.')
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date of the report. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date of the report.')
@click.option('--outfile', '-o', help='Full path to the output file.', type=click.Path())
@click.pass_obj
def list_breaches(program_state, acknowledged, tags, minimal, minscore, days, start_date, end_date, outfile):
    """List Darktrace model breaches"""
    end_date, start_date = determine_date_range(days, end_date, start_date)

    if minscore > 1.0:
        minscore = 1.0
    if minscore < 0.0:
        minscore = 0.0
    minscore = round(minscore, 1)

    output = get_breaches(program_state.api, acknowledged, tags, minimal, minscore, start_date, end_date)
    process_output(output, outfile)


@click.command('report', short_help='Generate reports for Darktrace model breaches')
@click.argument('arg', type=click.Choice(['brief', 'commented', 'acknowledged']))
@click.option('--days', '-d', default=7, type=click.INT,
              help='Number of days in the past for the start date of the report.')
@click.option('--start-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='Start date of the report. (overwrites the "--days" flag)')
@click.option('--end-date', type=click.DateTime(formats=('%d-%m-%Y',)),
              help='End date of the report.')
@click.option('--outfile', '-o', help='Full path to the output file.'
                                      ' Defaults to: ./breaches_%Y-%m-%d_%H.%M.%S.xlsx',
              type=click.Path())
@click.option('--template', '-t', help='Full path to the template excel file. Appends breaches to sheet "RawData". '
                                       'Will append to a table if a table named "RawDataTable" is found.')
@click.option('--output', '-f', help='Specify output format', default='xlsx', type=click.Choice(['csv', 'xlsx']))
@click.pass_obj
def report(program_state, arg, days, start_date, end_date, outfile, template, output):
    """
    Generate reports for Darktrace model breaches

    \b
    Arguments:
        brief               Brief report with summary statistics of model breaches
        commented           Only report breaches with comments from analysts
        acknowledged        Only report acknowledged breaches
    """
    end_date, start_date = determine_date_range(days, end_date, start_date)

    if not outfile:
        outfile = f'./breaches_{arg}_{dt.datetime.now():%Y-%m-%d_%H.%M.%S}.{output}'

    report_breaches(program_state, arg, start_date, end_date, outfile, template, output)
