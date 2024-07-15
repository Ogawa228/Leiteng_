function updateTabs() {
  chrome.tabs.query({}, function (tabs) {
    console.log('Updating tabs:', tabs);
    for (let tab of tabs) {
      chrome.tabs.sendMessage(tab.id, { tabs }).catch((error) => {
        console.error('Error sending message to tab:', tab.id, error);
      });
    }
  });
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete') {
    updateTabs();
  }
});
chrome.tabs.onRemoved.addListener(updateTabs);
chrome.tabs.onActivated.addListener(updateTabs);

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  console.log('Received message:', request);
  if (request.activateTabId) {
    chrome.tabs.update(request.activateTabId, { active: true });
  }
  if (request.closeTabId) {
    chrome.tabs.remove(request.closeTabId);
  }
});
