// 書籍管理頁面 JavaScript

export function init() {
  console.log('store.js 模組初始化');
  // 綁定在容器上（比如整個子頁區塊）
  const container = document.getElementById("store-page");
  
  if (!container) {
      console.error('找不到 store-page 元素');
      return;
  }

  // 更新頁面
  updatePage();
  
  // 監聽搜尋框輸入，顯示/隱藏清除按鈕
  const searchInput = document.getElementById("book-search");
  searchInput.addEventListener("input", function() {
      clearSearchBtn.style.display = this.value ? "flex" : "none";
  });
  
  // 監聽 Enter 鍵
  searchInput.addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
          event.preventDefault();
          const currentPage = document.getElementById("current-page");
          currentPage.value = 1;
          updatePage();
      }
  });
  
  // 監聽清除按鈕點擊
  const clearSearchBtn = document.getElementById("clear-search");
  clearSearchBtn.addEventListener("click", function() {
      searchInput.value = "";
      this.style.display = "none";
      const currentPage = document.getElementById("current-page");
      currentPage.value = 1;
      updatePage();
  });

  // 監聽搜尋按鈕點擊
  const searchBtn = document.getElementById("search-button");
  searchBtn.addEventListener("click", function() {
    const currentPage = document.getElementById("current-page");
    currentPage.value = 1;
    updatePage();
  });

  // 監聽上一頁按鈕點擊
  const prevPageBtn = document.getElementById("prev-page");
  prevPageBtn.addEventListener("click", function() {
    const currentPage = document.getElementById("current-page");
    if (currentPage.value > 1) {
      currentPage.value--;
      updatePage();
    }
  });

  // 監聽下一頁按鈕點擊
  const nextPageBtn = document.getElementById("next-page");
  nextPageBtn.addEventListener("click", function() {
    const currentPage = document.getElementById("current-page");
    if (currentPage.value < parseInt(currentPage.max)) {
      currentPage.value++;
      updatePage();
    }
  });
  
  // 監聽頁碼輸入變化
  const currentPageInput = document.getElementById("current-page");
  currentPageInput.addEventListener("input", function() {
      const value = parseInt(this.value);
      if (value < 1) {
          this.value = 1;
      } else if (this.max && value > parseInt(this.max)) {
          this.value = this.max;
      }
      updatePage();
  });
  
  console.log('store.js 事件監聽器已設置');
}


// 獲取書籍列表與總頁數
async function getBookList(search_keyword, page) {
  try {
      const response = await fetch(`/customer/store/content?search_keyword=${encodeURIComponent(search_keyword)}&page=${page}`);
      const data = await response.json();
      console.log("請求成功");
      return data;
  } catch (error) {
      console.error("請求失敗:", error);
      return null;
  }
}

async function updatePage() {
  const search_keyword = document.getElementById("book-search").value;
  const page = document.getElementById("current-page").value;
  console.log("搜尋:" + search_keyword + " 頁數:" + page);

  // 顯示載入中
  showLoading(true);

  try {
    const content = await getBookList(search_keyword, page);
    if (content) {
        const totalPages = document.getElementById("total-pages");
        const currentPage = document.getElementById("current-page");
        totalPages.textContent = content.total_pages;
        currentPage.max = content.total_pages;

        updateBookList(content.book_list);
        updatePaginationButtons();
    } else {
        showError("無法獲取書籍資料");
    }
  } catch (error) {
    console.error("更新頁面失敗:", error);
    showError("更新頁面時發生錯誤");
  } finally {
    showLoading(false);
  }
}

