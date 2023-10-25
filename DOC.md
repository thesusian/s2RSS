# Documentation for s2RSS

## Web-facing APIs

All Web-facing APIs require the user to be logged-in, they are mainly used for functionality in the app

### `/fetch-source [POST]`

Downloads the source of the `address` and returns it in plain texts

**Request**

-   Parameters
    -   `address` the address of the URL to get the source code from, must start with http or https
-   Example

```json
{ "address": "https://thesusian.com" }
```

**Response**

-   Parameters
    -   `source_code` the source code of the URL
-   Example

```json
{ "source_code": "<!DOCTYPE html>\n<html lang=\"en-US\">\n..." }
```

### `/fetch_pattern_result [POST]`

Applies a pattern/filter to the `source_code` and returns a formatted plain-text list of the items found and their elements

**Request**

-   Parameters
    -   `source_code` the source code to extract the items from
    -   `pattern` the pattern/filter to find the desired items from the source
-   Example

```json
{
	"pattern": "<b>{*}",
	"source_code": "<!DOCTYPE html>\n<html lang=\"en-US\">\n..."
}
```

**Response**

-   Parameters
    -   `pattern_result` a plain-text formatted list of the items found and their elements
-   Example

```json
{ "pattern_result": "Item 1:\n{%1}: /\n\nItem 2:\n{%1}: /about..." }
```

### `/fetch_template_result [POST]`

Takes the source-code, the pattern, the template for the title, link, and description of the items and returns a plain-text list of items with their elements formatted according to the template

**Request**

-   Parameters

    -   `pattern` the pattern/filter to find the desired items from the source
    -   `source_code` the source code to extract the items from
    -   `title_item_template` the template for the item element for the RSS feed
    -   `link_item_template` the template for the link element for the RSS feed
    -   `desc_item_template` the template for the description element for the RSS feed

-   Example

```json
{
	"pattern": "<a href=\"{%}\">{%}",
	"source_code": "<!DOCTYPE html>\n<html lang=\"en-US\">...",
	"title_item_template": "{%1}",
	"link_item_template": "{%2}",
	"desc_item_template": "{%3}"
}
```

**Response**

-   Parameters
    -   `template_result` a plain-text formatted list of items with their elements formatted according to the template
-   Example

```json
{"template_result": "Title: /\nLink: \nDesc: \n\nTitle: /about...`}
```

## Helper Functions

Functions within the Python Flask environment, can be found in `app.helpers`

### `get_address_source(str) -> str`

Returns the source code of the requested website URL in plain text

**Parameters**

-   `address` _required_, of type `str`

**Returns**

-   `str` will be empty if URL could not load for any reason

### `get_foramtted_list(str, str) -> str`

Used mainly by `/fetch_pattern_result`, applies a pattern/filter to the `source_code` and returns a formatted plain-text list of the items found and their elements

**Parameters**

-   `source_code` _required_, of type `str`
-   `pattern` _required_, of type `str`

**Returns**

-   `str` will be empty if no matches were found

### `get_json_list(str, str) -> str`

The same output as `get_formatted_list()` but in JSON for easier processing, is called every time someone requests a feed

**Parameters**

-   `source_code` _required_, of type `str`
-   `pattern` _required_, of type `str`

**Returns**

-   `flask.Response()` json, can be used like `list = <output>.json`
