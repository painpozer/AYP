import pygame
import sys
import calendar
from datetime import datetime
from typing import Dict, List, Optional
from ui import CalendarView, NoteModal
from storage import load_notes, save_notes


class NoNotesError(Exception):
    pass


def show_pygame_message(message: str) -> None:
    pygame.init()
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Сообщение")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()
    button = pygame.Rect(150, 130, 100, 40)

    running = True
    while running:
        screen.fill((240, 240, 240))
        text_surf = font.render(message, True, (0, 0, 0))
        screen.blit(text_surf, (200 - text_surf.get_width() // 2, 60))

        pygame.draw.rect(screen, (180, 180, 180), button)
        pygame.draw.rect(screen, (0, 0, 0), button, 2)
        btn_text = font.render("ОК", True, (0, 0, 0))
        screen.blit(btn_text, (button.x + 30, button.y + 7))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


class CalendarApp:
    def __init__(self, notes: Dict[str, List[str]]) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption("Календарь")
        self.__notes = notes
        now = datetime.now()
        self.__year = now.year
        self.__month = now.month
        self.__calendar_view = CalendarView(self.__year, self.__month, self.__notes)
        self.__font = pygame.font.SysFont(None, 32)
        self.__modal: Optional[NoteModal] = None

    @property
    def year(self) -> int:
        return self.__year

    @property
    def month(self) -> int:
        return self.__month

    def __draw_header(self) -> None:
        month_name = calendar.month_name[self.__month]
        header = self.__font.render(f"{month_name} {self.__year}", True, (0, 0, 0))
        self.__screen.blit(header, (250, 20))
        pygame.draw.polygon(self.__screen, (0, 0, 0), [(210, 30), (200, 40), (210, 50)])
        pygame.draw.polygon(self.__screen, (0, 0, 0), [(460, 30), (470, 40), (460, 50)])

    def run(self) -> None:
        running = True
        while running:
            self.__screen.fill((255, 255, 255))
            self.__draw_header()
            self.__calendar_view.draw(self.__screen)

            if self.__modal:
                save_btn, del_btn, cancel_btn = self.__modal.draw(self.__screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_notes(self.__notes)
                    running = False

                elif self.__modal:
                    self.__modal.handle_event(event)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if save_btn.collidepoint(event.pos):
                            self.__notes[self.__modal.date] = self.__modal.note_lines
                            self.__modal = None
                        elif del_btn.collidepoint(event.pos):
                            self.__notes.pop(self.__modal.date, None)
                            self.__modal = None
                        elif cancel_btn.collidepoint(event.pos):
                            self.__modal = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 200 <= event.pos[0] <= 210 and 30 <= event.pos[1] <= 50:
                        self.__month -= 1
                        if self.__month < 1:
                            self.__month = 12
                            self.__year -= 1
                        self.__calendar_view = CalendarView(self.__year, self.__month, self.__notes)

                    elif 460 <= event.pos[0] <= 470 and 30 <= event.pos[1] <= 50:
                        self.__month += 1
                        if self.__month > 12:
                            self.__month = 1
                            self.__year += 1
                        self.__calendar_view = CalendarView(self.__year, self.__month, self.__notes)

                    else:
                        clicked = self.__calendar_view.handle_click(event.pos)
                        if clicked:
                            self.__modal = NoteModal(clicked, self.__notes.get(clicked, []))

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    notes = load_notes()
    try:
        if not notes:
            raise NoNotesError("Заметки не добавлены")
    except NoNotesError as e:
        show_pygame_message(str(e))

    app = CalendarApp(notes)
    app.run()