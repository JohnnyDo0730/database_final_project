// 退貨管理頁面 JavaScript

export function init() {
    console.log('return.js 模組初始化');
    // 綁定在容器上（比如整個子頁區塊）
    const container = document.getElementById("return-page");
    
    if (!container) {
        console.error('找不到 return-page 元素');
        return;
    }
  
    /*
    container.addEventListener("click", function (event) {
      const targetBtn = event.target.closest(".my-button");
      if (targetBtn) {
        console.log("你點擊了退貨管理頁面 的按鈕:", targetBtn.dataset.name);
        // 呼叫該模組內的專屬函數
        doSomething(targetBtn.dataset.name);
      }
    });
    */
    
    console.log('return.js 事件監聽器已設置');
}