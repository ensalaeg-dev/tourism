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
			"fieldname": "guide_name",
			"label": _("Guide Name"),
			"fieldtype": "Link",
			"options": "Guide",
			"width": 200
		},
		{
			"fieldname": "region",
			"label": _("Region"),
			"fieldtype": "Link",
			"options": "Region",
			"width": 120
		},
		{
			"fieldname": "languages",
			"label": _("Languages"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "experience_years",
			"label": _("Experience (Years)"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "specialization",
			"label": _("Specialization"),
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
			guide_name,
			region,
			languages,
			experience_years,
			specialization,
			price_per_day,
			phone,
			status
		FROM `tabGuide`
		WHERE enabled = 1
		{conditions}
		ORDER BY guide_name
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("region"):
		conditions += " AND region = %(region)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	return conditions

