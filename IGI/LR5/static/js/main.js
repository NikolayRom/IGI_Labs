document.addEventListener('DOMContentLoaded', () => {
    initThemeSwitcher();
    initAgeVerification();
    initHeroSlider();
});


function initThemeSwitcher() {
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (!themeBtn) return;


    const savedTheme = localStorage.getItem('site-theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeBtn.textContent = '☀️ Светлая тема';
    } else {
        themeBtn.textContent = '🌙 Тёмная тема';
    }

    themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        const isDark = document.body.classList.contains('dark-theme');

        localStorage.setItem('site-theme', isDark ? 'dark' : 'light');
        themeBtn.textContent = isDark ? '☀️ Светлая тема' : '🌙 Тёмная тема';
    });
}


function showWelcomeMessage(age, dayOfWeek) {
    const oldMsg = document.getElementById('age-message-banner');
    if (oldMsg) oldMsg.remove();

    const banner = document.createElement('div');
    banner.id = 'age-message-banner';
    banner.className = 'age-welcome-message';
    banner.innerHTML = `
        <button type="button" class="close-msg-btn" onclick="this.parentElement.remove();">&times;</button>
        <h4>✔ Возраст подтвержден</h4>
        <p>Вам <strong>${age} лет</strong> (совершеннолетний пользователь).</p>
        <p>День недели вашего рождения: <strong>${dayOfWeek}</strong>.</p>
        <p><small style="color: #7f8c8d;">Вам предоставлен полный доступ к каталогу и оптовым заказам.</small></p>
    `;
    document.body.appendChild(banner);

    setTimeout(() => {
        if (banner.parentNode) {
            banner.style.transition = 'opacity 0.5s ease';
            banner.style.opacity = '0';
            setTimeout(() => banner.remove(), 500);
        }
    }, 9000);
}

function askBirthDate(force = false) {
    if (!force && sessionStorage.getItem('age-verified')) return;

    setTimeout(() => {
        const inputDate = prompt('Добро пожаловать в Toy Factory!\nПожалуйста, укажите дату рождения в формате ГГГГ-ММ-ДД (например, 2002-05-15):');
        if (!inputDate) return;

        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateRegex.test(inputDate.trim())) {
            alert('Ошибка ввода! Формат даты должен быть строго ГГГГ-ММ-ДД (например, 2002-11-24).');
            return;
        }

        const birthDate = new Date(inputDate);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (isNaN(birthDate.getTime())) {
            alert('Введена некорректная календарная дата!');
            return;
        }

        if (birthDate > today) {
            alert(`Ошибка валидации! Введена дата из будущего (${inputDate}). Вы еще не родились!`);
            return;
        }

        if (today.getFullYear() - birthDate.getFullYear() > 120) {
            alert('Ошибка валидации! Возраст не может превышать 120 лет.');
            return;
        }

        let age = today.getFullYear() - birthDate.getFullYear();
        const m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        const days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
        const dayOfWeek = days[birthDate.getDay()];

        if (age >= 18) {
            showWelcomeMessage(age, dayOfWeek);
            sessionStorage.setItem('age-verified', 'true');
        } else {
            alert(`Вам ${age} лет.\nДень недели вашего рождения: ${dayOfWeek}.\n\nВНИМАНИЕ! Для использования оптового портала и оформления заказов требуется официальное разрешение родителей!`);
            sessionStorage.setItem('age-verified', 'minor');
        }
    }, 400);
}

function initAgeVerification() {
    askBirthDate(false);


    const testAgeBtn = document.getElementById('recheck-age-btn');
    if (testAgeBtn) {
        testAgeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            askBirthDate(true);
        });
    }
}


class ToySlider {
    constructor(containerSelector, options = {}) {
        this.container = document.querySelector(containerSelector);
        if (!this.container) return;


        this.options = Object.assign({
            loop: true,
            navs: true,
            pags: true,
            auto: true,
            stopMouseHover: true,
            delay: 5
        }, options);

        this.slides = this.container.querySelectorAll('.slider-slide');
        this.totalSlides = this.slides.length;
        this.currentIndex = 0;
        this.timer = null;

        this.initDOM();
        this.bindEvents();
        this.updateSlide(0);

        if (this.options.auto) {
            this.startAutoPlay();
        }
    }

