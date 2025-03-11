import pytest
import inspect
import sys
from test.TestUtils import TestUtils
from event_management_system import *

class TestFunctional:
    """Test class to verify event management functions match requirements"""
    
    def test_required_functions_and_scope(self):
        """Test required functions exist and use proper scope management"""
        try:
            # List of required function names
            required_functions = [
                "calculate_event_capacity", "register_attendee", 
                "calculate_registration_stats", "create_pricing_calculator",
                "allocate_resources", "calculate_resource_costs", 
                "check_resource_availability", "generate_resource_report",
                "categorize_expenses", "analyze_budget_variance", 
                "calculate_event_profitability", "generate_financial_projection",
                "format_currency", "format_percentage", 
                "attendee_check_in_generator", "main"
            ]
            
            # Import current module
            current_module = sys.modules["event_management_system"]
            
            # Get all function names from the module
            module_functions = [name for name, obj in inspect.getmembers(current_module) 
                                if inspect.isfunction(obj) and not name.startswith('_')]
            
            # Check each required function exists
            for func_name in required_functions:
                assert func_name in module_functions, f"Required function '{func_name}' is missing"
            
            # Check that register_attendee uses keyword-only arguments
            sig = inspect.signature(register_attendee)
            has_keyword_only = any(p.kind == p.KEYWORD_ONLY for p in sig.parameters.values())
            assert has_keyword_only, "register_attendee should use keyword-only arguments"
            
            # Check that create_pricing_calculator creates closure and uses nonlocal
            pricing_code = inspect.getsource(create_pricing_calculator)
            assert "def calculate_price" in pricing_code, "Missing nested function in create_pricing_calculator"
            assert "nonlocal" in pricing_code, "Missing nonlocal keyword in create_pricing_calculator"
            
            # Test the closure behavior
            calculator = create_pricing_calculator(100)
            assert callable(calculator), "create_pricing_calculator should return a function"
            
            # Test position-only arguments in financial projection
            sig = inspect.signature(generate_financial_projection)
            has_pos_only = any(p.kind == p.POSITIONAL_ONLY for p in sig.parameters.values())
            assert has_pos_only, "generate_financial_projection should use position-only arguments"
            
            # Test generator function
            test_data = {"attendees": [{"id": "A1"}], "hour_9": 1}
            generator = attendee_check_in_generator(test_data)
            assert inspect.isgenerator(generator), "attendee_check_in_generator should return a generator"
            
            TestUtils.yakshaAssert("TestRequiredFunctionsAndScope", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestRequiredFunctionsAndScope", False, "functional")
            pytest.fail(f"Function and scope test failed: {str(e)}")
    
    def test_core_functionality(self):
        """Test core event management functionality"""
        try:
            # Test event capacity calculation
            venue = {
                "capacity": 200,
                "layout_options": ["theater", "classroom", "banquet"],
                "availability": {"2023-09-15": True}
            }
            
            theater_capacity = calculate_event_capacity(venue, "theater")
            classroom_capacity = calculate_event_capacity(venue, "classroom")
            banquet_capacity = calculate_event_capacity(venue, "banquet")
            
            assert theater_capacity == 200, "Theater setup should use full capacity"
            assert classroom_capacity == 120, "Classroom setup should be 60% of full capacity"
            assert banquet_capacity == 100, "Banquet setup should be 50% of full capacity"
            
            # Test registration functionality
            event = {
                "name": "Test Event",
                "date": "2023-09-15",
                "venue": "Test Venue",
                "capacity": 100,
                "registered_attendees": 50,
                "status": "upcoming"
            }
            
            attendee = {
                "id": "A12345",
                "name": "Test User",
                "email": "test@example.com",
                "ticket_type": "Standard",
                "check_in_status": False
            }
            
            # Test registration with default and explicit ticket type
            default_registration = register_attendee(event, attendee)
            vip_registration = register_attendee(event, attendee, ticket_type="VIP")
            
            assert default_registration["ticket_type"].lower() == "standard", "Default ticket type should be standard"
            assert vip_registration["ticket_type"] == "VIP", "Explicit ticket type should be used"
            assert default_registration["event_name"] == "Test Event", "Registration should include event name"
            
            # Test registration stats
            event_full = {
                "name": "Full Event",
                "date": "2023-09-15",
                "venue": "Test Venue",
                "capacity": 100,
                "registered_attendees": 100,
                "status": "upcoming"
            }
            
            stats = calculate_registration_stats(event)
            full_stats = calculate_registration_stats(event_full)
            
            assert stats["percentage_filled"] == 50.0, "Percentage filled should be 50%"
            assert stats["remaining_spots"] == 50, "Remaining spots should be 50"
            assert stats["is_sold_out"] == False, "Event should not be marked as sold out"
            assert full_stats["is_sold_out"] == True, "Event at capacity should be marked as sold out"
            
            # Test pricing calculator
            calculator = create_pricing_calculator(100)
            standard_price = calculator("standard", 1)
            vip_price = calculator("vip", 1)
            early_bird_price = calculator("early_bird", 1)
            group_price = calculator("standard", 10)
            
            assert standard_price == 100, "Standard price should be base fee"
            assert vip_price == 200, "VIP price should be double the base fee"
            assert early_bird_price == 80, "Early bird price should be 80% of base fee"
            assert group_price == 900, "Group of 10 should get 10% discount (90 × 10 = 900)"
            
            TestUtils.yakshaAssert("TestCoreFunctionality", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestCoreFunctionality", False, "functional")
            pytest.fail(f"Core functionality test failed: {str(e)}")
    
    def test_resource_management(self):
        """Test resource management functionality"""
        try:
            venue = {
                "capacity": 200,
                "layout_options": ["theater", "classroom"],
                "availability": {"2023-09-15": True}
            }
            
            # Test resource allocation
            resources = allocate_resources(venue, 100, "conference")
            assert any(r["type"] == "Chair" and r["quantity"] == 100 for r in resources), "Should allocate chairs for all attendees"
            assert any(r["type"] == "Projector" for r in resources), "Conference should include projector"
            assert any(r["type"] == "Table" for r in resources), "Conference should include tables"
            
            # Test resource cost calculation
            test_resources = [
                {"type": "Chair", "quantity": 100, "cost_per_unit": 2.50, "assigned_to": "Main Hall"},
                {"type": "Projector", "quantity": 2, "cost_per_unit": 75.00, "assigned_to": "Main Hall"}
            ]
            
            # Test with rental period = 1 (default)
            costs1 = calculate_resource_costs(test_resources)
            expected_total1 = (100 * 2.50) + (2 * 75.00)
            assert costs1["total_cost"] == expected_total1, "Total cost calculation with default rental period is incorrect"
            
            # Test with rental period = 3
            costs3 = calculate_resource_costs(test_resources, rental_period=3)
            expected_total3 = expected_total1 * 3
            assert costs3["total_cost"] == expected_total3, "Total cost calculation with rental period = 3 is incorrect"
            
            # Test resource availability with *args
            resource1 = {"type": "Projector", "quantity": 2}
            resource2 = {"type": "Microphone", "quantity": 5}
            resource3 = {"type": "Chair", "quantity": 500}  # Edge case - exactly available amount
            
            single_check = check_resource_availability(resource1, event_date="2023-09-15")
            multi_check = check_resource_availability(resource1, resource2, event_date="2023-09-15")
            edge_check = check_resource_availability(resource3, event_date="2023-09-15")
            
            assert "resources" in single_check, "Resource check should return resources info"
            assert "Projector" in single_check["resources"], "Resource check should include requested resource type"
            assert len(multi_check["resources"]) == 2, "Multi-resource check should include both resources"
            assert edge_check["resources"]["Chair"]["available"] == True, "Resource with quantity equal to available should be available"
            assert edge_check["all_available"] == True, "All resources should be available when quantities match exactly"
            
            # Test resource report options
            basic_report = generate_resource_report()
            detailed_report = generate_resource_report(format="detailed", include_costs=True)
            no_costs_report = generate_resource_report(include_costs=False)
            
            assert "options" in basic_report, "Report should include options"
            assert basic_report["options"]["format"] == "summary", "Default format should be summary"
            assert detailed_report["options"]["format"] == "detailed", "Format option should be respected"
            assert detailed_report["total_value"] > 0, "Report with costs should have positive total value"
            assert no_costs_report["total_value"] == 0, "Report without costs should have zero total value"
            
            TestUtils.yakshaAssert("TestResourceManagement", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestResourceManagement", False, "functional")
            pytest.fail(f"Resource management test failed: {str(e)}")
    
    def test_financial_analysis(self):
        """Test financial analysis functionality"""
        try:
            # Test expense categorization
            expenses = [
                {"category": "venue", "amount": 1000, "description": "Venue rental"},
                {"category": "catering", "amount": 500, "description": "Food"},
                {"category": "catering", "amount": 300, "description": "Drinks"},
                {"category": "marketing", "amount": 200, "description": "Advertising"},
                {"category": "unknown", "amount": 300, "description": "Miscellaneous"}
            ]
            
            categorized = categorize_expenses(*expenses)
            assert categorized["total_expenses"] == 2300, "Total expenses should be calculated correctly"
            assert categorized["venue"]["Venue rental"] == 1000, "Venue expense should be categorized correctly"
            assert categorized["catering"]["Food"] + categorized["catering"]["Drinks"] == 800, "Catering expenses should be categorized correctly"
            assert categorized["miscellaneous"]["Miscellaneous"] == 300, "Unknown category should go to miscellaneous"
            assert categorized["venue_total"] == 1000, "Venue category total should be calculated correctly"
            assert categorized["catering_total"] == 800, "Catering category total should be calculated correctly"
            
            # Test with missing fields
            missing_fields = [
                {"category": "venue"},  # Missing amount
                {"amount": 300}  # Missing category
            ]
            
            missing_categorized = categorize_expenses(*missing_fields)
            assert missing_categorized["total_expenses"] == 0, "Missing fields should be handled gracefully"
            
            # Test budget variance calculation
            planned = {"venue": 1000, "catering": 700, "marketing": 300}
            actual = {"venue": 1200, "catering": 650, "marketing": 250, "staff": 100}
            
            variance = analyze_budget_variance(planned, actual)
            assert variance["total_planned"] == 2000, "Total planned should be calculated correctly"
            assert variance["total_actual"] == 2200, "Total actual should be calculated correctly"
            assert variance["total_variance"] == -200, "Total variance should be calculated correctly (planned - actual)"
            assert variance["categories"]["venue"]["variance"] == -200, "Venue variance should be calculated correctly"
            assert variance["categories"]["staff"]["planned"] == 0, "Missing planned category should default to 0"
            
            # Test profitability calculation
            revenue = {"tickets": 10000, "sponsorships": 5000, "merchandise": 2000}
            expenses = {"venue": 5000, "catering": 3000, "marketing": 2000}
            
            profit_data = calculate_event_profitability(revenue, expenses)
            total_revenue, total_expenses, net_profit, profit_margin, roi = profit_data
            
            assert total_revenue == 17000, "Total revenue should be calculated correctly"
            assert total_expenses == 10000, "Total expenses should be calculated correctly"
            assert net_profit == 7000, "Net profit should be calculated correctly"
            assert profit_margin == (7000 / 17000) * 100, "Profit margin should be calculated correctly"
            assert roi == (7000 / 10000) * 100, "ROI should be calculated correctly"
            
            # Test financial projection
            pricing_tiers = {
                "standard": {"price": 50, "percentage": 80},
                "vip": {"price": 100, "percentage": 20}
            }
            
            projection = generate_financial_projection(5000, 100, pricing_tiers)
            discount_projection = generate_financial_projection(5000, 100, pricing_tiers, discount_rate=0.1)
            
            # Standard tier: 80 attendees at $50 each = $4000
            # VIP tier: 20 attendees at $100 each = $2000
            # Total revenue: $6000
            expected_revenue = 6000
            expected_discounted_revenue = 6000 * 0.9  # 10% discount
            
            assert projection["revenue"]["total"] == expected_revenue, "Revenue calculation is incorrect"
            assert discount_projection["revenue"]["total"] == expected_discounted_revenue, "Discounted revenue calculation is incorrect"
            assert projection["costs"]["variable"] == 100 * 25, "Variable costs should be $25 per attendee"
            assert projection["net_profit"] == expected_revenue - (5000 + (100 * 25)), "Net profit calculation is incorrect"
            
            # Test formatting functions
            assert format_currency(1234.56) == "$1,234.56", "Currency formatting is incorrect"
            assert format_percentage(12.34) == "12.34%", "Percentage formatting is incorrect"
            
            TestUtils.yakshaAssert("TestFinancialAnalysis", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestFinancialAnalysis", False, "functional")
            pytest.fail(f"Financial analysis test failed: {str(e)}")
    
    def test_check_in_generator(self):
        """Test the check-in generator functionality"""
        try:
            # Test with multiple check-in times
            check_in_data = {
                "attendees": [{"id": "A1"}, {"id": "A2"}, {"id": "A3"}, {"id": "A4"}],
                "hour_8": 1,  # 25%
                "hour_9": 1,  # +25% = 50%
                "hour_10": 1,  # +25% = 75%
                "hour_11": 1  # +25% = 100%
            }
            
            # Generate check-in data
            hours = list(attendee_check_in_generator(check_in_data))
            
            # There should be at least 4 hours (8-11)
            assert len(hours) >= 4, "Generator should yield at least 4 entries"
            
            # First check the structure of the tuple to avoid index errors
            if len(hours) > 0 and len(hours[0]) == 3:
                # Check progressive percentages
                hours_dict = {h[0]: (h[1], h[2]) for h in hours if h[0] != "No attendees registered"}
                
                # Verify cumulative percentages
                if "8:00" in hours_dict and "9:00" in hours_dict:
                    assert hours_dict["9:00"][1] > hours_dict["8:00"][1], "Percentages should increase cumulatively"
            
            # Final hour should show 100% check-in if all attendees checked in
            if "11:00" in hours_dict and len(hours_dict["11:00"]) > 1:
                assert abs(hours_dict["11:00"][1] - 100.0) < 0.01, "Final hour should show 100% if all attendees checked in"
            
            # Test with no attendees
            empty_data = {"attendees": []}
            empty_hours = list(attendee_check_in_generator(empty_data))
            assert len(empty_hours) >= 1, "Should yield at least one result for empty data"
            assert "No attendees" in empty_hours[0][0], "Should indicate no attendees"
            
            # Test with missing attendees key
            missing_key_data = {"hour_9": 2}
            missing_key_hours = list(attendee_check_in_generator(missing_key_data))
            assert len(missing_key_hours) >= 1, "Should yield at least one result for missing attendees key"
            assert "No attendees" in missing_key_hours[0][0], "Should indicate no attendees when key is missing"
            
            # Test with partial check-ins
            partial_data = {
                "attendees": [{"id": "A1"}, {"id": "A2"}, {"id": "A3"}, {"id": "A4"}],
                "hour_9": 2,  # 50%
                "hour_10": 1  # +25% = 75%
            }
            
            partial_hours = list(attendee_check_in_generator(partial_data))
            partial_hours_dict = {h[0]: (h[1], h[2]) for h in partial_hours if h[0] != "No attendees registered"}
            
            # The total checked in should be 75% of attendees
            if len(partial_hours) > 0 and len(partial_hours[0]) == 3:
                max_percentage = max(h[2] for h in partial_hours if h[0] != "No attendees registered" and len(h) == 3)
                assert abs(max_percentage - 75.0) < 0.01, "Maximum check-in percentage should be 75%"
            
            TestUtils.yakshaAssert("TestCheckInGenerator", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestCheckInGenerator", False, "functional")
            pytest.fail(f"Check-in generator test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])