// 書籍管理頁面 JavaScript

export function init() {
    console.log('book.js 模組初始化');
    // 綁定在容器上（比如整個子頁區塊）
    const container = document.getElementById("book-page");
    
    if (!container) {
        console.error('找不到 book-page 元素');
        return;
    }

    // 更新頁面
    updatePage();
    
    // 監聽搜尋框輸入，顯示/隱藏清除按鈕
    const searchInput = document.getElementById("book-search");
    searchInput.addEventListener("input", function() {
        const clearSearchBtn = document.getElementById("clear-search");
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
        const searchInput = document.getElementById("book-search");
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
    
    console.log('初始化完成');
}


// 獲取書籍列表與總頁數
async function getBookList(search_keyword, page) {
  try {
      const response = await fetch(`/backstage/book/content?search_keyword=${encodeURIComponent(search_keyword)}&page=${page}`);
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

    const bookInfo = document.createElement("div");
    bookInfo.classList.add("book-info");
    bookInfo.innerHTML = `
      <h3 class="book-title">${escapeHtml(book.title)}</h3>
      <p><strong>ISBN:</strong> ${escapeHtml(book.ISBN)}</p>
      <p><strong>作者:</strong> ${escapeHtml(book.author)}</p>
      <p><strong>出版社:</strong> ${escapeHtml(book.publisher)}</p>
      <p><strong>價格:</strong> ${escapeHtml(book.price)}</p>
      <p><strong>庫存:</strong> ${escapeHtml(book.stock)}</p>
      <p><strong>類型:</strong> ${escapeHtml(book.type)}</p>
      <p><strong>語言:</strong> ${escapeHtml(book.language)}</p>
      <p><strong>出版日期:</strong> ${escapeHtml(book.publish_date)}</p>
    `;
    bookBlock.appendChild(bookInfo);

    const bookOrder = document.createElement("div");
    bookOrder.classList.add("book-order");
    bookOrder.innerHTML = `
      <label for="order-quantity">訂購數量:</label>
      <input type="number" class="order-quantity" min="1" value="1">
      <button class="order-btn" data-isbn="${book.ISBN}">加入購物車</button>
    `;
    bookBlock.appendChild(bookOrder);

    bookBlock.addEventListener("click", function (event) {
      const orderBtn = event.target.closest(".order-btn");
      if (orderBtn) {
        const isbn = orderBtn.dataset.isbn;
        const quantity = orderBtn.closest(".book-order").querySelector(".order-quantity").value;
        console.log(`下訂書籍 ISBN: ${isbn}, 數量: ${quantity}`);

        // 呼叫訂購函數(未實現)
        addToCart(isbn, quantity);
      }
    });

    bookContainer.appendChild(bookBlock);
  });
}


async function addToCart(isbn, quantity) {
  try {
    const response = await fetch(`/backstage/book/add_to_cart`, {
      method: 'POST',
      // 傳送 JSON 資料
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ isbn, quantity })
    });
    if (response.ok) {
      alert("書籍加入購物車成功");
    } else {
      alert("書籍加入購物車失敗");
    }
  } catch (error) {
    console.error("書籍加入購物車失敗:", error);
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