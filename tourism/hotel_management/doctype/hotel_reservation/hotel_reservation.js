// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel Reservation', {
	refresh: function(frm) {
		// Set rate from room type
		if (frm.doc.room_type && !frm.doc.rate_per_night) {
			frappe.db.get_value('Room Type', frm.doc.room_type, 'base_price', function(r) {
				if (r && r.base_price) {
					frm.set_value('rate_per_night', r.base_price);
				}
			});
		}
		
		if (!frm.is_new()) {
			// Confirm Reservation button (for draft)
			if (frm.doc.docstatus === 0 && frm.doc.status === 'Draft') {
				frm.add_custom_button(__('Confirm Reservation'), function() {
					frappe.call({
						method: 'tourism.hotel_management.doctype.hotel_reservation.hotel_reservation.confirm_reservation',
						args: {
							reservation_name: frm.doc.name
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint(__('Reservation confirmed successfully'));
							}
						}
					});
				}, __('Actions'));
			}
			
			// Create Folio button (for confirmed reservations)
			if ((frm.doc.status === 'Confirmed' || frm.doc.status === 'Draft') && !frm.doc.hotel_folio) {
				frm.add_custom_button(__('Create Hotel Folio'), function() {
					frappe.call({
						method: 'tourism.hotel_management.doctype.hotel_reservation.hotel_reservation.create_hotel_folio',
						args: {
							reservation_name: frm.doc.name
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint(__('Hotel Folio {0} created', [r.message]));
								frappe.set_route('Form', 'Hotel Folio', r.message);
							}
						}
					});
				}, __('Actions'));
			}
			
			// View Folio button
			if (frm.doc.hotel_folio) {
				frm.add_custom_button(__('View Hotel Folio'), function() {
					frappe.set_route('Form', 'Hotel Folio', frm.doc.hotel_folio);
				}, __('Actions'));
			}
			
			// Mark No Show button (for confirmed reservations past check-in date)
			if (frm.doc.docstatus === 1 && frm.doc.status === 'Confirmed') {
				frm.add_custom_button(__('Mark No Show'), function() {
					frappe.confirm(
						__('Are you sure you want to mark this reservation as No Show?'),
						function() {
							frappe.call({
								method: 'tourism.hotel_management.doctype.hotel_reservation.hotel_reservation.mark_no_show',
								args: {
									reservation_name: frm.doc.name
								},
								callback: function(r) {
									if (r.message) {
										frm.reload_doc();
										frappe.msgprint(__('Reservation marked as No Show'));
									}
								}
							});
						}
					);
				}, __('Actions'));
			}
			
			// Cancel button (for draft)
			if (frm.doc.docstatus === 0 && frm.doc.status !== 'Cancelled') {
				frm.add_custom_button(__('Cancel Reservation'), function() {
					frappe.confirm(
						__('Are you sure you want to cancel this reservation?'),
						function() {
							frappe.call({
								method: 'tourism.hotel_management.doctype.hotel_reservation.hotel_reservation.cancel_reservation',
								args: {
									reservation_name: frm.doc.name
								},
								callback: function(r) {
									if (r.message) {
										frm.reload_doc();
										frappe.msgprint(__('Reservation cancelled'));
									}
								}
							});
						}
					);
				}, __('Actions'));
			}
		}
	},
	
	room_type: function(frm) {
		if (frm.doc.room_type) {
			frappe.db.get_value('Room Type', frm.doc.room_type, 'base_price', function(r) {
				if (r && r.base_price) {
					frm.set_value('rate_per_night', r.base_price);
				}
			});
		}
	},
	
	check_in_date: function(frm) {
		calculate_nights_and_total(frm);
	},
	
	check_out_date: function(frm) {
		calculate_nights_and_total(frm);
	},
	
	rate_per_night: function(frm) {
		calculate_nights_and_total(frm);
	},
	
	number_of_rooms: function(frm) {
		calculate_nights_and_total(frm);
	},
	
	advance_amount: function(frm) {
		frm.set_value('balance_amount', (frm.doc.total_room_rate || 0) - (frm.doc.advance_amount || 0));
	}
});

function calculate_nights_and_total(frm) {
	if (frm.doc.check_in_date && frm.doc.check_out_date) {
		var check_in = frappe.datetime.str_to_obj(frm.doc.check_in_date);
		var check_out = frappe.datetime.str_to_obj(frm.doc.check_out_date);
		var nights = frappe.datetime.get_diff(check_out, check_in);
		if (nights < 1) nights = 1;
		frm.set_value('nights', nights);
		
		var total = nights * (frm.doc.rate_per_night || 0) * (frm.doc.number_of_rooms || 1);
		frm.set_value('total_room_rate', total);
		frm.set_value('balance_amount', total - (frm.doc.advance_amount || 0));
	}
}

