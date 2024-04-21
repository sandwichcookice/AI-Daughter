async function Ischinese(str) {

    var pattern = /[\u4e00-\u9fa5]/;
    return pattern.test(str);

}

async function isEnglish(text) {

    var pattern = /[a-zA-Z]/;
    return pattern.test(text);

}


async function Language_Judgment(text) {

    if (await Ischinese(text)) {
        return "Chinese";
    } else if (await isEnglish(text)) {
        return "English";
    } else {
        return "Unknown";
    }

}

module.exports = {
    Language_Judgment : Language_Judgment
}