import os

from dash.testing.application_runners import import_app
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

'''
Name of test methods always have to start with test_ e.g. test_clickbutton or test_three
Run this test suite using: python -m pytest dash_test while having the Main.py running and debug mode on false.
To run these tests, selenium and any web driver are required (ChromeDriver / GeckoDriver) 
Find set of browser testing APIs and explanation at https://dash.plotly.com/testing
'''


def test_home_page_when_starting_app(dash_duo):
    """
    Test if the home page is correctly loaded without doing anything yet.
    :param dash_duo: dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs
    and Python Selenium API
    """
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
    dash_duo.wait_for_contains_text("#page-content", "Welcome to the interactive data visualiser")
    dash_duo.wait_for_text_to_equal("#titleLink", "Interactive data visualizer")
    dash_duo.wait_for_text_to_equal("#upload-data", "Drag and Drop or Select Files")
    dash_duo.wait_for_text_to_equal("#navlink-home", "Home")
    dash_duo.wait_for_text_to_equal("#navlink-instructions", "Instructions")
    dash_duo.wait_for_text_to_equal("#navlink-plotting", "Plot")

    # Verify that 'home' is the selected tab.
    active_nav_link = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert active_nav_link.text == "Home"

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_collapsing_sidebar(dash_duo):
    """
    Test whether the sidebar collapses when clicking the icon with 3 dashes in it.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)
    sidebar_toggler = dash_duo.driver.find_element_by_id("sidebar-toggle")

    #Click the toggle sidebar to collapse it
    sidebar_toggler.click()
    sidebar = dash_duo.driver.find_element_by_id("sidebar")
    assert sidebar.get_attribute("class") == "collapsed"

    sidebar_toggler.click()
    assert sidebar.get_attribute("class") != "collapsed"

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_click_title_link_from_home_page(dash_duo):
    """
    Test whether the application stays on the home page when clicking the title from the home page.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    currentURL = dash_duo.driver.current_url
    dash_duo.driver.get(currentURL)

    #Verify home page is open
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    dash_duo.wait_for_contains_text("#page-content", "Welcome to the interactive data visualiser")

    #click titlelink which redirects to home page
    title_link = dash_duo.driver.find_element_by_id("titleLink")
    title_link.click()

    #Verify home page is still open
    dash_duo.wait_for_contains_text("#page-content", "Welcome to the interactive data visualiser")

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_click_title_link_from_instruction_page(dash_duo):
    """
    Test whether the application goes back to the home page when clicking the title from the instructions page.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
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
    title_link = dash_duo.driver.find_element_by_id("titleLink")
    title_link.click()

    # Verify home page is open
    assert dash_duo.wait_for_contains_text("#page-content", "Welcome to the interactive data visualiser")

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_click_title_link_from_plot_page(dash_duo):
    """
    Test whether the application goes back to the home page when clicking the title from the plotting page.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
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

    # Click title link which redirects to home page
    title_link = dash_duo.driver.find_element_by_id("titleLink")
    title_link.click()

    # Verify home page is open
    assert dash_duo.wait_for_contains_text("#page-content", "Welcome to the interactive data visualiser")

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_opening_instructions_tab(dash_duo):
    """
    Test whether the instruction tab opens when clicking it
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Not in instructions page
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    page_content = dash_duo.driver.find_element_by_id('page-content')
    assert ("Instructions" not in page_content.text)

    # Verify that 'home' is the selected tab.
    active_nav_link = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert active_nav_link.text == "Home"

    # To go to the instructions page
    instructions_tab = dash_duo.driver.find_element_by_id("navlink-instructions")
    instructions_tab.click()

    # Verify that after clicking instructions tab, the instruction tab is the selected tab.
    active_nav_link = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert active_nav_link.text == "Instructions"

    # In the instructions page
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    assert ("Instructions" in page_content.text)

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_opening_plotting_tab(dash_duo):
    """
    Test whether the plotting tab opens when clicking it
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Not in plotting page
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "page-content")))
    page_content = dash_duo.driver.find_element_by_id('page-content')
    assert ("Plot" not in page_content.text)

    # Verify that 'home' is the selected tab.
    active_nav_link = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert active_nav_link.text == "Home"

    # To go to the plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Verify that after clicking plotting tab, the plotting tab is the selected tab.
    active_nav_link = dash_duo.driver.find_element_by_css_selector(".nav-link.active")
    assert active_nav_link.text == "Plot"

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_file_insertion(dash_duo):
    """
    Test whether inserted files appear in dropdown menus
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Verify that data.csv is selected in dropdown
    selected_file = WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "react-select-3--value-0")))
    assert "data.csv" in str(selected_file.text)

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_not_supported_file_insertion(dash_duo):
    """
    Test whether appears when uploading wrong file type.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Assert that no errors have occured before uploading wrong file.
    assert len(dash_duo.driver.get_log('browser')) == 0

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/png_test.png')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='select-file']")))
    select_file_dropdown.send_keys("png_test.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Assert that errors have occurred after uploading wrong file.
    assert len(dash_duo.driver.get_log('browser')) != 0


def test_setting_x_axis(dash_duo):
    """
    Test whether the x-axis of the graph gets setted properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

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
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-value-label")
    list_of_names = []
    for i in range(len(all_setted_dropdown_values)):
        list_of_names = list_of_names + [all_setted_dropdown_values[i].text]

    assert "column1" in list_of_names

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_setting_y_axis(dash_duo):
    """
    Test whether the y-axis of the graph gets setted properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

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
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-value-label")
    list_of_names = []
    for i in range(len(all_setted_dropdown_values)):
        list_of_names = list_of_names + [all_setted_dropdown_values[i].text]

    assert "column2" in list_of_names

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_setting_color(dash_duo):
    """
    Test whether the color of the graph gets setted properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

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
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-value-label")
    listOfNames = []
    for i in range(len(all_setted_dropdown_values)):
        listOfNames = listOfNames + [all_setted_dropdown_values[i].text]

    assert "No color" in listOfNames

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_all_plot_methods(dash_duo):
    """
    Test all different plot methods.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Select x-axis
    x_axis = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-variable-x-normal-plot']")))
    x_axis.send_keys("column1")
    x_axis.send_keys(Keys.ENTER);

    # Select y-axis
    y_axis = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-variable-y-normal-plot']")))
    y_axis.send_keys("column2")
    y_axis.send_keys(Keys.ENTER);

    # Select color
    color = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-characteristics-normal-plot']")))
    color.send_keys("No color")
    color.send_keys(Keys.ENTER);

    # Select plot
    select_plot = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-plot-options-normal-plot']")))

    # All plot methods that are available
    plot_methods = ["Area", "Bar", "Box", "Density", "Histogram", "Line", "Scatter"]

    for plot_method in plot_methods:
        # Select different plot methods
        select_plot.send_keys(plot_method)
        select_plot.send_keys(Keys.ENTER)

        # Plot graph on graph 1
        graph_1_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 1']")
        graph_1_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_apply_filter(dash_duo):
    """
    Test whether filters are applied correctly
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # find add filter button
    add_filter_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "add-filter-button")))
    add_filter_button.click()

    # Its hard to find dynamic created dropdown menus, therefore the dropdown menus are retrieved in another way
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-input")

    # Set filter values
    filter_select_column = all_setted_dropdown_values[len(all_setted_dropdown_values) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column1")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = all_setted_dropdown_values[len(all_setted_dropdown_values) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys(">")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(2)
    input_value.send_keys(Keys.ENTER);

    apply_button = dash_duo.driver.find_element_by_id("apply-filter-button")
    apply_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_apply_multiple_filters(dash_duo):
    """
    Test whether multiple filters are applied correctly
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Find add filter button
    add_filter_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "add-filter-button")))
    add_filter_button.click()

    # Its hard to find dynamic created dropdown menus, therefore the dropdown menus are retrieved in another way
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-input")

    # Set filter values
    filter_select_column = all_setted_dropdown_values[len(all_setted_dropdown_values) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column1")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = all_setted_dropdown_values[len(all_setted_dropdown_values) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys(">")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(2)
    input_value.send_keys(Keys.ENTER);

    # Create new filters and set the values of those filters
    add_filter_button.click()
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-input")
    filter_select_column = all_setted_dropdown_values[len(all_setted_dropdown_values) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column2")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = all_setted_dropdown_values[len(all_setted_dropdown_values) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys("<")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(8)
    input_value.send_keys(Keys.ENTER);

    add_filter_button.click()
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-input")

    filter_select_column = all_setted_dropdown_values[len(all_setted_dropdown_values) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column2")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = all_setted_dropdown_values[len(all_setted_dropdown_values) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys("!=")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(4)
    input_value.send_keys(Keys.ENTER);

    apply_button = dash_duo.driver.find_element_by_id("apply-filter-button")
    apply_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_applying_none_filter(dash_duo):
    """
    Test that nothing happens when a filter without values is applied.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Apply filters.
    apply_button = dash_duo.driver.find_element_by_id("apply-filter-button")
    apply_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0

def test_remove_filter(dash_duo):
    """
    Test whether a filter is correctly removed.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    add_filter_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "add-filter-button")))
    add_filter_button.click()

    all_remove_filter_buttons = dash_duo.driver.find_elements_by_class_name("remove-filter")
    all_remove_filter_buttons[len(all_remove_filter_buttons)-1].click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_remove_multiple_filters(dash_duo):
    """
    Test whether multiple filters are correctly removed.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    # Add and remove filters
    add_filter_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "add-filter-button")))
    add_filter_button.click()
    add_filter_button.click()
    add_filter_button.click()

    all_remove_filter_buttons = dash_duo.driver.find_elements_by_class_name("remove-filter")
    all_remove_filter_buttons[len(all_remove_filter_buttons) - 1].click()
    all_remove_filter_buttons[len(all_remove_filter_buttons) - 2].click()
    all_remove_filter_buttons[len(all_remove_filter_buttons) - 3].click()

    assert len(dash_duo.driver.get_log('browser')) == 0


def test_client_code_button(dash_duo):
    """
    Test whether the client code button works properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Click the example function button
    example_function_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "example-function-1-button")))
    example_function_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_reset_to_original_data(dash_duo):
    """
    Test whether the reset to original data button works properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Click the reset to original data button
    reset_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "reset-button")))
    reset_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_reset_to_original_data_after_filters(dash_duo):
    """
    Test whether the reset to original data button works properly after filters have been applied.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Upload .csv file
    WebDriverWait(dash_duo.driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data")))
    path = os.path.abspath('dash_test/data.csv')
    input_file = dash_duo.driver.find_element_by_xpath("//div[@id='upload-data']/div/input")
    input_file.send_keys(path)

    # Select data.csv file in dropdown
    select_file_dropdown = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-file']")))
    select_file_dropdown.send_keys("data.csv")
    select_file_dropdown.send_keys(Keys.ENTER);

    add_filter_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "add-filter-button")))
    add_filter_button.click()

    # Its hard to find dynamic created dropdown menus, therefore the dropdown menus are retrieved in another way
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-input")

    # Set values for multiple filters
    filter_select_column = all_setted_dropdown_values[len(all_setted_dropdown_values) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column1")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = all_setted_dropdown_values[len(all_setted_dropdown_values) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys(">")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(2)
    input_value.send_keys(Keys.ENTER);

    add_filter_button.click()
    allSelectedDropdownValues = dash_duo.driver.find_elements_by_class_name("Select-input")
    filter_select_column = allSelectedDropdownValues[len(allSelectedDropdownValues) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column2")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = allSelectedDropdownValues[len(allSelectedDropdownValues) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys("<")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(8)
    input_value.send_keys(Keys.ENTER);

    add_filter_button.click()
    allSelectedDropdownValues = dash_duo.driver.find_elements_by_class_name("Select-input")

    filter_select_column = allSelectedDropdownValues[len(allSelectedDropdownValues) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column2")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = allSelectedDropdownValues[len(allSelectedDropdownValues) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys("!=")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(4)
    input_value.send_keys(Keys.ENTER);

    # Apply multiple filters
    apply_button = dash_duo.driver.find_element_by_id("apply-filter-button")
    apply_button.click()

    # Click reset button
    reset_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "reset-button")))
    reset_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_addition_of_multiple_graphs(dash_duo):
    """
    Test whether the addition of multiple graphs works properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Add multiple graphs
    add_graph = dash_duo.driver.find_element_by_id("add-graph")
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_removal_of_multiple_graphs(dash_duo):
    """
    Test whether the deletion of multiple graphs works properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    # Delete multiple graphs
    remove_graph = dash_duo.driver.find_element_by_id("remove-graph")
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_removal_and_addition_of_multiple_graphs(dash_duo):
    """
    Test whether the addition and deletion combined of multiple graphs works properly.
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    """
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

    add_graph = dash_duo.driver.find_element_by_id("add-graph")
    remove_graph = dash_duo.driver.find_element_by_id("remove-graph")

    # Add and delete multiple graphs
    add_graph.click()
    add_graph.click()
    add_graph.click()
    remove_graph.click()
    add_graph.click()
    remove_graph.click()
    remove_graph.click()
    add_graph.click()
    remove_graph.click()
    remove_graph.click()
    remove_graph.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0


