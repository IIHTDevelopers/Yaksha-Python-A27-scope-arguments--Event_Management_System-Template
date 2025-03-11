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

class TestBoundary:
    """Boundary tests for event management functions."""
    
    def test_boundary_scenarios(self):
        """Consolidated test for boundary scenarios across all functions"""
        try:
            # Test venues with extreme capacities
            small_venue = {
                "capacity": 10,
                "hourly_rate": 50.00,
                "layout_options": ["boardroom", "u-shape"],
                "availability": {"2023-09-15": True}
            }
            
            large_venue = {
                "capacity": 10000,
                "hourly_rate": 5000.00,
                "layout_options": ["theater", "expo"],
                "availability": {"2023-09-15": True}
            }
            
            # Test capacity calculations
            min_capacity = calculate_event_capacity(small_venue, "boardroom")
            max_capacity = calculate_event_capacity(large_venue, "theater")
            
            assert min_capacity > 0, "Even small venues should have positive capacity"
            assert max_capacity == 10000, "Theater setup should use full capacity"
            
            # Test event registration with boundary conditions
            empty_event = {
                "name": "Empty Event",
                "date": "2023-09-15",
                "venue": "Small Room",
                "capacity": 0,
                "registered_attendees": 0,
                "status": "upcoming"
            }
            
            full_event = {
                "name": "Full Event",
                "date": "2023-09-15",
                "venue": "Large Hall",
                "capacity": 100,
                "registered_attendees": 100,
                "status": "upcoming"
            }
            
            completed_event = {
                "name": "Past Event",
                "date": "2023-01-15",
                "venue": "Conference Room",
                "capacity": 50,
                "registered_attendees": 40,
                "status": "completed"
            }
            
            test_attendee = {
                "id": "A99999",
                "name": "Test User",
                "email": "test@example.com",
                "ticket_type": "Standard",
                "check_in_status": False
            }
            
            full_registration = register_attendee(full_event, test_attendee)
            completed_registration = register_attendee(completed_event, test_attendee)
            
            assert full_registration["success"] == False, "Registration should fail for full events"
            assert completed_registration["success"] == False, "Registration should fail for completed events"
            
            # Test registration stats with boundary conditions
            empty_stats = calculate_registration_stats(empty_event)
            full_stats = calculate_registration_stats(full_event)
            
            assert empty_stats["percentage_filled"] == 0, "Empty event should have 0% filled"
            assert empty_stats["remaining_spots"] == 0, "Empty event should have 0 remaining spots"
            assert full_stats["percentage_filled"] == 100, "Full event should have 100% filled"
            assert full_stats["is_sold_out"] == True, "Full event should be marked as sold out"
            
            # Test pricing calculator with boundary values
            free_calculator = create_pricing_calculator(0)
            expensive_calculator = create_pricing_calculator(1000)
            
            assert free_calculator("standard", 1) == 0, "Free tickets should cost $0"
            assert free_calculator("vip", 1) == 0, "Free VIP tickets should cost $0"
            assert expensive_calculator("standard", 100) < expensive_calculator("vip", 100), "VIP tickets should cost more than standard"
            
            # Test resource allocation with boundary conditions
            min_resources = allocate_resources(small_venue, 0, "workshop")
            max_resources = allocate_resources(large_venue, 10000, "conference")
            
            assert len(min_resources) > 0, "Even small events should require some resources"
            assert any(r["quantity"] >= 10000 for r in max_resources), "Large events should have resources for all attendees"
            
            # Test resource costs with boundary values
            empty_resources = []
            single_resource = [
                {"type": "Chair", "quantity": 1, "cost_per_unit": 2.50, "assigned_to": "Room"}
            ]
            expensive_resources = [
                {"type": "Stage", "quantity": 1, "cost_per_unit": 10000.00, "assigned_to": "Main Hall"}
            ]
            
            empty_costs = calculate_resource_costs(empty_resources)
            single_costs = calculate_resource_costs(single_resource)
            expensive_costs = calculate_resource_costs(expensive_resources, rental_period=7)
            zero_period_costs = calculate_resource_costs(single_resource, rental_period=0)
            
            assert "total_cost" in empty_costs, "Empty resources should still return a valid response"
            assert empty_costs["total_cost"] == 0, "Empty resources should have zero cost"
            assert single_costs["total_cost"] == 2.50, "Single resource cost should be calculated correctly"
            assert expensive_costs["total_cost"] >= 10000.00, "Expensive resources should have high cost"
            assert "error" in zero_period_costs, "Zero rental period should return an error"
            
            # Test resource availability with boundary conditions
            no_resources = check_resource_availability(event_date="2023-09-15")
            unavailable_date = check_resource_availability(
                {"type": "Projector", "quantity": 10}, 
                event_date="2099-01-01"
            )
            
            assert isinstance(no_resources, dict), "No resources should still return a valid response"
            assert "all_available" in unavailable_date, "Unavailable date should still return a valid response"
            
            # Test resource report with different options
            minimal_report = generate_resource_report(include_costs=False)
            detailed_report = generate_resource_report(format="detailed", include_costs=True)
            
            assert isinstance(minimal_report, dict), "Minimal report should be a dictionary"
            assert "options" in minimal_report, "Report should include the provided options"
            assert "total_value" not in minimal_report or minimal_report["total_value"] == 0, "Report without costs should not show value"
            assert "total_value" in detailed_report, "Detailed report with costs should include total value"
            
            # Test expense categorization with boundary values
            empty_expenses = categorize_expenses()
            single_expense = categorize_expenses(
                {"category": "venue", "amount": 1000, "description": "Venue rental"}
            )
            invalid_expense = categorize_expenses(
                {"category": "unknown", "amount": 500, "description": "Miscellaneous"}
            )
            
            assert single_expense["total_expenses"] == 1000, "Single expense should be totaled correctly"
            assert "venue_total" in single_expense, "Category totals should be calculated"
            assert "unknown" not in invalid_expense, "Invalid categories should be handled gracefully"
            assert "miscellaneous" in invalid_expense, "Unknown categories should go to miscellaneous"
            
            # Test budget variance with boundary values
            empty_planned = {}
            empty_actual = {}
            simple_planned = {"venue": 1000}
            simple_actual = {"venue": 1200}
            
            empty_variance = analyze_budget_variance(empty_planned, empty_actual)
            simple_variance = analyze_budget_variance(simple_planned, simple_actual)
            
            assert empty_variance["total_variance"] == 0, "Empty budgets should have zero variance"
            assert simple_variance["total_variance"] < 0, "Over budget should have negative variance"
            assert "categories" in simple_variance, "Variance should include category details"
            assert "venue" in simple_variance["categories"], "Variance should include the provided category"
            
            # Test profitability calculation with boundary values
            zero_revenue = {}
            zero_expenses = {}
            balanced_revenue = {"tickets": 5000}
            balanced_expenses = {"venue": 5000}
            profitable_revenue = {"tickets": 10000}
            profitable_expenses = {"venue": 5000}
            
            zero_profit = calculate_event_profitability(zero_revenue, zero_expenses)
            balanced_profit = calculate_event_profitability(balanced_revenue, balanced_expenses)
            high_profit = calculate_event_profitability(profitable_revenue, profitable_expenses)
            
            assert zero_profit[0] == 0, "Zero revenue should be calculated correctly"
            assert zero_profit[2] == 0, "Zero net profit should be calculated correctly"
            assert balanced_profit[2] == 0, "Balanced budget should have zero profit"
            assert high_profit[2] > 0, "Profitable event should have positive net profit"
            assert high_profit[3] == 50.0, "Profit margin should be calculated correctly"
            
            # Test financial projection with boundary values
            empty_tiers = generate_financial_projection(0, 0, {}, discount_rate=0)
            negative_inputs = generate_financial_projection(-1000, -10, {"standard": {"price": 100, "percentage": 100}}, discount_rate=0)
            simple_projection = generate_financial_projection(1000, 100, 
                {"standard": {"price": 50, "percentage": 100}}, 
                discount_rate=0.1
            )
            
            assert "error" in negative_inputs, "Negative inputs should return an error"
            assert "costs" in simple_projection, "Projection should include costs"
            assert "revenue" in simple_projection, "Projection should include revenue"
            assert "net_profit" in simple_projection, "Projection should include net profit"
            
            # Test formatting functions with boundary values
            zero_currency = format_currency(0)
            small_currency = format_currency(0.01)
            large_currency = format_currency(1000000)
            
            zero_percent = format_percentage(0)
            small_percent = format_percentage(0.01)
            large_percent = format_percentage(100)
            
            assert zero_currency == "$0.00", "Zero should format as $0.00"
            assert small_currency == "$0.01", "Small amount should format as $0.01"
            assert large_currency == "$1,000,000.00", "Large amount should format correctly"
            assert zero_percent == "0.00%", "Zero should format as 0.00%"
            assert small_percent == "0.01%", "Small percentage should format as 0.01%"
            assert large_percent == "100.00%", "Large percentage should format as 100.00%"
            
            # Test generator with boundary values
            empty_data = {"attendees": []}
            single_attendee = {"attendees": [{"id": "A1", "name": "Test", "check_in_status": True}], "hour_9": 1}
            
            empty_gen = list(attendee_check_in_generator(empty_data))
            single_gen = list(attendee_check_in_generator(single_attendee))
            
            assert len(empty_gen) >= 1, "Empty data should yield at least one value"
            assert "No attendees" in empty_gen[0][0], "Empty data should indicate no attendees"
            assert len(single_gen) > 0, "Single attendee should yield values"
            
            TestUtils.yakshaAssert("TestBoundaryScenarios", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            pytest.fail(f"Boundary scenarios test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])