// 書店瀏覽頁面 JavaScript

export function init() {
    console.log('store.js 模組初始化');
    // 綁定在容器上（比如整個子頁區塊）
    const container = document.getElementById("store-page");
    
    if (!container) {
        console.error('找不到 store-page 元素');
        return;
    }
  
    /*
    container.addEventListener("click", function (event) {
      const targetBtn = event.target.closest(".my-button");
      if (targetBtn) {
        console.log("你點擊了書店瀏覽頁面 的按鈕:", targetBtn.dataset.name);
        // 呼叫該模組內的專屬函數
        doSomething(targetBtn.dataset.name);
      }
    });
    */
    
    console.log('store.js 事件監聽器已設置');
}