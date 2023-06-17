from modules.common import ModuleOptions
from typing import NotRequired
from util import get_output, write_at_0
import asyncio
import sys

class BatteryModuleOptions(ModuleOptions):
    interval: NotRequired[float]
    """Refresh interval in seconds"""

DefaultBatteryModuleOptions: BatteryModuleOptions = {
    'fs': sys.stdout,
    'notify': lambda: None,
    'interval': 5.0
}

async def battery_module(options: BatteryModuleOptions):
    """Battery Module"""

    options = DefaultBatteryModuleOptions | options

    async def get_battery_info():
        while True:
            acpi_output = get_output('acpi -ab')
            battery, adapter = acpi_output.split('\n')
            battery = battery[11:]
            adapter = adapter[11:]

            charge_status = 'discharging'
            if adapter == 'on-line':
                charge_status = 'charging'
                if 'Not charging' in battery or 'Full' in battery:
                    charge_status = 'fully charged'

            battery_percent = ''
            if charge_status != 'fully charged':
                battery_percent = battery.split(',')[1].strip() + '%'
                if 'zero' in battery:
                    battery_percent += ' at ø rate'

            output = f'{charge_status} {battery_percent}'

            write_at_0(options.get('fs'), output)
            options.get('notify')()

            await asyncio.sleep(options.get('interval', 5.0))

    task = asyncio.create_task(get_battery_info())

    def kill():
        task.cancel()
        options.get('fs').close()

    return kill