    initDOM() {

        this.counterElem = document.createElement('div');
        this.counterElem.className = 'slider-counter';
        this.container.appendChild(this.counterElem);


        if (this.options.navs) {
            this.prevBtn = document.createElement('button');
            this.prevBtn.className = 'slider-arrow slider-prev';
            this.prevBtn.innerHTML = '&#10094;';

            this.nextBtn = document.createElement('button');
            this.nextBtn.className = 'slider-arrow slider-next';
            this.nextBtn.innerHTML = '&#10095;';

            this.container.appendChild(this.prevBtn);
            this.container.appendChild(this.nextBtn);
        }


        if (this.options.pags) {
            this.pagsContainer = document.createElement('div');
            this.pagsContainer.className = 'slider-pagination';

            this.dots = [];
            for (let i = 0; i < this.totalSlides; i++) {
                const dot = document.createElement('div');
                dot.className = 'slider-dot';
                dot.dataset.index = i;
                this.pagsContainer.appendChild(dot);
                this.dots.push(dot);
            }
            this.container.appendChild(this.pagsContainer);
        }
    }

    bindEvents() {
        if (this.options.navs) {
            this.prevBtn.addEventListener('click', () => this.prev());
            this.nextBtn.addEventListener('click', () => this.next());
        }

        if (this.options.pags) {
            this.pagsContainer.addEventListener('click', (e) => {
                if (e.target.classList.contains('slider-dot')) {
                    const idx = parseInt(e.target.dataset.index, 10);
                    this.goTo(idx);
                }
            });
        }


        if (this.options.auto && this.options.stopMouseHover) {
            this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
            this.container.addEventListener('mouseleave', () => this.startAutoPlay());
        }
    }

    updateSlide(newIndex) {
        this.slides.forEach((slide, idx) => {
            slide.classList.toggle('active', idx === newIndex);
        });

        if (this.options.pags && this.dots) {
            this.dots.forEach((dot, idx) => {
                dot.classList.toggle('active', idx === newIndex);
            });
        }


        this.counterElem.textContent = `${newIndex + 1}/${this.totalSlides}`;
        this.currentIndex = newIndex;
    }

    next() {
        let nextIndex = this.currentIndex + 1;
        if (nextIndex >= this.totalSlides) {
            if (this.options.loop) {
                nextIndex = 0;
            } else {
                return;
            }
        }
        this.updateSlide(nextIndex);
    }

    prev() {
        let prevIndex = this.currentIndex - 1;
        if (prevIndex < 0) {
            if (this.options.loop) {
                prevIndex = this.totalSlides - 1;
            } else {
                return;
            }
        }
        this.updateSlide(prevIndex);
    }

    goTo(index) {
        this.updateSlide(index);
    }

    startAutoPlay() {
        this.stopAutoPlay();
        this.timer = setInterval(() => {
            this.next();
        }, this.options.delay * 1000);
    }

    stopAutoPlay() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    setDelay(seconds) {
        this.options.delay = seconds;
        if (this.options.auto) {
            this.startAutoPlay();
        }
    }
}


