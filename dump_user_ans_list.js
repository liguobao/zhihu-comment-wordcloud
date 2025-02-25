// ==UserScript==
// @name         知乎回答提取器
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  提取知乎页面上的回答内容
// @author       You
// @match        https://www.zhihu.com/people/*
// @grant        none
// @require      https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js
// ==/UserScript==

(function() {
    'use strict';
    var ans_list_key = "zhihu_ans_list";
    var ans_ids_key = "zhihu_ans_ids";
    var max_page = 20;
    var current_page = 1;
    function include_ans_id(ans_id) {
        var ans_ids = JSON.parse(localStorage.getItem(ans_ids_key) || '[]');
        return ans_ids.includes(ans_id);
    }
    function add_ans_id(ans_id) {
        var ans_ids = JSON.parse(localStorage.getItem(ans_ids_key) || '[]');
        ans_ids.push(ans_id);
        localStorage.setItem(ans_ids_key, JSON.stringify(ans_ids));
    }

    function add_ans_to_list(ans) {
        var ans_list = JSON.parse(localStorage.getItem(ans_list_key) || '[]');
        ans_list.push(ans);
        localStorage.setItem(ans_list_key, JSON.stringify(ans_list));
    }

    function check_ans_list_empty(){
        var answerItemList = document.querySelectorAll('.AnswerItem');
        if (answerItemList.length == 0) {
            console.log("没有找到回答，跳出");
            return false;
        }
        return true;
    }

    function saveAnswers() {
        let answerItemList = document.querySelectorAll('.AnswerItem');
        for (let answerItem of answerItemList) {
            var ansItemLabel =  answerItem.querySelector(".RichContent-inner");
            if (!ansItemLabel) {
                console.log(`answerItem:${answerItem} is not a valid answer item, skip`);
                continue;
            }
            var itemData = answerItem.getAttribute("data-zop");
            var ans_id = JSON.parse(itemData)["itemId"];
            if (include_ans_id(ans_id)) {
                console.log(`answer:${ans_id} 已存在，跳过`);
                continue;
            }
            add_ans_id(ans_id);
            var question_title = JSON.parse(itemData)["title"];
            ansItemLabel.click();
            console.log(`question_title:${question_title} 自动点击展开`);

            var answer_id = JSON.parse(itemData)["itemId"];
            var answer_content = answerItem.querySelector('.RichContent-inner').innerText;
            var answer = {
                question_title: question_title,
                answer_id: answer_id,
                answer_content: answer_content,
                answer_url: "https://www.zhihu.com/answer/" + answer_id
            };
            console.log(`answer:${answer_id} 已保存`);
            add_ans_to_list(answer);
        }
    }

    function click_next_page() {
        if (!check_ans_list_empty()) {
            console.log("没有找到回答，跳出");
            window.location.reload();
            return;
        }
        var next_page = document.querySelector(".PaginationButton-next");
        if (next_page) {
            next_page.click();
            console.log(`点击下一页，当前页码:${current_page}`);
            current_page++;
        }
    }

    // 等待页面加载完成后执行
    window.addEventListener('load', function() {
        var task_interval = setInterval(function() {
            saveAnswers();
            console.log(`等待10秒后点击下一页`);
            click_next_page();
            if (current_page > max_page) {
                console.log("已达到最大页数，跳出");
                clearInterval(task_interval);
            }
        }, 1000 * 10);

        // 导出所有回答
        async function exportToMarkdown() {
            let stored = JSON.parse(localStorage.getItem(ans_list_key) || '[]');

            // 创建新的 JSZip 实例
            const zip = new JSZip();

            // 为每个回答创建单独的 markdown 文件
            for (let answer of stored) {
                const safeTitle = answer.question_title.replace(/[\\/:*?"<>|]/g, '_');
                const fileName = `${answer.answer_id}_${safeTitle}.md`;

                let content = `# ${answer.question_title}\n\n`;
                content += `> 回答ID: ${answer.answer_id}\n\n`;
                content += `> 链接: ${answer.answer_url}\n\n`;
                content += `${answer.answer_content}\n\n`;

                // 将文件添加到 zip
                zip.file(fileName, content);
            }

            // 生成并下载 zip 文件
            const zipBlob = await zip.generateAsync({type: "blob"});
            const url = URL.createObjectURL(zipBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "zhihu_answers.zip";
            a.click();
            localStorage.removeItem(ans_list_key);
            localStorage.removeItem(ans_ids_key);
            URL.revokeObjectURL(url);
        }

        // 创建导出按钮
        function createExportButton() {
            // 添加 JSZip 库
            // const script = document.createElement('script');
            // script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
            // document.head.appendChild(script);

            const button = document.createElement('button');
            button.textContent = '导出回答';
            button.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 9999; padding: 10px;';
            button.onclick = exportToMarkdown;
            document.body.appendChild(button);
        }
        createExportButton();
    });
})();
