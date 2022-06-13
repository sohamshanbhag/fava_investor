#!/usr/bin/env python3
"""CLI for Metadata Summarizer for Beancount. See libsummarizer for more info."""

import click
import fava_investor.common.beancountinvestorapi as api
import libsummarizer
import tabulate
tabulate.PRESERVE_WHITESPACE = True


def pretty_print_table(rtypes, rrows):
    # TODO: Use the one in common
    headers = [i[0] for i in rtypes]
    print(tabulate.tabulate(rrows,
                            headers=headers[1:],
                            tablefmt='simple',
                            floatfmt=",.0f"))


@click.command()
@click.argument('beancount-file', type=click.Path(exists=True), envvar='BEANCOUNT_FILE')
def summarizer(beancount_file):
    """Displays metadata summaries from a config, as tables.

       The BEANCOUNT_FILE environment variable can optionally be set instead of specifying the file on the
       command line.

       The configuration for this module is expected to be supplied as a custom directive like so in your
       beancount file:

       \b
        2010-01-01 custom "fava-extension" "fava_investor" "{
          'summarizer': [
            { 'title' : 'Customer Service Phone Number',
              'directive_type'  : 'accounts',
              'acc_pattern' : '^Assets:(Investments|Banks)',
              'col_labels': [ 'Account', 'Phone_number'],
              'columns' : [ 'account', 'customer_service_phone'],
              'sort_by' : 0,
            }]}"

    """
    accapi = api.AccAPI(beancount_file, {})
    configs = accapi.get_custom_config('summarizer')
    tables = libsummarizer.build_tables(accapi, configs)
    for title, (rtypes, rrows, _, _) in tables:
        print("# " + title)
        pretty_print_table(rtypes, rrows)
        print()
        print()


if __name__ == '__main__':
    summarizer()