function initHeroSlider() {
    const sliderContainer = document.querySelector('#main-toy-slider');
    if (!sliderContainer) return;


    const savedConfig = JSON.parse(localStorage.getItem('toy-slider-config')) || {
        loop: true,
        navs: true,
        pags: true,
        auto: true,
        stopMouseHover: true,
        delay: 5
    };


    const heroSlider = new ToySlider('#main-toy-slider', savedConfig);


    const delayInp = document.getElementById('cfg-delay');
    if (delayInp) {
        const loopInp = document.getElementById('cfg-loop');
        const navsInp = document.getElementById('cfg-navs');
        const pagsInp = document.getElementById('cfg-pags');
        const autoInp = document.getElementById('cfg-auto');
        const hoverInp = document.getElementById('cfg-hover');
        const saveBtn = document.getElementById('save-slider-config-btn');

        delayInp.value = savedConfig.delay;
        loopInp.checked = savedConfig.loop;
        navsInp.checked = savedConfig.navs;
        pagsInp.checked = savedConfig.pags;
        autoInp.checked = savedConfig.auto;
        hoverInp.checked = savedConfig.stopMouseHover;

        saveBtn.addEventListener('click', () => {
            const newConfig = {
                delay: parseInt(delayInp.value, 10) || 5,
                loop: loopInp.checked,
                navs: navsInp.checked,
                pags: pagsInp.checked,
                auto: autoInp.checked,
                stopMouseHover: hoverInp.checked
            };

            localStorage.setItem('toy-slider-config', JSON.stringify(newConfig));
            alert('Настройки слайдера сохранены в памяти браузера! Страница будет перезагружена.');
            location.reload();
        });
    }
}


function initClientCatalogPagination() {
    const container = document.querySelector('.products-grid-container');
    if (!container) return;

    const cards = Array.from(container.querySelectorAll('.product-grid-card'));
    if (cards.length === 0) return;


    const perPageSelect = document.getElementById('items-per-page-select');
    const paginationBar = document.getElementById('client-pagination-nav');
    const pageInfo = document.getElementById('client-page-counter-info');
    if (!paginationBar) return;

    let itemsPerPage = perPageSelect ? parseInt(perPageSelect.value, 10) : 3;
    let currentPage = 1;

    function renderPage(page) {
        currentPage = page;
        const totalItems = cards.length;


        const limit = itemsPerPage === 0 ? totalItems : itemsPerPage;
        const totalPages = Math.ceil(totalItems / limit) || 1;

        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        const startIndex = (currentPage - 1) * limit;
        const endIndex = startIndex + limit;


        cards.forEach((card, idx) => {
            if (idx >= startIndex && idx < endIndex) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });


        renderPaginationButtons(totalPages);

        if (pageInfo) {
            pageInfo.textContent = `Показаны товары ${totalItems > 0 ? startIndex + 1 : 0}–${Math.min(endIndex, totalItems)} из ${totalItems} (Страница ${currentPage} из ${totalPages})`;
        }
    }

    function renderPaginationButtons(totalPages) {
        paginationBar.innerHTML = '';
        if (totalPages <= 1 && itemsPerPage !== 0) return;


        const prevBtn = document.createElement('button');
        prevBtn.type = 'button';
        prevBtn.className = 'client-page-btn';
        prevBtn.innerHTML = '&larr; Назад';
        prevBtn.disabled = currentPage === 1;
        prevBtn.addEventListener('click', () => renderPage(currentPage - 1));
        paginationBar.appendChild(prevBtn);


        for (let i = 1; i <= totalPages; i++) {
            const numBtn = document.createElement('button');
            numBtn.type = 'button';
            numBtn.className = `client-page-btn ${i === currentPage ? 'active' : ''}`;
            numBtn.textContent = i;
            numBtn.addEventListener('click', () => renderPage(i));
            paginationBar.appendChild(numBtn);
        }


        const nextBtn = document.createElement('button');
        nextBtn.type = 'button';
        nextBtn.className = 'client-page-btn';
        nextBtn.innerHTML = 'Вперед &rarr;';
        nextBtn.disabled = currentPage === totalPages;
        nextBtn.addEventListener('click', () => renderPage(currentPage + 1));
        paginationBar.appendChild(nextBtn);
    }

    if (perPageSelect) {
        perPageSelect.addEventListener('change', () => {
            itemsPerPage = parseInt(perPageSelect.value, 10);
            renderPage(1);
        });
    }


    renderPage(1);
}


