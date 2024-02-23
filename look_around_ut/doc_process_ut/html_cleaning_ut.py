import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../look_around')
# autopep8: off
from look_around.doc_process import html_cleaning as cl
# autopep8: on


class TestHtmlCleaning(unittest.TestCase):

    def test_pure_text(self):
        html = 'This is a text lacking any html elements. It should end up simply transformed to LOWER CASE.'
        text = cl.clean_html(html)
        self.assertEqual(html.lower(), text)

    def test_simple_html(self):
        html = '<!DOCTYPE html>AAA<strong class="bees">BBB</strong>1<br>2</br>3<br />4<br/>5<em class="seas">ccc</em>ddd'
        expect = 'aaabbb12345cccddd'
        text = cl.clean_html(html)
        self.assertEqual(expect, text)

    def test_nested_html(self):
        html = '<!DOCTYPE html><meta charset="UTF-8"><html><body class="headless">AAA<strong class="bees">BBB</strong>1<br>2</br>3<br />4<br/>5<em class="seas">ccc</em>ddd</body><div>eee</div></html>'
        expect = 'aaabbb12345cccdddeee'
        text = cl.clean_html(html)
        self.assertEqual(expect, text)

    def test_complex_html(self):
        html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Junior Backend Developer - fxamghqbf Corp.</title></head><body><h2 id="job_name">Junior Backend Developer</h2><p><div>fxamghqbf Corp.</div><div id="company_location">Abrahamsplains</div></p><p id="company_description">Our company are the number one company in the b2b markets. with our solutions we come up with solutions for the use of process analysis.</p><p><div>What you are going to achieve</div><ul id="job_tasks"><li>develop our data warehouses</li><li>set up and run our machine learning tools together with the clients</li><li>define and maintain our databases</li><li>define our customer projects</li></ul></p><p><div>What you have done already:</div><ul id="job_experience"><li>first knowledge of Node JS</li><li>sound experience in software testing, C, and Spring Boot</li><li>at least two years of experience in software testing, integration tests, and Software Containers</li><li>sound experience in software testing, R, and CouchDB</li></ul></p><p><div>You can expect:</div><ul id="job_benefits"><li>3 working days per week</li><li>Company car</li><li>45 working hours per week</li><li>Health insurance</li><li>Free food in the canteen of the company</li></ul></p></body></html>'
        expect = 'Junior Backend Developer - fxamghqbf Corp.Junior Backend Developerfxamghqbf Corp.AbrahamsplainsOur company are the number one company in the b2b markets. with our solutions we come up with solutions for the use of process analysis.What you are going to achievedevelop our data warehousesset up and run our machine learning tools together with the clientsdefine and maintain our databasesdefine our customer projectsWhat you have done already:first knowledge of Node JSsound experience in software testing, C, and Spring Bootat least two years of experience in software testing, integration tests, and Software Containerssound experience in software testing, R, and CouchDBYou can expect:3 working days per weekCompany car45 working hours per weekHealth insuranceFree food in the canteen of the company'.lower()
        text = cl.clean_html(html)
        self.assertEqual(expect, text)


if __name__ == '__main__':
    unittest.main()
