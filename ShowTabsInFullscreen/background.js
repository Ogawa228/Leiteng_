chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ showTabs: true });
  });
  
  chrome.action.onClicked.addListener((tab) => {
    chrome.storage.sync.get('showTabs', (data) => {
      const showTabs = !data.showTabs;
      chrome.storage.sync.set({ showTabs });
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      });
    });
  });
  