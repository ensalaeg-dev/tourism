import frappe


def get_notification_config():
	return {
		"for_doctype": {
			"Tour Registration": {"status": ("in", ("Draft", "Pending"))},
			"Tour Package": {"status": "Active"},
			"Hotel Folio": {"status": ("in", ("Draft", "Checked In"))},
			"Tourism Contract": {"status": "Active"},
		},
	}

