// 訂單查詢頁面 JavaScript

export function init() {
    console.log('order_record.js 模組初始化');
    // 綁定在容器上（比如整個子頁區塊）
    const container = document.getElementById("order-page");
    
    if (!container) {
        console.error('找不到 order-page 元素');
        return;
    }
  
    // 載入頁面後立即獲取訂單資料
    fetchOrderData();
    
    // 綁定退貨按鈕事件
    container.addEventListener("click", function (event) {
        const returnBtn = event.target.closest(".return-btn");
        if (returnBtn) {
            const orderId = returnBtn.dataset.orderId;
            console.log(`使用者點擊了訂單 ${orderId} 的退貨按鈕`);
            // 呼叫退貨函數
            returnOrder(orderId);
        }
    });
    
    console.log('order_record.js 事件監聽器已設置');
}

// 獲取訂單資料
 async function fetchOrderData() {
    try {
        const response = await fetch('/customer/order_record/get_orders');
        const data = await response.json();
        
        if (data.success) {
            displayOrders(data.orders);
        } else {
            showErrorMessage(data.error || '獲取訂單資料失敗');
        }
    } catch (error) {
        console.error('獲取訂單資料時發生錯誤:', error);
        showErrorMessage('無法連接到伺服器，請稍後再試');
    } finally {
        // 隱藏載入動畫
        document.querySelector('.loading-container').style.display = 'none';
        // 顯示訂單容器
        document.querySelector('.orders-container').style.display = 'block';
    }
}

// 顯示訂單列表
 function displayOrders(orders) {
    const ordersContainer = document.querySelector('.orders-container');
    const noOrdersMessage = document.querySelector('.no-orders-message');
    
    // 清空現有內容（但保留 no-orders-message 元素）
    const childElements = Array.from(ordersContainer.children);
    childElements.forEach(child => {
        if (!child.classList.contains('no-orders-message')) {
            ordersContainer.removeChild(child);
        }
    });
    
    if (orders.length === 0) {
        // 如果沒有訂單，顯示提示訊息
        noOrdersMessage.style.display = 'block';
        return;
    }
    
    // 隱藏無訂單提示
    noOrdersMessage.style.display = 'none';
    
    // 取得模板
    const orderTemplate = document.getElementById('order-template');
    const orderItemTemplate = document.getElementById('order-item-template');
    
    // 遍歷所有訂單並創建訂單區塊
    orders.forEach(order => {
        // 複製訂單模板
        const orderElement = document.importNode(orderTemplate.content, true);
        
        // 填充訂單資訊
        orderElement.querySelector('.order-id').textContent = order.order_id;
        orderElement.querySelector('.order-date').textContent = formatDate(order.order_date);
        orderElement.querySelector('.order-status').textContent = translateOrderStatus(order.order_status);
        orderElement.querySelector('.order-amount').textContent = order.total_amount.toFixed(2);
        
        // 設置退貨按鈕的 data 屬性
        orderElement.querySelector('.return-btn').dataset.orderId = order.order_id;
        
        // 填充訂單項目
        const itemsContainer = orderElement.querySelector('.items-container');
        
        order.items.forEach(item => {
            // 複製項目模板
            const itemElement = document.importNode(orderItemTemplate.content, true);
            
            // 填充項目資訊
            itemElement.querySelector('.item-title').textContent = item.title;
            itemElement.querySelector('.item-quantity').textContent = item.quantity;
            itemElement.querySelector('.item-price').textContent = `${item.price.toFixed(2)} 元`;
            itemElement.querySelector('.item-total').textContent = `${item.total_price.toFixed(2)} 元`;
            
            // 將項目添加到訂單中
            itemsContainer.appendChild(itemElement);
        });
        
        // 將訂單添加到容器中
        ordersContainer.insertBefore(orderElement, noOrdersMessage);
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

// 顯示錯誤訊息
 function showErrorMessage(message) {
    // 創建錯誤訊息元素
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.style.cssText = `
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
        text-align: center;
    `;
    
    // 將錯誤訊息加入頁面
    const ordersContainer = document.querySelector('.orders-container');
    ordersContainer.insertBefore(errorElement, ordersContainer.firstChild);
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