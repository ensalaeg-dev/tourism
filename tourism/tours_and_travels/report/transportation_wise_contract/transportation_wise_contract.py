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
			"fieldname": "transportation",
			"label": _("Transportation"),
			"fieldtype": "Link",
			"options": "Transportation",
			"width": 150
		},
		{
			"fieldname": "vehicle",
			"label": _("Vehicle"),
			"fieldtype": "Link",
			"options": "Vehicle",
			"width": 100
		},
		{
			"fieldname": "rate_per_day",
			"label": _("Rate Per Day"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "rate_per_km",
			"label": _("Rate Per KM"),
			"fieldtype": "Currency",
			"width": 100
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
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			tc.name as contract,
			tc.contract_name,
			cti.transportation,
			cti.vehicle,
			cti.rate_per_day,
			cti.rate_per_km,
			cti.season,
			cti.valid_from,
			cti.valid_to,
			tc.status
		FROM `tabTourism Contract` tc
		INNER JOIN `tabContract Transportation Item` cti ON cti.parent = tc.name
		WHERE tc.contract_type IN ('Transportation', 'Combined')
		{conditions}
		ORDER BY tc.creation DESC
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("transportation"):
		conditions += " AND cti.transportation = %(transportation)s"
	
	if filters.get("status"):
		conditions += " AND tc.status = %(status)s"
	
	if filters.get("from_date"):
		conditions += " AND tc.start_date >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND tc.end_date <= %(to_date)s"
	
	return conditions

