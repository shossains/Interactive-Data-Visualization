import os
from selenium.webdriver.support.ui import Select

from dash.testing.application_runners import import_app
from selenium import webdriver
from selenium import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



'''
Name of test methods always have to start with test_ e.g. test_clickbutton or test_three
Run this test suite using: python -m pytest dash_test while having the Main.py running
Find set of browser testing APIs and explanation at https://dash.plotly.com/testing
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

def test_collapsing_sidebar(dash_duo):
    '''
    Test whether the sidebar collapses when clicking the icon with 3 dashes in it.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)
    sidebarToggler = dash_duo.driver.find_element_by_id("sidebar-toggle")

    #Click the toggle sidebar to collapse it
    sidebarToggler.click()
    sidebar = dash_duo.driver.find_element_by_id("sidebar")
    assert sidebar.get_attribute("class") == "collapsed"

    sidebarToggler.click()
    assert sidebar.get_attribute("class") != "collapsed"
#

# def test_click_titleLink_from_home_page(dash_duo):
#     '''
#     Test whether the application goes back to the home page when clicking the title from the home page.
#     :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
#     '''
#     app = import_app("src.main.python.oop.Main")
#     dash_duo.start_server(app)
#
#     currentURL = dash_duo.driver.current_url
#     dash_duo.driver.get(currentURL)
#
#     #Verify home page is open
#     page_content = WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
#     assert(page_content.text == "This is the content of the home page!")
#
#     #click titlelink which redirects to home page
#     titlelink = dash_duo.driver.find_element_by_id("titleLink")
#     titlelink.click()
#
#     #Verify home page is still open
#     assert dash_duo.wait_for_text_to_equal("#page-content", "This is the content of the home page!")


def test_click_titleLink_from_instruction_page(dash_duo):
    '''
    Test whether the application goes back to the home page when clicking the title from the instructions page.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to instructions page
    currentURL = dash_duo.driver.current_url
    instructionURL = currentURL + "instructions"
    dash_duo.driver.get(instructionURL)

    # Verify home page is not open
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    text = dash_duo.driver.find_element_by_id('page-content')
    assert(text != "This is the content of the home page!")

    # Click titlelink which redirects to home page
    titlelink = dash_duo.driver.find_element_by_id("titleLink")
    titlelink.click()

    # Verify home page is open
    assert dash_duo.wait_for_text_to_equal("#page-content", "This is the content of the home page!")

def test_click_titleLink_from_plot_page(dash_duo):
    '''
    Test whether the application goes back to the home page when clicking the title from the plotting page.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    currentURL = dash_duo.driver.current_url
    plottingURL = currentURL + "plotting"
    dash_duo.driver.get(plottingURL)

    # Home page is not open
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    text = dash_duo.driver.find_element_by_id('page-content')
    assert(text != "This is the content of the home page!")

    # Click titlelink which redirects to home page
    titlelink = dash_duo.driver.find_element_by_id("titleLink")
    titlelink.click()

    assert dash_duo.wait_for_text_to_equal("#page-content", "This is the content of the home page!")


def test_opening_instructions_tab(dash_duo):
    '''
    Test whether the instruction tab opens when clicking it
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Not in instructions page
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    pageContent = dash_duo.driver.find_element_by_id('page-content')
    assert ("Welcome to the interactive data visualiser" not in pageContent.text)

    # Verify that 'home' is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Home"

    # To go to the instructions page
    instructionsTab = dash_duo.driver.find_element_by_id("navlink-instructions")
    instructionsTab.click()

    # Verify that after clicking instructions tab, the instruction tab is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Instructions"

    # In the instructions page
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    assert ("Welcome to the interactive data visualiser" in pageContent.text)

def test_opening_plotting_tab(dash_duo):
    '''
    Test whether the plotting tab opens when clicking it
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Not in plotting page
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    pageContent = dash_duo.driver.find_element_by_id('page-content')
    assert ("Welcome to the interactive data visualiser" not in pageContent.text)

    # Verify that 'home' is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Home"

    # To go to the instructions page
    plottingTab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plottingTab.click()

    # Verify that after clicking plotting tab, the plotting tab is the selected tab.
    activeNavLink = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert activeNavLink.text == "Plot"

    # In the plotting page
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "dash-graph")))
    dash_graph = dash_duo.driver.find_element_by_class_name('dash-graph')
    assert ("Graph 1" in dash_graph.text)

