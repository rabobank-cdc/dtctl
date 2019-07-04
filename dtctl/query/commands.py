# pylint: disable=C0111
from urllib.parse import urlparse
import click
from dtctl.utils.output import process_output


@click.command('get', short_help='Send custom GET request to Darktrace API')
@click.argument('endpoint', type=click.STRING)
@click.option('--outfile', '-o', type=click.Path(), help="Full path to the output file")
@click.pass_obj
def get(program_state, endpoint, outfile):
    """
    Send a GET request to Darktrace

    \b
    Arguments:
        ENDPOINT        The Darktrace API endpoint including URL parameters

    \b
    Examples:
        dtctl query get "/status"
        dtctl query get "/breaches?starttime=1558303200000&endtime=1558475999000"
    """
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint

    parsed_endpoint = urlparse(endpoint)

    output_json = program_state.api.get('{path}?{query}'.format(path=parsed_endpoint.path,
                                                                query=parsed_endpoint.query))
    process_output(output_json, outfile)


@click.command('post', short_help='Send custom POST request to Darktrace API')
@click.argument('endpoint', type=click.STRING)
@click.option('--body', '-b', required=True, help='Body of the POST request. Should match URL parameter')
@click.option('--outfile', '-o', type=click.Path(), help='Full path to the output file')
@click.pass_obj
def post(program_state, endpoint, body, outfile):
    """
    Send a POST request to Darktrace.

    \b
    Note: The Darktrace API requires the body content to be reflected in the URL for
    a valid signature to be generated.

    \b
    Arguments:
        ENDPOINT        The Darktrace API endpoint including URL parameters

    \b
    Examples:
        dtctl query post "/intelfeed?addentry=www.evildomain.com" -b addentry=www.evildomain.com
    """
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint

    parsed_endpoint = urlparse(endpoint)

    if '=' not in body:
        raise SystemExit('Invalid POST body.\nBody must be of format key=value')

    key, value = body.split('=')

    output_json = program_state.api.post('{path}?{query}'.format(path=parsed_endpoint.path,
                                                                 query=parsed_endpoint.query),
                                         postdata={key: value})
    process_output(output_json, outfile)
