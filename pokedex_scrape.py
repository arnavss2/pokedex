""" urllib for downloading images
    timg for rendering images on cmd
    questionary for asking questions
    cli for making cmd application
    Figlet for customised fonts
    colored for colored text
    webdriver for webscraping sites
    ChromeDriverManager for Chrome """
import urllib
import timg
import questionary
from plumbum import cli
from pyfiglet import Figlet
from termcolor import colored
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def print_banner(set_font, set_text, set_color, set_attrs):
    """ Prints set_text with the given set_font, set_color and set_attrs. """
    print(colored(Figlet(font = set_font).renderText(set_text), set_color, attrs=set_attrs))

def get_pokemon_driver():
    """ Gets the pokemon driver by asking the user for the pokemon to search. """
    pokemon = questionary.text("Which pokemon do you want to search?").ask()

    base_url = "https://www.pokemon.com/us/pokedex"
    full_url = f"{base_url}/{pokemon}"

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = option)
    driver.get(full_url)
    return driver

def get_pokemon_title(driver):
    """ Gets the pokemon title including the name and the number of the pokemon. """
    return driver.find_element_by_class_name("pokedex-pokemon-pagination-title").text

def render_image(driver):
    """ Renders the image of the pokemon onto the command line. """
    img = driver.find_element_by_xpaths('//img[contains(@src,"https://assets.pokemon.com/assets/cms2/img/pokedex/full/")]')
    src = img.get_attribute('src')
    pokemon = get_pokemon_title(driver)[0]

    # download the image
    urllib.request.urlretrieve(src, f"./images/{pokemon}.png")

    obj = timg.Renderer()
    obj.load_image_from_file(f"./images/{pokemon}.png")
    obj.resize(200,200)
    obj.render(timg.ASCIIMethod)

def get_color(pokemon_type):
    """ Returns the color and the attributes corresponding to the given type. """
    color = ''
    attrs = []
    if pokemon_type == 'Normal' :
        color = 'white'
    elif pokemon_type == 'Fire' :
        color = 'red'
    elif pokemon_type == 'Water' :
        color = 'blue'
    elif pokemon_type == 'Grass' :
        color = 'green'
    elif pokemon_type == 'Electric' :
        color = 'yellow'
    elif pokemon_type == 'Ice' :
        color = 'cyan'
    elif pokemon_type == 'Psychic' :
        color = 'magenta'
    elif pokemon_type == 'Steel' :
        color = 'grey'
    elif pokemon_type == 'Fighting' :
        color = 'red'
        attrs.append('bold')
    elif pokemon_type == 'Poison' :
        color = 'magenta'
        attrs.append('dark')
    elif pokemon_type == 'Ground' :
        color = 'yellow'
        attrs.append('dark')
    elif pokemon_type == 'Flying' :
        color = 'cyan'
        attrs.append('dark')
    elif pokemon_type == 'Bug' :
        color = 'green'
        attrs.append('dark')
    elif pokemon_type == 'Ghost' :
        color = 'grey'
        attrs.append('bold')
    elif pokemon_type == 'Dark' :
        color = 'white'
        attrs.append('dark')
    elif pokemon_type == 'Dragon' :
        color = 'blue'
        attrs.append('dark')
    elif pokemon_type == 'Fairy' :
        color = 'magenta'
        attrs.append('bold')
    elif pokemon_type == 'Rock' :
        color = 'yellow'
        attrs.append('bold')
    return color, attrs

def print_types(driver):
    """ Prints the types of the given pokemon scraped from the pokemon website. """
    print_banner('epic', "Type:", 'white', [])

    types = driver.find_elements_by_xpath('//a[contains(@href,"/us/pokedex/?type=")]')
    for pokemon_type in types :
        print_banner('roman', pokemon_type.text, get_color(pokemon_type.text)[0],
        get_color(pokemon_type.text)[1])

def print_weaknesses(driver):
    """ Prints the weaknesses of the given pokemon scraped from the pokemon website. """
    print_banner('epic', "Weakness:", 'white', [])

    weaknesses = driver.find_elements_by_xpath('//a[contains(@href,"/us/pokedex/?weakness=")]')
    for weakness in weaknesses:
        print_banner('roman', weakness.text, get_color(weakness.text)[0],
        get_color(weakness.text)[1])

class PokedexScrape(cli.Application):
    """ PokedexScrape class that scrapes the information of pokemons from the website. """
    VERSION = "1.0"
    weakness = cli.Flag(['w', 'weakness'], help = "Shows the weaknesses of the pokemon")

    def main(self):
        print_banner('slant', "Welcome to Pokedex Scrape!", 'white', ['bold'])
        driver = get_pokemon_driver()
        print_banner('ogre', get_pokemon_title(driver), 'white', [])
        render_image(driver)
        print_types(driver)
        if self.weakness:
            print_weaknesses(driver)

if __name__ == "__main__":
    PokedexScrape()

### TESTS

def test_get_pokemon_title():
    """ Test to check if the pokemon title sscraped is correct. """
    full_url = "https://www.pokemon.com/us/pokedex/pikachu"

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = option)
    driver.get(full_url)
    pokemon_title = get_pokemon_title(driver)
    title = pokemon_title.split()
    assert title[0] == "Pikachu"
    assert title[1] == "#025"

def test_get_color():
    """ Test to check if the colors and attributes are correct. """
    assert get_color('Normal')[0] == 'white'
    assert get_color('Normal')[1] == []
    assert get_color('Fire')[0] == 'red'
    assert get_color('Fire')[1] == []
    assert get_color('Water')[0] == 'blue'
    assert get_color('Water')[1] == []
    assert get_color('Grass')[0] == 'green'
    assert get_color('Grass')[1] == []
    assert get_color('Electric')[0] == 'yellow'
    assert get_color('Electric')[1] == []
    assert get_color('Ice')[0] == 'cyan'
    assert get_color('Ice')[1] == []
    assert get_color('Psychic')[0] == 'magenta'
    assert get_color('Psychic')[1] == []
    assert get_color('Steel')[0] == 'grey'
    assert get_color('Steel')[1] == []
    assert get_color('Fighting')[0] == 'red'
    assert get_color('Fighting')[1] == ['bold']
    assert get_color('Poison')[0] == 'magenta'
    assert get_color('Poison')[1] == ['dark']
    assert get_color('Fighting')[0] == 'red'
    assert get_color('Fighting')[1] == ['bold']
    assert get_color('Ground')[0] == 'yellow'
    assert get_color('Ground')[1] == ['dark']
    assert get_color('Flying')[0] == 'cyan'
    assert get_color('Flying')[1] == ['dark']
    assert get_color('Bug')[0] == 'green'
    assert get_color('Bug')[1] == ['dark']
    assert get_color('Ghost')[0] == 'grey'
    assert get_color('Ghost')[1] == ['bold']
    assert get_color('Dark')[0] == 'white'
    assert get_color('Dark')[1] == ['dark']
    assert get_color('Dragon')[0] == 'blue'
    assert get_color('Dragon')[1] == ['dark']
    assert get_color('Fairy')[0] == 'magenta'
    assert get_color('Fairy')[1] == ['bold']
    assert get_color('Rock')[0] == 'yellow'
    assert get_color('Rock')[1] == ['bold']
