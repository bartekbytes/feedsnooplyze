import pytest
from bs4 import BeautifulSoup
from feedsnooplyze.parser.generic_parsers import AllDocumentParser
from feedsnooplyze.parser.generic_parsers import DivClassParser
from feedsnooplyze.parser.generic_parsers import MainElementParser

@pytest.fixture
def parser():
    return AllDocumentParser()

def test_parse_returns_body_tag_when_present(parser):
    html = "<html><body><p>Hello World</p></body></html>"
    result = parser.parse(html)
    assert isinstance(result, BeautifulSoup().body.__class__)
    assert result.name == "body"
    assert "Hello World" in result.text

def test_parse_returns_none_when_body_missing(parser):
    html = "<html><head><title>No Body</title></head></html>"
    result = parser.parse(html)
    assert result is None

def test_parse_returns_body_with_attributes(parser):
    html = '<html><body id="main-body">Content</body></html>'
    result = parser.parse(html)
    assert result is not None
    assert result.get("id") == "main-body"
    assert "Content" in result.text

def test_parse_handles_empty_string(parser):
    html = ""
    result = parser.parse(html)
    assert result is None

def test_parse_handles_malformed_html(parser):
    html = "<html><body><p>Unclosed tag"
    result = parser.parse(html)
    assert result is not None
    assert "Unclosed tag" in result.text
    
@pytest.fixture
def parser():
    return DivClassParser(class_name="target-class")

def test_parse_returns_div_with_class(parser):
    html = '<div class="target-class">Hello</div>'
    result = parser.parse(html)
    assert result is not None
    assert result.name == "div"
    assert "Hello" in result.text
    assert "target-class" in result.get("class", [])

def test_parse_returns_none_if_class_not_found(parser):
    html = '<div class="other-class">Hello</div>'
    result = parser.parse(html)
    assert result is None

def test_parse_returns_first_div_with_class(parser):
    html = '''
        <div class="target-class">First</div>
        <div class="target-class">Second</div>
    '''
    result = parser.parse(html)
    assert result is not None
    assert "First" in result.text

def test_parse_returns_none_if_no_div(parser):
    html = '<span class="target-class">Not a div</span>'
    result = parser.parse(html)
    assert result is None

def test_parse_handles_empty_string(parser):
    html = ''
    result = parser.parse(html)
    assert result is None

def test_parse_handles_malformed_html(parser):
    html = '<div class="target-class">Unclosed'
    result = parser.parse(html)
    assert result is not None
    assert "Unclosed" in result.text
    
@pytest.fixture
def main_parser():
    return MainElementParser()

def test_parse_returns_main_tag_when_present(main_parser):
    html = "<html><body><main><p>Main Content</p></main></body></html>"
    result = main_parser.parse(html)
    assert result is not None
    assert result.name == "main"
    assert "Main Content" in result.text

def test_parse_returns_none_when_main_missing(main_parser):
    html = "<html><body><div>No Main</div></body></html>"
    result = main_parser.parse(html)
    assert result is None

def test_parse_returns_main_with_attributes(main_parser):
    html = '<main id="main-section" class="main-class">Content</main>'
    result = main_parser.parse(html)
    assert result is not None
    assert result.get("id") == "main-section"
    assert "main-class" in result.get("class", [])
    assert "Content" in result.text

def test_parse_handles_empty_string(main_parser):
    html = ""
    result = main_parser.parse(html)
    assert result is None

def test_parse_handles_malformed_html(main_parser):
    html = "<main><p>Unclosed tag"
    result = main_parser.parse(html)
    assert result is not None
    assert "Unclosed tag" in result.text

