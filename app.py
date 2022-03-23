from flask import Flask, flash, render_template, send_file, request
from flask_bootstrap import Bootstrap
from werkzeug.datastructures import MultiDict
from xml.etree import ElementTree
import requests
import config
import io
from forms import PcapForm

app = Flask(__name__)
app.secret_key = config.secret_key
app.config['WTF_CSRF_ENABLED'] = False 
Bootstrap(app)

KEY = config.api_key
BASE_URL = 'https://sefags1097.secotools.net/api/'

# The route for the main page. Validates the input, sends request to API if ok. 
# Otherwise send feedback to the user about errors.
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        # Convert from json to a format WTForms understands to be able to use its validators
        data = MultiDict(mapping=request.json)
        form = PcapForm(data)
        if form.validate():
            try:          
                pcap_id = form.pcap_id.data
                device_name = form.device_name.data.strip()
                session_id = form.session_id.data
                search_time = form.search_time.data.strip()

                url = format_url(pcap_id, device_name, session_id, search_time)
                report = get_report(url)

                if(not report_is_found(report)):
                    print("Could not find the report")
                    flash("Error while downloading report. Error: Could not find the report, check your input", "error")
                    return ("Error: Could not find the report", 400)
                
                f = io.BytesIO(report.content)

                flash("Successfully downloaded the file", "success")
                return send_file(f,
                    mimetype='application/vnd.tcpdump.pcap',
                    attachment_filename='packet.pcap',
                    as_attachment=True,
                    cache_timeout=0)

            except Exception as error:
                print("Error: ", error)
                flash("Error while downloading report. Error: {}".format(str(error)), "error")
                return ("Error: Could not connect", 400)
        else: 
            flash_errors(form)
            return ("Error: Invalid input", 400)

    form = PcapForm()
    return render_template('index.html', form=form)

# Get the flashed errors produced from the forms input fields
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), "error")

# Do the call to the API
def get_report(url):
    try:
        return requests.get(url, verify=False)
    except:
        raise ConnectionError("Failed to connect")

# Construct the url for the API-call
def format_url(pcap_id, device_name, session_id, search_time):
    url = BASE_URL + '?key={}&type=export&category=threat-pcap&pcap-id={}&device_name={}&sessionid={}&search-time={}'.format(KEY, pcap_id, device_name, session_id, search_time)
    return url

# Check if the report is found. Returns as 200, so need to check XML-response that the report acutally was found
def report_is_found(report):
    try:
        tree = ElementTree.fromstring(report.content)
        event_id = tree.attrib['status']
        msg = tree.find('./msg/line')
        if(event_id == 'error'):
            print ('Error occured: ', msg.text)
            return False
        return True
    except:
        print('Successfully downloaded the file')
        return True




