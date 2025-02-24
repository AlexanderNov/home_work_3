import flet as ft
import os
from archfunc import folder_to_zip, analyse_path


def main(page: ft.Page):
    def pick_source_folder_result(e: ft.FilePickerResultEvent):
        selected_source_folder.value = e.path
        selected_source_folder.update()

    def pick_destination_folder_result(e: ft.FilePickerResultEvent):
        selected_destination_folder.value = e.path
        selected_destination_folder.update()

    def btn_clicked_analyse(e):
        analyse_path(selected_source_folder.value)

    def btn_clicked_arch(e):
        folder_to_zip(selected_source_folder.value, selected_destination_folder.value)

    pick_source_folder_dialog = ft.FilePicker(on_result=pick_source_folder_result)
    selected_source_folder = ft.Text()
    page.overlay.append(pick_source_folder_dialog)
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Выберете папку для архивации/анализа:",
                    icon=ft.Icons.FOLDER,
                    on_click=lambda _: pick_source_folder_dialog.get_directory_path(
                        initial_directory=os.getcwd()
                    ),
                ),
                selected_source_folder,
            ]
        )
    )

    pick_destination_folder_dialog = ft.FilePicker(on_result=pick_destination_folder_result)
    selected_destination_folder = ft.Text()
    page.overlay.append(pick_destination_folder_dialog)
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Выберете папку для архива:",
                    icon=ft.Icons.FOLDER,
                    on_click=lambda _: pick_destination_folder_dialog.get_directory_path(
                        initial_directory=os.getcwd()
                    ),
                ),
                selected_destination_folder,
            ]
        )
    )

    btn_arch = ft.ElevatedButton(text="Архивировать", on_click=btn_clicked_arch)
    page.add(btn_arch)
    btn_analyse = ft.ElevatedButton(text="Анализировать", on_click=btn_clicked_analyse)
    page.add(btn_analyse)

    page.update()


ft.app(target=main)
