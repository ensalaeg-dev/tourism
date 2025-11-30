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
			"fieldname": "restaurant_name",
			"label": _("Restaurant Name"),
			"fieldtype": "Link",
			"options": "Restaurant",
			"width": 200
		},
		{
			"fieldname": "cuisine_type",
			"label": _("Cuisine Type"),
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
			"fieldname": "city",
			"label": _("City"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "seating_capacity",
			"label": _("Seating Capacity"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "phone",
			"label": _("Phone"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "email",
			"label": _("Email"),
			"fieldtype": "Data",
			"width": 150
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
			restaurant_name,
			cuisine_type,
			region,
			city,
			seating_capacity,
			phone,
			email,
			status
		FROM `tabRestaurant`
		WHERE enabled = 1
		{conditions}
		ORDER BY restaurant_name
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("region"):
		conditions += " AND region = %(region)s"
	
	if filters.get("cuisine_type"):
		conditions += " AND cuisine_type = %(cuisine_type)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	return conditions

