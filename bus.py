import discord
import passiogo
from utils import refresh
from datetime import datetime, time
from os import getenv

BASE = getenv('BASE_URL')
BUS_URL = getenv('SCHEDULE_URL')
AUTHOR = getenv('BUS_AUTHOR')
ICON_URL = getenv('BUS_ICON_URL')
SCHEDULE_COLOR = getenv('SCHEDULE_COLOR')
BUS_SYSTEM_ID = getenv('BUS_SYSTEM_ID')

def bus_alert() -> discord.Embed:
    system = passiogo.getSystemFromID(BUS_SYSTEM_ID)
    alerts = [alert.__dict__ for alert in system.getSystemAlerts()]
    #busses = BUS_URL
    announce_list = ''
    for alert in alerts:
        announce_list += f'* **{alert["gtfsAlertHeaderText"]}**\n{alert["gtfsAlertDescriptionText"]}\n'

    bus_embed = discord.Embed(title="Campus Shuttle Announcements",
                              #url=busses,
                              description=announce_list,
                              color=SCHEDULE_COLOR)
    bus_embed.set_author(name=AUTHOR,
                         icon_url=ICON_URL)
    bus_embed.set_footer(text=datetime.now().strftime('%B %d, %Y | %I:%M:%S %p'))

    return bus_embed

"""
UNCOMMENT TO ENABLE WEBSCRAPING
def bus_info(num: int) -> discord.Embed:
    bus_content = refresh(BUS_URL)
    bus_url = BUS_URL
    system = passiogo.getSystemFromID(BUS_SYSTEM_ID)
    info_available = True
    schedules = Replace this with a bs4 statement that retrieves the bus schedule titles
    
    description = ''
    if int(num) == 0:
        color = SCHEDULE_COLOR
        title = 'Bus Schedules'
        sched_links = [f'* [{schedule.text}]({BASE + schedule["href"]})' for schedule in schedules]
        for sched in sched_links:
            description = description + f'{sched}\n'
    else:
        title = schedules[int(num) - 1].text
        route = [route.__dict__ for route in system.getRoutes() if route.__dict__["name"] in title]
        if len(route) == 1:
            route = route[0]
        bus = [vehicle.__dict__ for vehicle in system.getVehicles() if vehicle.__dict__["routeName"] == route["name"]]
        if len(bus) == 1:
            bus = bus[0]
        color = int(f'{route["groupColor"][1:]}', 16)
        route_url = BASE + schedules[int(num) - 1]['href']
        route_content = refresh(route_url)
        
        IF YOU HAVE A WAY TO DETERMINE STOP TIMES, DO IT HERE
        
        bus_url = route_url
        title = schedules[int(num) - 1].text


    embed = discord.Embed(title=title,
                            url=bus_url,
                            description=description,
                            color=color)
    embed.set_author(name=AUTHOR,
                     icon_url=ICON_URL)
    embed.set_footer(text=datetime.now().strftime('%B %d, %Y | %I:%M:%S %p'))

    return embed
    """
