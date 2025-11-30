# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	return columns, data, None, chart


def get_columns():
	return [
		{
			"fieldname": "name",
			"label": _("Registration"),
			"fieldtype": "Link",
			"options": "Tour Registration",
			"width": 150
		},
		{
			"fieldname": "registration_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "tour_package",
			"label": _("Tour Package"),
			"fieldtype": "Link",
			"options": "Tour Package",
			"width": 150
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"fieldname": "arrival_date",
			"label": _("Arrival Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "departure_date",
			"label": _("Departure Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "total_pax",
			"label": _("Total Pax"),
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "region",
			"label": _("Region"),
			"fieldtype": "Link",
			"options": "Region",
			"width": 100
		},
		{
			"fieldname": "grand_total",
			"label": _("Grand Total"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			name,
			registration_type,
			tour_package,
			customer,
			arrival_date,
			departure_date,
			total_pax,
			region,
			grand_total,
			status
		FROM `tabTour Registration`
		WHERE docstatus < 2
		{conditions}
		ORDER BY creation DESC
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("registration_type"):
		conditions += " AND registration_type = %(registration_type)s"
	
	if filters.get("tour_package"):
		conditions += " AND tour_package = %(tour_package)s"
	
	if filters.get("customer"):
		conditions += " AND customer = %(customer)s"
	
	if filters.get("region"):
		conditions += " AND region = %(region)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	if filters.get("from_date"):
		conditions += " AND arrival_date >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND departure_date <= %(to_date)s"
	
	return conditions


def get_chart(data):
	if not data:
		return None
	
	# Group by status
	status_count = {}
	for row in data:
		status = row.get("status") or "Unknown"
		status_count[status] = status_count.get(status, 0) + 1
	
	return {
		"data": {
			"labels": list(status_count.keys()),
			"datasets": [
				{
					"name": _("Registrations"),
					"values": list(status_count.values())
				}
			]
		},
		"type": "pie"
	}

