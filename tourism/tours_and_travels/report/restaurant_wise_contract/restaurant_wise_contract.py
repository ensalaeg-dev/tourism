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
			"fieldname": "contract",
			"label": _("Contract"),
			"fieldtype": "Link",
			"options": "Tourism Contract",
			"width": 150
		},
		{
			"fieldname": "contract_name",
			"label": _("Contract Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "restaurant",
			"label": _("Restaurant"),
			"fieldtype": "Link",
			"options": "Restaurant",
			"width": 150
		},
		{
			"fieldname": "meal_type",
			"label": _("Meal Type"),
			"fieldtype": "Link",
			"options": "Meal Type",
			"width": 100
		},
		{
			"fieldname": "rate_per_person",
			"label": _("Rate Per Person"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "season",
			"label": _("Season"),
			"fieldtype": "Link",
			"options": "Travelling Season",
			"width": 100
		},
		{
			"fieldname": "valid_from",
			"label": _("Valid From"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "valid_to",
			"label": _("Valid To"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "region",
			"label": _("Region"),
			"fieldtype": "Link",
			"options": "Region",
			"width": 100
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			tc.name as contract,
			tc.contract_name,
			cri.restaurant,
			cri.meal_type,
			cri.rate_per_person,
			cri.season,
			cri.valid_from,
			cri.valid_to,
			tc.status,
			tc.region
		FROM `tabTourism Contract` tc
		INNER JOIN `tabContract Restaurant Item` cri ON cri.parent = tc.name
		WHERE tc.contract_type IN ('Restaurant', 'Combined')
		{conditions}
		ORDER BY tc.creation DESC
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("restaurant"):
		conditions += " AND cri.restaurant = %(restaurant)s"
	
	if filters.get("region"):
		conditions += " AND tc.region = %(region)s"
	
	if filters.get("status"):
		conditions += " AND tc.status = %(status)s"
	
	if filters.get("from_date"):
		conditions += " AND tc.start_date >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND tc.end_date <= %(to_date)s"
	
	return conditions

