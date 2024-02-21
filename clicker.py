import flet as ft
import asyncio


def create_image() -> ft.Image:
    return ft.Image(
        src="image/vega.png",
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE)
    )


def create_progress_bar(page: ft.Page) -> ft.ProgressBar:
    return ft.ProgressBar(
        value=0,
        width=page.width - 100,
        bar_height=20,
        color="#ff8b1f",
        bgcolor="#bf6524"
    )


def create_snack_bar(page: ft.Page):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(
            value="Хочешь накопить на свое окно?",
            size=20,
            color="#ff8b1f",
            text_align=ft.TextAlign.CENTER
        ),
        bgcolor="#25223a",
        open=False
    )
    return page.snack_bar


def configure_page(page: ft.Page):
    page.title = "Coin"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.font = {"Gabriela-Regular": "fonts/Gabriela-Regular.ttf"}
    page.theme = ft.Theme(font_family="Gabriela-Regular")


async def main(page: ft.Page) -> None:
    configure_page(page)
    score = ft.Text(value="0", size=100, data=0)
    score_counter = ft.Text(size=50,no_wrap=True, animate_opacity=ft.Animation(duration=100, curve=ft.AnimationCurve.BOUNCE_IN))
    image = create_image()
    progress_bar = create_progress_bar(page)
    snack_bar = create_snack_bar(page)

    async def score_up(event: ft.ContainerTapEvent):
        score.data += 1
        score.value = str(score.data)
        image.scale = 0.95
        score_counter.opacity = 1
        score_counter.value = "+1"
        score_counter.right = 0
        score_counter.left = event.local_x
        score_counter.top = event.local_y
        score_counter.bottom = 0
        progress_bar.value += 0.01
        if score.data % 10 == 0:
            snack_bar.open = True
            progress_bar.value = 0
        await page.update_async()
        await asyncio.sleep(0.2)
        score_counter.opacity = 0
        image.scale = 1
        await page.update_async()

    await page.add_async(
        score,
        ft.Container(
            content=ft.Stack(controls=[image, score_counter]),
            on_click=score_up,
            margin=ft.Margin(0, 0, 0, 30)
        ),
        ft.Container(
            content=progress_bar,
            border_radius=ft.BorderRadius(10, 10, 10, 10)
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
