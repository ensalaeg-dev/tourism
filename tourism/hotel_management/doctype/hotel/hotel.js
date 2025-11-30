// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add Room button
			frm.add_custom_button(__('Add Room'), function() {
				frappe.new_doc('Hotel Room Master', {
					hotel: frm.doc.name
				});
			}, __('Actions'));
			
			// View Rooms button
			frm.add_custom_button(__('View Rooms'), function() {
				frappe.set_route('List', 'Hotel Room Master', {
					hotel: frm.doc.name
				});
			}, __('View'));
			
			// View Folios button
			frm.add_custom_button(__('View Folios'), function() {
				frappe.set_route('List', 'Hotel Folio', {
					hotel: frm.doc.name
				});
			}, __('View'));
			
			// View Reservations button
			frm.add_custom_button(__('View Reservations'), function() {
				frappe.set_route('List', 'Hotel Reservation', {
					hotel: frm.doc.name
				});
			}, __('View'));
			
			// New Folio button
			frm.add_custom_button(__('New Folio'), function() {
				frappe.new_doc('Hotel Folio', {
					hotel: frm.doc.name
				});
			}, __('Create'));
			
			// New Reservation button
			frm.add_custom_button(__('New Reservation'), function() {
				frappe.new_doc('Hotel Reservation', {
					hotel: frm.doc.name
				});
			}, __('Create'));
			
			// Room Availability Report
			frm.add_custom_button(__('Room Availability'), function() {
				frappe.set_route('query-report', 'Room Availability', {
					hotel: frm.doc.name
				});
			}, __('Reports'));
			
			// Show room summary in dashboard
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel Room Master',
					filters: {
						hotel: frm.doc.name
					}
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Total Rooms: {0}', [r.message]), 'blue');
					}
				}
			});
			
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel Room Master',
					filters: {
						hotel: frm.doc.name,
						status: 'Available'
					}
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Available: {0}', [r.message]), 'green');
					}
				}
			});
			
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel Room Master',
					filters: {
						hotel: frm.doc.name,
						status: 'Occupied'
					}
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Occupied: {0}', [r.message]), 'red');
					}
				}
			});
		}
	},
	
	region: function(frm) {
		if (frm.doc.region) {
			frappe.db.get_doc('Region', frm.doc.region).then(function(r) {
				if (r) {
					if (!frm.doc.city) frm.set_value('city', r.city);
					if (!frm.doc.state) frm.set_value('state', r.state);
					if (!frm.doc.country) frm.set_value('country', r.country);
				}
			});
		}
	}
});

// Child table events for Hotel Room
frappe.ui.form.on('Hotel Room', {
	room_type: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.room_type) {
			frappe.db.get_doc('Room Type', row.room_type).then(function(r) {
				if (r) {
					frappe.model.set_value(cdt, cdn, 'price_per_night', r.base_price);
				}
			});
		}
	}
});

