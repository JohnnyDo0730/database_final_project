// 補貨管理頁面 JavaScript

export function init() {
    console.log('restock.js 模組初始化');
    // 綁定在容器上（比如整個子頁區塊）
    const container = document.getElementById("restock-page");
    
    if (!container) {
        console.error('找不到 restock-page 元素');
        return;
    }
  
    // 更新頁面
    updatePage();
    
    console.log('restock.js 事件監聽器已設置');
}

// 獲取補貨清單
async function getRestockList() {
    try {
        const response = await fetch('/backstage/restock/get_restock_list');
        const data = await response.json();
        console.log("請求成功");
        console.log(data);
        return data;
    } catch (error) {
        console.error("請求失敗:", error);
        return null;
    }
}

async function updatePage() {
    // 顯示載入中
    showLoading(true);
    
    try {
        const content = await getRestockList();
        if (content && content.success) {
            updateRestockList(content.restock_list);
        } else {
            showError("無法獲取補貨清單");
        }
    } catch (error) {
        console.error("更新頁面失敗:", error);
        showError("更新頁面時發生錯誤");
    } finally {
        showLoading(false);
    }
}

function updateRestockList(restockList) {
    const restockContainer = document.getElementById("restock-container");
    const noRestockMessage = document.getElementById("no-restock-message");
    
    restockContainer.innerHTML = "";
    
    if (restockList.length === 0) {
        noRestockMessage.style.display = "block";
        return;
    } else {
        noRestockMessage.style.display = "none";
    }
    
    restockList.forEach(item => {
        const restockItem = document.createElement("div");
        restockItem.classList.add("restock-item");
        
        restockItem.innerHTML = `
            <div class="restock-info">
                <p><strong>isbn:</strong> ${escapeHtml(item.isbn)}</p>
                <p><strong>書名:</strong> ${escapeHtml(item.title)}</p>
                <p><strong>需補貨數量:</strong> ${escapeHtml(item.quantity)}</p>
            </div>
            <div class="restock-actions">
                <button class="add-to-cart-btn" data-isbn="${escapeHtml(item.isbn)}">加入購物車</button>
            </div>
        `;
        
        restockItem.addEventListener("click", function(event) {
            const addToCartBtn = event.target.closest(".add-to-cart-btn");
            if (addToCartBtn) {
                const isbn = addToCartBtn.dataset.isbn;
                addToCart(isbn);
            }
        });
        
        restockContainer.appendChild(restockItem);
    });
}

async function addToCart(isbn) {
    try {
        const response = await fetch('/backstage/restock/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ isbn })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 更新補貨清單
            updatePage();
            alert("已成功加入購物車");
        } else {
            alert("加入購物車失敗: " + data.error);
        }
    } catch (error) {
        console.error("加入購物車失敗:", error);
        alert("加入購物車時發生錯誤");
    }
}

// 顯示載入中
function showLoading(show) {
    const loadingElement = document.getElementById("loading-indicator");
    if (loadingElement) {
        loadingElement.style.display = show ? "block" : "none";
    }
}

// 顯示錯誤訊息
function showError(message) {
    const errorElement = document.getElementById("error-message");
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = "block";
        setTimeout(() => {
            errorElement.style.display = "none";
        }, 3000);
    }
}

// XSS 防護
function escapeHtml(unsafe) {
    if (unsafe === undefined || unsafe === null) return '';
    return String(unsafe)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}