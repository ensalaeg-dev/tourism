# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Region(Document):
	def validate(self):
		if self.city and self.country:
			# Auto-generate region name if not provided
			if not self.region_name:
				self.region_name = f"{self.city}, {self.country}"

