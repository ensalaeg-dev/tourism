# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, date_diff, get_datetime


class HotelFolio(Document):
	def validate(self):
		self.calculate_nights()
		self.calculate_totals()
	
	def calculate_nights(self):
		if self.check_in_date and self.check_out_date:
			check_in = get_datetime(self.check_in_date).date()
			check_out = get_datetime(self.check_out_date).date()
			self.nights = date_diff(check_out, check_in)
			if self.nights < 1:
				self.nights = 1
	
	def calculate_totals(self):
		# Calculate room charges
		self.room_charges = flt(self.nights or 1) * flt(self.rate_per_night)
		self.total_room_charges = self.room_charges
		
		# Calculate service charges
		self.total_services = 0
		for service in self.services:
			service.amount = flt(service.qty) * flt(service.rate)
			self.total_services += flt(service.amount)
		
		# Calculate totals
		self.total_amount = flt(self.total_room_charges) + flt(self.total_services)
		self.balance_amount = flt(self.total_amount) - flt(self.paid_amount)


@frappe.whitelist()
def create_sales_invoice(folio_name):
	"""Create Sales Invoice from Hotel Folio"""
	folio = frappe.get_doc("Hotel Folio", folio_name)
	
	if folio.sales_invoice:
		frappe.throw(_("Sales Invoice already exists for this folio"))
	
	if not folio.customer:
		frappe.throw(_("Please set Customer before creating invoice"))
	
	# Check if Sales Invoice doctype exists
	if not frappe.db.exists("DocType", "Sales Invoice"):
		frappe.throw(_("Sales Invoice DocType not found"))
	
	# Get default income account
	company = frappe.defaults.get_user_default("Company")
	if not company:
		frappe.throw(_("Please set default company"))
	
	invoice = frappe.new_doc("Sales Invoice")
	invoice.customer = folio.customer
	invoice.posting_date = frappe.utils.nowdate()
	invoice.due_date = frappe.utils.nowdate()
	invoice.company = company
	
	# Add room charges as item
	if folio.total_room_charges > 0:
		invoice.append("items", {
			"item_name": f"Room Charges - {folio.hotel} ({folio.room_type or 'Standard'})",
			"description": f"Room charges for {folio.nights} night(s)",
			"qty": folio.nights or 1,
			"rate": folio.rate_per_night,
			"amount": folio.total_room_charges
		})
	
	# Add service charges
	for service in folio.services:
		if service.amount > 0:
			invoice.append("items", {
				"item_name": f"{service.service_type} - {service.description or ''}",
				"description": service.description,
				"qty": service.qty,
				"rate": service.rate,
				"amount": service.amount
			})
	
	invoice.insert(ignore_permissions=True)
	
	folio.db_set("sales_invoice", invoice.name)
	
	return invoice.name


@frappe.whitelist()
def check_in(folio_name):
	"""Check in guest"""
	folio = frappe.get_doc("Hotel Folio", folio_name)
	folio.status = "Checked In"
	if not folio.check_in_date:
		folio.check_in_date = frappe.utils.now()
	folio.save()
	
	# Update room status if room_master is set
	if folio.room_master:
		frappe.db.set_value("Hotel Room Master", folio.room_master, {
			"status": "Occupied",
			"current_folio": folio.name,
			"current_guest": folio.guest_name,
			"check_in_date": folio.check_in_date,
			"expected_checkout": folio.check_out_date
		})
	
	return folio


@frappe.whitelist()
def check_out(folio_name):
	"""Check out guest"""
	folio = frappe.get_doc("Hotel Folio", folio_name)
	folio.status = "Checked Out"
	if not folio.check_out_date:
		folio.check_out_date = frappe.utils.now()
	folio.save()
	
	# Update room status if room_master is set
	if folio.room_master:
		frappe.db.set_value("Hotel Room Master", folio.room_master, {
			"status": "Cleaning",
			"current_folio": None,
			"current_guest": None,
			"check_in_date": None,
			"expected_checkout": None
		})
	
	return folio

