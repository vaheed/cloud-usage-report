from flask import Flask, render_template, request, redirect, url_for, flash
import redis
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
import hashlib
import hmac
import base64
from datetime import datetime
import json
import logging
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and Redis connection
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a more secure secret key
r = redis.StrictRedis(host='redis', port=6379, db=0)

# CloudStack API credentials
CLOUDSTACK_API_URL = os.getenv('CLOUDSTACK_API_URL')
ACCESS_KEY = os.getenv('CLOUDSTACK_ACCESS_KEY')
SECRET_KEY = os.getenv('CLOUDSTACK_SECRET_KEY')

# Function to generate a signature for CloudStack API requests
def generate_signature(params, secret_key):
    query_string = '&'.join(['{}={}'.format(k, requests.utils.quote(str(v), safe='')) for k, v in sorted(params.items())])
    digest = hmac.new(secret_key.encode('utf-8'), query_string.lower().encode('utf-8'), hashlib.sha1).digest()
    signature = base64.b64encode(digest).decode('utf-8')
    return signature

# Function to make API request to CloudStack
def make_cloudstack_request(params):
    try:
        response = requests.get(url, timeout=10)  # Add timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from CloudStack: {e}")
        flash(f"Error fetching data from CloudStack: {str(e)}", "error")
        return None

# Function to get cached data from Redis
def get_cached_data(key):
    cached_data = r.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

# Function to set cached data in Redis
def set_cached_data(key, data, expiry=3600):  # Cache for 1 hour by default
    r.setex(key, expiry, json.dumps(data))

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add this dictionary to map usage type codes to names
USAGE_TYPE_MAP = {
    1: "Running VM",
    2: "Allocated VM",
    3: "IP Address",
    4: "Network Usage",
    5: "VPN Users",
    6: "Volume",
    7: "Template",
    8: "ISO",
    9: "Snapshot",
    10: "Security Group",
    11: "Load Balancer",
    12: "Port Forwarding Rule",
    13: "Network Offering",
    14: "VPC",
    15: "CPU",
    16: "Memory",
    17: "Primary Storage",
    18: "Secondary Storage"
}

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain_id = request.form.get('domainID', '').strip()
        start_date = request.form.get('startdate', '').strip()
        end_date = request.form.get('enddate', '').strip()
        selected_usage_types = request.form.getlist('usageTypes')

        logger.debug(f"Received POST request with domain_id: {domain_id}, start_date: {start_date}, end_date: {end_date}, usage_types: {selected_usage_types}")

        if not domain_id or not start_date or not end_date:
            flash('All fields are required!', 'error')
            return render_template('index.html', usage_types=USAGE_TYPE_MAP)

        try:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
            if start_datetime >= end_datetime:
                raise ValueError("End date must be after start date")
        except ValueError as e:
            flash(f'Invalid date format or range: {str(e)}', 'error')
            return render_template('index.html', usage_types=USAGE_TYPE_MAP)

        # Prepare parameters for the API call to get usage records
        params = {
            'command': 'listUsageRecords',
            'domainid': domain_id,
            'startdate': start_date,
            'enddate': end_date
        }

        # Check cache first
        cache_key = f"usage_{domain_id}_{start_date}_{end_date}_{','.join(sorted(selected_usage_types))}"
        cached_data = get_cached_data(cache_key)
        if cached_data:
            logger.debug("Returning cached data")
            return render_template('index.html', usage_data=cached_data, usage_types=USAGE_TYPE_MAP)

        # If not in cache, make the API call
        usage_data = make_cloudstack_request(params)
        logger.debug(f"API response: {usage_data}")

        if usage_data and 'listusagerecordsresponse' in usage_data:
            usage_records = usage_data['listusagerecordsresponse'].get('usagerecord', [])
            processed_records = defaultdict(lambda: {'usage': 0, 'startdate': None, 'enddate': None})
            for record in usage_records:
                usage_type = int(record.get('usagetype', 0))
                if not selected_usage_types or USAGE_TYPE_MAP.get(usage_type, str(usage_type)) in selected_usage_types:
                    key = (record.get('description', 'N/A'), usage_type)
                    data = processed_records[key]
                    data['description'] = record.get('description', 'N/A')
                    data['usage'] += float(record.get('usage', '0 Hrs').split()[0])
                    data['usagetype'] = USAGE_TYPE_MAP.get(usage_type, str(usage_type))
                    data['startdate'] = min(data['startdate'] or record.get('startdate'), record.get('startdate', 'N/A'))
                    data['enddate'] = max(data['enddate'] or record.get('enddate'), record.get('enddate', 'N/A'))

            processed_records = list(processed_records.values())
            for record in processed_records:
                record['usage'] = f"{record['usage']:.2f} Hrs"
            
            logger.debug(f"Processed usage records: {processed_records}")
            set_cached_data(cache_key, processed_records)
            return render_template('index.html', usage_data=processed_records, usage_types=USAGE_TYPE_MAP)
        else:
            flash('No usage data found or error in API response', 'error')
            logger.error(f"Error in API response: {usage_data}")

    return render_template('index.html', usage_types=USAGE_TYPE_MAP)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
