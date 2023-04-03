from abc import ABCMeta, abstractmethod

class Filters(metaclass=ABCMeta):
  @abstractmethod
  def get_params(self) -> dict:
    return {
      "p_l": 0.0,
      "p_vp": 0.0,
      "dy": 0.0,
      "p_ebita": 0.0,
      "p_ebit": 0.0,
      "dividaliquida_patrimonioliquido": 0.0,
      "dividaliquida_ebitda": 0.0,
      "dividaliquida_ebit": 0.0,
      ""
    }

  @abstractmethod
  def dividens(self, params: dict) ->
