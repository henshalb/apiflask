import pytest


def test_docs_favicon(app, client):
    app.config['DOCS_FAVICON'] = '/my-favicon.png'

    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b'href="/my-favicon.png"' in rv.data


@pytest.mark.parametrize('config_value', [True, False])
def test_docs_use_google_font(app, client, config_value):
    app.config['REDOC_USE_GOOGLE_FONT'] = config_value

    rv = client.get('/redoc')
    assert rv.status_code == 200
    assert bool(b'fonts.googleapis.com' in rv.data) is config_value


def test_redoc_standalone_js(app, client):
    app.config['REDOC_STANDALONE_JS'] = 'https://cdn.example.com/redoc.js'

    rv = client.get('/redoc')
    assert rv.status_code == 200
    assert b'src="https://cdn.example.com/redoc.js"' in rv.data


def test_swagger_ui_resources(app, client):
    app.config['SWAGGER_UI_CSS'] = 'https://cdn.example.com/swagger-ui.css'
    app.config['SWAGGER_UI_BUNDLE_JS'] = 'https://cdn.example.com/swagger-ui.bundle.js'
    app.config['SWAGGER_UI_STANDALONE_PRESET_JS'] = \
        'https://cdn.example.com/swagger-ui.preset.js'

    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b'href="https://cdn.example.com/swagger-ui.css"' in rv.data
    assert b'src="https://cdn.example.com/swagger-ui.bundle.js"' in rv.data
    assert b'src="https://cdn.example.com/swagger-ui.preset.js"' in rv.data


def test_swagger_ui_layout(app, client):
    app.config['SWAGGER_UI_LAYOUT'] = 'StandaloneLayout'

    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b'StandaloneLayout' in rv.data
    assert b'BaseLayout' not in rv.data


def test_swagger_ui_config(app, client):
    app.config['SWAGGER_UI_CONFIG'] = {
        'deepLinking': False,
        'layout': 'StandaloneLayout'
    }

    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b'"deepLinking": false' in rv.data
    assert b'"layout": "StandaloneLayout"' in rv.data


def test_swagger_ui_oauth_config(app, client):
    app.config['SWAGGER_UI_OAUTH_CONFIG'] = {
        'clientId': 'foo',
        'usePkceWithAuthorizationCodeGrant': True
    }

    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b'ui.initOAuth(' in rv.data
    assert b'"clientId": "foo"' in rv.data
    assert b'"usePkceWithAuthorizationCodeGrant": true' in rv.data
