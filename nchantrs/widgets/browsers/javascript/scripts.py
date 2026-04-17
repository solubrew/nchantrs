# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


def alert(text=None):
    """"""
    script = """alert("<[text]>")"""
    if text is not None:
        script = script.replace("<[text]>", text)
    return script


def background(color):
    """"""
    script = """
        document.body.style.backgroundColor = "<[color]>";  
    """
    if color is not None:
        script = script.replace("<[color]>", color)
    return script


def button_submit(element=None):
    """"""
    script = """
    try {
        // Locate the element using the given XPath
        const xpath = "<[element]>";
        const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        const submitButton = result.singleNodeValue; // Get the first node from the evaluation
        if (submitButton) {
            // Simulate a click event on the submit button
            submitButton.click();
            console.log("Submit button was successfully clicked.");
        } else {
            console.error("Submit button not found with the given XPath.");
        }
    } catch (error) {
        console.error("An error occurred while triggering the submit button:", error);
    }
    """
    if element is not None:
        script = script.replace("<[element]>", element)
    return script


def event_listener_middle_click():
    """"""
    script = """
    document.body.addEventListener("mousedown", function(event) {
        if (event.button === 1) {  // Middle mouse button
            let element = event.target.closest("a[href]");
            if (element) {
                console.log("middleClick:" + element.href);  // Send URL to Python
                event.preventDefault();  // Prevent default middle-click behavior
            }
        }
    });
    """
    return script


def extract_images():
    """"""
    script = """"""
    script = script.replace("<[text]>", text)
    return script


def extract_table():
    """"""
    script = """"""
    script = script.replace("<[text]>", text)
    return script


def extract_text():
    """"""
    script = """"""
    script = script.replace("<[text]>", text)
    return script


def find(field):
    """"""
    script = """
        try {
            const <[field]>Input = document.querySelector("input[name='<[field]>']");
        } catch (error) {
            console.error("Error finding name", error);
        }
    """
    script = script.replace("<[field]>", field)
    return script


def find_all(field):
    """"""
    script = """
        try {
            const <[field]>Input = document.querySelectorAll("input[name='<[field]>']");
        } catch (error) {
            console.error("Error finding name", error);
        }
    """
    script = script.replace("<[field]>", field)
    return script


def find_name():
    """"""
    script = """
    try {
        const nameInput = document.querySelector("input[name='name']");
    } catch (error) {
        console.error("Error finding name", error);
    }
    """
    return script


def find_phone():
    """"""
    script = """
    try {
        const nameInput = document.querySelector("input[name='name']");
    } catch (error) {
        console.error("Error finding name", error);
    }
    """
    return script


def find_street():
    """"""
    script = """
    try {
        const nameInput = document.querySelector("input[name='name']");
    } catch (error) {
        console.error("Error finding name", error);
    }
    """
    return script


def find_state():
    """"""
    script = """
    try {
        const nameInput = document.querySelector("input[name='name']");
    } catch (error) {
        console.error("Error finding name", error);
    }
    """
    return script


def find_zipcode():
    """"""
    script = """
    try {
        const nameInput = document.querySelector("input[name='name']");
    } catch (error) {
        console.error("Error finding name", error);
    }
    """
    return script


def inject_script():
    """"""
    script = """
    const script = document.createElement("script");
    script.src = "https://example.com/your-script.js"; // Replace with your script URL
    document.head.appendChild(script);
    """
    script = script.replace("<[text]>", text)
    return script


def rich_text_area_insert(element=None, text=None):
    """"""
    script = """
    try {
        var xpath = '<[element]>';
        var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        var richTextarea = result.singleNodeValue;
        if (richTextarea) {
            // Step 3: Create TrustedHTML and assign it to `innerHTML`
            const message = "<[text]>";       
            if (window.trustedTypes && window.trustedTypes.createPolicy) {
                // Create a TrustedHTML policy if the API is available
                const policy = trustedTypes.createPolicy("myPolicy", {
                    createHTML: (html) => html
                });
                // Use the created policy to generate TrustedHTML
                const trustedHTML = policy.createHTML(message);
                richTextarea.innerHTML = trustedHTML; // Assign TrustedHTML
            } else {
                // For browsers without Trusted Types (fallback, though might still fail)
                richTextarea.innerHTML = message;
            }
            // Dispatch necessary events to notify the application
            richTextarea.dispatchEvent(new Event('input', { bubbles: true }));
            richTextarea.dispatchEvent(new Event('change', { bubbles: true }));
        } else {
            console.error("Element not found! Please verify the XPath.");
        }
    } catch (error) {
        // Log any errors encountered during the injection
        console.error("An error occurred during JavaScript injection:", error);
    }
    """
    if element is not None:
        script = script.replace("<[element]>", element)
    if text is not None:
        script = script.replace("<[text]>", text)
    return script


def scroll_page():
    """"""
    script = """
    try {
        const target = document.querySelector("TARGET_SELECTOR");
        if (target) {
            target.scrollIntoView({ behavior: "smooth" });
        } else {
            console.error("Element not found");
        }
    } catch (error) {
        console.error("Error scrolling to element:", error);
    }
    """
    script = script.replace("<[text]>", text)
    return script


def text_area_insert(element=None, text=None):
    """"""
    script = """
    var xpath = '<[element]>';
    var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    var textarea = result.singleNodeValue;  // Get the textarea element
    if (textarea) {
        textarea.focus();  // Focus the element        
        // Simulate typing by dispatching keyboard events
        textarea.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, cancelable: true, key: 'a' }));
        textarea.dispatchEvent(new KeyboardEvent('keypress', { bubbles: true, cancelable: true, key: 'a' }));
        textarea.value = "<[text]>";  // Set the value programmatically
        textarea.dispatchEvent(new Event('input', { bubbles: true }));  // Trigger input event
        textarea.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true, cancelable: true, key: 'a' }));
        // Optionally blur the element if needed
        textarea.blur();
    }    
    """
    if element is not None:
        script = script.replace("<[element]>", element)
    if text is not None:
        script = script.replace("<[text]>", text)
    return script


def media_pause():
    """"""
    script = """
    (() => {
      try {
        const elems = [...document.querySelectorAll('video, audio')];
        elems.forEach(m => {
          try {
            // If it's playing, pause it
            if (!m.paused && !m.ended) m.pause();
            // Avoid CPU drain on hidden tabs
            m.autoplay = false;
          } catch(e) {}
        });
        return elems.length;
      } catch(_) { return -1; }
    })();
    """
    return script


def media_play():
    """"""
    script = """
    (() => {
      try {
        const elems = [...document.querySelectorAll('video, audio')];
        // Only resume those that were intended to play via autoplay attribute or have 'data-should-play'
        elems.forEach(m => {
          try {
            if (m.getAttribute('data-should-play') === '1') m.play().catch(()=>{});
          } catch(e) {}
        });
        return elems.length;
      } catch(_) { return -1; }
    })();
    """
    return script


def media_mark_intent_to_play():
    """"""
    script = """
    (() => {
      try {
        const elems = [...document.querySelectorAll('video, audio')];
        elems.forEach(m => {
          // Mark items that had autoplay so we can selectively resume
          if (m.autoplay) m.setAttribute('data-should-play', '1');
          // Disable autoplay globally
          m.autoplay = false;
        });
        return elems.length;
      } catch(_) { return -1; }
    })();
    """
    return script


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
