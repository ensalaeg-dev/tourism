# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class TravellingSeason(Document):
	def validate(self):
		if self.start_date and self.end_date:
			if self.start_date > self.end_date:
				frappe.throw(_("End Date cannot be before Start Date"))
		
		if self.price_multiplier and self.price_multiplier <= 0:
			frappe.throw(_("Price Multiplier must be greater than 0"))

