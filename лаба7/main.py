import PySimpleGUI as sg
from openpyxl import Workbook
from calc import GruzCalculation, LegCalculation, PasCalculation


class TripCalculatorGUI:
    def __init__(self, current_calc_type='Грузовой'):
        self._calc_types = ['Грузовой', 'Легковой', 'Пассажирский']
        self._current_calc_type = current_calc_type
        self._last_result = None
        self._initialize_gui()
    def _initialize_gui(self):
        sg.theme('LightBlue')
        self.window = self._create_window()
    def _create_window(self):
        layout = [
            [self._create_calc_type_selector()],
            [sg.Column(self._get_param_layout(), key='-PARAM-')],
            [self._create_action_buttons()],
            [self._create_output_field()]
        ]
        return sg.Window('Расчёт поездок', layout, finalize=True)
    def _create_calc_type_selector(self):
        return [
            sg.Text('Выберите тип расчёта:'),
            sg.Combo(
                self._calc_types,
                key='-TYPE-',
                default_value=self._current_calc_type,
                enable_events=True
            )
        ]

    def _get_param_layout(self):
        common_fields = [
            [sg.Text('Тип топлива'),
             sg.Combo(['бенз', 'диз'], key='fuel_type', default_value='бенз')]
        ]

        if self._current_calc_type == 'Грузовой':
            return common_fields + [
                [sg.Text('Масса прицепа (кг)'), sg.Input(key='gpr')],
                [sg.Text('Масса груза (кг)'), sg.Input(key='ggr')],
                [sg.Text('Расстояние (км)'), sg.Input(key='d')],
                [sg.Text('Скорость (км/ч)'), sg.Input(key='v')]
            ]
        elif self._current_calc_type == 'Легковой':
            return common_fields + [
                [sg.Text('Расстояние (км)'), sg.Input(key='d')],
                [sg.Text('Скорость (км/ч)'), sg.Input(key='v')],
                [sg.Text('Кол-во пассажиров'), sg.Input(key='np')],
                [sg.Text('Вес багажа (кг)'), sg.Input(key='bg')]
            ]
        else:  # Пассажирский
            return common_fields + [
                [sg.Text('Кол-во пассажиров'), sg.Input(key='np')],
                [sg.Text('Вес багажа (кг)'), sg.Input(key='bg')],
                [sg.Text('Расстояние (км)'), sg.Input(key='d')],
                [sg.Text('Скорость (км/ч)'), sg.Input(key='v')]
            ]

    def _create_action_buttons(self):
        return [
            sg.Button('Рассчитать', key='-CALCULATE-'),
            sg.Button('Сохранить отчёт (XLS)', key='-SAVE-')
        ]

    def _create_output_field(self):
        return [sg.Multiline(size=(60, 15), key='-OUTPUT-', disabled=True)]

    def _validate_inputs(self, values):
        required_fields = {
            'Грузовой': ['fuel_type', 'gpr', 'ggr', 'd', 'v'],
            'Легковой': ['fuel_type', 'd', 'v', 'np', 'bg'],
            'Пассажирский': ['fuel_type', 'np', 'bg', 'd', 'v']
        }

        for field in required_fields[self._current_calc_type]:
            if not values.get(field):
                raise ValueError(f"Поле '{field}' не заполнено")

    def _create_calculation(self, values):
        try:
            if self._current_calc_type == 'Грузовой':
                return GruzCalculation(
                    values['fuel_type'],
                    values['gpr'],
                    values['ggr'],
                    values['d'],
                    values['v']
                )
            elif self._current_calc_type == 'Легковой':
                return LegCalculation(
                    values['fuel_type'],
                    values['d'],
                    values['v'],
                    values['np'],
                    values['bg']
                )
            else:
                return PasCalculation(
                    values['fuel_type'],
                    values['np'],
                    values['bg'],
                    values['d'],
                    values['v']
                )
        except ValueError as e:
            raise ValueError(f"Ошибка в данных: {str(e)}")

    def _save_report(self, path, values, result):
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = 'Отчёт'

            ws.append([f"Тип расчёта: {self._current_calc_type}"])
            ws.append([])

            ws.append(['Входные данные'])
            for field in values:
                if field in ['fuel_type', 'gpr', 'ggr', 'd', 'v', 'np', 'bg']:
                    ws.append([field, values[field]])
            ws.append([])

            ws.append(['Результаты', 'Значение'])
            ws.append(['Расход топлива', result[0]])
            ws.append(['Стоимость', result[1]])
            ws.append(['Время', result[2]])

            wb.save(path)
            return True
        except Exception as e:
            sg.PopupError(f"Ошибка при сохранении файла: {str(e)}")
            return False

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            if event == '-TYPE-':
                self._current_calc_type = values['-TYPE-']
                self.window.close()
                self._initialize_gui()
                continue

            if event == '-CALCULATE-':
                try:
                    self._validate_inputs(values)
                    calc = self._create_calculation(values)
                    self._last_result = calc.calculate()
                    self.window['-OUTPUT-'].update(
                        f"Расход топлива: {self._last_result[0]}\n"
                        f"Стоимость: {self._last_result[1]}\n"
                        f"Время: {self._last_result[2]}"
                    )
                except Exception as e:
                    sg.PopupError(f"Ошибка: {str(e)}")

            if event == '-SAVE-':
                if not self._last_result:
                    sg.Popup("Сначала выполните расчёт")
                    continue

                path = sg.popup_get_file(
                    'Сохранить отчёт',
                    save_as=True,
                    file_types=(('Excel Files', '*.xlsx'),),
                    default_extension='.xlsx'
                )

                if path:
                    if self._save_report(path, values, self._last_result):
                        sg.Popup("Отчёт успешно сохранён")

        self.window.close()


if __name__ == '__main__':
    try:
        TripCalculatorGUI().run()
    except Exception as e:
        sg.PopupError(f"Критическая ошибка: {str(e)}")