const {PythonShell} = require('python-shell')

// 定義一個執行 Python 腳本的異步函數
async function runPythonScript(options, scriptPath) {
  
  // 返回一個 Promise 對象
  return new Promise((resolve, reject) => {
    // 使用 PythonShell 庫運行指定的 Python 腳本
    PythonShell.run(scriptPath, options).then(messages => {

      // 將結果傳遞給調用者
      resolve(messages);

    }).catch(err => {
      // 在發生錯誤時拒絕 Promise
      reject(err);
    });
  });
}

// 導出 runPythonScript 函數
module.exports = { 
  runPythonScript: runPythonScript
}