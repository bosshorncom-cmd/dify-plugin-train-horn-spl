from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.spl_calc import SplCalculationError, format_prediction, predict_spl


class TrainHornSplTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        attenuation = tool_parameters.get("attenuation_db_per_km", 0)
        if attenuation is None or attenuation == "":
            attenuation = 0
        try:
            result = predict_spl(
                reference_spl_db=tool_parameters.get("reference_spl_db"),
                reference_distance_m=tool_parameters.get("reference_distance_m"),
                target_distance_m=tool_parameters.get("target_distance_m"),
                attenuation_db_per_km=attenuation,
            )
        except SplCalculationError as exc:
            payload = {"ok": False, "error": str(exc)}
            yield self.create_json_message(payload)
            yield self.create_text_message(str(exc))
            return

        payload = {"ok": True, **result}
        yield self.create_json_message(payload)
        yield self.create_text_message(format_prediction(result))
