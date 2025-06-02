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
                    <p>訂單日期: <span class="order-date">${escapeHtml(formatDate(order.order_date))}</span></p>
                    <p>訂單狀態: <span class="order-status">${escapeHtml(translateOrderStatus(order.order_status))}</span></p>
                </div>
                <div class="order-total">
                    <p>訂單總金額: <span class="order-amount">${escapeHtml(order.total_amount.toFixed(2))}</span> 元</p>
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
                            <td class="item-price">${escapeHtml(item.price.toFixed(2))} 元</td>
                            <td class="item-total">${escapeHtml(item.total_price.toFixed(2))} 元</td>
                        </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <div class="order-actions">
                <button class="return-btn" data-order-id="${escapeHtml(order.order_id)}">申請退貨</button>
            </div>
    `;
    
    ordersContainer.appendChild(orderBlock);
  });
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


// 退貨函數
async function returnOrder(orderId) {
  // 退貨功能目前還未實現
  alert(`退貨功能開發中，訂單編號: ${orderId}`);

  // 退貨功能實現後的代碼如下：
  /*
  try {
      const response = await fetch('/customer/order_record/return', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ order_id: orderId })
      });
      
      const data = await response.json();
      
      if (data.success) {
          alert('退貨申請已提交，待審核');
          // 重新載入訂單資料
          fetchOrderData();
      } else {
          alert(`退貨申請失敗: ${data.error || '未知錯誤'}`);
      }
  } catch (error) {
      console.error('退貨申請發生錯誤:', error);
      alert('無法連接到伺服器，請稍後再試');
  }
  */
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