function initProductCards3DTilt() {
    const cards = document.querySelectorAll('.product-grid-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;


            const rotateX = ((y - centerY) / centerY) * -12;
            const rotateY = ((x - centerX) / centerX) * 12;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.03, 1.03, 1.03)`;
            card.style.boxShadow = `0 15px 30px rgba(0, 0, 0, 0.15)`;
        });

        card.addEventListener('mouseleave', () => {

            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
            card.style.boxShadow = '';
        });
    });
}


document.addEventListener('DOMContentLoaded', () => {
    initClientCatalogPagination();
    initProductCards3DTilt();
});


function initInteractiveStaffTable() {
    const tableElem = document.getElementById('main-staff-table');
    if (!tableElem) return;

    let staffList = [];
    let filteredList = [];
    let currentPage = 1;
    const itemsPerPage = 3;
    let sortColumn = 'fio';
    let sortAsc = true;

    const selectedEmployeeIds = new Set();

    const tbody = document.getElementById('staff-table-body');
    const paginationNav = document.getElementById('staff-pagination-nav');
    const loadingSpinner = document.getElementById('table-loading-spinner');
    const searchInput = document.getElementById('staff-search-input');
    const searchBtn = document.getElementById('staff-search-btn');
    const resetBtn = document.getElementById('staff-search-reset-btn');
    const checkAllBox = document.getElementById('check-all-staff');

    function generateFallbackStaff() {
        const list = [];
        const names = [
            'Иванов Иван Иванович', 'Петров Петр Сергеевич', 'Сидорова Анна Павловна',
            'Ковалев Дмитрий Олегович', 'Морозова Елена Викторовна', 'Новиков Артем Игоревич',
            'Федорова Ольга Михайловна', 'Васильев Денис Андреевич', 'Павлова Мария Сергеевна',
            'Семенов Алексей Николаевич'
        ];
        const roles = [
            'Главный технолог по полимерам', 'Мастер цеха сборки конструкторов', 'Контролер ОТК качества',
            'Инженер по автоматизации конвейера', 'Специалист по закупкам сырья', 'Оператор термопластавтомата',
            'Дизайнер мягких игрушек', 'Менеджер оптовых отгрузок', 'Логист складского комплекса',
            'Художник-оформитель упаковки'
        ];

        for (let i = 0; i < 10; i++) {
            list.push({
                id: 'emp-' + (i + 1),
                fio: names[i],
                avatar: `https://randomfox.ca/images/${i + 10}.jpg`,
                info: roles[i],
                phone: `+375 (29) 111-22-${i < 9 ? '0' + (i + 1) : (i + 1)}`,
                email: `employee_${i + 1}@toyfactory.by`
            });
        }
        return list;
    }

    loadingSpinner.style.display = 'block';
    tableElem.style.display = 'none';

    const apiUrl = window.location.pathname.includes('/api/')
        ? '/api/employees-data/'
        : '/employees-data/';

    setTimeout(() => {
        fetch(apiUrl)
            .then(res => {
                if (!res.ok) throw new Error('Network response was not ok');
                return res.json();
            })
            .then(data => {
                let incoming = data.employees || [];
                if (incoming.length < 10) {
                    const fallback = generateFallbackStaff();
                    incoming = incoming.concat(fallback.slice(incoming.length));
                }
                staffList = incoming;
                filteredList = [...staffList];
                loadingSpinner.style.display = 'none';
                tableElem.style.display = 'table';
                renderTable();
            })
            .catch(err => {
                console.warn('API fetch warning, using fallback data:', err);
                staffList = generateFallbackStaff();
                filteredList = [...staffList];
                loadingSpinner.style.display = 'none';
                tableElem.style.display = 'table';
                renderTable();
            });
    }, 500);

    function renderTable() {
        tbody.innerHTML = '';
        const totalItems = filteredList.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage) || 1;

        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        const start = (currentPage - 1) * itemsPerPage;
        const pageItems = filteredList.slice(start, start + itemsPerPage);

        if (pageItems.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Ничего не найдено.</td></tr>';
            paginationNav.innerHTML = '';
            return;
        }

        pageItems.forEach(emp => {
            const tr = document.createElement('tr');
            tr.className = 'staff-row-selectable';

            const isChecked = selectedEmployeeIds.has(emp.id);

            tr.innerHTML = `
                <td style="text-align: center;" onclick="event.stopPropagation();">
                    <input type="checkbox" class="staff-row-check" data-id="${emp.id}" ${isChecked ? 'checked' : ''} />
                </td>
                <td class="staff-avatar-cell"><img src="${emp.avatar}" alt="Фото" /></td>
                <td><strong>${emp.fio}</strong></td>
                <td>${emp.info}</td>
                <td>${emp.phone}</td>
                <td>${emp.email}</td>
            `;

            const chk = tr.querySelector('.staff-row-check');
            chk.addEventListener('change', () => {
                if (chk.checked) {
                    selectedEmployeeIds.add(emp.id);
                } else {
                    selectedEmployeeIds.delete(emp.id);
                    if (checkAllBox) checkAllBox.checked = false;
                }
                updateCheckAllState(pageItems);
            });

            tr.addEventListener('click', () => {
                showDetailCard(emp);
            });

            tbody.appendChild(tr);
        });

        renderPagination(totalPages);
        updateSortIcons();
        updateCheckAllState(pageItems);
    }

    function renderPagination(totalPages) {
        paginationNav.innerHTML = '';
        if (totalPages <= 1) return;

        const prevBtn = document.createElement('button');
        prevBtn.type = 'button';
        prevBtn.className = 'client-page-btn';
        prevBtn.innerHTML = '&larr; Назад';
        prevBtn.disabled = currentPage === 1;
        prevBtn.onclick = () => { currentPage--; renderTable(); };
        paginationNav.appendChild(prevBtn);

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `client-page-btn ${i === currentPage ? 'active' : ''}`;
            btn.textContent = i;
            btn.onclick = () => { currentPage = i; renderTable(); };
            paginationNav.appendChild(btn);
        }

        const nextBtn = document.createElement('button');
        nextBtn.type = 'button';
        nextBtn.className = 'client-page-btn';
        nextBtn.innerHTML = 'Вперед &rarr;';
        nextBtn.disabled = currentPage === totalPages;
        nextBtn.onclick = () => { currentPage++; renderTable(); };
        paginationNav.appendChild(nextBtn);
    }

    tableElem.querySelectorAll('thead th[data-column]').forEach(th => {
        th.addEventListener('click', () => {
            const col = th.dataset.column;
            if (sortColumn === col) {
                sortAsc = !sortAsc;
            } else {
                sortColumn = col;
                sortAsc = true;
            }

            filteredList.sort((a, b) => {
                const valA = (a[sortColumn] || '').toLowerCase();
                const valB = (b[sortColumn] || '').toLowerCase();
                if (valA < valB) return sortAsc ? -1 : 1;
                if (valA > valB) return sortAsc ? 1 : -1;
                return 0;
            });

            renderTable();
        });
    });

    function updateSortIcons() {
        tableElem.querySelectorAll('thead th[data-column]').forEach(th => {
            const icon = th.querySelector('.sort-icon');
            if (icon) {
                if (th.dataset.column === sortColumn) {
                    icon.textContent = sortAsc ? ' ▲' : ' ▼';
                } else {
                    icon.textContent = ' ⇅';
                }
            }
        });
    }

    function showDetailCard(emp) {
        const detailCard = document.getElementById('staff-detail-view-card');
        if (!detailCard) return;
        document.getElementById('detail-card-img').src = emp.avatar;
        document.getElementById('detail-card-fio').textContent = emp.fio;
        document.getElementById('detail-card-info').textContent = emp.info;
        document.getElementById('detail-card-phone').textContent = emp.phone;
        document.getElementById('detail-card-email').textContent = emp.email;
        detailCard.style.display = 'block';
        detailCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function updateCheckAllState(currentPageItems) {
        if (!checkAllBox || currentPageItems.length === 0) return;
        const allOnPageChecked = currentPageItems.every(emp => selectedEmployeeIds.has(emp.id));
        checkAllBox.checked = allOnPageChecked;
    }

    if (checkAllBox) {
        checkAllBox.addEventListener('change', () => {
            const start = (currentPage - 1) * itemsPerPage;
            const pageItems = filteredList.slice(start, start + itemsPerPage);

            pageItems.forEach(emp => {
                if (checkAllBox.checked) {
                    selectedEmployeeIds.add(emp.id);
                } else {
                    selectedEmployeeIds.delete(emp.id);
                }
            });

            tbody.querySelectorAll('.staff-row-check').forEach(chk => {
                chk.checked = checkAllBox.checked;
            });
        });
    }

    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', () => {
            tableElem.style.display = 'none';
            loadingSpinner.style.display = 'block';

            setTimeout(() => {
                const query = searchInput.value.trim().toLowerCase();
                if (!query) {
                    filteredList = [...staffList];
                } else {
                    filteredList = staffList.filter(emp =>
                        emp.fio.toLowerCase().includes(query) ||
                        emp.info.toLowerCase().includes(query) ||
                        emp.phone.toLowerCase().includes(query) ||
                        emp.email.toLowerCase().includes(query)
                    );
                }
                currentPage = 1;
                loadingSpinner.style.display = 'none';
                tableElem.style.display = 'table';
                renderTable();
            }, 400);
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            searchInput.value = '';
            filteredList = [...staffList];
            currentPage = 1;
            renderTable();
        });
    }

    const awardBtn = document.getElementById('award-bonus-btn');
    const bonusBox = document.getElementById('bonus-order-box');
    const bonusText = document.getElementById('bonus-order-text');

    if (awardBtn) {
        awardBtn.addEventListener('click', () => {
            const selectedStaffMembers = staffList.filter(emp => selectedEmployeeIds.has(emp.id));

            if (selectedStaffMembers.length === 0) {
                alert('Пожалуйста, отметьте галочками сотрудников для премирования (можно выбрать на разных страницах пагинации)!');
                return;
            }

            tableElem.style.display = 'none';
            loadingSpinner.style.display = 'block';
            if (bonusBox) bonusBox.style.display = 'none';

            setTimeout(() => {
                loadingSpinner.style.display = 'none';
                tableElem.style.display = 'table';

                const dateStr = new Date().toLocaleDateString('ru-RU');
                if (bonusText) {
                    bonusText.innerHTML = `
                        <p><strong>ПРИКАЗ № ${Math.floor(Math.random() * 900 + 100)}/ПР от ${dateStr} г.</strong></p>
                        <p>За добросовестное выполнение трудовых обязанностей и высокие производственные показатели:</p>
                        <p><strong>1. НАГРАДИТЬ ДЕНЕЖНОЙ ПРЕМИЕЙ СЛЕДУЮЩИХ СОТРУДНИКОВ (Всего: ${selectedStaffMembers.length} чел.):</strong></p>
                        <ul>
                            ${selectedStaffMembers.map(emp => `<li><strong>${emp.fio}</strong> (${emp.info}) — в размере 100% оклада.</li>`).join('')}
                        </ul>
                        <p><em>Основание: Решение генерального директора фабрики «Toy Factory».</em></p>
                    `;
                }
                if (bonusBox) {
                    bonusBox.style.display = 'block';
                    bonusBox.scrollIntoView({ behavior: 'smooth' });
                }
            }, 450);
        });
    }

    initStaffAddFormValidation((newEmployee) => {
        staffList.unshift(newEmployee);
        filteredList = [...staffList];
        currentPage = 1;
        renderTable();
        alert(`Сотрудник ${newEmployee.fio} успешно добавлен в реестр!`);
    });
}

