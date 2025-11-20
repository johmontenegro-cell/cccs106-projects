# main.py
"""Weather Application using Flet v0.28.3"""

import flet as ft
from weather_service import WeatherService
from config import Config
import json
from pathlib import Path
import httpx
from datetime import datetime
import math

class WeatherApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        
        # State Setup
        self.units = "metric"
        self.current_weather_data = None
        self.forecast_data = None 
        self.chart_selection = "temp" # Track what chart we are showing
        
        # History Setup
        self.history_file = Path("mod6_labs/search_history.json")
        self.search_history = self.load_history()
        
        self.setup_page()
        self.build_ui()
        
        # Auto-fetch location on start
        self.page.run_task(self.get_current_location_weather)
    
    # --- History Methods ---
    def load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f: return json.load(f)
            except: return []
        return []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w') as f: json.dump(self.search_history, f)
        except: pass
    
    def add_to_history(self, city: str):
        city = city.title()
        if city in self.search_history: self.search_history.remove(city)
        self.search_history.insert(0, city)
        self.search_history = self.search_history[:10]
        self.save_history()
        self.update_history_ui()

    def update_history_ui(self):
        self.history_dropdown.options = [ft.dropdown.Option(city) for city in self.search_history]
        self.history_dropdown.visible = len(self.search_history) > 0
        self.page.update()

    def on_history_select(self, e):
        if self.history_dropdown.value:
            self.city_input.value = self.history_dropdown.value
            self.history_dropdown.value = None 
            self.page.run_task(self.get_weather)

    # --- Unit Logic ---
    async def toggle_units(self, e):
        selected = e.control.selected
        if not selected: return
        self.units = list(selected)[0]
        # Refresh display if data exists
        if self.current_weather_data and self.forecast_data:
            await self.display_data(self.current_weather_data, self.forecast_data)

    def convert_temp(self, temp_c):
        return (temp_c * 9/5) + 32 if self.units == "imperial" else temp_c

    def convert_speed(self, speed_ms):
        return speed_ms * 2.237 if self.units == "imperial" else speed_ms

    # --- Location & Theme Logic ---
    async def get_current_location_weather(self, e=None):
        self.loading.visible = True
        self.tabs.visible = False
        self.weather_container.opacity = 0
        self.page.update()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://ipapi.co/json/", timeout=5.0)
                data = response.json()
                city = data.get('city', '')
                
                if city:
                    self.city_input.value = city
                    self.page.update()
                    await self.get_weather(trigger_update=False)
                else:
                    if e is not None: self.show_error("Location not found")
                    
        except Exception:
            if e is not None: self.show_error("Could not detect location")
        finally:
            self.loading.visible = False
            self.page.update()

    def get_weather_theme(self, condition: str):
        condition = condition.lower()
        theme = { "bg": ft.Colors.ORANGE_100, "text": ft.Colors.ORANGE_900, "icon": ft.Colors.ORANGE, "sub": ft.Colors.ORANGE_800 }
        
        if "cloud" in condition:
            theme = { "bg": ft.Colors.BLUE_GREY_100, "text": ft.Colors.BLUE_GREY_900, "icon": ft.Colors.BLUE_GREY_700, "sub": ft.Colors.BLUE_GREY_800 }
        elif "rain" in condition or "drizzle" in condition:
            theme = { "bg": ft.Colors.BLUE_200, "text": ft.Colors.BLUE_900, "icon": ft.Colors.BLUE_700, "sub": ft.Colors.BLUE_800 }
        elif "thunder" in condition:
            theme = { "bg": ft.Colors.DEEP_PURPLE_100, "text": ft.Colors.DEEP_PURPLE_900, "icon": ft.Colors.DEEP_PURPLE_700, "sub": ft.Colors.DEEP_PURPLE_800 }
        elif "snow" in condition:
            theme = { "bg": ft.Colors.LIGHT_BLUE_50, "text": ft.Colors.GREY_900, "icon": ft.Colors.CYAN_300, "sub": ft.Colors.GREY_800 }
        elif any(x in condition for x in ["mist", "fog", "haze"]):
            theme = { "bg": ft.Colors.GREY_300, "text": ft.Colors.GREY_900, "icon": ft.Colors.GREY_600, "sub": ft.Colors.GREY_800 }
        return theme

    # --- Page Setup ---
    def setup_page(self):
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = 800 
        self.page.window.resizable = False
        self.page.window.center()

    def build_ui(self):
        # Header
        self.unit_switch = ft.SegmentedButton(
            selected={"metric"}, on_change=self.toggle_units,
            segments=[ft.Segment(value="metric", label=ft.Text("°C")), ft.Segment(value="imperial", label=ft.Text("°F"))],
            style=ft.ButtonStyle(padding=0, shape=ft.RoundedRectangleBorder(radius=8))
        )
        self.theme_button = ft.IconButton(icon=ft.Icons.DARK_MODE, on_click=self.toggle_theme)
        
        header = ft.Row([
            ft.Text("Weather App", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Row([self.unit_switch, self.theme_button], spacing=5)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Input Row
        self.city_input = ft.TextField(label="City", hint_text="London", expand=True, on_submit=self.on_search, border_radius=10)
        self.location_btn = ft.IconButton(icon=ft.Icons.MY_LOCATION, icon_color=ft.Colors.BLUE_700, on_click=lambda e: self.page.run_task(self.get_current_location_weather))
        input_row = ft.Row([self.city_input, self.location_btn])
        
        # History & Search
        self.history_dropdown = ft.Dropdown(label="Recent", visible=len(self.search_history) > 0, 
                                            options=[ft.dropdown.Option(city) for city in self.search_history], 
                                            on_change=self.on_history_select)
        self.search_button = ft.ElevatedButton("Get Weather", icon=ft.Icons.SEARCH, on_click=self.on_search, 
                                               style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700), width=Config.APP_WIDTH)

        # Main Content Area (Tabs)
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            visible=False,
            expand=True,
            tabs=[
                ft.Tab(text="Current", icon=ft.Icons.TODAY, content=ft.Container()),
                ft.Tab(text="Forecast", icon=ft.Icons.CALENDAR_MONTH, content=ft.Container()),
                ft.Tab(text="Trends", icon=ft.Icons.SHOW_CHART, content=ft.Container()),
            ],
        )

        self.loading = ft.ProgressRing(visible=False)
        self.error_message = ft.Text("", color=ft.Colors.RED_700, visible=False)

        # Container for all weather content
        self.weather_container = ft.Container(
            content=self.tabs,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=20,
            padding=10,
            animate=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
            opacity=0,
            visible=True,
            expand=True 
        )

        self.page.add(
            ft.Column([
                header,
                input_row,
                self.history_dropdown,
                self.search_button,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.loading,
                self.error_message,
                self.weather_container
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        )

    # --- Core Logic ---
    def on_search(self, e):
        self.page.run_task(self.get_weather)

    async def get_weather(self, trigger_update=True):
        city = self.city_input.value.strip()
        if not city:
            self.show_error("Please enter a city name")
            return
        
        if trigger_update:
            self.loading.visible = True
            self.error_message.visible = False
            self.tabs.visible = False
            self.weather_container.opacity = 0
            self.page.update()
        
        try:
            current_data = await self.weather_service.get_weather(city)
            forecast_data = await self.weather_service.get_forecast(city)
            
            self.current_weather_data = current_data
            self.forecast_data = forecast_data
            
            city_name_from_api = current_data.get("name", city)
            self.add_to_history(city_name_from_api)
            
            await self.display_data(current_data, forecast_data)
            
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.loading.visible = False
            self.page.update()

    async def display_data(self, current: dict, forecast: dict):
        weather_main = current.get("weather", [{}])[0].get("main", "")
        theme = self.get_weather_theme(weather_main)

        self.weather_container.bgcolor = theme["bg"]

        # 1. Current Weather (Now passes forecast data too for High/Low)
        current_view = self.build_current_view(current, forecast, theme)
        self.tabs.tabs[0].content = current_view

        # 2. Forecast
        forecast_view = self.build_forecast_view(forecast, theme)
        self.tabs.tabs[1].content = forecast_view

        # 3. Charts
        chart_view = self.build_chart_view(forecast, theme)
        self.tabs.tabs[2].content = chart_view
        
        self.tabs.visible = True
        self.weather_container.opacity = 1
        self.page.update()

    # --- Tab 1: Current Weather ---
    def build_current_view(self, data: dict, forecast: dict, theme: dict):
        # --- Existing Data Extraction ---
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        raw_temp = data.get("main", {}).get("temp", 0)
        raw_feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        wind_raw = data.get("wind", {}).get("speed", 0)
        desc = data.get("weather", [{}])[0].get("description", "").title()
        icon = data.get("weather", [{}])[0].get("icon", "01d")
        
        # --- New: Calculate Today's High/Low from Forecast ---
        # We look at the first 8 items (approx 24h) of forecast to find local min/max
        temps_today = [x['main']['temp'] for x in forecast['list'][:8]]
        high_temp = self.convert_temp(max(temps_today)) if temps_today else 0
        low_temp = self.convert_temp(min(temps_today)) if temps_today else 0

        temp = self.convert_temp(raw_temp)
        feels = self.convert_temp(raw_feels_like)
        wind = self.convert_speed(wind_raw)
        
        t_unit = "°F" if self.units == "imperial" else "°C"
        w_unit = "mph" if self.units == "imperial" else "m/s"

        return ft.Column([
            ft.Text(f"{city_name}, {country}", size=24, weight="bold", color=theme["text"]),
            
            # Main Weather Row
            ft.Row([
                ft.Image(src=f"https://openweathermap.org/img/wn/{icon}@4x.png", width=120, color=theme["text"]),
                ft.Column([
                    ft.Text(f"{temp:.0f}{t_unit}", size=60, weight="bold", color=theme["text"]),
                    ft.Text(desc, size=18, color=theme["sub"], weight="w500"),
                ], spacing=0),
            ], alignment=ft.MainAxisAlignment.CENTER),

            # High / Low Display
            ft.Row([
                ft.Text(f"H: {high_temp:.0f}°", weight="bold", color=theme["text"]),
                ft.Text(f"L: {low_temp:.0f}°", weight="bold", color=theme["sub"]),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),

            ft.Text(f"Feels like {feels:.0f}{t_unit}", color=theme["sub"], size=12),
            
            ft.Divider(color=theme["sub"], thickness=0.5),
            
            # Details Row
            ft.Row([
                self.create_info_card(ft.Icons.WATER_DROP, "Humidity", f"{humidity}%", theme),
                self.create_info_card(ft.Icons.AIR, "Wind", f"{wind:.1f} {w_unit}", theme)
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, spacing=10)

    # --- Tab 2: 5-Day Forecast (Feature 5) ---
    def build_forecast_view(self, data: dict, theme: dict):
        daily_summary = {}
        
        for item in data['list']:
            dt_txt = item['dt_txt']
            date_str = dt_txt.split(" ")[0]
            
            if date_str not in daily_summary:
                # Initialize with the first available data point for that day
                daily_summary[date_str] = {
                    "temps": [], 
                    "icon": item['weather'][0]['icon'], 
                    "desc": item['weather'][0]['main']
                }
            
            daily_summary[date_str]["temps"].append(item['main']['temp'])
            
            # Try to grab the weather icon from Noon for consistency
            if "12:00:00" in dt_txt:
                daily_summary[date_str]["icon"] = item['weather'][0]['icon']
                daily_summary[date_str]["desc"] = item['weather'][0]['main']

        forecast_items = []
        t_unit = "°F" if self.units == "imperial" else "°C"

        # Skip the first key (today) to show the next 5 days
        for date_str, summary in list(daily_summary.items())[1:6]: 
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = date_obj.strftime("%a, %b %d")
            
            temps = summary["temps"]
            max_t = self.convert_temp(max(temps))
            min_t = self.convert_temp(min(temps))
            
            card = ft.Container(
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                border_radius=10,
                content=ft.Row([
                    ft.Column([
                        ft.Text(day_name, weight="bold", color=theme["text"], size=16),
                        ft.Text(summary["desc"], size=12, color=theme["sub"])
                    ], expand=True),
                    ft.Image(src=f"https://openweathermap.org/img/wn/{summary['icon']}.png", width=50),
                    ft.Column([
                        ft.Text(f"H: {max_t:.0f}{t_unit}", weight="bold", color=theme["text"]),
                        ft.Text(f"L: {min_t:.0f}{t_unit}", color=theme["sub"])
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
            forecast_items.append(card)

        return ft.Column(forecast_items, scroll=ft.ScrollMode.AUTO, spacing=10)

    # --- Tab 3: Charts (Feature 6 - Enhanced) ---
    async def update_chart_type(self, e):
        # When user clicks segment button, update state and redraw chart
        self.chart_selection = list(e.control.selected)[0]
        # Rebuild just the chart view using existing forecast data
        weather_main = self.current_weather_data.get("weather", [{}])[0].get("main", "")
        theme = self.get_weather_theme(weather_main)
        
        chart_content = self.build_chart_view(self.forecast_data, theme)
        self.tabs.tabs[2].content = chart_content
        self.page.update()

    def build_chart_view(self, data: dict, theme: dict):
        chart_data = data['list'][:8] 
        points = []
        x_labels = []
        
        min_y = 1000
        max_y = -1000
        
        is_temp = self.chart_selection == "temp"
        is_humid = self.chart_selection == "humid"
        is_wind = self.chart_selection == "wind"

        t_unit = "°F" if self.units == "imperial" else "°C"
        w_unit = "mph" if self.units == "imperial" else "m/s"
        
        # Moved title out of the chart axis to avoid rotation bugs
        chart_title_text = f"Temperature ({t_unit})"
        if is_humid: chart_title_text = "Humidity (%)"
        if is_wind: chart_title_text = f"Wind Speed ({w_unit})"

        for i, item in enumerate(chart_data):
            dt_obj = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
            time_label = dt_obj.strftime("%H:%M")
            
            if is_temp: val = self.convert_temp(item['main']['temp'])
            elif is_humid: val = item['main']['humidity']
            elif is_wind: val = self.convert_speed(item['wind']['speed'])
            else: val = 0

            if val < min_y: min_y = val
            if val > max_y: max_y = val

            tooltip_text = f"{val:.1f}"
            points.append(ft.LineChartDataPoint(i, val, tooltip=tooltip_text))
            # Simplified axis label to ensure it's upright
            x_labels.append(ft.ChartAxisLabel(value=i, label=ft.Text(time_label, size=10, color=theme["sub"])))

        selector = ft.SegmentedButton(
            selected={self.chart_selection},
            on_change=self.update_chart_type,
            segments=[
                ft.Segment(value="temp", label=ft.Text("Temp")),
                ft.Segment(value="humid", label=ft.Text("Humidity")),
                ft.Segment(value="wind", label=ft.Text("Wind")),
            ],
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.SELECTED: theme["text"],
                    ft.ControlState.DEFAULT: theme["sub"],
                }
            )
        )

        chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=points,
                    stroke_width=4,
                    color=theme["text"],
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=ft.Colors.with_opacity(0.2, theme["text"]),
                    # Show dots on the line to make hovering easier
                    point=True, 
                    selected_below_line=ft.Colors.with_opacity(0.5, theme["text"]),
                )
            ],
            border=ft.border.all(1, ft.Colors.TRANSPARENT),
            left_axis=ft.ChartAxis(
                labels_size=35,
                title_size=0, # Hide axis title (moved to top)
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=30,
            ),
            tooltip_bgcolor=theme["text"],
            min_y=math.floor(min_y - 2) if not is_humid else 0,
            max_y=math.ceil(max_y + 2) if not is_humid else 100,
            # CRITICAL FIXES FOR HOVER:
            min_x=0,
            max_x=7, # Since we have 8 data points (0-7)
            expand=True,
        )

        return ft.Column([
            ft.Container(selector, alignment=ft.alignment.center),
            ft.Text(chart_title_text, size=14, weight="bold", color=theme["sub"]), # Title moved here
            ft.Container(content=chart, padding=10, height=250)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

    # --- Helpers ---
    def create_info_card(self, icon, label, value, theme):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=24, color=theme["icon"]),
                ft.Text(label, size=12, color=theme["sub"]),
                ft.Text(value, size=16, weight="bold", color=theme["text"]),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
            bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
            border_radius=10, padding=10, width=140
        )

    def show_error(self, message: str):
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.tabs.visible = False
        self.weather_container.opacity = 0
        self.page.update()

    def toggle_theme(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.theme_button.icon = ft.Icons.LIGHT_MODE if self.page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE
        self.page.update()

def main(page: ft.Page):
    WeatherApp(page)

if __name__ == "__main__":
    if Config.validate():
        ft.app(target=main)