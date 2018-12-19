import re
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pprint import pprint
from tika import parser
import email_results


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def test():
    test_html = simple_get("http://www.coloradosupremecourt.com/Future%20Lawyers/BarExaminationResults.asp")
    return test_html


def find_pdf():
    with open("C:/temp/test.txt", 'wb') as f:
        target_url = "http://www.coloradosupremecourt.com/Future%20Lawyers/BarExaminationResults.asp"
        temp = simple_get(target_url)
        if temp is not None:
            f.write(temp)
    with open("C:/temp/test.txt") as html:
        if temp is not None:
            html = BeautifulSoup(temp, 'html.parser')
            for link in html.find_all('a'):
                link = link.get('href')
                target = re.findall(r'List.pdf', link)
                if target:
                    pdf = "http://www.coloradosupremecourt.com" + str(link.replace(' ', '%20'))
                    goal = re.findall(r'February', pdf)
                    pprint(goal)
                    if not goal:
                        return True, pdf
                    return False, pdf


def payload(first, last, target, middle):
    target_pdf = get(target, stream=True)
#    if not first and not middle:
#        last_name_payload = last.upper() + ', '
#    if not middle and first:
#        last_first_payload = last.upper() + ', ' + first.upper()
#    if middle and first:
#        full_name_payload = last.upper() + ', ' + first.upper() + ' ' + middle.upper()

    with open("C:/temp/new.pdf", 'wb') as f:
        if target_pdf is not None:
            f.write(target_pdf.content)
    raw = parser.from_file("C:/temp/new.pdf")
    if not middle and not first:
        payload = last.upper() + ', '
    if not middle and first:
        payload = last.upper() + ', ' + first.upper()
    if middle and first:
        payload = last.upper() + ', ' + first.upper() + ' ' + middle.upper()

#    if not middle:
#        payload = last.upper() + ', ' + first.upper()
#        if not first:
#            payload = last.upper() + ', '
#    if not first:
#        payload = last.upper() + ', '
#        if not middle:
#            payload = last.upper() + ', ' + first.upper()
#        else:
#            payload = last.upper() + ', ' + first.upper() + ' ' + middle.upper()
#    else:
#        payload = last.upper() + ', ' + first.upper() + ' ' + middle.upper()

    t4 = re.findall(payload, raw['content'])
#    pprint(t4)
    if t4:
        return True
    else:
        return False


def passed(last, targetPdf, first=None, middle=None):
    status = payload(first, last, targetPdf, middle)
    if middle:
        payload_text = 'Full Name Scan Results: '
    else:
        payload_text = 'Last, First Name Scan Results: '
    if not first:
        payload_text = 'Last Name Only Scan Results: '

        if status:
            payload_text += last + ' Bar Status: Success!!!!'
            return payload_text
        else:
            payload_text += last + ' Bar Status: Fail'
            return payload_text
    else:
        if status:
            payload_text += first + ' ' + last + ' Bar Status: Success!!!!'
            return payload_text
        else:
            payload_text += first + ' ' + last + ' Bar Status: Fail'
            return payload_text


def main():
    email_body = []
    email_text = "Relevant 2018 June Bar Results: \n"
    target = find_pdf()
    pprint(target)

    # email_body.append(passed("Rachel", "Bell", target))
    # email_body.append(passed("Kristina", "Bush", target))
    # email_body.append(passed("Kristina", "Bush", target, "Mary"))
    # email_body.append(passed("Benjamin", "Ryan", target, "wham"))

    email_body.append(passed("Bush", target[1], "Kristina", "Mary"))
    email_body.append(passed("Bush", target[1], "Kristina"))
    email_body.append(passed("Bush", target[1]))
    email_body.append("\n")
    email_body.append(passed("Rhodes", target[1], "Alyssa"))
    email_body.append(passed("Rhodes", target[1]))
    email_body.append("\n")

    for line in email_body:
        email_text += line + '\n'

    pprint(email_text)
    if target[0]:
        #email_results.results_email(email_text)
        return False
    else:
        pprint("Results not released")
        return True


if __name__ == "__main__":
    x = main()
