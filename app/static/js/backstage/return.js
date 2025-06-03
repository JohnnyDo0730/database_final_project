// 退貨管理頁面 JavaScript

export function init() {
    console.log('return.js 模組初始化');
    // 綁定在容器上（比如整個子頁區塊）
    const container = document.getElementById("return-page");
    
    if (!container) {
        console.error('找不到 return-page 元素');
        return;
    }
  
    // 更新頁面
    updatePage();
    
    console.log('return.js 事件監聽器已設置');
}

// 獲取退貨訂單資料
async function getReturnOrderData() {
    const response = await fetch('/backstage/return/get_returns');
    const data = await response.json();
    return data;
}

// 更新頁面
async function updatePage() {
    // 顯示載入中
    showLoading(true);

    try {
        const content = await getReturnOrderData();
        if (content) {
            // 更新退貨訂單列表
            updateReturnList(content.returns);
        } else {
            showError("無法獲取退貨訂單資料");
        }
    } catch (error) {
        console.error("更新頁面失敗:", error);
        showError("更新頁面時發生錯誤");
    } finally {
        showLoading(false);
    }
}

// 更新退貨訂單列表
function updateReturnList(return_list) {
    console.log('退貨訂單列表:', return_list);
    const returnsContainer = document.getElementById("returns-container");
    returnsContainer.innerHTML = "";

    if (return_list.length === 0) {
        const noResultsMsg = document.createElement("div");
        noResultsMsg.className = "no-results";
        noResultsMsg.textContent = "沒有退貨中的訂單";
        returnsContainer.appendChild(noResultsMsg);
        console.log('沒有退貨中的訂單');
        return;
    }
  
    return_list.forEach(order => {
        const returnBlock = document.createElement("div");
        returnBlock.classList.add("return-block");
        
        returnBlock.innerHTML = `
          <div class="return-header">
                    <div class="return-info">
                        <h3>訂單編號: <span class="order-id">${escapeHtml(order.order_id)}</span></h3>
                        <p><strong>申請客戶:</strong> ${escapeHtml(order.name)}</p>
                        <p><strong>訂單日期:</strong> ${escapeHtml(formatDate(order.order_date))}</p>
                        <p><strong>訂單狀態:</strong> ${escapeHtml(order.order_status)}</p>
                    </div>
                    <div class="return-total">
                        <p>訂單總金額: <span class="order-amount">${escapeHtml(order.total_amount.toFixed(2))}</span> 元</p>
                    </div>
                </div>
                <div class="return-items">
                    <table>
                        <thead>
                            <tr>
                                <th>書名</th>
                                <th>數量</th>
                                <th>單價</th>
                                <th>總價</th>
                            </tr>
                        </thead>
                        <tbody class="items-container">
                            ${order.items.map(item => `
                            <tr class="return-item">
                                <td class="item-title">${escapeHtml(item.title)}</td>
                                <td class="item-quantity">${escapeHtml(item.quantity)}</td>
                                <td class="item-price">${escapeHtml(item.price.toFixed(2))} 元</td>
                                <td class="item-total">${escapeHtml(item.total_price.toFixed(2))} 元</td>
                            </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                <div class="return-actions">
                    <button class="reject-return-btn" data-order-id="${escapeHtml(order.order_id)}">拒絕退貨</button>
                    <button class="confirm-return-btn" data-order-id="${escapeHtml(order.order_id)}">確認退貨</button>
                </div>
        `;
        
        // 監聽確認退貨按鈕
        const confirmReturnBtn = returnBlock.querySelector('.confirm-return-btn');
        if (confirmReturnBtn) {
            confirmReturnBtn.addEventListener('click', () => {
                console.log('確認退貨按鈕被點擊');
                // 確認退貨
                confirmReturn(confirmReturnBtn.dataset.orderId);
            });
        }
        
        // 監聽拒絕退貨按鈕
        const rejectReturnBtn = returnBlock.querySelector('.reject-return-btn');
        if (rejectReturnBtn) {
            rejectReturnBtn.addEventListener('click', () => {
                console.log('拒絕退貨按鈕被點擊');
                // 拒絕退貨
                rejectReturn(rejectReturnBtn.dataset.orderId);
            });
        }
        
        returnsContainer.appendChild(returnBlock);
    });
}

// 確認退貨功能
async function confirmReturn(orderId) {
    console.log('確認退貨:', orderId);
    // 呼叫後端 API 確認退貨
    const response = await fetch('/backstage/return/confirm', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ order_id: orderId })
    });
    const result = await response.json();
    if (result.success) {
        alert('退貨確認成功');
        // 重新載入頁面資料
        updatePage();
    } else {
        showError(result.error || '退貨確認失敗');
    }
}

// 拒絕退貨功能
async function rejectReturn(orderId) {
    console.log('拒絕退貨:', orderId);
    // 呼叫後端 API 拒絕退貨
    const response = await fetch('/backstage/return/reject', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ order_id: orderId })
    });
    const result = await response.json();
    if (result.success) {
        alert('退貨已拒絕');
        // 重新載入頁面資料
        updatePage();
    } else {
        showError(result.error || '拒絕退貨失敗');
    }
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}年${month}月${day}日`;
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