def test_file_insertion(dash_duo):
    '''
    Test whether inserted files appear in dropdown menus
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plottingTab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plottingTab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    inputFile = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    inputFile.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Verify that data.csv is selected in dropdown
    selectedFile = WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "react-select-3--value-0")))
    assert "data.csv" in str(selectedFile.text)

def test_setting_x_axis(dash_duo):
    '''
    Test whether the x-axis of the graph gets setted properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plottingTab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plottingTab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    inputFile = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    inputFile.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Select x-axis value in dropdown
    x_axis = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-variable-x-normal-plot']")))
    x_axis.send_keys("column1")
    x_axis.send_keys(Keys.ENTER);

    # Verify that 'column1' is a selected dropdown value
    WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "Select-value-label")))
    allSelectedDropdownValues = dash_duo.driver.find_elements_by_class_name("Select-value-label")
    listOfNames = []
    for i in range(len(allSelectedDropdownValues)):
        listOfNames = listOfNames + [allSelectedDropdownValues[i].text]

    assert "column1" in listOfNames

def test_setting_y_axis(dash_duo):
    '''
    Test whether the x-axis of the graph gets setted properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plottingTab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plottingTab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    inputFile = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    inputFile.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Select x-axis value in dropdown
    y_axis = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-variable-y-normal-plot']")))
    y_axis.send_keys("column2")
    y_axis.send_keys(Keys.ENTER);

    # Verify that 'column2' is a selected dropdown value
    WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "Select-value-label")))
    allSelectedDropdownValues = dash_duo.driver.find_elements_by_class_name("Select-value-label")
    listOfNames = []
    for i in range(len(allSelectedDropdownValues)):
        listOfNames = listOfNames + [allSelectedDropdownValues[i].text]

    assert "column2" in listOfNames

def test_setting_color(dash_duo):
    '''
    Test whether the color of the graph gets setted properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plottingTab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plottingTab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    inputFile = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    inputFile.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Select color value in dropdown
    color = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-characteristics-normal-plot']")))
    color.send_keys("No color")
    color.send_keys(Keys.ENTER);

    # Verify that 'No color' is a selected dropdown value
    WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "Select-value-label")))
    allSelectedDropdownValues = dash_duo.driver.find_elements_by_class_name("Select-value-label")
    listOfNames = []
    for i in range(len(allSelectedDropdownValues)):
        listOfNames = listOfNames + [allSelectedDropdownValues[i].text]

    assert "No color" in listOfNames


def test_plotting_on_multiple_graphs(dash_duo):
    '''
    Test to plot multiple graphs
    Note: If no errors occur, this test is probably working. To completely verify this test is working, check the actual generated graphs.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotTab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotTab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    inputFile = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    inputFile.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Select x-axis
    x_axis = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-variable-x-normal-plot']")))
    x_axis.send_keys("column1")
    x_axis.send_keys(Keys.ENTER);

    # Select y-axis
    y_axis = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-variable-y-normal-plot']")))
    y_axis.send_keys("column2")
    y_axis.send_keys(Keys.ENTER);

    # Select color
    color = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-characteristics-normal-plot']")))
    color.send_keys("No color")
    color.send_keys(Keys.ENTER);

    # Plot graph on graph 1
    graph_1_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 1']")
    graph_1_button.click()

    # Select another color
    color.send_keys("column1")
    color.send_keys(Keys.ENTER);

    # Plot graph with another color on graph 2
    graph_2_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 2']")
    graph_2_button.click()

    # Select another x-axis
    x_axis.send_keys("column2")
    x_axis.send_keys(Keys.ENTER);

    # Plot graph with another x-axis on graph 3
    graph_3_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 3']")
    graph_3_button.click()

    import time
    time.sleep(5)

if __name__ == '__main__':
    """"
    Main function to be run
    """
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:8050/plotting")
















