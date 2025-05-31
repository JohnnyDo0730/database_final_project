// customer.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('客戶頁面初始化');
    
    // 初始化事件委派
    initEventDelegation();
    
    // 載入適當的頁面內容（從 sessionStorage 或默認頁面）
    initPageContent();
});

/**
 * 初始化事件委派
 * 設置所有通過事件委派處理的事件監聽器
 */
function initEventDelegation() {
    console.log('初始化事件委派');
    
    // 使用事件委派處理所有點擊事件
    document.addEventListener('click', function(event) {
        // 處理側欄導航按鈕點擊
        const navItem = event.target.closest('.nav-item');
        if (navItem) {
            console.log('導航按鈕被點擊:', navItem.getAttribute('data-page'));
            handleNavigation(navItem);
            return;
        }
        
        // 處理登出按鈕點擊
        const logoutBtn = event.target.closest('#logout-btn');
        if (logoutBtn) {
            console.log('登出按鈕被點擊');
            handleLogout();
            return;
        }
    });
}

/**
 * 初始化頁面內容
 * 根據 sessionStorage 或默認設置載入適當的頁面
 */
function initPageContent() {
    console.log('初始化頁面內容');
    
    // 從 sessionStorage 獲取上次訪問的頁面
    const activePage = sessionStorage.getItem('customerActivePage');
    
    if (activePage) {
        console.log('從 sessionStorage 載入頁面:', activePage);
        loadPage(activePage);
    } else {
        // 沒有歷史記錄，載入默認頁面
        const defaultPage = 'store';
        console.log('載入默認頁面:', defaultPage);
        
        // 載入默認頁面
        loadPage(defaultPage);
    }
}

/**
 * 更新側欄狀態
 * 根據當前頁面名稱更新側欄按鈕的選中狀態
 * @param {string} pageName - 當前頁面名稱
 */
function updateSidebarState(pageName) {
    console.log('更新側欄狀態:', pageName);
    
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        // 移除所有按鈕的 active 類
        item.classList.remove('active');
        
        // 為當前頁面對應的按鈕添加 active 類
        if (item.getAttribute('data-page') === pageName) {
            item.classList.add('active');
        }
    });
}

/**
 * 載入頁面內容
 * 通過 AJAX 請求載入頁面內容
 * @param {string} pageName - 要載入的頁面名稱
 */
function loadPage(pageName) {
    console.log('載入頁面:', pageName);
    sessionStorage.setItem('customerActivePage', pageName);
    
    // 獲取內容容器
    const content = document.getElementById('content');
    if (!content) {
        console.error('找不到內容容器元素');
        return;
    }
    
    // 顯示載入中
    content.innerHTML = '<div class="loading">載入中...</div>';

    // 發送 AJAX 請求
    fetch(`/customer/${pageName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`頁面載入失敗: ${response.status} ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            // 更新頁面內容
            content.innerHTML = html;
            
            console.log('頁面內容已更新:', pageName);
            
            // 檢查並調用對應頁面的初始化函數
            const initFunctionName = `init${pageName.charAt(0).toUpperCase() + pageName.slice(1)}Page`;
            if (window[initFunctionName] && typeof window[initFunctionName] === 'function') {
                console.log('調用頁面初始化函數:', initFunctionName);
                window[initFunctionName]();
            }

            updateSidebarState(pageName);
        })
        .catch(error => {
            console.error('頁面載入錯誤:', error);
            content.innerHTML = `<div class="error">載入失敗: ${error.message}</div>`;
            alert('頁面載入失敗');
        });
}

/**
 * 處理側欄導航點擊
 * 當用戶點擊側欄導航按鈕時調用
 * @param {HTMLElement} navItem - 被點擊的導航按鈕元素
 */
function handleNavigation(navItem) {
    // 獲取目標頁面名稱
    const pageName = navItem.getAttribute('data-page');
    if (!pageName) {
        console.error('導航按鈕缺少 data-page 屬性');
        return;
    }
    
    console.log('處理導航點擊:', pageName);

    // 載入目標頁面
    loadPage(pageName);
}

/**
 * 處理登出按鈕點擊
 */
function handleLogout() {
    console.log('處理登出');
    
    // 禁用按鈕並顯示狀態
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.disabled = true;
        const originalText = logoutBtn.textContent;
        logoutBtn.textContent = '登出中...';
    }
    
    // 發送登出請求
    fetch('/logout', {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('登出成功，即將跳轉');
            window.location.href = '/login';
        } else {
            console.log('登出失敗');
            alert('登出失敗');
            // 恢復按鈕狀態
            if (logoutBtn) {
                logoutBtn.disabled = false;
                logoutBtn.textContent = originalText;
            }
        }
    })
    .catch(error => {
        console.error('登出錯誤:', error);
        alert('登出過程發生錯誤');
        // 恢復按鈕狀態
        if (logoutBtn) {
            logoutBtn.disabled = false;
            logoutBtn.textContent = originalText;
        }
    });
}
