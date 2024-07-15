document.getElementById('toggleTabs').addEventListener('click', () => {
    chrome.storage.sync.get('showTabs', (data) => {
      const showTabs = !data.showTabs;
      chrome.storage.sync.set({ showTabs }, () => {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ['content.js']
          });
        });
      });
    });
  });
  