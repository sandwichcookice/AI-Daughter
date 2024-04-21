//使用py虛擬環境 : .env\Scripts\activate

const readline = require('readline');

const { NLP_Process } = require('./functions/NLP_Processing/index.js');


const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});


function askQuestion() {
    rl.question('請輸入文本（輸入 "exit" 退出）: ', async (input) => {

        if (input.toLowerCase() === "exit") {
            rl.close();  // 關閉readline接口
            return;
        }

        await NLP_Process(input).then(result => {
            console.log(JSON.parse(result));
        });

        askQuestion();
    });
}


function starter() {

    askQuestion();
        
}

starter();