function initStaffAddFormValidation(onSuccessAdd) {
    const toggleBtn = document.getElementById('toggle-add-staff-form-btn');
    const formBox = document.getElementById('staff-add-form-wrapper');
    const form = document.getElementById('staff-create-form');
    const cancelBtn = document.getElementById('btn-cancel-staff');
    const submitBtn = document.getElementById('btn-submit-staff');

    const inpFio = document.getElementById('inp-fio');
    const inpEmail = document.getElementById('inp-email');
    const inpPhone = document.getElementById('inp-phone');
    const inpAvatar = document.getElementById('inp-avatar');
    const inpInfo = document.getElementById('inp-info');

    const errPhone = document.getElementById('err-phone');
    const errAvatar = document.getElementById('err-avatar');

    toggleBtn.addEventListener('click', () => {
        formBox.style.display = formBox.style.display === 'block' ? 'none' : 'block';
    });

    cancelBtn.addEventListener('click', () => {
        formBox.style.display = 'none';
    });


    function validateUrl(url) {

        const regex = /^https?:\/\/.+\.(php|html)$/i;
        return regex.test(url.trim());
    }


    function validatePhone(phone) {

        const regex = /^(\+375|8)\s*\(?\s*\d{2}\s*\)?[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}$/;
        return regex.test(phone.trim());
    }

    function checkFormValidity() {
        const isUrlValid = validateUrl(inpAvatar.value);
        const isPhoneValid = validatePhone(inpPhone.value);
        const isFilled = inpFio.value.trim() && inpEmail.value.trim() && inpInfo.value.trim();


        if (inpAvatar.value.length > 0) {
            if (!isUrlValid) {
                inpAvatar.classList.add('input-invalid');
                errAvatar.textContent = 'Ошибка: URL должен начинаться с http:// или https:// и заканчиваться на .php или .html'
            } else {
                inpAvatar.classList.remove('input-invalid');
                errAvatar.textContent = '';
            }
        } else {
            inpAvatar.classList.remove('input-invalid');
            errAvatar.textContent = '';
        }


        if (inpPhone.value.length > 0) {
            if (!isPhoneValid) {
                inpPhone.classList.add('input-invalid');
                errPhone.textContent = 'Ошибка формата: пример +375 (29) 111-22-33 или 80291112233';
            } else {
                inpPhone.classList.remove('input-invalid');
                errPhone.textContent = '';
            }
        } else {
            inpPhone.classList.remove('input-invalid');
            errPhone.textContent = '';
        }


        submitBtn.disabled = !(isUrlValid && isPhoneValid && isFilled);
    }

    [inpFio, inpEmail, inpPhone, inpAvatar, inpInfo].forEach(input => {
        input.addEventListener('input', checkFormValidity);
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (submitBtn.disabled) return;

        const newEmp = {
            id: 'client-' + Date.now(),
            fio: inpFio.value.trim(),
            avatar: inpAvatar.value.trim(),
            info: inpInfo.value.trim(),
            phone: inpPhone.value.trim(),
            email: inpEmail.value.trim()
        };

        onSuccessAdd(newEmp);
        form.reset();
        checkFormValidity();
        formBox.style.display = 'none';
    });
}


