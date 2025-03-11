import enum
from typing import Annotated
from livekit.agents import llm
import logging

logger=logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)

class Zone(enum.Enum):
    living_room = "living_room"
    master_bedroom = "master_bedroom"
    guest_bedroom = "guest_bedroom"
    kitchen = "kitchen"
    bathroom = "bathroom"
    office = "office"

class AssistantFunction(llm.FunctionContext):
    def __int__(self) -> None:
        super(). __init__()

        self._temperature = {
            Zone.living_room: 24,
            Zone.office: 24,
            Zone.kitchen: 24,
            Zone.guest_bedroom: 26,
            Zone.master_bedroom: 25,
            Zone.bathroom: 26
        }
    @llm.ai_callable(description="get the temperature in a specific room")
    def get_temperature(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")]):
        logger.info("get temp - zone %s", zone)
        temp = self._temperature[Zone(zone)]
        return f"the temperature in the {zone} is {temp}C"

    @llm.ai_callable(description="set the temperature in a specific room")
    def set_temperature(self,
                        zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")],
                        temp: Annotated[int, llm.TypeInfo(description="The temperature to set")],

    ):
        logger.info("set temp - zone %s, temp: %s", zone, temp)
        self._temperature[Zone(zone)] = temp
        return f"the temperature in the {zone} is now {temp}C"