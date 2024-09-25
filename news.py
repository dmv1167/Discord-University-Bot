import discord
from utils import refresh
from datetime import datetime

BASE = 'https://www.rit.edu'
URL = f'{BASE}/news'
TIMEOUT = 30

def get_timeout() -> int:
    return TIMEOUT

def set_timeout(time: int) -> None:
    global TIMEOUT
    TIMEOUT = time

def get_news_embed() -> discord.Embed:
    news_list = ''
    news_elements = refresh(URL).findAll('li', {'class': 'py-3'})
    for newsElement in news_elements:
        news = newsElement.find('span', {'class': 'field-content'}).find('a', recursive=False)
        news_list += f'* [{news.text}](<https://www.rit.edu/{news.get("href")}>)\n'

    news_embed = discord.Embed(title="Headline News",
                              url="https://www.rit.edu/news",
                              description=news_list,
                              color=0xFF6900)
    news_embed.set_author(name="RIT News",
                         icon_url='https://pbs.twimg.com/profile_images/1105451876689068033/eZFMq8pb_400x400.png')
    news_embed.set_footer(text=datetime.now().strftime('%B %d, %Y | %I:%M:%S %p'))

    return news_embed

def parse_descriptions(site: str) -> list:
    desc_list = []
    descriptions = (refresh(site).find('div', {'class': 'single-column-container-31914'})
                    .findAll('div', {'class': 'card-text'}))
    for description in descriptions:
        desc_list.append(description.find('p').text)
    return desc_list


def make_desc(label: int) -> discord.Embed:
    extra_elements = (refresh(URL).find('div', {'class': 'single-column-container-31914'})
                     .findAll('a', {'class': 'card-link'}))

    desc_embed = discord.Embed(title=extra_elements[label].find('p', {'class': 'card-title'}).text,
                               url=extra_elements[label].get('href'),
                               description=parse_descriptions(URL)[label], color=0xFF6900)
    desc_embed.set_author(name="RIT News",
                         icon_url='https://pbs.twimg.com/profile_images/1105451876689068033/eZFMq8pb_400x400.png')
    thumbnail = extra_elements[label].find('img', {'class': 'card-img-top'}).get('data-src')
    try:
        date = refresh(extra_elements[label].get('href')).find('div', {'id': 'content--news'}).find('div', {'class': 'd-inline'}).text
        desc_embed.set_footer(text='Posted ' + date.strip())
    except:
        pass

    desc_embed.set_thumbnail(url='https://www.rit.edu' + thumbnail)
    return desc_embed


class NewsView(discord.ui.View):

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=None)

    @discord.ui.button(label='More',
                       style=discord.ButtonStyle.red)
    async def more(self, interaction: discord.Interaction, button: discord.ui.Button):
        extra_list = ''
        extra_elements = refresh(URL).find('div',
                                           {'class': 'single-column-container-31914'}).findAll('a',
                                                                                              {'class': 'card-link'})
        for extraElement in extra_elements:
            extra = extraElement.find('p', {'class': 'card-title'})
            extra_list += f'{str(extra_elements.index(extraElement) + 1)}. [{extra.text.strip()}](<{extraElement.get("href")}>)\n'

        extra_embed = discord.Embed(title="Latest News",
                                   url="https://www.rit.edu/news",
                                   description=extra_list,
                                   color=0xFF6900)
        extra_embed.set_author(name="RIT News",
                              icon_url='https://pbs.twimg.com/profile_images/1105451876689068033/eZFMq8pb_400x400.png')
        extra_embed.set_footer(
            text=f'{datetime.now().strftime("%B %d, %Y | %I:%M:%S %p")}   (Buttons below for more info)')
        await interaction.response.edit_message(embed=extra_embed, view=MoreView(timeout=TIMEOUT))


class MoreView(discord.ui.View):

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

    @discord.ui.button(label='1',
                       style=discord.ButtonStyle.blurple)
    async def desc1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(0), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='2',
                       style=discord.ButtonStyle.blurple)
    async def desc2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(1), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='3',
                       style=discord.ButtonStyle.blurple)
    async def desc3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(2), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='4',
                       style=discord.ButtonStyle.blurple)
    async def desc4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(3), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='Back',
                       style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=get_news_embed(), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='5',
                       style=discord.ButtonStyle.blurple)
    async def desc5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(4), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='6',
                       style=discord.ButtonStyle.blurple)
    async def desc6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(5), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='7',
                       style=discord.ButtonStyle.blurple)
    async def desc7(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(6), view=NewsView(timeout=TIMEOUT))

    @discord.ui.button(label='8',
                       style=discord.ButtonStyle.blurple)
    async def desc8(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=make_desc(7), view=NewsView(timeout=TIMEOUT))