def test_entire_application(dash_duo):
    '''
    Tests the entire application
    Note: If no errors occur, this test is probably working. To completely verify this test is working, uncomment
    the sleep at the end of this test and verify by eye whether the generated graphs are correct
    :param dash_duo: Standalone WebDriver with access to both the high-level Dash testing APIs and Python Selenium API
    '''
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)

    # Go to plotting page
    plotting_tab = dash_duo.driver.find_element_by_id("navlink-plotting")
    plotting_tab.click()

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

    # Select plot
    plot_method = WebDriverWait(dash_duo.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='select-plot-options-normal-plot']")))

    # Plot graph on graph 1
    graph_1_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 1']")
    graph_1_button.click()

    # Select another color
    color.send_keys("column1")
    color.send_keys(Keys.ENTER);

    # Plot graph with another color on graph 2
    graph_2_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 2']")
    graph_2_button.click()

    # Select another plot method
    plot_method.send_keys("Density")
    plot_method.send_keys(Keys.ENTER)

    # Select no color
    color.send_keys("No color")
    color.send_keys(Keys.ENTER);

    # Plot graph with another x-axis and another graph kind on graph 3
    graph_3_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 3']")
    graph_3_button.click()

    # Add 4 graphs
    add_graph = dash_duo.driver.find_element_by_id("add-graph")
    add_graph.click()
    add_graph.click()
    add_graph.click()
    add_graph.click()

    # Add filters, apply filters, and plot the modified dataframes
    add_filter_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "add-filter-button")))
    add_filter_button.click()

    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-input")
    filter_select_column = all_setted_dropdown_values[len(all_setted_dropdown_values) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column2")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = all_setted_dropdown_values[len(all_setted_dropdown_values) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys(">")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(-20)
    input_value.send_keys(Keys.ENTER);

    apply_button = dash_duo.driver.find_element_by_id("apply-filter-button")
    apply_button.click()

    # Select another plot method
    plot_method.send_keys("Scatter")
    plot_method.send_keys(Keys.ENTER)

    graph_4_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 4']")
    graph_4_button.click()

    add_filter_button.click()
    time.sleep(1)
    all_setted_dropdown_values = dash_duo.driver.find_elements_by_class_name("Select-input")

    filter_select_column = all_setted_dropdown_values[len(all_setted_dropdown_values) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column2")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = all_setted_dropdown_values[len(all_setted_dropdown_values) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys("<")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(5)
    input_value.send_keys(Keys.ENTER);

    apply_button.click()

    graph_5_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 5']")
    graph_5_button.click()

    add_filter_button.click()
    time.sleep(1)
    allSelectedDropdownValues = dash_duo.driver.find_elements_by_class_name("Select-input")

    filter_select_column = allSelectedDropdownValues[len(allSelectedDropdownValues) - 2].find_element_by_xpath("input")
    filter_select_column.send_keys("column2")
    filter_select_column.send_keys(Keys.ENTER);

    filter_select_greater = allSelectedDropdownValues[len(allSelectedDropdownValues) - 1].find_element_by_xpath("input")
    filter_select_greater.send_keys("!=")
    filter_select_greater.send_keys(Keys.ENTER);

    all_input_values = dash_duo.driver.find_elements_by_class_name("filter-input")
    input_value = all_input_values[len(all_input_values) - 1]
    input_value.send_keys(0)
    input_value.send_keys(Keys.ENTER);

    apply_button.click()

    graph_6_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 6']")
    graph_6_button.click()

    # Reset data frame and plot
    reset_button = WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.ID, "reset-button")))
    reset_button.click()

    graph_7_button = dash_duo.driver.find_element_by_xpath("//*[text()='Graph 7']")
    graph_7_button.click()

    # Browser should not contain errors
    assert len(dash_duo.driver.get_log('browser')) == 0














