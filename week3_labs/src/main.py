import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    page.window.alignment = ft.alignment.center
    page.window.frameless = True
    page.window.title = "User Login" # type: ignore
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT
    page.theme_mode = ft.ThemeMode.LIGHT
    
    login = ft.Text("User Login", 
                    size = 20, 
                    weight = ft.FontWeight.BOLD, 
                    font_family = "Arial", 
                    text_align = ft.TextAlign.CENTER)

    username = ft.TextField(
            label = "Username", 
            hint_text = "Enter your user name", 
            helper_text = "This is your unique identifier", 
            width = 300,
            autofocus = True,
            prefix_icon = ft.Icons.PERSON,
            bgcolor = ft.Colors.LIGHT_BLUE_ACCENT
        )

    password = ft.TextField(
            label = "Password",
            hint_text = "Enter your password",
            helper_text = "This is your secret key",
            width = 300,
            password = True,
            can_reveal_password = True,
            prefix_icon = ft.Icons.PASSWORD,
            bgcolor = ft.Colors.LIGHT_BLUE_ACCENT
        )

    async def login_click(e):

        success_dialog = ft.AlertDialog(
                modal = True,
                title = ft.Text("Login Successful"),
                content = ft.Text(f"Welcome {username.value}!"),
                actions = [
                    ft.TextButton(
                        "OK", 
                        on_click = lambda e: page.close(success_dialog))],
                icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color = ft.Colors.GREEN)
            )

        failure_dialog = ft.AlertDialog(
                modal = True,
                title = ft.Text("Login Failed"),
                content = ft.Text("Invalid username or password"),
                actions = [
                    ft.TextButton(
                        "OK", 
                        on_click = lambda e: page.close(failure_dialog))],
                icon = ft.Icon(ft.Icons.ERROR_ROUNDED, color = ft.Colors.RED)
            )

        invalid_input_dialog = ft.AlertDialog(
                modal = True,
                title = ft.Text("Input Error"),
                content = ft.Text("Please enter username and password"),
                actions = [
                    ft.TextButton(
                        "OK", 
                        on_click = lambda e: page.close(invalid_input_dialog))],
                icon = ft.Icon(ft.Icons.INFO_ROUNDED, color = ft.Colors.BLUE)
            )

        database_error_dialog = ft.AlertDialog(
                modal = True,
                title = ft.Text("Database Error"),
                content = ft.Text("An error occurred while connecting to the database"),
                alignment = ft.alignment.center,
                actions = [
                    ft.TextButton(
                        "OK", 
                        on_click = lambda e: page.close(database_error_dialog))]
            )
            

        if not username.value or not password.value:
            page.open(invalid_input_dialog)
            page.update()
            return
        
        try:
            db = connect_db()
            if not db:
                page.open(database_error_dialog)
                page.update()
                return

            cursor = db.cursor(dictionary = True)

            query = "SELECT * FROM users WHERE username = %s AND password = %s"

            cursor.execute(query, (username.value, password.value))

            result = cursor.fetchone()

            cursor.close()
            db.close()

            if result:
                page.open(success_dialog)
            else:
                page.open(failure_dialog)

        except mysql.connector.Error as e:
            page.open(database_error_dialog)
        
        page.update()

    login_button = ft.ElevatedButton(
            text = "Login",
            width = 100,
            icon = ft.Icons.LOGIN,
            bgcolor = ft.Colors.WHITE,
            color = ft.Colors.BLUE_500,
            on_click = login_click,
        )

    page.add(
    ft.Container(
        ft.Column(
            [login, username, password, 
             ft.Container(content = login_button, 
                          alignment = ft.alignment.top_right, 
                          margin = ft.margin.Margin(0, 20, 40, 0))],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )
)



ft.app(target = main)
