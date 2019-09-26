"""Utility classes for extending click functionality"""
import click


class OptionMutex(click.Option):
    """Mutex class for mutually exclusive command line options"""

    def __init__(self, *args, **kwargs):
        """Create OptionMutex object for mutually excluding options"""
        self.not_required_if: list = kwargs.pop('not_required_if')

        assert self.not_required_if, '"not_required_if" parameter required'
        kwargs['help'] = (kwargs.get('help', '') + ' [Conflicts with "' + ', '.join(
            self.not_required_if
        ) + '"].').strip()

        super(OptionMutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        """Handle parse result"""
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError('"' + str(self.name) + '" is mutually exclusive with "'
                                           + str(mutex_opt) + '".')
                self.prompt = None
        return super(OptionMutex, self).handle_parse_result(ctx, opts, args)
