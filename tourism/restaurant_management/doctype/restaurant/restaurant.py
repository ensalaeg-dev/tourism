# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Restaurant(Document):
	def validate(self):
		self.update_region_info()
	
	def update_region_info(self):
		"""Update city, state, country from region if selected"""
		if self.region:
			region = frappe.get_doc("Region", self.region)
			if not self.city:
				self.city = region.city
			if not self.state:
				self.state = region.state
			if not self.country:
				self.country = region.country

