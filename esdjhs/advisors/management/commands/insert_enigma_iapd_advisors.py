import functools
from itertools import izip_longest
import json
from optparse import make_option
import urllib2

from django.core.management import BaseCommand

from advisors.models import Advisor, Company


__author__ = 'brentpayne'

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def create_companies(base_uri, advisors):
    crd_list = "|".join([advisor.get('indvlpk') for advisor in advisors if advisor and advisor.get('indvlpk')])
    advisor_employment_uri = "{base}/search/@indvlpk ({crd_list})/".format(base=base_uri,
                                                                    crd_list=crd_list)
    response = grab_response(advisor_employment_uri)
    if not response:
        return {}  # yes, silently bail, this is demo code
    advisor_employment_data = json.loads(response.read())
    company_lookup = {}
    for result in advisor_employment_data.get('result'):
        try:
            company_name = result.get('orgnm', '')
            full_address = ''
            if result.get('str1'):
                full_address += result.get('str1')
            if result.get('str2'):
                full_address +=  ' ' + result.get('str2')
            if result.get('city'):
                full_address +=  ',' + result.get('city')
            if result.get('state'):
                full_address +=  ',' + result.get('state')
            if result.get('postlcd'):
                full_address +=  ' ' + result.get('postlcd')
            if result.get('cntry'):
                full_address +=  ' ' + result.get('cntry')
            company, _ = Company.objects.get_or_create(company_name=company_name, full_address=full_address)
            company_lookup[int(result['indvlpk'])] = company
        except (IndexError, AttributeError) as _:
            pass
    return company_lookup


def add_advisors(base_uri, advisors, company_lookup, seen):
    advisors_to_add = []
    for advisor in advisors:
        if not advisor:
            continue
        first_name = advisor.get('firstnm')
        last_name = advisor.get('lastnm')
        crd = int(advisor.get('indvlpk'))
        if not (first_name and last_name and crd):
            continue

        company = company_lookup.get(crd)

        # We are bulk adding advisors and are not concerned with duplicate names for advisors for this demo
        if not seen.get(crd):
            advisors_to_add.append(Advisor(first_name=first_name, last_name=last_name, crd=crd, company=company))
            seen[crd] = True
    Advisor.objects.bulk_create(advisors_to_add)


def grab_response(uri):
    try:
        response = urllib2.urlopen(uri)
    except urllib2.URLError as _:  # retry
        try:
            response = urllib2.urlopen(uri)
        except urllib2.URLError as _:
            response = None  # skip this is just for a demo
    return response


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (make_option('--apikey', dest='api_key'),)
    args = '--argkey=<ENIGMA_IO_API_KEY>'
    help = """
    This script reads some of the IAPD data from ENIGMA.IO and inserts it into your database

    Example:
        python manage.py insert_enigma_iapd_advisors --apikey=INSERT_API_KEY_HERE

    """

    def handle(self, *args, **options):
        api_key = options.get('api_key')
        base_advisor_iapd_uri = 'https://api.enigma.io/v2/data/{api_key}/us.gov.sec.iapd.othrnm'.format(api_key=api_key)
        base_active_employment_iapd_uri = 'https://api.enigma.io/v2/data/{api_key}/us.gov.sec.iapd.crntemp'.format(
            api_key=api_key)
        seen = {}
        add_advisors_primed = functools.partial(add_advisors, base_uri=base_advisor_iapd_uri, seen=seen)
        create_companies_primed = functools.partial(create_companies, base_uri=base_active_employment_iapd_uri)
        for page in range(1, 275*2+1):
            advisors_uri = "{base_uri}/page/{page_num}/".format(base_uri=base_advisor_iapd_uri, page_num=page)
            response = grab_response(advisors_uri)
            if not response:
                continue
            advisors_data = json.loads(response.read())
            for advisors in grouper(advisors_data.get('result'), 100):
                company_lookup = create_companies_primed(advisors=advisors)
                add_advisors_primed(advisors=advisors, company_lookup=company_lookup)




