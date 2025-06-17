document.getElementById("readBtn").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    if (currentTab && currentTab.id) {
      chrome.scripting.executeScript({
        target: { tabId: currentTab.id },
        function: readSelectedText
      });
    } else {
      alert("Could not get current tab.");
    }
  });
});

function readSelectedText() {
  const selectedText = window.getSelection().toString();
  if (selectedText) {
    chrome.runtime.sendMessage({ text: selectedText });
  } else {
    alert("No text selected!");
  }
}
// This script is for the popup of the Chrome extension.
// It listens for a button click to read the selected text on the current page.