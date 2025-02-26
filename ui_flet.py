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
        lv.controls.clear()

        if not os.path.exists(str(selected_source_folder.value)):
            results.value = "Укажите корректный путь к папке, которую хотите анализировать"
            results.update()
            raise ValueError("Укажите корректный путь к папке, которую хотите анализировать")

        analyse_results = analyse_path(selected_source_folder.value)
        results.value = "Результат работы:"
        results.update()

        for item in analyse_results:
            lv.controls.append(ft.Text(f"{item}"))

        lv.update()

    def btn_clicked_arch(e):
        lv.controls.clear()

        if not os.path.exists(str(selected_source_folder.value)):
            results.value = "Укажите корректный путь к папке, которую хотите архивировать"
            results.update()
            raise ValueError("Укажите корректный путь к папке, которую хотите архивировать")

        folder_to_zip(selected_source_folder.value, selected_destination_folder.value)

        archive_results = folder_to_zip(selected_source_folder.value, selected_destination_folder.value)
        results.value = "Результат работы:"
        results.update()

        for item in archive_results:
            lv.controls.append(ft.Text(f"{item}"))

        lv.update()

    page.title = "Программа архивации и анализа папок"

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
    selected_destination_folder.value = os.getcwd()

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
    btn_analyse = ft.ElevatedButton(text="Анализировать", on_click=btn_clicked_analyse)
    page.add(ft.Row([btn_arch, btn_analyse]))

    results = ft.Text("Результат работы:")
    page.add(results)

    lv = ft.ListView(expand=False, spacing=10)
    page.add(lv)

    page.update()


ft.app(target=main)
