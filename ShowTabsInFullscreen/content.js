chrome.storage.sync.get('showTabs', (data) => {
    if (data.showTabs) {
      document.documentElement.style.setProperty('--chrome-tabs-display', 'block');
    } else {
      document.documentElement.style.setProperty('--chrome-tabs-display', 'none');
    }
  });
  