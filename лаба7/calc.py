from abc import ABC, abstractmethod

class CalculationBase(ABC):
    def __init__(self, fuel_type):
        self.fuel_type = fuel_type
    @property
    def fuel_type(self):
        return self._fuel_type
    @fuel_type.setter
    def fuel_type(self, value):
        self._fuel_type = value

    @abstractmethod
    def calculate(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self._get_params_str()})"

    def _get_params_str(self):
        params = []
        for key, value in vars(self).items():
            if not key.startswith('__'):
                params.append(f"{key[1:] if key.startswith('_') else key}={value}")
        return ', '.join(params)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return vars(self) == vars(other)


class GruzCalculation(CalculationBase):
    def __init__(self, fuel_type, gpr, ggr, d, v):
        super().__init__(fuel_type)
        self.gpr = gpr
        self.ggr = ggr
        self.d = d
        self.v = v

    @property
    def gpr(self):
        return self._gpr

    @gpr.setter
    def gpr(self, value):
        self._gpr = float(value)

    @property
    def ggr(self):
        return self._ggr

    @ggr.setter
    def ggr(self, value):
        self._ggr = float(value)

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = float(value)

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = float(value)

    def calculate(self):
        from packet.gruz import gruz
        return gruz(self.fuel_type, self.gpr, self.ggr, self.d, self.v)



class LegCalculation(CalculationBase):
    def __init__(self, fuel_type, d, v, np, bg):
        super().__init__(fuel_type)
        self.d = d
        self.v = v
        self.np = np
        self.bg = bg

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = float(value)

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = float(value)

    @property
    def np(self):
        return self._np

    @np.setter
    def np(self, value):
        self._np = int(value)

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, value):
        self._bg = float(value)

    def calculate(self):
        from packet.leg import leg
        return leg(self.fuel_type, self.d, self.v, self.np, self.bg)


class PasCalculation(CalculationBase):
    def __init__(self, fuel_type, np, bg, d, v):
        super().__init__(fuel_type)
        self.np = np
        self.bg = bg
        self.d = d
        self.v = v

    @property
    def np(self):
        return self._np

    @np.setter
    def np(self, value):
        self._np = int(value)

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, value):
        self._bg = float(value)

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = float(value)

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = float(value)

    def calculate(self):
        from packet.pas import pas
        return pas(self.fuel_type, self.np, self.bg, self.d, self.v)
