#!usr/bin/env python

"""
Script initially used to get the HGNC ID for a gene target (if it exists).

Obsolete - there is now a dump file of HGNC IDs and associated gene symbols
in the main app, which means that it's not necessary to query the API for
every gene target whenever anything gets updated.
"""


import httplib2 as http
import json
from ratelimit import limits

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


# Limit API calls by this function to at most 10 per second
@limits(calls=10, period=1)
def get_hgnc(single_target):
    """Get associated HGNC ID (where it exists) for a gene target.

	Args:
		single_target [string]: string value for gene target

	Returns:
		hgnc_id [string]: target's HGNC ID if it exists, 'None' otherwise
	"""
    
    # Exclude targets which won't have an HGNC ID to save time & API calls
    if ('&' in single_target) or \
		('/' in single_target) or \
		('CHROMOSOME' in single_target) or \
		('DELETION' in single_target) or \
		('DEPENDENT' in single_target) or \
		('HOTSPOT' in single_target) or \
		('KARYOTYPE' in single_target) or \
		('MULTIPLE' in single_target) or \
		('NUMBER' in single_target) or \
		('OTHER' in single_target) or \
		('PROMOTER' in single_target) or \
		('REARRANGEMENT' in single_target) or \
		('REGION' in single_target) or \
		('TRISOMY' in single_target) or \
		('TYPE' in single_target) or \
		(single_target[:4] == 'DEL(') or \
		(single_target[:4] == 'INV(') or \
		(single_target[:2] == 'I(') or \
		(single_target[:2] == 'T('):
        
        return 'None'
    
    # Construct request to the HGNC website REST using target's gene symbol
    headers = {'Accept': 'application/json'}
    method = 'GET'
    body = ''
    h = http.Http()
    uri = 'http://rest.genenames.org'
    
    # Define a URL to search for the target in 'current gene symbols'
    current_path = '/search/symbol/' + str(single_target)
    current_target = urlparse(uri + current_path)
    
    # Define a URL to search for the target in 'previous gene symbols'
    previous_path = '/search/prev_symbol/' + str(single_target)
    previous_target = urlparse(uri + previous_path)
    
    # Make request to API with these URLs (look in current symbols first)
    for target_url in [current_target, previous_target]:
        response, content = h.request(
            target_url.geturl(),
            method,
            body,
            headers
            )
            
        # If the request is successful, load json content
        if response['status'] == '200':
            data = json.loads(content)

            try:
                # If the target is a current gene symbol, return its HGNC ID
                hgnc_id = str(data['response']['docs'][0]['hgnc_id'])
                return hgnc_id
            
            except IndexError:
                # If the loop has only looked in 'current gene symbols' so far,
                # progress to 'previous gene symbols'
                if target_url == current_target:
                    continue

                # Otherwise assume the target doesn't have an HGNC ID
                else:
                    return 'None'

        # If the request is unsuccessful, print an error message
        else:
            print(
                'Error in API response for "{a}":'.format(a=single_target),
                response['status'],
                )
            return 'None'
