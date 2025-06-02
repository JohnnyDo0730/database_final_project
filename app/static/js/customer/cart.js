// 購物車 JavaScript

export function init() {
  console.log('cart.js 模組初始化');
  // 綁定在容器上（比如整個子頁區塊）
  const container = document.getElementById("cart-page");
  
  if (!container) {
      console.error('找不到 cart-page 元素');
      return;
  }

  updatePage();

  // 監聽結帳按鈕
  const submitOrderBtn = container.querySelector('#submit-order');
  if (submitOrderBtn) {
      submitOrderBtn.addEventListener('click', function() {
          console.log('結帳按鈕被點擊');

          // 發送訂單
          sendOrder();
      });
  }

  console.log('cart.js 事件監聽器已設置');
}


// 獲取購物車內容
async function getCartContent() {
  try {
      const response = await fetch(`/customer/cart/content`);
      const data = await response.json();
      console.log("請求成功");
      return data;
  } catch (error) {
      console.error("請求失敗:", error);
      return null;
  }
}


// 更新頁面
async function updatePage() {
  console.log("更新購物車頁面");
  
  // 顯示載入中
  showLoading(true);
  
  try {
      const content = await getCartContent();
      if (content) {
       // 更新書籍列表
      updateBookList(content.cart_content);
      } else {
          showError("無法獲取購物車資料");
      }
  } catch (error) {
      console.error("更新頁面失敗:", error);
      showError("更新頁面時發生錯誤");
  } finally {
      showLoading(false);
  }

}


// 更新書籍列表
function updateBookList(book_list) {
  const cartContainer = document.getElementById("cart-container");
  cartContainer.innerHTML = "";
  
  if (book_list.length === 0) {
    const noResultsMsg = document.createElement("div");
    noResultsMsg.className = "no-results";
    noResultsMsg.textContent = "購物車為空";
    cartContainer.appendChild(noResultsMsg);
    return;
  }
  
  book_list.forEach(book => {
    const bookBlock = document.createElement("div");
    bookBlock.classList.add("book-block");

    const bookInfo = document.createElement("div");
    bookInfo.classList.add("book-info");
    bookInfo.innerHTML = `
      <h3 class="book-title">${escapeHtml(book.title)}</h3>
      <div class="quantity">
        <span>數量: </span>
        <span class="quantity-value">${escapeHtml(book.quantity)}</span>
      </div>
    `;
    bookBlock.appendChild(bookInfo);

    const bookRemove = document.createElement("div");
    bookRemove.classList.add("book-remove");
    bookRemove.innerHTML = `
      <button class="remove-btn" data-isbn="${escapeHtml(book.isbn)}">移除</button>
    `;
    bookBlock.appendChild(bookRemove);

    bookBlock.addEventListener("click", function (event) {
      const removeBtn = event.target.closest(".remove-btn");
      if (removeBtn) {

        // 呼叫移除函數
        const isbn = removeBtn.dataset.isbn;
        removeFromCart(isbn);
      }
    });

    cartContainer.appendChild(bookBlock);
  });
}


// 發送訂單
async function sendOrder() {
  console.log('發送訂單');
  const response = await fetch(`/customer/cart/submit`)
  const data = await response.json();
  if (data.success) {
      alert('訂單已送出');
      updatePage();
  } else {
      alert("訂單送出失敗: " + data.error);
  }
}


// 移除書籍
async function removeFromCart(isbn) {
  console.log(`移除書籍 ISBN: ${isbn}`);
  await fetch(`/customer/cart/remove`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          isbn: isbn,
      })
  })
  updatePage();
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