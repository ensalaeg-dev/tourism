# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "transportation_name",
			"label": _("Transportation Name"),
			"fieldtype": "Link",
			"options": "Transportation",
			"width": 200
		},
		{
			"fieldname": "transportation_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "region",
			"label": _("Region"),
			"fieldtype": "Link",
			"options": "Region",
			"width": 120
		},
		{
			"fieldname": "base_location",
			"label": _("Base Location"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "price_per_day",
			"label": _("Price Per Day"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "price_per_km",
			"label": _("Price Per KM"),
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"fieldname": "phone",
			"label": _("Phone"),
			"fieldtype": "Data",
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
			transportation_name,
			transportation_type,
			region,
			base_location,
			price_per_day,
			price_per_km,
			phone,
			status
		FROM `tabTransportation`
		WHERE enabled = 1
		{conditions}
		ORDER BY transportation_name
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("region"):
		conditions += " AND region = %(region)s"
	
	if filters.get("transportation_type"):
		conditions += " AND transportation_type = %(transportation_type)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	return conditions

