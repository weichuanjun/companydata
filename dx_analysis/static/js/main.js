document.addEventListener('DOMContentLoaded', () => {
    const convertBtn = document.getElementById('convertBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const statusDiv = document.getElementById('status');
    const companyTabs = document.getElementById('companyTabs');
    const analysisContent = document.getElementById('analysisContent');

    // 转换PDF文件
    convertBtn.addEventListener('click', async () => {
        try {
            statusDiv.textContent = 'PDFファイルを変換中...';
            convertBtn.disabled = true;

            const response = await fetch('/convert', {
                method: 'POST'
            });

            const data = await response.json();

            if (data.status === 'success') {
                statusDiv.textContent = 'PDFファイルの変換が完了しました。';
                analyzeBtn.disabled = false;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            statusDiv.textContent = `エラー: ${error.message}`;
        } finally {
            convertBtn.disabled = false;
        }
    });

    // 分析公司
    analyzeBtn.addEventListener('click', async () => {
        try {
            statusDiv.textContent = '分析中...';
            analyzeBtn.disabled = true;

            const response = await fetch('/analyze', {
                method: 'POST'
            });

            const data = await response.json();

            if (data.status === 'success') {
                displayResults(data.analyses);
                statusDiv.textContent = '分析が完了しました。';
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            statusDiv.textContent = `エラー: ${error.message}`;
        } finally {
            analyzeBtn.disabled = false;
        }
    });

    // 显示分析结果
    function displayResults(analyses) {
        // 清空现有内容
        companyTabs.innerHTML = '';
        analysisContent.innerHTML = '';

        // 获取模板
        const tabTemplate = document.getElementById('tabTemplate');
        const contentTemplate = document.getElementById('contentTemplate');

        // 创建标签和内容
        analyses.forEach((analysis, index) => {
            // 创建标签
            const tabClone = tabTemplate.content.cloneNode(true);
            const tab = tabClone.querySelector('.tab');

            tab.dataset.company = analysis.company_name;
            tab.querySelector('.company-name').textContent = analysis.company_name;
            tab.querySelector('.score').textContent = `${analysis.total_score}点`;

            // 根据分数设置颜色
            if (analysis.total_score >= 80) {
                tab.classList.add('score-high');
            } else if (analysis.total_score >= 60) {
                tab.classList.add('score-medium');
            } else {
                tab.classList.add('score-low');
            }

            // 第一个标签默认激活
            if (index === 0) {
                tab.classList.add('active');
            }

            companyTabs.appendChild(tab);

            // 创建内容
            const contentClone = contentTemplate.content.cloneNode(true);
            const content = contentClone.querySelector('.analysis-section');

            content.dataset.company = analysis.company_name;
            content.querySelector('.company-title').textContent = analysis.company_name;
            content.querySelector('.total-score .score').textContent = `${analysis.total_score}点`;

            // 设置各项分数
            const scores = {
                'DX現状': analysis.dx_status.score,
                'プロセスマイニング': analysis.process_mining.score,
                '営業力': analysis.sales_enhancement.score,
                'クラウド': analysis.cloud_usage.score,
                '自動化': analysis.automation.score,
                '基幹システム': analysis.core_system.score
            };

            Object.entries(scores).forEach(([key, value]) => {
                const scoreItem = content.querySelector(`.score-item:has(.label:contains('${key}')) .value`);
                if (scoreItem) {
                    scoreItem.textContent = `${value}点`;
                }
            });

            // 设置分析内容
            content.querySelector('.dx-status').textContent = analysis.dx_status.analysis;
            content.querySelector('.process-mining').textContent = analysis.process_mining.analysis;
            content.querySelector('.sales-enhancement').textContent = analysis.sales_enhancement.analysis;
            content.querySelector('.cloud-usage').textContent = analysis.cloud_usage.analysis;
            content.querySelector('.automation').textContent = analysis.automation.analysis;
            content.querySelector('.core-system').textContent = analysis.core_system.analysis;
            content.querySelector('.financial-indicators').textContent = analysis.financial_indicators.analysis;
            content.querySelector('.business-opportunities').textContent = analysis.business_opportunities.analysis;
            content.querySelector('.risks').textContent = analysis.risks.analysis;
            content.querySelector('.priorities').textContent = analysis.priorities.analysis;
            content.querySelector('.final-evaluation').textContent = analysis.final_evaluation.analysis;

            // 第一个内容默认显示
            if (index === 0) {
                content.classList.add('active');
            }

            analysisContent.appendChild(content);
        });

        // 添加标签切换事件
        const tabs = companyTabs.querySelectorAll('.tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // 移除所有活动状态
                tabs.forEach(t => t.classList.remove('active'));
                analysisContent.querySelectorAll('.analysis-section').forEach(section => {
                    section.classList.remove('active');
                });

                // 设置当前标签和内容为活动状态
                tab.classList.add('active');
                const company = tab.dataset.company;
                analysisContent.querySelector(`.analysis-section[data-company="${company}"]`).classList.add('active');
            });
        });
    }
}); 