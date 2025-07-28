import unittest
import sys
import os

# Add path for TestUtils and import the event management system
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from test.TestUtils import TestUtils
from skeleton import *

class TestEventManagementSystem(unittest.TestCase):
    def setUp(self):
        self.test_obj = TestUtils()
        self.events = get_sample_events()
        self.attendees = get_sample_attendees()
        self.venues = get_sample_venues()
        self.resources = get_sample_resources()

    def test_calculate_event_capacity(self):
        """
        Test case for calculate_event_capacity() function.
        """
        try:
            venue = self.venues["Convention Center"]
            result = calculate_event_capacity(venue, "theater")
            expected = 500  # 500 * 1.0
            if result == expected:
                self.test_obj.yakshaAssert("TestCalculateEventCapacity", True, "functional")
                print("TestCalculateEventCapacity = Passed")
            else:
                self.test_obj.yakshaAssert("TestCalculateEventCapacity", False, "functional")
                print("TestCalculateEventCapacity = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestCalculateEventCapacity", False, "functional")
            print("TestCalculateEventCapacity = Failed")

    def test_register_attendee(self):
        """
        Test case for register_attendee() function.
        """
        try:
            event = self.events[0]  # Tech Conference 2023
            attendee = self.attendees[0]
            result = register_attendee(event, attendee, ticket_type="VIP")
            if result["success"]:
                self.test_obj.yakshaAssert("TestRegisterAttendee", True, "functional")
                print("TestRegisterAttendee = Passed")
            else:
                self.test_obj.yakshaAssert("TestRegisterAttendee", False, "functional")
                print("TestRegisterAttendee = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestRegisterAttendee", False, "functional")
            print("TestRegisterAttendee = Failed")

    def test_calculate_registration_stats(self):
        """
        Test case for calculate_registration_stats() function.
        """
        try:
            event = self.events[0]
            stats = calculate_registration_stats(event)
            if isinstance(stats, dict) and "percentage_filled" in stats:
                self.test_obj.yakshaAssert("TestCalculateRegistrationStats", True, "functional")
                print("TestCalculateRegistrationStats = Passed")
            else:
                self.test_obj.yakshaAssert("TestCalculateRegistrationStats", False, "functional")
                print("TestCalculateRegistrationStats = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestCalculateRegistrationStats", False, "functional")
            print("TestCalculateRegistrationStats = Failed")

    def test_create_pricing_calculator(self):
        """
        Test case for create_pricing_calculator() function.
        """
        try:
            calc = create_pricing_calculator(100)
            result = calc("VIP", 1)
            expected = 200.0
            if result == expected:
                self.test_obj.yakshaAssert("TestCreatePricingCalculator", True, "functional")
                print("TestCreatePricingCalculator = Passed")
            else:
                self.test_obj.yakshaAssert("TestCreatePricingCalculator", False, "functional")
                print("TestCreatePricingCalculator = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestCreatePricingCalculator", False, "functional")
            print("TestCreatePricingCalculator = Failed")

    def test_allocate_resources(self):
        """
        Test case for allocate_resources() function.
        """
        try:
            venue = self.venues["Convention Center"]
            result = allocate_resources(venue, 300, "conference")
            if any(r["type"] == "Projector" for r in result):
                self.test_obj.yakshaAssert("TestAllocateResources", True, "functional")
                print("TestAllocateResources = Passed")
            else:
                self.test_obj.yakshaAssert("TestAllocateResources", False, "functional")
                print("TestAllocateResources = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestAllocateResources", False, "functional")
            print("TestAllocateResources = Failed")

    def test_calculate_event_profitability(self):
        """
        Test case for calculate_event_profitability() function.
        """
        try:
            revenue = {"tickets": 15000, "sponsorships": 5000}
            expenses = {"venue": 5000, "staff": 2000}
            result = calculate_event_profitability(revenue, expenses)
            expected_profit = 15000 + 5000 - (5000 + 2000)
            if result[2] == expected_profit:
                self.test_obj.yakshaAssert("TestCalculateEventProfitability", True, "functional")
                print("TestCalculateEventProfitability = Passed")
            else:
                self.test_obj.yakshaAssert("TestCalculateEventProfitability", False, "functional")
                print("TestCalculateEventProfitability = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestCalculateEventProfitability", False, "functional")
            print("TestCalculateEventProfitability = Failed")

    def test_check_resource_availability(self):
        """
        Test case for check_resource_availability() function.
        """
        try:
            res1 = {"type": "Projector", "quantity": 2, "cost_per_unit": 75.5}
            res2 = {"type": "Microphone", "quantity": 3, "cost_per_unit": 35.0}
            result = check_resource_availability(res1, res2, event_date="2023-09-15")
            if result["all_available"]:
                self.test_obj.yakshaAssert("TestCheckResourceAvailability", True, "functional")
                print("TestCheckResourceAvailability = Passed")
            else:
                self.test_obj.yakshaAssert("TestCheckResourceAvailability", False, "functional")
                print("TestCheckResourceAvailability = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestCheckResourceAvailability", False, "functional")
            print("TestCheckResourceAvailability = Failed")

    def test_generate_resource_report(self):
        """
        Test case for generate_resource_report() function.
        """
        try:
            result = generate_resource_report(include_costs=True)
            if "total_value" in result and result["total_value"] > 0:
                self.test_obj.yakshaAssert("TestGenerateResourceReport", True, "functional")
                print("TestGenerateResourceReport = Passed")
            else:
                self.test_obj.yakshaAssert("TestGenerateResourceReport", False, "functional")
                print("TestGenerateResourceReport = Failed")
        except Exception:
            self.test_obj.yakshaAssert("TestGenerateResourceReport", False, "functional")
            print("TestGenerateResourceReport = Failed")

if __name__ == '__main__':
    unittest.main()
