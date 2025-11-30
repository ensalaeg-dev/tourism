# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{
			"fieldname": "hotel",
			"label": _("Hotel"),
			"fieldtype": "Link",
			"options": "Hotel",
			"width": 180
		},
		{
			"fieldname": "room_number",
			"label": _("Room Number"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "room_type",
			"label": _("Room Type"),
			"fieldtype": "Link",
			"options": "Room Type",
			"width": 120
		},
		{
			"fieldname": "floor",
			"label": _("Floor"),
			"fieldtype": "Data",
			"width": 60
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "current_guest",
			"label": _("Current Guest"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "check_in_date",
			"label": _("Check In"),
			"fieldtype": "Datetime",
			"width": 140
		},
		{
			"fieldname": "expected_checkout",
			"label": _("Expected Checkout"),
			"fieldtype": "Datetime",
			"width": 140
		},
		{
			"fieldname": "price_per_night",
			"label": _("Price/Night"),
			"fieldtype": "Currency",
			"width": 100
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			hotel,
			room_number,
			room_type,
			floor,
			status,
			current_guest,
			check_in_date,
			expected_checkout,
			price_per_night
		FROM `tabHotel Room Master`
		WHERE 1=1
		{conditions}
		ORDER BY hotel, room_number
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("hotel"):
		conditions += " AND hotel = %(hotel)s"
	
	if filters.get("room_type"):
		conditions += " AND room_type = %(room_type)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	if filters.get("floor"):
		conditions += " AND floor = %(floor)s"
	
	return conditions


def get_chart(data):
	status_counts = {}
	for row in data:
		status = row.get("status", "Unknown")
		status_counts[status] = status_counts.get(status, 0) + 1
	
	return {
		"data": {
			"labels": list(status_counts.keys()),
			"datasets": [
				{
					"name": _("Rooms"),
					"values": list(status_counts.values())
				}
			]
		},
		"type": "pie",
		"colors": ["#28a745", "#dc3545", "#ffc107", "#17a2b8", "#6c757d", "#fd7e14"]
	}


def get_summary(data):
	total = len(data)
	available = len([d for d in data if d.get("status") == "Available"])
	occupied = len([d for d in data if d.get("status") == "Occupied"])
	
	return [
		{
			"value": total,
			"indicator": "Blue",
			"label": _("Total Rooms"),
			"datatype": "Int"
		},
		{
			"value": available,
			"indicator": "Green",
			"label": _("Available"),
			"datatype": "Int"
		},
		{
			"value": occupied,
			"indicator": "Red",
			"label": _("Occupied"),
			"datatype": "Int"
		}
	]

