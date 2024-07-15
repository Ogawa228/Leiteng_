document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement) {
      console.log('Entered fullscreen mode');
      showTabContainer();
    } else {
      console.log('Exited fullscreen mode');
      hideTabContainer();
    }
  });
  
  chrome.runtime.onMessage.addListener(function (message) {
    console.log('Received message in content script:', message);
    if (message.tabs) {
      updateTabList(message.tabs);
    }
  });
  
  function showTabContainer() {
    const tabContainer = document.getElementById('tab-container');
    if (tabContainer) {
      tabContainer.style.display = 'block';
    } else {
      createTabContainer();
    }
  }
  
  function hideTabContainer() {
    const tabContainer = document.getElementById('tab-container');
    if (tabContainer) {
      tabContainer.style.display = 'none';
    }
  }
  
  function createTabContainer() {
    const container = document.createElement('div');
    container.id = 'tab-container';
    container.setAttribute('aria-labelledby', 'tab-button');
    container.innerHTML = `
      <div id="tab-button">Tabs</div>
      <div id="tab-content" aria-labelledby="tab-button" role="tabpanel">
        <div id="tab-list"></div>
      </div>
    `;
    document.body.appendChild(container);
  }
  
  function updateTabList(tabs) {
    const tabList = document.getElementById('tab-list');
    tabList.innerHTML = '';
    for (let tab of tabs) {
      const tabBox = document.createElement('div');
      tabBox.className = 'tab-box';
      tabBox.innerHTML = `
        <div class="tab-link" role="button">${tab.title}</div>
        <div class="tab-close" data-tab-id="${tab.id}" role="button">X</div>
      `;
      tabList.appendChild(tabBox);
  
      tabBox.querySelector('.tab-link').addEventListener('click', () => {
        chrome.runtime.sendMessage({ activateTabId: tab.id });
      });
  
      tabBox.querySelector('.tab-close').addEventListener('click', () => {
        chrome.runtime.sendMessage({ closeTabId: tab.id });
      });
    }
  }
  