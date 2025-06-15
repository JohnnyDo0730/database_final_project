// 訂單查詢頁面 JavaScript

export function init() {
    console.log('order_record.js 模組初始化');
    // 綁定在容器上（比如整個子頁區塊）
    const container = document.getElementById("order-page");
    
    if (!container) {
        console.error('找不到 order-page 元素');
        return;
    }
  
    // 更新頁面
    updatePage();

    
    console.log('order_record.js 事件監聽器已設置');
}

// 獲取訂單資料
async function getOrderData() {
    const response = await fetch('/customer/order_record/get_orders');
    const data = await response.json();
    return data;
}

// 更新頁面
async function updatePage() {
    // 顯示載入中
    showLoading(true);

    try {
        const content = await getOrderData();
        if (content) {
            // 更新訂單列表
            updateOrderList(content.orders);
        } else {
            showError("無法獲取訂單資料");
        }
    } catch (error) {
        console.error("更新頁面失敗:", error);
        showError("更新頁面時發生錯誤");
    } finally {
        showLoading(false);
    }

}


// 更新訂單列表
function updateOrderList(order_list) {
  console.log('訂單列表:', order_list);
  const ordersContainer = document.getElementById("orders-container");
  ordersContainer.innerHTML = "";


  if (order_list.length === 0) {
    const noResultsMsg = document.createElement("div");
    noResultsMsg.className = "no-results";
    noResultsMsg.textContent = "訂單為空";
    ordersContainer.appendChild(noResultsMsg);
    console.log('訂單為空');
    return;
  }
  
  order_list.forEach(order => {
    const orderBlock = document.createElement("div");
    orderBlock.classList.add("order-block");
    const test = document.createElement("div");
    test.textContent = `測試`;
    orderBlock.appendChild(test);
    
    orderBlock.innerHTML = `
      <div class="order-header">
                <div class="order-info">
                    <h3>訂單編號: <span class="order-id">${escapeHtml(order.order_id)}</span></h3>
                    <p><strong>訂單日期:</strong> ${escapeHtml(formatDate(order.order_date))}</p>
                    <p><strong>訂單狀態:</strong> ${escapeHtml(translateOrderStatus(order.order_status))}</p>
                </div>
                <div class="order-total">
                    <p>訂單總金額: <span class="order-amount">${escapeHtml(order.total_amount)}</span> 元</p>
                </div>
            </div>
            <div class="order-items">
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
                        <tr class="order-item">
                            <td class="item-title">${escapeHtml(item.title)}</td>
                            <td class="item-quantity">${escapeHtml(item.quantity)}</td>
                            <td class="item-price">${escapeHtml(item.price)} 元</td>
                            <td class="item-total">${escapeHtml(item.total_price)} 元</td>
                        </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <div class="order-actions">
                <button class="return-btn" data-order-id="${escapeHtml(order.order_id)}" ${order.order_status.includes('不接受退貨') || order.order_status == '退貨中' || order.order_status == '已退貨' ? 'disabled' : ''}>申請退貨</button>
            </div>
    `;
    //監聽退貨按鈕
    const returnBtn = orderBlock.querySelector('.return-btn');
    if (returnBtn) {
      returnBtn.addEventListener('click', () => {
        if (returnBtn.disabled) {
          alert('此訂單不接受退貨');
          return;
        }
        console.log('退貨按鈕被點擊');
        // 發送退貨申請
        sendReturnRequest(returnBtn.dataset.orderId);
      });
    }
    
    ordersContainer.appendChild(orderBlock);
  });
}


async function sendReturnRequest(orderId) {
  console.log('受理退貨申請:', orderId);
  const response = await fetch('/customer/order_record/return', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ order_id: orderId })
  });
  const data = await response.json();
  if (data.success) {
    console.log(data.message);
    alert(data.message);
  } else {
    console.log(data.error);
    alert(data.error);
  }
  updatePage();
}

// 格式化日期
function formatDate(dateString) {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}年${month}月${day}日`;
}

// 轉換訂單狀態為中文
function translateOrderStatus(status) {
  const statusMap = {
      'pending': '待處理',
      'processing': '處理中',
      'shipped': '已出貨',
      'delivered': '已送達',
      'completed': '已完成',
      'canceled': '已取消',
      'return_requested': '申請退貨中',
      'returned': '已退貨'
  };

  return statusMap[status] || status;
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