const { runPythonScript } = require('../runPythonscript/index.js');
const { Language_Judgment } = require('../Language_Judgment/index.js');

async function NLP_Process(input){

    let Script;

    const options = {
        mode: 'text',
        pythonPath: './.env/Scripts/python.exe',
        pythonOptions: ['-u'],
        scriptPath: './NLP_Scripts',
        args: [input]
    };

    await Language_Judgment(input).then(async (result) => {

        switch (result) {
            case "Chinese":
                Script = "NLP_zh.py";
                break;
            case "English":
                Script = "NLP_en.py";
                break;
            default:
                return "我無法解析這個語言";
        }

    });

    return new Promise((resolve, reject) => {
        
        // 調用runPythonScript函數執行Python腳本
        runPythonScript(options, Script)
           .then(result => {
                resolve(result);  // 解析結果
            })
           .catch(error => {
                reject(error);  // 拒絕錯誤
            });

    });

}

// 導出NLP_Process函數
module.exports = {
    NLP_Process : NLP_Process
}