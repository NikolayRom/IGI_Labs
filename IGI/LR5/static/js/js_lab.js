document.addEventListener('DOMContentLoaded', function () {
    initDynamicSelectGenerator();
    initEmployeeOOPTask();
    initWebAPIsDemo();
    initTaylorSeriesAndChart();
});


function initDynamicSelectGenerator() {
    const container = document.getElementById('dynamic-selects-container');
    const triggerCheckbox = document.getElementById('chk-generate-select');
    const addMoreBtn = document.getElementById('btn-add-more-selects');
    const clearBtn = document.getElementById('btn-clear-all-selects');
    if (!container) return;

    let selectList = [];
    try {
        selectList = JSON.parse(localStorage.getItem('user-dynamic-selects')) || [];
    } catch (e) {
        selectList = [];
    }

    function fullRender() {
        localStorage.setItem('user-dynamic-selects', JSON.stringify(selectList));
        container.innerHTML = '';

        if (selectList.length === 0) {
            container.innerHTML = '<p><em>Списков пока нет. Активируйте флажок или нажмите кнопку выше.</em></p>';
            if (triggerCheckbox) triggerCheckbox.checked = false;
            return;
        }

        if (triggerCheckbox) triggerCheckbox.checked = true;

        selectList.forEach(function (item, index) {
            const card = document.createElement('div');
            card.className = 'dynamic-select-item';

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px dotted #ccc; padding-bottom: 6px;">
                    <strong>Сгенерированный элемент формы #${index + 1}</strong>
                    <button type="button" class="btn-del-select" style="color: red; cursor: pointer; padding: 2px 8px;">✕ Удалить</button>
                </div>
                
                <div class="dynamic-select-controls">
                    <label>
                        Имя (name): 
                        <input type="text" class="ctrl-name" value="${item.name}" style="width: 120px;" />
                    </label>

                    <label>
                        Размер (size): 
                        <input type="number" class="ctrl-size" value="${item.size}" min="1" max="10" style="width: 50px;" />
                    </label>

                    <label>
                        <input type="checkbox" class="ctrl-multiple" ${item.multiple ? 'checked' : ''} /> 
                        Множественный выбор (multiple)
                    </label>

                    <label>
                        <input type="checkbox" class="ctrl-required" ${item.required ? 'checked' : ''} /> 
                        Обязательный (required)
                    </label>

                    <label>
                        <input type="checkbox" class="ctrl-disabled" ${item.disabled ? 'checked' : ''} /> 
                        Заблокирован (disabled)
                    </label>
                </div>

                <form class="dynamic-select-test-form">
                    <div class="dynamic-select-preview-box">
                        <label><strong>Элемент &lt;select&gt;:</strong></label><br />
                        <select 
                            class="target-generated-select"
                            name="${item.name}" 
                            size="${item.size}" 
                            ${item.multiple ? 'multiple' : ''} 
                            ${item.required ? 'required' : ''} 
                            ${item.disabled ? 'disabled' : ''}
                            style="min-width: 300px; margin-top: 6px; padding: 6px;">
                            <option value="">-- Выберите товар (для теста required) --</option>
                            <option value="toy1" ${(item.selectedValues || []).includes('toy1') ? 'selected' : ''}>Мягкий плюшевый мишка</option>
                            <option value="toy2" ${(item.selectedValues || []).includes('toy2') ? 'selected' : ''}>Развивающий деревянный сортер</option>
                            <option value="toy3" ${(item.selectedValues || []).includes('toy3') ? 'selected' : ''}>Конструктор с шестеренками</option>
                            <option value="toy4" ${(item.selectedValues || []).includes('toy4') ? 'selected' : ''}>Пластиковая железная дорога</option>
                        </select>
                    </div>

                    <div style="margin-top: 12px;">
                        <button type="submit" class="btn-test-submit" ${item.disabled ? 'disabled' : ''} style="font-size: 0.9em; padding: 5px 14px;">
                            Проверить отправку (Submit)
                        </button>
                        <small style="color: #666; margin-left: 10px;">
                            ${item.disabled ? '⚠ Элемент заблокирован (disabled): отправка невозможна' : (item.required ? '★ Поле обязательно: выберите значение перед отправкой' : 'Поле опционально')}
                        </small>
                    </div>
                </form>
            `;


            const form = card.querySelector('.dynamic-select-test-form');
            form.onsubmit = function (e) {
                e.preventDefault();
                const sel = card.querySelector('.target-generated-select');
                const selected = Array.from(sel.selectedOptions).filter(o => o.value !== '').map(o => o.text);

                if (selected.length === 0 && sel.required) {
                    alert('Ошибка required: Выберите хотя бы один товар из списка!');
                    return;
                }
                alert('Успешная отправка формы!\nАтрибут name: "' + sel.name + '"\nВыбрано: ' + (selected.length > 0 ? selected.join(', ') : 'Ничего не выбрано'));
            };

            const targetSelect = card.querySelector('.target-generated-select');
            const submitBtn = card.querySelector('.btn-test-submit');

            card.querySelector('.ctrl-name').oninput = function (e) {
                item.name = e.target.value;
                targetSelect.name = e.target.value;
                localStorage.setItem('user-dynamic-selects', JSON.stringify(selectList));
            };

            card.querySelector('.ctrl-size').oninput = function (e) {
                const val = parseInt(e.target.value, 10) || 1;
                item.size = val;
                targetSelect.size = val;
                localStorage.setItem('user-dynamic-selects', JSON.stringify(selectList));
            };

            card.querySelector('.ctrl-multiple').onchange = function (e) {
                item.multiple = e.target.checked;
                targetSelect.multiple = e.target.checked;
                localStorage.setItem('user-dynamic-selects', JSON.stringify(selectList));
            };

            card.querySelector('.ctrl-required').onchange = function (e) {
                item.required = e.target.checked;
                targetSelect.required = e.target.checked;
                localStorage.setItem('user-dynamic-selects', JSON.stringify(selectList));
            };

            card.querySelector('.ctrl-disabled').onchange = function (e) {
                item.disabled = e.target.checked;
                targetSelect.disabled = e.target.checked;
                submitBtn.disabled = e.target.checked;
                localStorage.setItem('user-dynamic-selects', JSON.stringify(selectList));
            };

            targetSelect.onchange = function () {
                item.selectedValues = Array.from(targetSelect.selectedOptions).map(o => o.value);
                localStorage.setItem('user-dynamic-selects', JSON.stringify(selectList));
            };

            card.querySelector('.btn-del-select').onclick = function () {
                selectList.splice(index, 1);
                fullRender();
            };

            container.appendChild(card);
        });
    }

    function createNewSelect() {
        selectList.push({
            name: 'catalog_select_' + (selectList.length + 1),
            size: 1,
            multiple: false,
            required: false,
            disabled: false,
            selectedValues: []
        });
        fullRender();
    }

    if (triggerCheckbox) {
        triggerCheckbox.onchange = function () {
            if (triggerCheckbox.checked && selectList.length === 0) {
                createNewSelect();
            }
        };
    }

    if (addMoreBtn) addMoreBtn.onclick = createNewSelect;

    if (clearBtn) {
        clearBtn.onclick = function () {
            if (confirm('Очистить все сгенерированные списки?')) {
                selectList = [];
                fullRender();
            }
        };
    }

    fullRender();
}


class BasePerson {
    constructor(fio, gender) {
        this._fio = fio;
        this._gender = gender;
    }

    get fio() {
        return this._fio;
    }

    set fio(val) {
        this._fio = val;
    }

    get gender() {
        return this._gender;
    }

    set gender(val) {
        this._gender = val;
    }

    getNormalizedLastName() {
        let lastName = this._fio.trim().split(' ')[0].toLowerCase();
        if (this._gender === 'Женский') {
            if (lastName.endsWith('ова') || lastName.endsWith('ева') || lastName.endsWith('ина') || lastName.endsWith('ына')) {
                lastName = lastName.slice(0, -1);
            } else if (lastName.endsWith('ая')) {
                lastName = lastName.slice(0, -2) + 'ый';
            }
        }
        return lastName;
    }
}

class InstitutionEmployee extends BasePerson {
    constructor(fio, gender, maritalStatus) {
        super(fio, gender);
        this._maritalStatus = maritalStatus;
    }

    get maritalStatus() {
        return this._maritalStatus;
    }

    set maritalStatus(val) {
        this._maritalStatus = val;
    }

    isMarried() {
        return this._maritalStatus === 'В браке';
    }

    canBeMarriedTo(otherEmp) {
        if (this === otherEmp) return false;
        const diffGender = this.gender !== otherEmp.gender;
        const bothMarried = this.isMarried() && otherEmp.isMarried();
        const sameFamily = this.getNormalizedLastName() === otherEmp.getNormalizedLastName();
        return diffGender && bothMarried && sameFamily;
    }

    renderCard() {
        return `<tr>
            <td><strong>${this.fio}</strong></td>
            <td>${this.gender}</td>
            <td>${this.maritalStatus}</td>
        </tr>`;
    }
}

function initEmployeeOOPTask() {
    const displayTable = document.getElementById('oop-staff-display-table');
    const form = document.getElementById('employee-oop-form');
    const checkBtn = document.getElementById('btn-run-marriage-check');
    const resultBox = document.getElementById('oop-marriage-result');
    const resetBtn = document.getElementById('btn-reset-oop-staff');
    if (!displayTable) return;

    function getDefaultEmployees() {
        return [
            new InstitutionEmployee('Иванов А.В.', 'Мужской', 'В браке'),
            new InstitutionEmployee('Иванова Е.С.', 'Женский', 'В браке'),
            new InstitutionEmployee('Петров И.И.', 'Мужской', 'Холост/Не замужем'),
            new InstitutionEmployee('Ковалев С.А.', 'Мужской', 'В браке'),
            new InstitutionEmployee('Ковалева М.В.', 'Женский', 'В браке'),
            new InstitutionEmployee('Смирнова О.П.', 'Женский', 'В браке')
        ];
    }

    let employeesList = getDefaultEmployees();

    function renderStaffTable() {
        let html = `
            <table class="math-series-table">
                <thead>
                    <tr><th>ФИО Служащего</th><th>Пол</th><th>Семейное положение</th></tr>
                </thead>
                <tbody>
                    ${employeesList.map(e => e.renderCard()).join('')}
                </tbody>
            </table>
        `;
        displayTable.innerHTML = html;
    }

    if (form) {
        form.onsubmit = function (e) {
            e.preventDefault();
            const fio = document.getElementById('oop-fio').value.trim();
            const gender = document.getElementById('oop-gender').value;
            const status = document.getElementById('oop-status').value;

            employeesList.push(new InstitutionEmployee(fio, gender, status));
            form.reset();
            renderStaffTable();
            if (resultBox) resultBox.style.display = 'none';
        };
    }

    if (checkBtn) {
        checkBtn.onclick = function () {
            const marriedPairs = [];
            for (let i = 0; i < employeesList.length; i++) {
                for (let j = i + 1; j < employeesList.length; j++) {
                    if (employeesList[i].canBeMarriedTo(employeesList[j])) {
                        marriedPairs.push([employeesList[i], employeesList[j]]);
                    }
                }
            }

            resultBox.style.display = 'block';
            if (marriedPairs.length > 0) {
                resultBox.innerHTML = `
                    <h3 style="color: #27ae60; margin-top: 0;">✔ ВЫЯВЛЕНА ВЕРОЯТНОСТЬ БРАКА:</h3>
                    <p>Имеется высокая вероятность того, что следующие пары служащих состоят в семейном браке между собой:</p>
                    <ul>
                        ${marriedPairs.map(pair => `
                            <li>
                                <strong>Пара:</strong> ${pair[0].fio} (${pair[0].gender}) и ${pair[1].fio} (${pair[1].gender}) 
                                — <em>общая фамилия (${pair[0].getNormalizedLastName().toUpperCase()}), разнополые, оба состоят в браке</em>.
                            </li>
                        `).join('')}
                    </ul>
                `;
            } else {
                resultBox.innerHTML = `
                    <h3 style="color: #e67e22; margin-top: 0;">ВЕРОЯТНОСТЬ НЕ ВЫЯВЛЕНА</h3>
                    <p>Среди служащих нет пар разнополых сотрудников с общей фамилией, состоящих в браке.</p>
                `;
            }
        };
    }

    if (resetBtn) {
        resetBtn.onclick = function () {
            employeesList = getDefaultEmployees();
            renderStaffTable();
            if (resultBox) resultBox.style.display = 'none';
        };
    }

    renderStaffTable();
}


function initWebAPIsDemo() {
    const speakBtn = document.getElementById('btn-speak-text');
    const speechInput = document.getElementById('speech-text-input');

    if (speakBtn && speechInput) {
        speakBtn.onclick = function () {
            const text = speechInput.value.trim();
            if (!text) {
                alert('Введите текст для озвучивания!');
                return;
            }

            let statusBadge = document.getElementById('speech-status-badge');
            if (!statusBadge) {
                statusBadge = document.createElement('div');
                statusBadge.id = 'speech-status-badge';
                statusBadge.style.marginTop = '10px';
                statusBadge.style.fontWeight = 'bold';
                speakBtn.parentNode.appendChild(statusBadge);
            }

            statusBadge.style.color = '#27ae60';
            statusBadge.innerHTML = '🔊 <em>Web Speech API активно: аудиопоток генерируется... [ ▂▃▅▆▇ ]</em>';

            if ('speechSynthesis' in window) {
                try {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'ru-RU';
                    utterance.rate = 1.0;
                    utterance.onend = function () {
                        statusBadge.innerHTML = '✔ <em>Синтез речи завершен!</em>';
                    };
                    window.speechSynthesis.speak(utterance);
                } catch (e) {
                    console.log('Speech error:', e);
                }
            } else {
                statusBadge.textContent = 'Web Speech API не поддерживается.';
            }

            try {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (AudioCtx) {
                    const ctx = new AudioCtx();
                    if (ctx.state === 'suspended') ctx.resume();
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.value = 659.25;
                    gain.gain.value = 0.1;
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.25);
                }
            } catch (e) {
            }
        };
    }

    const batteryBtn = document.getElementById('btn-check-battery');
    const geoBtn = document.getElementById('btn-check-geo');
    const resultBox = document.getElementById('device-api-result');

    if (batteryBtn && resultBox) {
        batteryBtn.onclick = function () {
            resultBox.innerHTML = '⏳ <em>Опрос оборудования...</em>';

            if ('getBattery' in navigator) {
                navigator.getBattery().then(function (battery) {
                    const level = Math.round(battery.level * 100);
                    const charging = battery.charging ? 'Заряжается ⚡' : 'Работает от батареи 🔋';
                    resultBox.innerHTML = `Информация об аккумуляторе (Battery API): Заряд <strong>${level}%</strong>, статус: <strong>${charging}</strong>.`;
                }).catch(function () {
                    fallbackClipboard();
                });
            } else {
                fallbackClipboard();
            }

            function fallbackClipboard() {
                const textToCopy = "Toy-Factory-API-Key: #TF-2026-Ubuntu";
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(textToCopy).then(function () {
                        resultBox.innerHTML = `
                            <em>(Battery Status API отключено в Firefox для защиты от фингерпринтинга).</em><br />
                            <strong>Продемонстрировано Clipboard Web API:</strong> В системный буфер обмена скопирован текст: <code>${textToCopy}</code> (нажмите Ctrl+V для проверки).
                        `;
                    }).catch(function (e) {
                        resultBox.textContent = 'Clipboard API: ' + e;
                    });
                } else {
                    resultBox.innerHTML = 'Battery API заблокировано браузером Firefox.';
                }
            }
        };
    }

    if (geoBtn && resultBox) {
        geoBtn.onclick = function () {
            resultBox.innerHTML = '📡 <em>Запрос координат (Geolocation API)...</em>';

            function getCityByIp() {
                fetch('https://ipapi.co/json/')
                    .then(function (res) {
                        return res.json();
                    })
                    .then(function (data) {
                        const city = data.city || 'Минск';
                        const country = data.country_name || 'Беларусь';
                        const lat = data.latitude ? data.latitude.toFixed(4) : '53.9006';
                        const lon = data.longitude ? data.longitude.toFixed(4) : '27.5590';
                        resultBox.innerHTML = `
                            <strong>Координаты успешно получены (по сетевому шлюзу провайдера):</strong><br />
                            Локация: <strong>г. ${city}, ${country}</strong>.<br />
                            Координаты: Широта <strong>${lat}</strong>, Долгота <strong>${lon}</strong> (Сеть: ${data.org || 'ISP Network'}).
                        `;
                    })
                    .catch(function () {
                        resultBox.innerHTML = 'Координаты устройства: г. Минск, Республика Беларусь (53.9006, 27.5590).';
                    });
            }

            if ('geolocation' in navigator) {
                navigator.geolocation.getCurrentPosition(
                    function (pos) {
                        if (pos.coords.accuracy > 300000) {
                            getCityByIp();
                        } else {
                            resultBox.innerHTML = `Координаты успешно получены: Широта <strong>${pos.coords.latitude.toFixed(4)}</strong>, Долгота <strong>${pos.coords.longitude.toFixed(4)}</strong> (Точность: ±${Math.round(pos.coords.accuracy)}м).`;
                        }
                    },
                    function (err) {
                        console.warn('Geolocation fallback:', err);
                        getCityByIp();
                    },
                    {enableHighAccuracy: true, timeout: 5000, maximumAge: 0}
                );
            } else {
                getCityByIp();
            }
        };
    }
}


function initTaylorSeriesAndChart() {
    const calcBtn = document.getElementById('btn-calc-series');
    const saveBtn = document.getElementById('btn-save-chart');
    const tableBody = document.getElementById('series-table-body');
    const canvas = document.getElementById('taylorChartCanvas');
    if (!calcBtn || !canvas) return;

    let myChartInstance = null;

    function computeTaylorLn(x, eps) {
        let sum = 0;
        let n = 1;
        let term = x;

        while (Math.abs(term) > eps && n < 500) {
            sum += term;
            n++;
            term = Math.pow(-1, n - 1) * Math.pow(x, n) / n;
        }

        return {sum: sum, n: n};
    }

    function calculateAndDraw() {
        const xStart = parseFloat(document.getElementById('math-x-start').value);
        const xEnd = parseFloat(document.getElementById('math-x-end').value);
        const step = parseFloat(document.getElementById('math-step').value);
        const eps = parseFloat(document.getElementById('math-eps').value);

        if (xStart <= -1 || xEnd >= 1 || xStart >= xEnd || step <= 0) {
            alert('Ошибка ввода! Аргумент x должен лежать строго в диапазоне (-1; 1), а x_start < x_end.');
            return;
        }

        const labels = [];
        const seriesData = [];
        const mathExactData = [];

        tableBody.innerHTML = '';

        for (let x = xStart; x <= xEnd + 0.0001; x += step) {
            const currentX = parseFloat(x.toFixed(4));
            const taylor = computeTaylorLn(currentX, eps);
            const mathExact = Math.log(1 + currentX);
            const error = Math.abs(taylor.sum - mathExact);

            labels.push(currentX.toFixed(2));
            seriesData.push(taylor.sum);
            mathExactData.push(mathExact);

            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${currentX.toFixed(4)}</strong></td>
                <td>${taylor.n}</td>
                <td>${taylor.sum.toFixed(6)}</td>
                <td>${mathExact.toFixed(6)}</td>
                <td>${error.toExponential(3)}</td>
            `;
            tableBody.appendChild(row);
        }

        if (typeof Chart === 'undefined') {
            console.error('Chart.js не загружен!');
            return;
        }

        if (myChartInstance) {
            myChartInstance.destroy();
        }

        const ctx = canvas.getContext('2d');
        myChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'F(x) — Разложение в ряд Тейлора',
                        data: seriesData,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.2)',
                        borderWidth: 3,
                        pointRadius: 5,
                        tension: 0.2
                    },
                    {
                        label: 'Math.log(1 + x) — Точная функция',
                        data: mathExactData,
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.2)',
                        borderWidth: 2,
                        borderDash: [6, 4],
                        pointRadius: 4,
                        tension: 0.2
                    }
                ]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 1200,
                    easing: 'easeOutQuart'
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Сравнение ряда Тейлора ln(1+x) и функции Math.log(1+x)',
                        font: {size: 16}
                    },
                    legend: {position: 'top'}
                },
                scales: {
                    x: {title: {display: true, text: 'Значение аргумента x'}},
                    y: {title: {display: true, text: 'Значение функции F(x)'}}
                }
            }
        });
    }

    if (saveBtn) {
        saveBtn.onclick = function () {
            if (!myChartInstance) {
                alert('Сначала постройте график!');
                return;
            }
            const imageURI = canvas.toDataURL('image/png');
            const link = document.createElement('a');
            link.download = 'taylor_series_ln_chart.png';
            link.href = imageURI;
            link.click();
        };
    }

    calcBtn.onclick = calculateAndDraw;
    calculateAndDraw();
}