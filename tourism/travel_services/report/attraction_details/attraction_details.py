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
			"fieldname": "attraction_name",
			"label": _("Attraction Name"),
			"fieldtype": "Link",
			"options": "Attraction",
			"width": 200
		},
		{
			"fieldname": "attraction_type",
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
			"fieldname": "city",
			"label": _("City"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "entry_fee",
			"label": _("Entry Fee"),
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"fieldname": "duration_hours",
			"label": _("Duration (Hours)"),
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "opening_time",
			"label": _("Opening Time"),
			"fieldtype": "Time",
			"width": 100
		},
		{
			"fieldname": "closing_time",
			"label": _("Closing Time"),
			"fieldtype": "Time",
			"width": 100
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			attraction_name,
			attraction_type,
			region,
			city,
			entry_fee,
			duration_hours,
			opening_time,
			closing_time
		FROM `tabAttraction`
		WHERE enabled = 1
		{conditions}
		ORDER BY attraction_name
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("region"):
		conditions += " AND region = %(region)s"
	
	if filters.get("attraction_type"):
		conditions += " AND attraction_type = %(attraction_type)s"
	
	return conditions

