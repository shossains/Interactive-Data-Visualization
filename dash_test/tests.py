from dash.testing.application_runners import import_app


def test_one(dash_duo):
    app = import_app("dash_test.app")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("h1", "HellosadfDash", timeout=4)

def test_two(dash_duo):
    app = import_app("dash_test.app")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("h1", "Hello Dash", timeout=4)


#run using python -m pytest dash_test