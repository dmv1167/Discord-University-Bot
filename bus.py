import discord
from utils import refresh
from datetime import datetime, time

BASE = 'https://www.rit.edu'
BUS = f'{BASE}/parking/campus-shuttles'

def bus_alert() -> discord.Embed:
    elements = refresh(BUS)
    announcements = elements.find('div', {'class': ['py-3', 'py-mdlg-4']}).findAll('p', {'class': 'h3'})
    announce_list = ''
    for announcement in announcements:
        announce_list += f'* {announcement.text}\n'

    bus_embed = discord.Embed(title="Campus Shuttle Announcements",
                             url=BUS,
                             description=announce_list,
                             color=0xFF6900)
    bus_embed.set_author(name="RIT Busses",
                        icon_url='https://pbs.twimg.com/profile_images/1105451876689068033/eZFMq8pb_400x400.png')
    bus_embed.set_footer(text=datetime.now().strftime('%B %d, %Y | %I:%M:%S %p'))

    return bus_embed


def bus_info(num: int) -> discord.Embed:
    bus_content = refresh(BUS)
    bus_url = BUS

    schedules = bus_content.find('div', {'class': 'view-grouping-content'}).find_all('a')
    description = ''
    if int(num) == 0:
        title = 'Bus Schedules'
        sched_links = [f'* [{schedule.text}]({BASE + schedule["href"]})' for schedule in schedules]
        for sched in sched_links:
            description = description + f'{sched}\n'
    else:
        route_url = BASE + schedules[int(num) - 1]['href']
        route_content = refresh(route_url)
        table = route_content.find('table', {'class': 'table-striped'})
        stops = {}
        for header in table.find('thead').find_all('th'):
            if header not in stops:
                stops[header.text] = []
        next_time = None
        next_stop = None
        for row in table.find('tbody').find_all('tr'):
            for index, arrival in enumerate(row.find_all('td')):
                if arrival is not None:
                    time_split = arrival.text.split(':')
                    hour = int(time_split[0])
                    minute = int(time_split[1][:2])
                    if time_split[1][3:] == 'pm':
                        hour += 12
                        hour = hour % 24
                    stop_time = time(hour = hour,minute = minute, second=0)
                    stop = list(stops.keys())[index]
                    if index == 0 and next_time is None:
                        next_time = stop_time
                        next_stop = stop
                    if datetime.now().time() < stop_time:
                        next_time = stop_time
                        next_stop = stop
                    elif datetime.now().time() >= stop_time:
                        description = f'Next stop: **{next_stop}** at **{next_time.strftime("%I:%M %p")}**'
                    stops[stop].append(arrival.text)
        bus_url = route_url
        title = schedules[int(num) - 1].text


    embed = discord.Embed(title=title,
                            url=bus_url,
                            description=description,
                            color=0xFF6900)
    embed.set_author(name="RIT Busses",
                     icon_url='https://pbs.twimg.com/profile_images/1123208686875414528/ecELpGo__400x400.png')
    embed.set_footer(text=datetime.now().strftime('%B %d, %Y | %I:%M:%S %p'))

    return embed