document.addEventListener('DOMContentLoaded', () => {
    initInteractiveStaffTable();
});


function initScrollConveyorAnimation() {
    const section = document.getElementById('toy-conveyor-section');
    const track = document.getElementById('conveyor-track');
    const statusText = document.getElementById('conveyor-status-indicator');
    if (!section || !track) return;

    let prevScrollY = window.pageYOffset || document.documentElement.scrollTop;

    function moveConveyor() {

        const currentScrollY = window.pageYOffset || document.documentElement.scrollTop;
        const rect = section.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;


        if (rect.bottom > 0 && rect.top < windowHeight) {


            const isScrollingDown = currentScrollY >= prevScrollY;
            if (statusText) {
                statusText.innerHTML = isScrollingDown
                    ? '▶ <strong>Конвейер запущен вперед:</strong> транспортировка партии игрушек...'
                    : '◀ <strong>Реверс конвейера:</strong> движение ленты в обратном направлении...';
            }


            const totalRange = windowHeight + rect.height;
            const currentOffset = windowHeight - rect.top;
            const progress = Math.min(Math.max(currentOffset / totalRange, 0), 1);


            const totalMoveDistance = 650;
            const currentTranslate = progress * totalMoveDistance;


            track.style.transform = `translate3d(-${currentTranslate.toFixed(1)}px, 0, 0)`;
        }

        prevScrollY = currentScrollY;
    }


    window.addEventListener('scroll', moveConveyor, {passive: true});


    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        mainContent.addEventListener('scroll', moveConveyor, {passive: true});
    }


    moveConveyor();
}


document.addEventListener('DOMContentLoaded', () => {
    initScrollConveyorAnimation();
});