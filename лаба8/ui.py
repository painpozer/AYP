import pygame
import calendar
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict


class AbstractModalWindow(ABC):
    def __init__(self, width: int = 460, height: int = 300, title: str = "") -> None:
        self.__rect = pygame.Rect(120, 80, width, height)
        self.__title = title
        self.__font = pygame.font.SysFont(None, 24)

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def title(self) -> str:
        return self.__title

    @property
    def font(self) -> pygame.font.Font:
        return self.__font

    def _draw_base(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (230, 230, 230), self.__rect)
        pygame.draw.rect(screen, (0, 0, 0), self.__rect, 2)
        if self.__title:
            title_surf = self.__font.render(self.__title, True, (0, 0, 0))
            screen.blit(title_surf, (self.__rect.x + 10, self.__rect.y + 10))

    def _draw_buttons(self, screen: pygame.Surface) -> Tuple[pygame.Rect, ...]:
        save_btn = pygame.Rect(150, 400, 80, 30)
        del_btn = pygame.Rect(250, 400, 80, 30)
        cancel_btn = pygame.Rect(350, 400, 80, 30)

        for btn, label in zip([save_btn, del_btn, cancel_btn], ["Сохранить", "Удалить", "Отмена"]):
            pygame.draw.rect(screen, (180, 180, 180), btn)
            pygame.draw.rect(screen, (0, 0, 0), btn, 1)
            screen.blit(self.__font.render(label, True, (0, 0, 0)), (btn.x + 5, btn.y + 5))

        return save_btn, del_btn, cancel_btn

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> Tuple[pygame.Rect, ...]:
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass


class NoteModal(AbstractModalWindow):
    def __init__(self, date: str, lines: List[str]) -> None:
        super().__init__(title=f"Заметки на {date}")
        self.__date = date
        self.__note_lines = lines.copy()
        self.__input_boxes: List[Tuple[pygame.Rect, str]] = []
        self.__create_inputs()

    @property
    def date(self) -> str:
        return self.__date

    @property
    def note_lines(self) -> List[str]:
        return [text for _, text in self.__input_boxes]

    def __create_inputs(self) -> None:
        self.__input_boxes = []
        for i, line in enumerate(self.__note_lines or [""]):
            rect = pygame.Rect(150, 150 + i * 40, 400, 30)
            self.__input_boxes.append((rect, line))

    def draw(self, screen: pygame.Surface) -> Tuple[pygame.Rect, ...]:
        self._draw_base(screen)

        for rect, text in self.__input_boxes:
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            text_surf = self.font.render(text, True, (0, 0, 0))
            screen.blit(text_surf, (rect.x + 5, rect.y + 5))

        return self._draw_buttons(screen)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                new_rect = pygame.Rect(150, 150 + len(self.__input_boxes) * 40, 400, 30)
                self.__input_boxes.append((new_rect, ""))
            elif self.__input_boxes:
                rect, text = self.__input_boxes[-1]
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                self.__input_boxes[-1] = (rect, text)


class CalendarView(AbstractModalWindow):
    def __init__(self, year: int, month: int, notes: Dict[str, List[str]]) -> None:
        super().__init__(width=580, height=400, title=f"Календарь {calendar.month_name[month]} {year}")
        self.__year = year
        self.__month = month
        self.__notes = notes
        self.__font = pygame.font.SysFont(None, 24)
        self.__buttons: List[Tuple[pygame.Rect, int, str]] = []
        self.__generate_buttons()

    def __generate_buttons(self) -> None:
        self.__buttons = []
        days = calendar.monthcalendar(self.__year, self.__month)
        for row_idx, week in enumerate(days):
            for col_idx, day in enumerate(week):
                if day != 0:
                    rect = pygame.Rect(self.rect.x + 20 + col_idx * 80, self.rect.y + 50 + row_idx * 60, 60, 40)
                    date_str = f"{self.__year}-{self.__month:02}-{day:02}"
                    self.__buttons.append((rect, day, date_str))

    def draw(self, screen: pygame.Surface) -> Tuple[pygame.Rect, ...]:
        self._draw_base(screen)

        for rect, day, date_str in self.__buttons:
            pygame.draw.rect(screen, (200, 200, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            text = self.__font.render(str(day), True, (0, 0, 0))
            screen.blit(text, (rect.x + 20, rect.y + 10))
            if date_str in self.__notes:
                pygame.draw.circle(screen, (255, 0, 0), (rect.right - 10, rect.top + 10), 5)
        return ()

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        for rect, _, date_str in self.__buttons:
            if rect.collidepoint(pos):
                return date_str
        return None
