// backstage.js
document.addEventListener('DOMContentLoaded', function() {
    // 登出功能
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // 側欄導航功能
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.addEventListener('click', handleNavigation);
    }
});


// 處理登出
function handleLogout() {
    fetch('/logout', {
        method: 'POST',
        credentials: 'include'  // 包含cookies
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/login';
        } else {
            alert('登出失敗');
        }
    })
    .catch(error => {
        console.error('登出錯誤:', error);
        alert('登出過程發生錯誤');
    });
}


// 在 handleNavigation 函數之前添加
const pageInitializers = {
    'book': initBookPage,
    'purchase_cart': initPurchaseCartPage,
    'return': initReturnPage,
    'reorder': initReorderPage,
    'purchase_record': initPurchaseRecordPage
};

// 處理導航
function handleNavigation(e) {
    if (e.target.classList.contains('nav-item')) {
        // 更新按鈕狀態
        document.querySelectorAll('.nav-item').forEach(btn => {
            btn.classList.remove('active');
        });
        e.target.classList.add('active');

        // 載入中
        const content = document.getElementById('content');
        content.innerHTML = '<div class="loading">載入中...</div>';

        // 載入頁面
        const page = e.target.getAttribute('data-page');
        
        fetch(`/backstage/${page}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('頁面載入失敗');
                }
                return response.text();
            })
            .then(html => {
                document.getElementById('content').innerHTML = html;
                if (pageInitializers[page]) {
                    pageInitializers[page]();
                }
            })
            .catch(error => {
                console.error('頁面載入錯誤:', error);
                alert('頁面載入失敗');
            });
    }
}

// 各頁面的初始化函數
function initBookPage() {
    console.log('初始化書籍管理頁面');
    // 書籍管理頁面的初始化邏輯
    // 例如：載入書籍列表、設置事件監聽器等
}

function initPurchaseCartPage() {
    console.log('初始化購物車管理頁面');
    // 購物車管理頁面的初始化邏輯
}

function initReturnPage() {
    console.log('初始化退貨管理頁面');
    // 退貨管理頁面的初始化邏輯
}

function initReorderPage() {
    console.log('初始化補貨管理頁面');
    // 補貨管理頁面的初始化邏輯
}

function initPurchaseRecordPage() {
    console.log('初始化採購記錄頁面');
    // 採購記錄頁面的初始化邏輯
}