// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel Room Master', {
	refresh: function(frm) {
		// Mark Available button (for cleaning/maintenance rooms)
		if (frm.doc.status === 'Cleaning' || frm.doc.status === 'Maintenance') {
			frm.add_custom_button(__('Mark Available'), function() {
				frappe.call({
					method: 'tourism.hotel_management.doctype.hotel_room_master.hotel_room_master.mark_available',
					args: {
						room_name: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.msgprint(__('Room marked as available'));
						}
					}
				});
			}, __('Actions'));
		}
		
		// Mark for Cleaning button (for occupied rooms)
		if (frm.doc.status === 'Occupied') {
			frm.add_custom_button(__('Mark for Cleaning'), function() {
				frappe.call({
					method: 'tourism.hotel_management.doctype.hotel_room_master.hotel_room_master.mark_for_cleaning',
					args: {
						room_name: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.msgprint(__('Room marked for cleaning'));
						}
					}
				});
			}, __('Actions'));
		}
		
		// View Current Folio button
		if (frm.doc.current_folio) {
			frm.add_custom_button(__('View Current Folio'), function() {
				frappe.set_route('Form', 'Hotel Folio', frm.doc.current_folio);
			}, __('Actions'));
		}
		
		// Create New Folio button (for available rooms)
		if (frm.doc.status === 'Available') {
			frm.add_custom_button(__('Create Folio'), function() {
				frappe.new_doc('Hotel Folio', {
					hotel: frm.doc.hotel,
					room_type: frm.doc.room_type,
					room_number: frm.doc.room_number,
					rate_per_night: frm.doc.price_per_night,
					room_master: frm.doc.name
				});
			}, __('Actions'));
		}
		
		// Set status indicator
		if (frm.doc.status === 'Available') {
			frm.dashboard.set_headline_alert('<span class="indicator-pill green">' + __('Room is Available') + '</span>');
		} else if (frm.doc.status === 'Occupied') {
			frm.dashboard.set_headline_alert('<span class="indicator-pill red">' + __('Room is Occupied') + '</span>');
		} else if (frm.doc.status === 'Cleaning') {
			frm.dashboard.set_headline_alert('<span class="indicator-pill yellow">' + __('Room needs cleaning') + '</span>');
		} else if (frm.doc.status === 'Maintenance') {
			frm.dashboard.set_headline_alert('<span class="indicator-pill orange">' + __('Room under maintenance') + '</span>');
		}
	},
	
	room_type: function(frm) {
		if (frm.doc.room_type) {
			frappe.db.get_doc('Room Type', frm.doc.room_type).then(function(r) {
				if (r) {
					frm.set_value('price_per_night', r.base_price);
					frm.set_value('max_occupancy', r.max_occupancy);
					frm.set_value('extra_bed_available', r.extra_bed_available);
					frm.set_value('extra_bed_price', r.extra_bed_price);
				}
			});
		}
	}
});

