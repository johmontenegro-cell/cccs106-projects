import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, search_text = None):
    """Fetches and displays all contacts in the ListView."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_text)

    for contact in contacts:
        contact_id, name, phone, email = contact

        """ Task 5: Refine the UI """
        contacts_list_view.controls.append(
            ft.Card(
                content = ft.Container(
                    content = ft.Column(
                        [
                            ft.Text(name, size = 18, weight = ft.FontWeight.BOLD),
                            ft.Row(
                                [ft.Icon(ft.Icons.PHONE), ft.Text(phone if phone else "-")],
                                spacing = 5,
                            ),
                            ft.Row(
                                [ft.Icon(ft.Icons.EMAIL), ft.Text(email if email else "-")],
                                spacing = 5,
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon = ft.Icons.EDIT,
                                        tooltip = "Edit",
                                        on_click = lambda _, c = contact: open_edit_dialog(
                                            page, c, db_conn, contacts_list_view
                                        ),
                                    ),
                                    ft.IconButton(
                                        icon = ft.Icons.DELETE,
                                        tooltip = "Delete",
                                        on_click = lambda _, cid = contact_id: confirm_delete_contact(
                                            page, cid, db_conn, contacts_list_view
                                        ),
                                    ),
                                ],
                                alignment = ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing = 5,
                    ),
                    padding = 10,
                ),
                elevation = 3,
                margin = 5,
            )
        ) 
    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact and refreshes the list."""
    name_input, phone_input, email_input = inputs

    """ Task 1: Input Validation """
    if not name_input.value.strip():
        name_input.error_text = "Name cannot not be empty"
        page.update()
        return
    else:
        name_input.error_text = None

    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)

    for field in inputs:
        field.value = ""

    display_contacts(page, contacts_list_view, db_conn)
    page.update()   

def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    display_contacts(page, contacts_list_view, db_conn)

def confirm_delete_contact(page, contact_id, db_conn, contacts_list_view):
    """ Task 2: Confirmation on Delete """
    def yes(e):
        dialog.open = False
        delete_contact_db(db_conn, contact_id)
        display_contacts(page, contacts_list_view, db_conn)
        page.update()

    def no(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("No", on_click = no),
            ft.TextButton("Yes", on_click = yes),
        ],
    )

    page.open(dialog)

def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact
    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value,
        edit_email.value)
        dialog.open = False # type: ignore
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email]),
        actions=[
        ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)
        or page.update()),
        ft.TextButton("Save", on_click=save_and_close),
        ],
        )
    page.open(dialog)