// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Type', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// View Rooms button
			frm.add_custom_button(__('View Rooms'), function() {
				frappe.set_route('List', 'Hotel Room Master', {
					room_type: frm.doc.name
				});
			}, __('View'));
			
			// View Folios button
			frm.add_custom_button(__('View Folios'), function() {
				frappe.set_route('List', 'Hotel Folio', {
					room_type: frm.doc.name
				});
			}, __('View'));
			
			// View Reservations button
			frm.add_custom_button(__('View Reservations'), function() {
				frappe.set_route('List', 'Hotel Reservation', {
					room_type: frm.doc.name
				});
			}, __('View'));
			
			// Show room count
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel Room Master',
					filters: {
						room_type: frm.doc.name
					}
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Total Rooms: {0}', [r.message]), 'blue');
					}
				}
			});
		}
	}
});

