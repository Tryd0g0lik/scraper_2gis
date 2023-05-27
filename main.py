# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

from scraper_gis import Gis_page as Gp


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':

if __name__ == "__main__":
    map = Gp(sity="novosibirsk", search_word="церкви")
    map.scrap_gi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