function updateBookList(book_list) {
  const bookContainer = document.getElementById("books-container");
  bookContainer.innerHTML = "";
  
  if (book_list.length === 0) {
    const noResultsMsg = document.createElement("div");
    noResultsMsg.className = "no-results";
    noResultsMsg.textContent = "沒有找到符合條件的書籍";
    bookContainer.appendChild(noResultsMsg);
    return;
  }
  
  book_list.forEach(book => {
    const bookBlock = document.createElement("div");
    bookBlock.classList.add("book-block");

    /* 添加書封 */
    const bookCover = document.createElement("div");
    bookCover.classList.add("book-cover");
    
    // 使用書籍的 isbn 作為圖片的 ID
    const coverImg = document.createElement("img");
    coverImg.src = book.cover_url || `/static/images/book_covers/${book.isbn}.jpg`;
    coverImg.alt = `${book.title} 封面`;
    coverImg.onerror = function() {
      // 如果圖片載入失敗，顯示預設圖片
      this.src = '/static/images/default_book_cover.jpg';
      // 移除 onerror 處理器，防止預設圖片也載入失敗時的無限循環
      this.onerror = null;
    };
    bookCover.appendChild(coverImg);
    bookBlock.appendChild(bookCover);

    /* 添加右側內容區域 */
    const bookContent = document.createElement("div");
    bookContent.classList.add("book-content");

    /* 添加書籍資訊 */
    const bookInfo = document.createElement("div");
    bookInfo.classList.add("book-info");
    bookInfo.innerHTML = `
      <h3 class="book-title">${escapeHtml(book.title)}</h3>
      <p><strong>isbn:</strong> ${escapeHtml(book.isbn)}</p>
      <p><strong>作者:</strong> ${escapeHtml(book.author)}</p>
      <p><strong>出版社:</strong> ${escapeHtml(book.publisher)}</p>
      <p><strong>價格:</strong> $${escapeHtml(book.price)}</p>
      <p><strong>庫存:</strong> ${escapeHtml(book.stock)}</p>
      <p><strong>類型:</strong> ${escapeHtml(book.type)}</p>
      <p><strong>語言:</strong> ${escapeHtml(book.language)}</p>
      <p><strong>出版日期:</strong> ${escapeHtml(book.publish_date)}</p>
    `;
    bookContent.appendChild(bookInfo);

    /* 添加訂購區域 */
    const bookOrder = document.createElement("div");
    bookOrder.classList.add("book-order");
    
    // 根據庫存狀態決定按鈕顏色和文字
    const hasStock = parseInt(book.stock) > 0;
    const buttonText = hasStock ? "加入購物車" : "預購";
    const buttonClass = hasStock ? "order-btn" : "order-btn preorder-btn";
    
    bookOrder.innerHTML = `
      <label for="order-quantity">購買數量:</label>
      <input type="number" class="order-quantity" min="1" max="${99}" value="1">
      <button class="${buttonClass}" data-isbn="${book.isbn}">${buttonText}</button>
    `;
    bookContent.appendChild(bookOrder);
    
    // 將內容區域添加到書籍區塊
    bookBlock.appendChild(bookContent);

    /* 添加訂購按鈕事件 */
    bookBlock.addEventListener("click", function (event) {
      const orderBtn = event.target.closest(".order-btn");
      if (orderBtn) {
        const isbn = orderBtn.dataset.isbn;
        const quantity = orderBtn.closest(".book-order").querySelector(".order-quantity").value;

        // 呼叫訂購函數
        addToCart(isbn, quantity);
      }
    });

    bookContainer.appendChild(bookBlock);
  });
}


async function addToCart(isbn, quantity) {
  try {
    const response = await fetch(`/customer/store/add_to_cart`, {
      method: 'POST',
      // 傳送 JSON 資料
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ isbn, quantity })
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log(result.message || "書籍加入購物車成功");
      alert(result.message || "書籍加入購物車成功");
    } else {
      console.error(result.error || "書籍加入購物車失敗");
      alert(result.error || "書籍加入購物車失敗");
    }
  } catch (error) {
    console.error("書籍加入購物車失敗:", error);
    alert("書籍加入購物車失敗，請稍後再試");
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

// 更新分頁按鈕狀態
function updatePaginationButtons() {
  const currentPage = document.getElementById("current-page");
  const prevPageBtn = document.getElementById("prev-page");
  const nextPageBtn = document.getElementById("next-page");

  prevPageBtn.disabled = currentPage.value <= 1;
  nextPageBtn.disabled = currentPage.value >= parseInt(currentPage.max);
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