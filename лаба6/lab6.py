import wx
import psycopg2
from openpyxl import Workbook
from packet.pas import pas
from packet.leg import leg
from packet.gruz import gruz

def benz(type):
    return 1 if type.lower() in 'бенз' else 0

def diz(type):
    return 1 if type.lower() in 'диз' else 0

class MainFrame(wx.Frame):
    def __init__(self, parent, title="Расчёт поездок"):
        wx.Frame.__init__(self, parent, title=title, size=(600, 500))
        self.panel = wx.Panel(self)
        self.current_module = None
        self.results = None
        calc_types = ["Грузовой", "Легковой", "Пассажирский"]

        st = wx.StaticText(self.panel, label="Выберите тип расчёта:")
        self.choice = wx.Choice(self.panel, choices=calc_types)
        self.choice.Bind(wx.EVT_CHOICE, self.onChoice)

        self.input_panel = wx.Panel(self.panel)
        self.input_sizer = wx.BoxSizer(wx.VERTICAL)
        self.input_panel.SetSizer(self.input_sizer)

        self.calc_btn = wx.Button(self.panel, label="Рассчитать")
        self.calc_btn.Bind(wx.EVT_BUTTON, self.onCalculate)

        self.save_report_btn = wx.Button(self.panel, label="Сохранить отчёт (XLS)")
        self.save_report_btn.Bind(wx.EVT_BUTTON, self.onSaveReport)

        self.save_db_btn = wx.Button(self.panel, label="Сохранить в БД")
        self.save_db_btn.Bind(wx.EVT_BUTTON, self.onSaveDB)

        self.result_tc = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(st, 0, wx.ALL, 5)
        main_sizer.Add(self.choice, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_panel, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.calc_btn, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(self.result_tc, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.save_report_btn, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(self.save_db_btn, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(main_sizer)
        self.inputs = {}
        self.Show()

    def clear_inputs(self):
        for child in self.input_panel.GetChildren():
            child.Destroy()
        self.input_sizer.Clear(True)
        self.inputs = {}

    def onChoice(self, event):
        self.clear_inputs()
        selection = self.choice.GetString(self.choice.GetSelection())
        self.current_module = selection

        common_fields = [("Тип топлива (бенз/диз)", "type")]

        if "Грузовой" in selection:
            fields = common_fields + [("Масса прицепа (кг)", "gpr"),
                                      ("Масса груза (кг)", "ggr"),
                                      ("Расстояние (км)", "d"),
                                      ("Скорость (км/ч)", "v")]
        elif "Легковой" in selection:
            fields = common_fields + [("Расстояние поездки (км)", "d"),
                                      ("Скорость (км/ч)", "v"),
                                      ("Количество пассажиров", "np"),
                                      ("Вес багажа (кг)", "bg")]
        elif "Пассажирский" in selection:
            fields = common_fields + [("Количество пассажиров", "np"),
                                      ("Вес багажа (кг)", "bg"),
                                      ("Расстояние (км)", "d"),
                                      ("Скорость (км/ч)", "v")]
        else:
            fields = common_fields

        for label_text, var_name in fields:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self.input_panel, label=label_text)
            ctrl = wx.Choice(self.input_panel, choices=["бенз", "диз"]) if var_name == "type" else wx.TextCtrl(self.input_panel)
            if var_name == "type":
                ctrl.SetSelection(0)
            hsizer.Add(label, 0, wx.ALL | wx.CENTER, 5)
            hsizer.Add(ctrl, 1, wx.ALL | wx.EXPAND, 5)
            self.input_sizer.Add(hsizer, 0, wx.EXPAND)
            self.inputs[var_name] = ctrl

        self.input_panel.Layout()
        self.panel.Layout()

    def onCalculate(self, event):
        try:
            type = self.inputs["type"].GetStringSelection().strip()
            if "Грузовой" in self.current_module:
                self.results = gruz(type,
                                    float(self.inputs["gpr"].GetValue()),
                                    float(self.inputs["ggr"].GetValue()),
                                    float(self.inputs["d"].GetValue()),
                                    float(self.inputs["v"].GetValue()))
            elif "Легковой" in self.current_module:
                self.results = leg(type,
                                   float(self.inputs["d"].GetValue()),
                                   float(self.inputs["v"].GetValue()),
                                   int(self.inputs["np"].GetValue()),
                                   float(self.inputs["bg"].GetValue()))
            elif "Пассажирский" in self.current_module:
                self.results = pas(type,
                                   int(self.inputs["np"].GetValue()),
                                   float(self.inputs["bg"].GetValue()),
                                   float(self.inputs["d"].GetValue()),
                                   float(self.inputs["v"].GetValue()))
            q, cost, t = self.results
            self.result_tc.SetValue(f"Расход топлива (л): {q}\nСтоимость поездки (₽): {cost}\nВремя в пути (ч): {t}")
        except Exception as e:
            wx.MessageBox(f"Ошибка при расчёте: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def onSaveReport(self, event):
        if not self.results:
            wx.MessageBox("Сначала выполните расчёт", "Информация", wx.OK | wx.ICON_INFORMATION)
            return
        with wx.FileDialog(self, "Сохранить отчёт", wildcard="Excel документ (*.xlsx)|*.xlsx",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fd:
            if fd.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fd.GetPath()
            if not pathname.endswith(".xlsx"):
                pathname += ".xlsx"
            self.save_xlsx(pathname)

    def save_xlsx(self, pathname):
        wb = Workbook()
        ws = wb.active
        ws.title = "Отчёт"
        ws.append(["Отчёт по расчёту"])
        ws.append([f"Тип расчёта: {self.current_module}"])
        ws.append([])
        ws.append(["Входные данные"])
        for key, ctrl in self.inputs.items():
            value = ctrl.GetStringSelection() if isinstance(ctrl, wx.Choice) else ctrl.GetValue()
            ws.append([key, value])
        ws.append([])
        ws.append(["Результаты расчёта"])
        q, cost, t = self.results
        ws.append(["Расход топлива (л)", q])
        ws.append(["Стоимость поездки (₽)", cost])
        ws.append(["Время в пути (ч)", t])
        try:
            wb.save(pathname)
            wx.MessageBox("Отчёт сохранён", "Информация", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Ошибка при сохранении: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def onSaveDB(self, event):
        if not self.results:
            wx.MessageBox("Сначала выполните расчёт", "Информация", wx.OK | wx.ICON_INFORMATION)
            return
        conn_params = {
            "host": "localhost",
            "port": 5432,
            "dbname": "postgres",
            "user": "postgres",
            "password": "2099"
        }
        try:
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS calculations (
                    calc_type VARCHAR(100),
                    input_data TEXT,
                    result_data TEXT
                )
            """)
            input_data = "; ".join([
                f"{k}: {v.GetStringSelection() if isinstance(v, wx.Choice) else v.GetValue()}"
                for k, v in self.inputs.items()
            ])
            q, cost, t = self.results
            result_data = f"Расход топлива: {q}, Стоимость: {cost}, Время: {t}"
            cur.execute("""
                INSERT INTO calculations (calc_type, input_data, result_data)
                VALUES (%s, %s, %s)
            """, (self.current_module, input_data, result_data))
            conn.commit()
            cur.close()
            conn.close()
            wx.MessageBox("Данные сохранены в БД", "Информация", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Ошибка сохранения в БД: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None)
    app.MainLoop()

