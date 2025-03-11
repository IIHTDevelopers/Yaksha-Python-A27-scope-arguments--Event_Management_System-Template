"""
Event Management System

This module provides functions for managing events, resources, budgets,
and generating reports for event planning and execution.
"""

# Sample data for demonstration
def get_sample_events():
    """Return sample event data for demonstration."""
    return [
        {"name": "Tech Conference 2023", "date": "2023-09-15", "venue": "Convention Center", 
         "capacity": 500, "registered_attendees": 350, "status": "upcoming"},
        {"name": "Charity Gala", "date": "2023-10-20", "venue": "Grand Ballroom", 
         "capacity": 250, "registered_attendees": 200, "status": "upcoming"},
        {"name": "Product Launch", "date": "2023-08-05", "venue": "Innovation Hub", 
         "capacity": 150, "registered_attendees": 150, "status": "completed"}
    ]

def get_sample_attendees():
    """Return sample attendee data for demonstration."""
    return [
        {"id": "A12345", "name": "Jane Smith", "email": "jane@example.com", 
         "ticket_type": "VIP", "check_in_status": False},
        {"id": "A12346", "name": "John Doe", "email": "john@example.com", 
         "ticket_type": "Standard", "check_in_status": True},
        {"id": "A12347", "name": "Mary Johnson", "email": "mary@example.com", 
         "ticket_type": "VIP", "check_in_status": True}
    ]

def get_sample_resources():
    """Return sample resource data for demonstration."""
    return [
        {"type": "Projector", "quantity": 3, "cost_per_unit": 75.50, "assigned_to": "Main Hall"},
        {"type": "Microphone", "quantity": 5, "cost_per_unit": 35.00, "assigned_to": "Main Hall"},
        {"type": "Chair", "quantity": 200, "cost_per_unit": 2.50, "assigned_to": "Main Hall"}
    ]

def get_sample_venues():
    """Return sample venue data for demonstration."""
    return {
        "Convention Center": {
            "capacity": 500, "hourly_rate": 750.00,
            "layout_options": ["theater", "classroom", "expo"],
            "availability": {"2023-09-15": True, "2023-10-20": False}
        },
        "Grand Ballroom": {
            "capacity": 250, "hourly_rate": 500.00,
            "layout_options": ["banquet", "reception", "theater"],
            "availability": {"2023-09-15": False, "2023-10-20": True}
        }
    }

# Event Management Functions
def calculate_event_capacity(venue, setup_type):
    """Calculate the maximum capacity of a venue based on setup type."""
    if not isinstance(venue, dict):
        raise TypeError("Venue must be a dictionary")
    
    if "capacity" not in venue or "layout_options" not in venue:
        raise KeyError("Venue must have capacity and layout_options")
    
    base_capacity = venue["capacity"]
    
    capacity_multipliers = {
        "theater": 1.0, "classroom": 0.6, "banquet": 0.5, "reception": 0.8,
        "expo": 0.4, "u-shape": 0.3, "boardroom": 0.7, "workshop": 0.5
    }
    
    if setup_type not in venue["layout_options"]:
        raise ValueError(f"Setup type '{setup_type}' is not available for this venue")
    
    adjusted_capacity = int(base_capacity * capacity_multipliers.get(setup_type, 1.0))
    return adjusted_capacity

def register_attendee(event, attendee, *, ticket_type="standard"):
    """Register an attendee for an event. Uses keyword-only arguments."""
    if not isinstance(event, dict) or not isinstance(attendee, dict):
        raise TypeError("Event and attendee must be dictionaries")
    
    if "registered_attendees" not in event or "capacity" not in event or "status" not in event:
        raise KeyError("Event must have registered_attendees, capacity, and status")
    
    if "id" not in attendee:
        raise KeyError("Attendee must have an id")
    
    if event["registered_attendees"] >= event["capacity"]:
        return {"success": False, "message": "Event is at full capacity"}
    
    if event["status"] != "upcoming":
        return {"success": False, "message": "Registration is closed for this event"}
    
    registration = {
        "attendee_id": attendee["id"],
        "event_name": event["name"],
        "event_date": event["date"],
        "ticket_type": ticket_type,
        "success": True,
        "message": f"Successfully registered for {event['name']}"
    }
    
    return registration

