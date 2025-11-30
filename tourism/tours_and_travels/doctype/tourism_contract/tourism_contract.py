# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class TourismContract(Document):
	def validate(self):
		self.validate_dates()
		self.validate_contract_items()
	
	def validate_dates(self):
		if self.start_date and self.end_date:
			if getdate(self.start_date) > getdate(self.end_date):
				frappe.throw(_("End Date cannot be before Start Date"))
	
	def validate_contract_items(self):
		"""Validate that at least one item is added based on contract type"""
		if self.contract_type == "Hotel" and not self.hotel_items:
			frappe.throw(_("Please add at least one Hotel item for Hotel contract"))
		elif self.contract_type == "Restaurant" and not self.restaurant_items:
			frappe.throw(_("Please add at least one Restaurant item for Restaurant contract"))
		elif self.contract_type == "Transportation" and not self.transportation_items:
			frappe.throw(_("Please add at least one Transportation item for Transportation contract"))
	
	def on_submit(self):
		self.status = "Active"
	
	def on_cancel(self):
		self.status = "Cancelled"
	
	def before_save(self):
		self.update_status_based_on_dates()
	
	def update_status_based_on_dates(self):
		"""Auto-update status based on dates"""
		if self.docstatus == 1:  # Only for submitted docs
			today = getdate(nowdate())
			if self.end_date and getdate(self.end_date) < today:
				self.status = "Expired"
			elif self.start_date and getdate(self.start_date) <= today:
				self.status = "Active"

