from dash.testing.application_runners import import_app

'''
Name of test methods always have to start with test_ e.g. test_clickbutton or test_three
Run this test suite using: python -m pytest dash_test
Find set of browser testing APIs and explanation at https://dash.plotly.com/testing
'''

def test_home_page_loaded(dash_duo):
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#page-content", "This is the content of the home page!", timeout=5)

def test_title_appearance(dash_duo):
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#titleLink", "Interactive data visualizer", timeout=5)

def test_title_appearance(dash_duo):
    app = import_app("src.main.python.oop.Main")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#titleLink", "Interactive data visualizer", timeout=5)