def calculate_registration_stats(event):
    """Calculate registration statistics for an event."""
    if not isinstance(event, dict):
        raise TypeError("Event must be a dictionary")
    
    if "registered_attendees" not in event or "capacity" not in event:
        raise KeyError("Event must have registered_attendees and capacity")
    
    registered = event["registered_attendees"]
    capacity = event["capacity"]
    
    if not isinstance(registered, (int, float)) or not isinstance(capacity, (int, float)):
        raise TypeError("Registered attendees and capacity must be numbers")
    
    percentage_filled = (registered / capacity) * 100 if capacity > 0 else 0
    remaining_spots = capacity - registered
    is_sold_out = registered >= capacity
    
    return {
        "total_capacity": capacity,
        "registered_attendees": registered,
        "percentage_filled": percentage_filled,
        "remaining_spots": remaining_spots,
        "is_sold_out": is_sold_out
    }

def create_pricing_calculator(base_fee):
    """Create a function that calculates ticket prices. Uses closures and nested functions."""
    if not isinstance(base_fee, (int, float)):
        raise TypeError("Base fee must be a number")
    
    standard_price = base_fee
    vip_price = base_fee * 2.0
    early_bird_price = base_fee * 0.8
    group_price = base_fee * 0.9
    
    def calculate_price(ticket_type, quantity):
        """Calculate the total price based on ticket type and quantity."""
        nonlocal standard_price, vip_price, early_bird_price, group_price
        
        if not isinstance(ticket_type, str):
            raise TypeError("Ticket type must be a string")
        
        if not isinstance(quantity, (int, float)):
            raise TypeError("Quantity must be a number")
        
        if quantity >= 10 and ticket_type.lower() == "standard":
            return quantity * group_price
        
        if ticket_type.lower() == "vip":
            return quantity * vip_price
        elif ticket_type.lower() == "early_bird":
            return quantity * early_bird_price
        else:  # Standard is the default
            return quantity * standard_price
    
    return calculate_price

