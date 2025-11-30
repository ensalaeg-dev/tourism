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
			"fieldname": "hotel_name",
			"label": _("Hotel Name"),
			"fieldtype": "Link",
			"options": "Hotel",
			"width": 200
		},
		{
			"fieldname": "star_rating",
			"label": _("Star Rating"),
			"fieldtype": "Data",
			"width": 100
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
			"fieldname": "country",
			"label": _("Country"),
			"fieldtype": "Link",
			"options": "Country",
			"width": 100
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
			"fieldname": "total_rooms",
			"label": _("Total Rooms"),
			"fieldtype": "Int",
			"width": 100
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
			h.hotel_name,
			h.star_rating,
			h.region,
			h.city,
			h.country,
			h.phone,
			h.email,
			(SELECT COUNT(*) FROM `tabHotel Room` hr WHERE hr.parent = h.name) as total_rooms,
			h.status
		FROM `tabHotel` h
		WHERE h.enabled = 1
		{conditions}
		ORDER BY h.hotel_name
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("region"):
		conditions += " AND h.region = %(region)s"
	
	if filters.get("star_rating"):
		conditions += " AND h.star_rating = %(star_rating)s"
	
	if filters.get("status"):
		conditions += " AND h.status = %(status)s"
	
	if filters.get("city"):
		conditions += " AND h.city = %(city)s"
	
	return conditions

