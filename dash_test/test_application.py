from dash.testing.application_runners import import_app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

'''
Name of test methods always have to start with test_ e.g. test_clickbutton or test_three
Run this test suite using: python -m pytest dash_test
Find set of browser testing APIs and explanation at https://dash.plotly.com/testing
Example tests found online: https://www.programcreek.com/python/example/97707/dash.Dash
'''

def test_home_page_when_starting_app(dash_duo):
    '''
    Test if the home page is correctly loaded without doing anything yet.
    :param dash_duo: dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Verify all elements are loaded.
    dash_duo.wait_for_element("#page-content")
    dash_duo.wait_for_element("#titleLink")
    dash_duo.wait_for_element("#sidebar-toggle")
    dash_duo.wait_for_element("#upload-data")
    dash_duo.wait_for_element("#navlink-home")
    dash_duo.wait_for_element("#navlink-instructions")
    dash_duo.wait_for_element("#navlink-plotting")

    # Verify that elements contain the correct text.
    dash_duo.wait_for_text_to_equal("#page-content", "This is the content of the home page!")
    dash_duo.wait_for_text_to_equal("#titleLink", "Interactive data visualizer")
    dash_duo.wait_for_text_to_equal("#upload-data", "Drag and Drop or Select Files")
    dash_duo.wait_for_text_to_equal("#navlink-home", "Home")
    dash_duo.wait_for_text_to_equal("#navlink-instructions", "Instructions")
    dash_duo.wait_for_text_to_equal("#navlink-plotting", "Plot")

    # Verify that 'home' is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Home"


def test_opening_plotting_tab(dash_duo):
    '''
    Test whether the instruction tabs opens when clicking it
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    # pageContent = dash_duo.driver.find_element_by_id('page-content')
    # assert ("Welcome to the interactive data visualiser" not in pageContent.text)

    # Verify that 'home' is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Home"

    instructionsTab = dash_duo.driver.find_element_by_id("navlink-plotting")
    instructionsTab.click()

    # Verify that after clicking instructions tab, the plotting tab is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Plot"

    # WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "dash-graph")))
    # dash_graph = dash_duo.driver.find_element_by_class_name('dash-graph')
    # assert ("Graph 1" in dash_graph.text)

def test_collapsing_sidebar(dash_duo):
    '''
    Test whether the sidebar collapses when clicking the icon with 3 dashes in it.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)
    sidebarToggler = dash_duo.driver.find_element_by_id("sidebar-toggle")

    sidebarToggler.click()
    sidebar = dash_duo.driver.find_element_by_id("sidebar")
    assert sidebar.get_attribute("class") == "collapsed"

    sidebarToggler.click()
    assert sidebar.get_attribute("class") != "collapsed"

def test_click_titleLink_from_instruction_page(dash_duo):
    '''
    Test whether the application goes back to the home page when clicking the title.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    currentURL = dash_duo.driver.current_url
    plottingURL = currentURL + "instructions"
    dash_duo.driver.get(plottingURL)

    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    text = dash_duo.driver.find_element_by_id('page-content')
    assert(text != "This is the content of the home page!")

    titlelink = dash_duo.driver.find_element_by_id("titleLink")
    titlelink.click()

    assert dash_duo.wait_for_text_to_equal("#page-content", "This is the content of the home page!")

def test_click_titleLink_from_plot_page(dash_duo):
    '''
    Test whether the application goes back to the home page when clicking the title.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    currentURL = dash_duo.driver.current_url
    plottingURL = currentURL + "plotting"
    dash_duo.driver.get(plottingURL)

    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    text = dash_duo.driver.find_element_by_id('page-content')
    assert(text != "This is the content of the home page!")

    titlelink = dash_duo.driver.find_element_by_id("titleLink")
    titlelink.click()

    assert dash_duo.wait_for_text_to_equal("#page-content", "This is the content of the home page!")


def test_opening_instructions_tab(dash_duo):
    '''
    Test whether the instruction tabs opens when clicking it
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    pageContent = dash_duo.driver.find_element_by_id('page-content')
    assert ("Welcome to the interactive data visualiser" not in pageContent.text)

    # Verify that 'home' is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Home"

    instructionsTab = dash_duo.driver.find_element_by_id("navlink-instructions")
    instructionsTab.click()

    # Verify that after clicking instructions tab, the instruction tab is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Instructions"

    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    text = dash_duo.driver.find_element_by_id('page-content')
    assert ("Welcome to the interactive data visualiser" in pageContent.text)



if __name__ == '__main__':
    """"
    Main function to be run
    """
    driver = webdriver.Chrome()
    print("abcdd")
    driver.get("http://127.0.0.1:8050/plotting")