# Resource Management Functions
def allocate_resources(venue, attendees, event_type):
    """Determine resource needs based on venue, attendees, and event type."""
    if not isinstance(venue, dict):
        raise TypeError("Venue must be a dictionary")
    
    if not isinstance(attendees, (int, float)):
        raise TypeError("Attendees must be a number")
    
    if not isinstance(event_type, str):
        raise TypeError("Event type must be a string")
    
    resources = []
    resources.append({"type": "Chair", "quantity": attendees, "notes": "One per attendee"})
    
    if event_type.lower() == "conference":
        resources.append({"type": "Projector", "quantity": max(1, attendees // 100)})
        resources.append({"type": "Microphone", "quantity": max(2, attendees // 50)})
        resources.append({"type": "Table", "quantity": max(5, attendees // 10)})
    elif event_type.lower() == "gala":
        resources.append({"type": "Table", "quantity": attendees // 8})
        resources.append({"type": "Speaker System", "quantity": 1})
    
    return resources

def calculate_resource_costs(resources, rental_period=1):
    """Calculate the cost of resources based on rental period."""
    if not isinstance(resources, list):
        raise TypeError("Resources must be a list")
    
    if rental_period < 1:
        return {"error": "Rental period must be at least 1 day"}
    
    cost_breakdown = {}
    total_cost = 0
    
    for resource in resources:
        if not isinstance(resource, dict):
            raise TypeError("Each resource must be a dictionary")
            
        if "type" not in resource or "quantity" not in resource or "cost_per_unit" not in resource:
            raise KeyError("Each resource must have type, quantity, and cost_per_unit")
            
        resource_type = resource["type"]
        quantity = resource["quantity"]
        cost_per_unit = resource["cost_per_unit"]
        
        resource_cost = quantity * cost_per_unit * rental_period
        cost_breakdown[resource_type] = resource_cost
        total_cost += resource_cost
    
    return {"cost_breakdown": cost_breakdown, "total_cost": total_cost}

def check_resource_availability(*resources, event_date):
    """Check if specified resources are available. Uses *args."""
    if not isinstance(event_date, str):
        raise TypeError("Event date must be a string")
        
    for resource in resources:
        if not isinstance(resource, dict):
            raise TypeError("Each resource must be a dictionary")
    
    availability_database = {
        "Projector": {"2023-09-15": 5, "2023-10-20": 3},
        "Microphone": {"2023-09-15": 10, "2023-10-20": 8},
        "Chair": {"2023-09-15": 500, "2023-10-20": 300}
    }
    
    availability_results = {}
    
    for resource in resources:
        resource_type = resource["type"]
        quantity_needed = resource["quantity"]
        
        if resource_type not in availability_database:
            availability_results[resource_type] = {"available": False}
            continue
            
        if event_date not in availability_database[resource_type]:
            availability_results[resource_type] = {"available": False}
            continue
        
        quantity_available = availability_database[resource_type][event_date]
        is_available = quantity_available >= quantity_needed
        
        availability_results[resource_type] = {
            "available": is_available,
            "quantity_available": quantity_available
        }
    
    all_available = all(result["available"] for result in availability_results.values()) if availability_results else False
    return {"all_available": all_available, "resources": availability_results}

def generate_resource_report(**options):
    """Generate a resource report with various options. Uses **kwargs."""
    default_options = {
        "include_costs": True,
        "format": "summary"
    }
    
    for key, value in default_options.items():
        if key not in options:
            options[key] = value
    
    resources = get_sample_resources()
    total_value = sum(r["quantity"] * r["cost_per_unit"] for r in resources) if options["include_costs"] else 0
    
    return {
        "options": options,
        "resource_count": len(resources),
        "total_value": total_value
    }

# Budget Analysis Functions
def categorize_expenses(*expenses):
    """Categorize expenses by type. Uses *args."""
    for expense in expenses:
        if not isinstance(expense, dict):
            raise TypeError("Each expense must be a dictionary")
    
    categorized = {
        "venue": {}, "catering": {}, "marketing": {}, 
        "staff": {}, "equipment": {}, "miscellaneous": {},
        "total_expenses": 0
    }
    
    # Add category totals
    categorized["venue_total"] = 0
    categorized["catering_total"] = 0
    categorized["marketing_total"] = 0
    categorized["staff_total"] = 0
    categorized["equipment_total"] = 0
    categorized["miscellaneous_total"] = 0
    
    for expense in expenses:
        if "category" not in expense or "amount" not in expense:
            continue
            
        category = expense["category"].lower()
        amount = expense["amount"]
        description = expense.get("description", "No description")
        
        if category in categorized:
            if description not in categorized[category]:
                categorized[category][description] = 0
            categorized[category][description] += amount
            categorized[f"{category}_total"] += amount
        else:
            if description not in categorized["miscellaneous"]:
                categorized["miscellaneous"][description] = 0
            categorized["miscellaneous"][description] += amount
            categorized["miscellaneous_total"] += amount
        
        categorized["total_expenses"] += amount
    
    return categorized

def analyze_budget_variance(planned, actual):
    """Calculate the variance between planned and actual budgets."""
    if not isinstance(planned, dict) or not isinstance(actual, dict):
        raise TypeError("Planned and actual budgets must be dictionaries")
    
    variance_analysis = {
        "categories": {},
        "total_planned": sum(planned.values()),
        "total_actual": sum(actual.values())
    }
    
    all_categories = set(list(planned.keys()) + list(actual.keys()))
    
    for category in all_categories:
        planned_amount = planned.get(category, 0)
        actual_amount = actual.get(category, 0)
        variance = planned_amount - actual_amount
        
        variance_analysis["categories"][category] = {
            "planned": planned_amount,
            "actual": actual_amount,
            "variance": variance
        }
    
    variance_analysis["total_variance"] = variance_analysis["total_planned"] - variance_analysis["total_actual"]
    return variance_analysis

def calculate_event_profitability(revenue, expenses):
    """Calculate the profitability of an event."""
    if not isinstance(revenue, dict) or not isinstance(expenses, dict):
        raise TypeError("Revenue and expenses must be dictionaries")
    
    total_revenue = sum(revenue.values())
    total_expenses = sum(expenses.values())
    
    net_profit = total_revenue - total_expenses
    profit_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0
    roi = (net_profit / total_expenses) * 100 if total_expenses > 0 else 0
    
    return (total_revenue, total_expenses, net_profit, profit_margin, roi)

def generate_financial_projection(base_cost, attendees, pricing_tiers, /, *, discount_rate=0):
    """Generate a financial projection. Uses position-only and keyword-only args."""
    if base_cost < 0 or attendees < 0:
        return {"error": "Base cost and attendees must be positive"}
    
    if not isinstance(pricing_tiers, dict):
        return {"error": "Pricing tiers must be a dictionary"}
    
    if discount_rate < 0 or discount_rate > 1:
        return {"error": "Discount rate must be between 0 and 1"}
    
    fixed_costs = base_cost
    
    revenue_by_tier = {}
    total_revenue = 0
    
    for tier, details in pricing_tiers.items():
        price = details["price"]
        percentage = details["percentage"] / 100
        tier_attendees = int(attendees * percentage)
        tier_revenue = tier_attendees * price * (1 - discount_rate)
        
        revenue_by_tier[tier] = tier_revenue
        total_revenue += tier_revenue
    
    variable_cost_per_attendee = 25
    total_variable_costs = attendees * variable_cost_per_attendee
    
    total_costs = fixed_costs + total_variable_costs
    net_profit = total_revenue - total_costs
    
    return {
        "costs": {"fixed": fixed_costs, "variable": total_variable_costs, "total": total_costs},
        "revenue": {"by_tier": revenue_by_tier, "total": total_revenue},
        "net_profit": net_profit
    }

# Report Generation Functions
def format_currency(amount):
    """Format a number as a currency string."""
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be a number")
    
    return f"${amount:,.2f}"

def format_percentage(value):
    """Format a number as a percentage string."""
    if not isinstance(value, (int, float)):
        raise TypeError("Value must be a number")
    
    return f"{value:.2f}%"

def attendee_check_in_generator(event_data):
    """Generator function that yields check-in statistics. Uses yield."""
    if not isinstance(event_data, dict):
        raise TypeError("Event data must be a dictionary")
    
    # Handle missing attendees key
    if "attendees" not in event_data:
        yield ("No attendees registered", 0, 0)
        return
    
    total_attendees = len(event_data["attendees"])
    if total_attendees == 0:
        yield ("No attendees registered", 0, 0)
        return
        
    for hour in range(8, 17):  # 8 AM to 4 PM
        # Simulate check-in data - in a real system this would come from a database
        checked_in_this_hour = event_data.get(f"hour_{hour}", 0)
        total_checked_in = sum(event_data.get(f"hour_{h}", 0) for h in range(8, hour+1))
        percentage = (total_checked_in / total_attendees) * 100
        
        yield (f"{hour}:00", checked_in_this_hour, percentage)

def main():
    """Main function demonstrating event management system."""
    print("===== EVENT MANAGEMENT SYSTEM =====")
    
    # Get sample data
    events = get_sample_events()
    attendees = get_sample_attendees()
    resources = get_sample_resources()
    venues = get_sample_venues()
    
    # Demonstrate event management
    event = events[0]
    venue = venues[event["venue"]]
    
    print(f"\n----- EVENT DETAILS: {event['name']} -----")
    capacity = calculate_event_capacity(venue, "theater")
    print(f"Maximum capacity (theater setup): {capacity}")
    
    # Demonstrate registration
    attendee = attendees[0]
    registration = register_attendee(event, attendee, ticket_type="VIP")
    print(f"Registration status: {registration['message']}")
    
    # Demonstrate pricing calculator
    pricing_calculator = create_pricing_calculator(100)  # $100 base fee
    vip_price = pricing_calculator("VIP", 1)
    group_price = pricing_calculator("standard", 15)
    print(f"VIP ticket: {format_currency(vip_price)}")
    print(f"Group of 15 standard tickets: {format_currency(group_price)}")
    
    # Demonstrate resource allocation
    required_resources = allocate_resources(venue, 300, "conference")
    resource_costs = calculate_resource_costs(resources, rental_period=2)
    print(f"Total resource cost: {format_currency(resource_costs['total_cost'])}")
    
    # Demonstrate budget analysis
    planned_budget = {"venue": 5000, "catering": 3000, "marketing": 2000}
    actual_expenses = {"venue": 5500, "catering": 2800, "marketing": 1800}
    
    variance = analyze_budget_variance(planned_budget, actual_expenses)
    print(f"Budget variance: {format_currency(variance['total_variance'])}")
    
    # Demonstrate profitability calculation
    revenue = {"tickets": 15000, "sponsorships": 5000, "merchandise": 1000}
    expenses = {"venue": 5500, "catering": 2800, "marketing": 1800, "staff": 2000}
    
    profit_data = calculate_event_profitability(revenue, expenses)
    print(f"Net profit: {format_currency(profit_data[2])}")
    print(f"Profit margin: {format_percentage(profit_data[3])}")
    
    # Demonstrate generator function
    print("\n----- CHECK-IN STATISTICS -----")
    check_in_data = {
        "attendees": attendees,
        "hour_8": 5,
        "hour_9": 15,
        "hour_10": 20,
        "hour_11": 10
    }
    
    for time, count, percentage in attendee_check_in_generator(check_in_data):
        print(f"{time}: {count} attendees checked in ({format_percentage(percentage)})")

if __name__ == "__main__":
    main()