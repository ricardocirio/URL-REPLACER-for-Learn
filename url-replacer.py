# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import argparse
from auth import AuthToken
from constants import *
import json
import html
import requests

import sys

requests.packages.urllib3.disable_warnings()

def get_inputs():
    parser = argparse.ArgumentParser(description='URL Replacer for Learn')
    parser.add_argument('-s', '--site', help='Base URL to process, eg test.blackboard.com', required=True)
    parser.add_argument('-f', '--file', help='File containing course ids, one per line',
                        required=True)
    parser.add_argument('-t', '--title', help='Title of Link content item that will be updated',
                        required=True)
    parser.add_argument('-c', '--current', help='Current URL', required=True)
    parser.add_argument('-r', '--replacement', help='Replacement URL', required=True)
    if len(sys.argv) > 1:
        return parser.parse_args()
    else:
        parser.print_help()

        print('Running with developer settings, see correct settings above')

def main(argv):
    inputs = get_inputs()
    target_url = inputs.site
    course_ids = set()
    url_title = inputs.title
    current_url = inputs.current
    new_url = inputs.replacement

    if inputs.file:
        course_ids = set()
        with open(inputs.file) as f:
            for course_id in f.readlines():
                course_id = course_id.strip().lower()
                course_ids.add(course_id)

    print ('[main] Target is:', target_url)
    
    print ('\n[main] Acquiring auth token...\n')
    authorized_session = AuthToken(target_url)
    authorized_session.setToken()
    print ('\n[main] Returned token: ' + authorized_session.getToken() + '\n')

    #"Authorization: Bearer $token"
    authStr = 'Bearer ' + authorized_session.getToken()

    for course_id in course_ids:
        print ('\n[main] Reading course id: ' + course_id + '\n')
        r = requests.get("https://" + target_url + '/learn/api/public/v1/courses/courseId:'+
                         course_id + '/contents?&title=' + url_title + '&recursive=true&reviewable=true',
                         headers={'Authorization':authStr},  verify=False)
        if r.text:
            res = json.loads(r.text)
            for result in res.get('results'):
                #print(json.dumps(result,indent=4, separators=(',', ': ')))
                if(result.get('title') == url_title and (result.get('contentHandler')).get('url') ==
                   current_url):
                    (result['contentHandler'])['url'] = new_url
                    print("[main] PATCH Request URL: https://" + target_url +
                          '/learn/api/public/v1/courses/courseId:' + course_id + '/contents/' +
                          result.get('id'))
                    print("[main] JSON Payload: " +
                          json.dumps({'contentHandler':result['contentHandler']}, indent=4,
                                     separators=(',', ': ')))
                    r = requests.patch("https://" + target_url + '/learn/api/public/v1/courses/courseId:'
                                       + course_id + '/contents/' + result.get('id'),
                                       data=json.dumps({'contentHandler':result['contentHandler']},
                                                       indent=4, separators=(',', ': ')),
                                                       headers={'Authorization':authStr,
                                                                'Content-Type':'application/json'},
                                                                verify=False)
                    print("[main] STATUS CODE: " + str(r.status_code))

    print("\n[main] Processing Complete")

    #revoke issued Token
    #authorized_session.revokeToken()

if __name__ == '__main__':
    main(sys.argv[1:])
