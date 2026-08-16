import flet as ft

def main(page: ft.Page):
    page.title = "Media Hub"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    # Состояние путей для папок (в будущем сохраняются в настройки)
    settings_data = {
        "theme": "Темная",
        "path_youtube": "/storage/emulated/0/Download/YouTube",
        "path_tiktok": "/storage/emulated/0/Download/TikTok",
        "path_pinterest": "/storage/emulated/0/Download/Pinterest",
        "path_twitch": "/storage/emulated/0/Download/Twitch",
        "path_spotify": "/storage/emulated/0/Download/Spotify",
        "path_music": "/storage/emulated/0/Music/Downloaded"
    }

    selected_source = "YouTube"

    # --- ЭЛЕМЕНТЫ ИНТЕРФЕЙСА (ЭКРАН 1: ГЛАВНЫЙ / СКАЧИВАНИЕ) ---
    url_input = ft.TextField(
        label="Вставьте ссылку...",
        border_radius=16,
        expand=True,
        border_color=ft.colors.OUTLINE,
        focused_border_color=ft.colors.PRIMARY
    )

    source_btn_text = ft.Text("YouTube", weight=ft.FontWeight.W_500)
    
    # Выпадающее меню выбора источника (справа от поля ввода)
    source_menu = ft.PopupMenuButton(
        content=ft.Row([source_btn_text, ft.Icon(ft.icons.ARROW_DROP_DOWN)], tight=True),
        items=[
            ft.PopupMenuItem(text="YouTube", on_click=lambda e: change_source("YouTube")),
            ft.PopupMenuItem(text="TikTok", on_click=lambda e: change_source("TikTok")),
            ft.PopupMenuItem(text="Pinterest", on_click=lambda e: change_source("Pinterest")),
            ft.PopupMenuItem(text="Spotify", on_click=lambda e: change_source("Spotify")),
            ft.PopupMenuItem(text="Twitch", on_click=lambda e: change_source("Twitch")),
        ],
        offset=ft.Offset(0, 40)
    )

    def change_source(source_name):
        nonlocal selected_source
        selected_source = source_name
        source_btn_text.value = source_name
        page.update()

    status_card = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.INFO_OUTLINE, color=ft.colors.PRIMARY),
            ft.Text(f"Готово к скачиванию из {selected_source}", expand=True)
        ]),
        padding=15,
        border_radius=16,
        bgcolor=ft.colors.SURFACE_CONTAINER_HIGH,
        visible=False
    )

    download_main_btn = ft.ElevatedButton(
        text="Скачать контент",
        icon=ft.icons.DOWNLOAD_ROUNDED,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=16),
            padding=20
        ),
        on_click=lambda e: trigger_download()
    )

    def trigger_download():
        if not url_input.value:
            status_card.content.controls[1].value = "Сначала вставьте ссылку!"
            status_card.visible = True
            page.update()
            return
        target_dir = settings_data.get(f"path_{selected_source.lower()}", "Default")
        status_card.content.controls[1].value = f"Загрузка в: {target_dir}"
        status_card.visible = True
        page.update()

    url_row = ft.Row([url_input, source_menu], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    download_view = ft.Column([
        ft.Text("Загрузчик медиа", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("Выберите источник справа и вставьте ссылку", color=ft.colors.ON_SURFACE_VARIANT),
        ft.Container(height=20),
        url_row,
        ft.Container(height=20),
        download_main_btn,
        ft.Container(height=20),
        status_card
    ], spacing=10, padding=20)


    # --- ЭКРАН 2: ПОИСК МУЗЫКИ ---
    search_input = ft.TextField(
        label="Введите название трека или исполнителя...",
        border_radius=16,
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: filter_music(e.control.value)
    )

    # Демо-база треков для динамического поиска
    mock_tracks = [
        {"title": "Blinding Lights", "artist": "The Weeknd", "duration": "3:20", "cover": "https://picsum.photos/200?1"},
        {"title": "Starboy", "artist": "The Weeknd, Daft Punk", "duration": "3:50", "cover": "https://picsum.photos/200?2"},
        {"title": "Numb", "artist": "Linkin Park", "duration": "3:07", "cover": "https://picsum.photos/200?3"},
        {"title": "Believer", "artist": "Imagine Dragons", "duration": "3:24", "cover": "https://picsum.photos/200?4"},
        {"title": "In the End", "artist": "Linkin Park", "duration": "3:36", "cover": "https://picsum.photos/200?5"},
    ]

    tracks_list_view = ft.ListView(expand=1, spacing=10, padding=10)

    # Элемент мини-плеера в стиле Telegram (снизу)
    player_title = ft.Text("Название трека", weight=ft.FontWeight.BOLD, size=14, no_wrap=True)
    player_artist = ft.Text("Исполнитель", size=12, color=ft.colors.ON_SURFACE_VARIANT)
    play_pause_icon = ft.Icon(ft.icons.PAUSE_ROUNDED, size=28)
    
    player_container = ft.Container(
        content=ft.Column([
            # Верхняя тонкая линия перемотки
            ft.Slider(min=0, max=100, value=30, height=10, active_color=ft.colors.PRIMARY),
            ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Image(src="https://picsum.photos/200", width=40, height=40, border_radius=8),
                        width=40, height=40
                    ),
                    ft.Column([player_title, player_artist], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
                ], spacing=10, expand=True),
                
                # Кнопки управления плеером
                ft.IconButton(icon=ft.icons.SKIP_PREVIOUS_ROUNDED, on_click=lambda e: print("Prev")),
                ft.IconButton(
                    content=play_pause_icon, 
                    on_click=lambda e: toggle_play_pause()
                ),
                ft.IconButton(icon=ft.icons.SKIP_NEXT_ROUNDED, on_click=lambda e: print("Next")),
                # Крестик закрытия плеера
                ft.IconButton(icon=ft.icons.CLOSE_ROUNDED, on_click=lambda e: close_player())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=0),
        padding=10,
        bgcolor=ft.colors.SURFACE_CONTAINER_HIGHEST,
        border_radius=ft.border_radius.only(top_left=24, top_right=24),
        visible=False # Скрыт по умолчанию
    )

    def toggle_play_pause():
        if play_pause_icon.name == ft.icons.PAUSE_ROUNDED:
            play_pause_icon.name = ft.icons.PLAY_ARROW_ROUNDED
        else:
            play_pause_icon.name = ft.icons.PAUSE_ROUNDED
        page.update()

    def close_player():
        player_container.visible = False
        page.update()

    def play_track(track):
        player_title.value = track["title"]
        player_artist.value = track["artist"]
        player_container.visible = True
        play_pause_icon.name = ft.icons.PAUSE_ROUNDED
        page.update()

    def download_track_action(track):
        print(f"Скачивание трека в папку: {settings_data['path_music']}")

    def render_tracks(tracks_to_show):
        tracks_list_view.controls.clear()
        for track in tracks_to_show:
            card = ft.Container(
                content=ft.Row([
                    ft.ClipRect(
                        border_radius=ft.border_radius.all(12),
                        content=ft.Image(src=track["cover"], width=50, height=50, fit=ft.ImageFit.COVER)
                    ),
                    ft.Column([
                        ft.Text(track["title"], weight=ft.FontWeight.W_600, size=15),
                        ft.Row([
                            ft.Text(track["artist"], size=12, color=ft.colors.ON_SURFACE_VARIANT),
                            ft.Text(" • ", size=12, color=ft.colors.ON_SURFACE_VARIANT),
                            ft.Text(track["duration"], size=12, color=ft.colors.ON_SURFACE_VARIANT),
                        ], spacing=2)
                    ], expand=True, spacing=2),
                    # Кнопка воспроизведения
                    ft.IconButton(
                        icon=ft.icons.PLAY_ARROW_ROUNDED,
                        bgcolor=ft.colors.SURFACE_CONTAINER_HIGH,
                        on_click=lambda e, t=track: play_track(t)
                    ),
                    # Кнопка скачивания трека напрямую
                    ft.IconButton(
                        icon=ft.icons.DOWNLOAD_ROUNDED,
                        bgcolor=ft.colors.SURFACE_CONTAINER_HIGH,
                        on_click=lambda e, t=track: download_track_action(t)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10,
                border_radius=16,
                bgcolor=ft.colors.SURFACE_CONTAINER,
            )
            tracks_list_view.controls.append(card)
        page.update()

    def filter_music(query):
        if not query:
            render_tracks(mock_tracks)
            return
        filtered = [t for t in mock_tracks if query.lower() in t["title"].lower() or query.lower() in t["artist"].lower()]
        render_tracks(filtered)

    search_view = ft.Column([
        ft.Text("Поиск музыки", size=28, weight=ft.FontWeight.BOLD),
        search_input,
        ft.Container(height=10),
        tracks_list_view
    ], expand=True, padding=20)

    # Инициализируем список треков при запуске
    render_tracks(mock_tracks)


    # --- ЭКРАН 3: НАСТРОЙКИ ---
    theme_dropdown = ft.Dropdown(
        label="Тема оформления",
        value=settings_data["theme"],
        options=[
            ft.dropdown.Option("Темная"),
            ft.dropdown.Option("Светлая"),
        ],
        border_radius=16,
        on_change=lambda e: change_theme(e.control.value)
    )

    def change_theme(theme_name):
        settings_data["theme"] = theme_name
        if theme_name == "Светлая":
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    # Поля путей для каждого типа скачивания
    tf_yt = ft.TextField(label="Папка YouTube", value=settings_data["path_youtube"], border_radius=12, text_size=12)
    tf_tt = ft.TextField(label="Папка TikTok", value=settings_data["path_tiktok"], border_radius=12, text_size=12)
    tf_pin = ft.TextField(label="Папка Pinterest", value=settings_data["path_pinterest"], border_radius=12, text_size=12)
    tf_twitch = ft.TextField(label="Папка Twitch", value=settings_data["path_twitch"], border_radius=12, text_size=12)
    tf_spot = ft.TextField(label="Папка Spotify", value=settings_data["path_spotify"], border_radius=12, text_size=12)
    tf_music = ft.TextField(label="Папка Музыки по словам", value=settings_data["path_music"], border_radius=12, text_size=12)

    def save_settings(e):
        settings_data["path_youtube"] = tf_yt.value
        settings_data["path_tiktok"] = tf_tt.value
        settings_data["path_pinterest"] = tf_pin.value
        settings_data["path_twitch"] = tf_twitch.value
        settings_data["path_spotify"] = tf_spot.value
        settings_data["path_music"] = tf_music.value
        
        # Уведомление об успехе
        page.snack_bar = ft.SnackBar(ft.Text("Настройки успешно сохранены!"))
        page.snack_bar.open = True
        page.update()

    settings_view = ft.ListView([
        ft.Text("Настройки", size=28, weight=ft.FontWeight.BOLD),
        ft.Container(height=10),
        theme_dropdown,
        ft.Divider(height=30),
        ft.Text("Пути для сохранения файлов:", weight=ft.FontWeight.BOLD, size=16),
        tf_yt, tf_tt, tf_pin, tf_twitch, tf_spot, tf_music,
        ft.Container(height=15),
        ft.ElevatedButton("Сохранить настройки", icon=ft.icons.SAVE_ROUNDED, on_click=save_settings, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=16), padding=15))
    ], expand=True, padding=20)


    # --- ГЛАВНЫЙ КОНТЕЙНЕР ПЕРЕКЛЮЧЕНИЯ ЭКРАНОВ И НАВИГАЦИЯ ---
    content_area = ft.Container(expand=True)

    def select_tab(index):
        if index == 0:
            content_area.content = download_view
        elif index == 1:
            content_area.content = search_view
        elif index == 2:
            content_area.content = settings_view
        page.update()

    # По умолчанию открыт первый экран (Скачивание по URL)
    select_tab(0)

    # Нижняя панель навигации Material 3 (NavigationBar)
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.DOWNLOAD_ROUNDED, label="URL-address"),
            ft.NavigationDestination(icon=ft.icons.MUSIC_NOTE_ROUNDED, label="Поиск песен"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS_ROUNDED, label="Настройки"),
        ],
        on_change=lambda e: select_tab(e.control.selected_index),
        selected_index=0
    )

    # Общий каркас приложения (Screen Layout)
    page.add(
        ft.Column([
            content_area,
            player_container,  # Всплывающий телеграм-плеер (наверху над навигацией)
            nav_bar
        ], expand=True, spacing=0)
    )

ft.app(target=main)
