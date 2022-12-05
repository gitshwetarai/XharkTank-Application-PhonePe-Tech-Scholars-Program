import time
import unittest
from unittest import TestCase

import pytest
import requests
import json
import logging
import socket


class XharkTankAssessment(TestCase):

    HEADERS = None
    maxDiff = None

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.HEADERS = {"Content-Type": "application/json"} # "X-Firebase-Auth": "INTERNAL_IMPERSONATE_USER_" + str(user),
        self.localhost = 'http://localhost:8081/'

        self.POSITIVE_STATUS_CODES = [200, 201, 202, 203]
        self.NEGATIVE_STATUS_CODES = [400, 401, 402, 403, 404, 405, 409]

    ### Helper functions
    def get_api(self, endpoint):
      
        response = requests.get(self.localhost + endpoint, headers=self.HEADERS,timeout=10)
        self.print_curl_request_and_response(response)
        return response

    def post_api(self, endpoint, body):
       
        response = requests.post(self.localhost + endpoint, headers=self.HEADERS,timeout=10, data=body)
        self.print_curl_request_and_response(response)
        return response

    def print_curl_request_and_response(self, response):
    
        if(response.status_code in self.POSITIVE_STATUS_CODES):
         
            self.decode_and_load_json(response)

    def patch_api(self, endpoint, body):
       
        response = self.http.patch(self.localhost + endpoint, headers = self.HEADERS,data = body)
        self.print_curl_request_and_response(response)
        return response

    def decode_and_load_json(self, response):
        try:
            text_response = response.content.decode('utf-8')
            data = json.loads(text_response)
        except Exception as e:
          
            logging.exception(str(e))
            return response
        return data

    def checkKey(self,dict,key):
        if key in dict:
            return True
        else:
            return False

    def check_server(self,address, port):
    # Create a TCP socket
        s = socket.socket()
    # print("Attempting to connect to {} on port {}".format(address, port))
        try:
            s.connect((address, port))
            # print( "Connected to %s on port %s" % (address, port))
            return True
        except socket.error:
            # print ("Connection to %s on port %s failed" % (address, port))
            return False
        finally:
            s.close()

    ### Helper functions end here

    @pytest.fixture(autouse=True)
    def slow_down_tests(self):
        yield
        time.sleep(5)

    @pytest.mark.order(0)
    def test_0_check_server_run_port_8081(self):
        """Verify if backend is running at port 8081"""
        status = self.check_server("localhost",8081)
        self.assertTrue(status)
            

    @pytest.mark.order(1)
    def test_1_get_all_pitches_when_empty_db(self):
        """Get All Pitches and Verify that response is an empty list and HTTP Status is OK"""
        endpoint = 'pitches'
        response = self.get_api(endpoint)
        self.assertEqual(response.status_code, 200)
        response_length = len(self.decode_and_load_json(response))
        self.assertEqual(0,response_length)

    @pytest.mark.order(2)
    def test_2_post_pitch(self):
        """Post a new Pitch and Verify that response is as per the API Spec and HTTP Status is Created """
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#1",
            "pitchTitle": "Sample Title #1",
            "pitchIdea" : "Sample Idea #1",
            "askAmount" : 1000000000,
            "equity": 25.3
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertEqual(1,len(data))


    @pytest.mark.order(3)
    def test_3_get_single_pitch(self):
        """Get a single Pitch provided id and Verify that response is as per the API Spec and HTTP Status is OK"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#2",
            "pitchTitle": "Sample Title #2",
            "pitchIdea" : "Sample Idea #2",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertEqual(1,len(data))
        endpoint = 'pitches/{}'.format(data["id"])
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertTrue(self.checkKey(data,"entrepreneur"))
        self.assertTrue(self.checkKey(data,"pitchIdea"))
        self.assertTrue(self.checkKey(data,"pitchTitle"))
        self.assertTrue(self.checkKey(data,"askAmount"))
        self.assertTrue(self.checkKey(data,"equity"))
        self.assertTrue(self.checkKey(data,"offers"))
        body["id"] = data["id"]
        body["offers"] = []
        self.assertDictEqual(body,data)
        self.assertEqual(7,len(data))


    @pytest.mark.order(4)
    def test_4_get_all_pitches_when_pitches_present_in_db(self):
        """Get all Pitches and Verify that response is as per the API Spec and HTTP Status is OK"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#3",
            "pitchTitle": "Sample Title #3",
            "pitchIdea" : "Sample Idea #3",
            "askAmount" : 1000000000,
            "equity": 25.3
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        response_length = len(self.decode_and_load_json(response))
        self.assertEqual(response_length, 3)


    @pytest.mark.order(5)
    def test_5_post_offer(self):
        """Post a new Offer provided pitch Id and Verify that response is as per the API Spec and HTTP Status is Created"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#4",
            "pitchTitle": "Sample Title #4",
            "pitchIdea" : "Sample Idea #4",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertEqual(1,len(data))
        endpoint = 'pitches/{}/makeOffer'.format(data["id"])
        body = {
            "investor": "Anupam Mittal",
            "amount" : 1000000000,
            "equity": 25.3,
            "comment":"A new concept in the ed-tech market. I can relate with the importance of the Learn By Doing philosophy. Keep up the Good Work! Definitely interested to work with you to scale the vision of the company!"
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertEqual(1,len(data))

# CRIO_SOLUTION_START_MODULE_BASIC

    @pytest.mark.order(6)
    def test_6_post_pitch_empty_body(self):
        """Post a new Pitch and Verify that response is HTTP Status Bad Request #1"""
        endpoint = 'pitches'
        body = {}
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(7)
    def test_7_post_pitch_invalid_body(self):
        """Post a new Pitch and Verify that response is HTTP Status Bad Request #2"""
        endpoint = 'pitches'
        body = {
            "entreprneur": "Yakshit#1",
            "pitcTitle": "Sample Title #1",
            "pitchIea" : "Sample Idea #1",
            "akAmount" : 1000000000,
            "equiy": 25
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(8)
    def test_8_post_pitch_invalid_data(self):
        """Post a new Pitch and Verify that response is HTTP Status Bad Request #3"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#5",
            "pitchTitle": "Sample Title #5",
            "pitchIdea" : "Sample Idea #5",
            "askAmount" : 1000000000,
            "equity": 1000
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)
        body = {
            "entrepreneur": None,
            "pitchTitle": None,
            "pitchIdea" : None,
            "askAmount" : None,
            "equity": None
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(9)
    def test_9_get_single_pitch_non_existent_test(self):
        """Get a Pitch provided non-existent id and response is HTTP Status Not Found"""
        endpoint = 'pitches/{}'.format("3412414")
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(10)
    def test_10_post_offer_empty_body(self):
        """Post a new Offer provided pitch id and Verify that response is HTTP Status Bad Request #1"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#6",
            "pitchTitle": "Sample Title #6",
            "pitchIdea" : "Sample Idea #6",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        endpoint = 'pitches/{}/makeOffer'.format(data["id"])
        body = {}
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(11)
    def test_11_post_offer_invalid_body(self):
        """Post a new Offer provided pitch id and Verify that response is HTTP Status Bad Request #2"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#7",
            "pitchTitle": "Sample Title #7",
            "pitchIdea" : "Sample Idea #7",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        endpoint = 'pitches/{}/makeOffer'.format(data["id"])
        body = {
            "invetor": "Anupam Mittal",
            "amont" : 1000000000,
            "euity": 25,
            "commen":"A new concept in the ed-tech market. I can relate with the importance of the Learn By Doing philosophy. Keep up the Good Work! Definitely interested to work with you to scale the vision of the company!"
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(12)
    def test_12_post_offer_invalid_data(self):
        """Post a new Offer provided pitch id  and Verify that response is HTTP Status Bad Request #3"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#8",
            "pitchTitle": "Sample Title #8",
            "pitchIdea" : "Sample Idea #8",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        endpoint = 'pitches/{}/makeOffer'.format(data["id"])
        body = {
            "investor": "Anupam Mittal",
            "amount" : 1000000000,
            "equity": 1000,
            "comment":"A new concept in the ed-tech market. I can relate with the importance of the Learn By Doing philosophy. Keep up the Good Work! Definitely interested to work with you to scale the vision of the company!"
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)
        body = {
            "investor": None,
            "amount" : None,
            "equity": None,
            "comment": None
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(13)
    def test_13_post_offer_invalid_pitch_id(self):
        """Post a new Offer provided pitch id  and Verify that response is HTTP Status Not Found"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#8",
            "pitchTitle": "Sample Title #8",
            "pitchIdea" : "Sample Idea #8",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        endpoint = 'pitches/{}/makeOffer'.format("hsdsddzfdhdDdgfd")
        body = {
            "investor": "Anupam Mittal",
            "amount" : 1000000000,
            "equity": 1000,
            "comment":"A new concept in the ed-tech market. I can relate with the importance of the Learn By Doing philosophy. Keep up the Good Work! Definitely interested to work with you to scale the vision of the company!"
        }
        response = self.post_api(endpoint, json.dumps(body))
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.order(14)
    def test_14_get_single_pitch_with_offer(self):
        """Get a single Pitch provided id and Verify that response is as per the API Spec and HTTP Status is OK #2"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#9",
            "pitchTitle": "Sample Title #9",
            "pitchIdea" : "Sample Idea #9",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        pitchId = data["id"]
        self.assertTrue(self.checkKey(data,"id"))
        endpoint = 'pitches/{}/makeOffer'.format(data["id"])
        offerBody = {
            "investor": "Anupam Mittal",
            "amount" : 1000000000,
            "equity": 25.3,
            "comment":"A new concept in the ed-tech market. I can relate with the importance of the Learn By Doing philosophy. Keep up the Good Work! Definitely interested to work with you to scale the vision of the company!"
        }
        response = self.post_api(endpoint, json.dumps(offerBody))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        endpoint = 'pitches/{}'.format(pitchId)
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertTrue(self.checkKey(data,"entrepreneur"))
        self.assertTrue(self.checkKey(data,"pitchIdea"))
        self.assertTrue(self.checkKey(data,"askAmount"))
        self.assertTrue(self.checkKey(data,"equity"))
        self.assertTrue(self.checkKey(data,"offers"))
        single_offer = data["offers"][0]
        self.assertTrue(self.checkKey(single_offer,"id"))
        self.assertTrue(self.checkKey(single_offer,"investor"))
        self.assertTrue(self.checkKey(single_offer,"amount"))
        self.assertTrue(self.checkKey(single_offer,"equity"))
        self.assertTrue(self.checkKey(single_offer,"comment"))
        body["id"] = data["id"]
        body["offers"] = data["offers"]
        self.assertDictEqual(body,data)

    @pytest.mark.order(15)
    def test_15_get_all_latest_pitches_when_pitches_present_in_db(self):
        """Get all Pitches and Verify that response is as per the API Spec and HTTP Status is OK #2"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#10",
            "pitchTitle": "Sample Title #10",
            "pitchIdea" : "Sample Idea #10",
            "askAmount" : 1000000000,
            "equity": 25.3
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        body["id"] = data["id"]
        body["offers"] = []
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertDictEqual(body,data[0])     
# CRIO_SOLUTION_END_MODULE_BASIC


if __name__ == '__main__':
    unittest.main()