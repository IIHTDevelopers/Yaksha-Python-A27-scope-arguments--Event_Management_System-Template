import pytest
from test.TestUtils import TestUtils
from event_management_system import (
    calculate_event_capacity,
    register_attendee,
    calculate_registration_stats,
    create_pricing_calculator,
    allocate_resources,
    calculate_resource_costs,
    check_resource_availability,
    generate_resource_report,
    categorize_expenses,
    analyze_budget_variance,
    calculate_event_profitability,
    generate_financial_projection,
    format_currency,
    format_percentage,
    attendee_check_in_generator
)

class TestExceptional:
    """Test class for exception handling tests of the Event Management System."""
    
    def test_error_handling(self):
        """Consolidated test for error handling of event management functions"""
        try:
            # Test invalid venue data
            invalid_venue = "not a dictionary"
            incomplete_venue = {"capacity": 100}  # Missing layout_options
            
            # Test invalid event data
            invalid_event = "not a dictionary"
            incomplete_event = {"name": "Test Event"}  # Missing capacity, etc.
            
            # Test venue capacity calculation with invalid inputs
            try:
                calculate_event_capacity(invalid_venue, "theater")
                assert False, "Should raise an exception with non-dict venue"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test venue capacity with incomplete venue data
            try:
                calculate_event_capacity(incomplete_venue, "theater")
                assert False, "Should raise an exception with incomplete venue"
            except (KeyError, AttributeError):
                pass  # Expected exception
                
            # Test venue capacity with invalid setup type
            valid_venue = {
                "capacity": 100,
                "layout_options": ["boardroom", "u-shape"],
                "availability": {"2023-09-15": True}
            }
            
            try:
                calculate_event_capacity(valid_venue, "invalid_setup")
                assert False, "Should raise ValueError with invalid setup type"
            except ValueError:
                pass  # Expected exception
                
            # Test registration with invalid inputs
            try:
                register_attendee(invalid_event, {"id": "A1"})
                assert False, "Should raise an exception with invalid event data"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test pricing calculator with invalid inputs
            try:
                invalid_calculator = create_pricing_calculator("not a number")
                assert False, "Should raise TypeError with non-numeric base fee"
            except (TypeError, ValueError):
                pass  # Expected exception
                
            # Test valid calculator with invalid inputs
            calculator = create_pricing_calculator(100)
            try:
                result = calculator(123, 1)  # Should expect string for ticket type
                # May handle gracefully or raise exception
            except (TypeError, ValueError, AttributeError):
                pass  # Exception is acceptable
                
            # Test resource allocation with invalid inputs
            try:
                allocate_resources(invalid_venue, 100, "conference")
                assert False, "Should raise an exception with invalid venue"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            try:
                allocate_resources(valid_venue, "not a number", "conference")
                assert False, "Should raise an exception with non-numeric attendees"
            except (TypeError, ValueError):
                pass  # Expected exception
                
            # Test resource costs with invalid inputs
            try:
                calculate_resource_costs("not a list")
                assert False, "Should raise an exception with non-list input"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test resource costs with invalid period
            resources = [{"type": "Chair", "quantity": 10, "cost_per_unit": 2.50}]
            negative_period = calculate_resource_costs(resources, rental_period=-1)
            assert "error" in negative_period, "Should return error for negative rental period"
            
            # Test resource availability with invalid inputs
            try:
                check_resource_availability(123, event_date="2023-09-15")
                # May handle gracefully or raise exception
            except (TypeError, AttributeError):
                pass  # Exception is acceptable
                
            # Test expense categorization with invalid inputs
            try:
                categorize_expenses(123, 456)  # Non-dict expenses
                assert False, "Should raise an exception or handle gracefully"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test with invalid expense data
            missing_fields = categorize_expenses({"description": "No category or amount"})
            assert missing_fields["total_expenses"] == 0, "Should handle missing fields gracefully"
            
            # Test budget variance with invalid inputs
            try:
                analyze_budget_variance("not a dict", {"venue": 1000})
                assert False, "Should raise an exception with non-dict input"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test profitability calculation with invalid inputs
            try:
                calculate_event_profitability("not a dict", {"venue": 1000})
                assert False, "Should raise an exception with non-dict input"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test financial projection with invalid inputs
            invalid_pricing = generate_financial_projection(1000, 100, "not a dict", discount_rate=0.1)
            assert "error" in invalid_pricing, "Should return error for invalid pricing tiers"
            
            invalid_discount = generate_financial_projection(1000, 100, {"standard": {"price": 50, "percentage": 100}}, discount_rate=2.0)
            assert "error" in invalid_discount, "Should return error for invalid discount rate"
            
            # Test formatting functions with invalid inputs
            try:
                format_currency("not a number")
                assert False, "Should raise TypeError with non-numeric input"
            except (TypeError, ValueError):
                pass  # Expected exception
                
            try:
                format_percentage("not a number")
                assert False, "Should raise TypeError with non-numeric input"
            except (TypeError, ValueError):
                pass  # Expected exception
                
            # Test generator with invalid inputs
            try:
                list(attendee_check_in_generator("not a dict"))
                assert False, "Should raise TypeError with non-dict input"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test with None values
            try:
                calculate_event_capacity(None, "theater")
                assert False, "Should raise TypeError with None input"
            except (TypeError, AttributeError):
                pass  # Expected exception
                
            # Test with edge cases that should be handled gracefully
            empty_event = {"capacity": 0, "registered_attendees": 0}
            empty_stats = calculate_registration_stats(empty_event)
            assert empty_stats["percentage_filled"] == 0, "Should handle empty event gracefully"
            
            TestUtils.yakshaAssert("TestErrorHandling", True, "exception")
        except Exception as e:
            TestUtils.yakshaAssert("TestErrorHandling", False, "exception")
            pytest.fail(f"Error handling test failed: {str(e)}")

    def test_invalid_inputs(self):
        """Test various invalid inputs across event management functions"""
        try:
            # Test with zero values where appropriate
            zero_capacity = calculate_event_capacity({"capacity": 0, "layout_options": ["theater"]}, "theater")
            assert zero_capacity == 0, "Zero capacity venue should return zero capacity"
            
            zero_attendees = allocate_resources({"capacity": 100, "layout_options": ["theater"]}, 0, "conference")
            assert isinstance(zero_attendees, list), "Zero attendees should return a valid resource list"
            
            zero_resources = calculate_resource_costs([])
            assert zero_resources["total_cost"] == 0, "Empty resources should have zero cost"
            
            # Test with negative values
            negative_resources = [
                {"type": "Chair", "quantity": -10, "cost_per_unit": 2.50},
                {"type": "Table", "quantity": 5, "cost_per_unit": -10.00}
            ]
            
            try:
                cost_result = calculate_resource_costs(negative_resources)
                # Should either handle gracefully or throw an exception
                if "error" not in cost_result:
                    # If no error, cost should still be calculated somehow (absolute values, zeros, etc.)
                    pass
            except ValueError:
                pass  # Exception is also acceptable
                
            # Test NaN and infinity handling
            import math
            
            try:
                nan_venue = {"capacity": math.nan, "layout_options": ["theater"]}
                nan_capacity = calculate_event_capacity(nan_venue, "theater")
                # Should either handle gracefully or throw an exception
            except (ValueError, TypeError):
                pass  # Expected exception
                
            try:
                inf_attendees = allocate_resources({"capacity": 100, "layout_options": ["theater"]}, math.inf, "conference")
                # Should either handle gracefully or throw an exception
            except (ValueError, TypeError, OverflowError):
                pass  # Expected exception
                
            # Test with malformed structures
            malformed_event = {
                "name": "Test Event",
                "registered_attendees": "not a number",  # Should be a number
                "capacity": 100
            }
            
            try:
                malformed_stats = calculate_registration_stats(malformed_event)
                # Should either handle gracefully or throw an exception
            except (TypeError, ValueError):
                pass  # Expected exception
                
            # Test with empty dictionaries or lists
            empty_dict_variance = analyze_budget_variance({}, {})
            assert empty_dict_variance["total_variance"] == 0, "Empty dictionaries should be handled gracefully"
            
            empty_revenue_profit = calculate_event_profitability({}, {})
            assert empty_revenue_profit[0] == 0 and empty_revenue_profit[1] == 0, "Empty revenue and expenses should be handled gracefully"
            
            # Test with missing required fields
            incomplete_resource = [{"type": "Chair"}]  # Missing quantity and cost_per_unit
            
            try:
                incomplete_cost = calculate_resource_costs(incomplete_resource)
                # Should either handle gracefully or throw an exception
            except (KeyError, AttributeError):
                pass  # Expected exception
                
            # Test generator with no attendees data
            no_attendees_checkin = list(attendee_check_in_generator({}))
            assert isinstance(no_attendees_checkin, list), "Generator should handle empty data gracefully"
            
            TestUtils.yakshaAssert("TestInvalidInputs", True, "exception")
        except Exception as e:
            TestUtils.yakshaAssert("TestInvalidInputs", False, "exception")
            pytest.fail(f"Invalid input test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])