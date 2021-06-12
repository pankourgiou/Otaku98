# project:PyBambooHR
# repository:http://github.com/smeggingsmegger/PyBambooHR
# license:mit (http://opensource.org/licenses/MIT)

"""
PyBambooHR.py contains a class by the same name with functions that correspond
to BambooHR API calls defined at http://www.bamboohr.com/api/documentation/.
"""

import requests


class PyBambooHR:
    """
    The PyBambooHR class is initialized with an API key, company subdomain,
    and an optional datatype argument (defaults to JSON). This class implements
    methods for basic CRUD operations for employees and more.
    """
    def __init__(self, subdomain=None, api_key=None, datatype='JSON'):
        """
        Using the subdomain, __init__ initializes the base_url for our API calls.
        This method also sets up some headers for our HTTP requests as well as our authentication (API key).
        @param subdomain: String containing a valid company subdomain for a company in BambooHR.
        @param api_key: String containing a valid API Key created in BambooHR.
        @param datatype: String of 'JSON' or 'XML'. Sets the Accept header for return type in our HTTP requests to BambooHR.
        """
        if not subdomain:
            raise ValueError('The `subdomain` argument can not be empty. Please provide a valid BambooHR company subdomain.')

        if not api_key:
            raise ValueError('The `api_key` argument can not be empty. Please provide a valid BambooHR API key.')

        # API Version
        self.api_version = 'v1'

        # Global headers
        self.headers = {}

        # Referred to in the documentation as [ Company ] sometimes
        self.subdomain = subdomain

        # All requests will start with this url
        self.base_url = 'https://api.bamboohr.com/api/gateway.php/{0}/{1}/'.format(self.subdomain, self.api_version)

        # JSON or XML
        self.datatype = datatype

        # You must create an API key through the BambooHR interface
        self.api_key = api_key

        # We are focusing on JSON for now
        if self.datatype == 'XML':
            raise NotImplemented('Returning XML is not currently supported.')

        if self.datatype == 'JSON':
            self.headers.update({'Accept': 'application/json'})

        # Report formats
        self.report_formats = {
            'csv': 'text/csv',
            'pdf': 'application/pdf',
            'xls': 'application/vnd.ms-excel',
            'xml': 'application/xml',
            'json': 'application/json'
        }

    def request_company_report(self, report_id, report_format='json', filter_duplicates=True):
        """
        API method for returning a company report by report ID.
        http://www.bamboohr.com/api/documentation/employees.php#requestCompanyReport
        Success Response: 200
        The report will be generated in the requested format.
        The HTTP Content-type header will be set with the mime type for the response.
        @param report_id: String of the report id.
        @param report_format: String of the format to receive the report. (csv, pdf, xls, xml, json)
        @param filter_duplicates: Boolean. True: apply standard duplicate field filtering (Default True)
        @return: A result in the format specified. (Will vary depending on format requested.)
        """
        if report_format not in self.report_formats:
            raise UserWarning('You requested an invalid report type. Valid values are: {0}'.format(','.join([k for k in self.report_formats])))

        filter_duplicates = 'yes' if filter_duplicates else 'no'
        url = self.base_url + 'reports/{0}?format={1}&fd={2}'.format(report_id, report_format, filter_duplicates)
        r = requests.get(url, headers=self.headers, auth=(self.api_key, ''))
        r.raise_for_status()

        if report_format == 'json':
            # return list/dict for json type
            result = r.json()
        elif report_format in ('csv', 'xml'):
            # return text for csv type
            result = r.text
        else:
            # return requests object for everything else after saving the file to the location specified.
            result = r
        return url, result
