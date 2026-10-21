// FitRadar BG Client Application Logic

let state = {
    category: "all",
    store: "all",
    query: "",
    sortBy: "price_per_100g_asc",
    stackItems: [
        { category: "Суроватъчен изолат", name: "Суроватъчен изолат" },
        { category: "Креатин", name: "Креатин монохидрат" }
    ]
};

// Store metadata with brand colors
const storeMeta = {
    silabg: { name: "Сила БГ", color: "bg-red-500/10 text-red-400 border-red-500/20" },
    workoutbg: { name: "Workout.bg", color: "bg-blue-500/10 text-blue-400 border-blue-500/20" },
    gymbeam: { name: "GymBeam BG", color: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
    fitnes1: { name: "Фитнес 1", color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
    myprotein: { name: "MyProtein BG", color: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20" },
    decathlon: { name: "Декатлон", color: "bg-sky-500/10 text-sky-400 border-sky-500/20" }
};

document.addEventListener("DOMContentLoaded", () => {
    console.log("[FitRadar BG] Initializing frontend application...");
    initEventListeners();
    fetchProducts();
    renderStackItems();
    executeBasketCompare();
});

function initEventListeners() {
    const searchInput = document.getElementById("searchInput");
    let debounceTimer;
    searchInput.addEventListener("input", (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            state.query = e.target.value.trim();
            fetchProducts();
        }, 250);
    });

    const sortSelect = document.getElementById("sortSelect");
    sortSelect.addEventListener("change", (e) => {
        state.sortBy = e.target.value;
        fetchProducts();
    });
}

function switchTab(tabName) {
    const tabs = ["catalog", "basket", "advisor"];
    tabs.forEach(t => {
        const content = document.getElementById(`tab-${t}`);
        const btn = document.getElementById(`tab-btn-${t}`);
        if (content) {
            if (t === tabName) {
                content.classList.remove("hidden");
                content.classList.add("block");
            } else {
                content.classList.add("hidden");
                content.classList.remove("block");
            }
        }
        if (btn) {
            if (t === tabName) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        }
    });

    if (tabName === "basket") {
        executeBasketCompare();
    }
}

function setCategory(cat) {
    state.category = cat;
    document.querySelectorAll(".cat-pill").forEach(p => {
        if (p.textContent.trim() === cat || (cat === "all" && p.textContent.includes("Всички"))) {
            p.classList.add("active");
        } else {
            p.classList.remove("active");
        }
    });
    fetchProducts();
}

function setStore(store) {
    state.store = store;
    document.querySelectorAll(".store-pill").forEach(p => {
        const onclickAttr = p.getAttribute("onclick") || "";
        if (onclickAttr.includes(`'${store}'`)) {
            p.classList.add("active");
        } else {
            p.classList.remove("active");
        }
    });
    fetchProducts();
}

async function fetchProducts() {
    const grid = document.getElementById("productGrid");
    const countElem = document.getElementById("productCount");

    grid.innerHTML = `
        <div class="col-span-full py-12 text-center text-slate-500">
            <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-emerald-400"></i>
            <p class="text-xs">Зареждане и сравняване на цени...</p>
        </div>
    `;

    try {
        const params = new URLSearchParams({
            q: state.query,
            category: state.category,
            store: state.store,
            sort_by: state.sortBy
        });

        const res = await fetch(`/api/products?${params}`);
        const data = await res.json();

        if (data.status === "success") {
            countElem.textContent = data.total;
            renderProducts(data.products);
        } else {
            grid.innerHTML = `<div class="col-span-full py-8 text-center text-red-400 text-xs">Грешка при зареждане на офертите.</div>`;
        }
    } catch (err) {
        console.error(err);
        grid.innerHTML = `<div class="col-span-full py-8 text-center text-red-400 text-xs">Грешка при връзка със сървъра.</div>`;
    }
}

function renderProducts(products) {
    const grid = document.getElementById("productGrid");

    if (products.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full py-16 text-center text-slate-500">
                <i class="fa-solid fa-box-open text-4xl mb-3 text-slate-600"></i>
                <h3 class="text-base font-bold text-slate-300">Няма открити оферти</h3>
                <p class="text-xs text-slate-500 mt-1">Опитайте с други ключови думи или премахнете филтрите.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = products.map(p => {
        const meta = storeMeta[p.store_code] || { name: p.store_name, color: "bg-slate-800 text-slate-300 border-slate-700" };
        const priceEur = p.price_eur ? p.price_eur : (p.price_bgn / 1.95583);
        const oldPriceEur = p.old_price_eur ? p.old_price_eur : (p.old_price_bgn ? p.old_price_bgn / 1.95583 : null);
        const price100gEur = p.price_per_100g_eur ? p.price_per_100g_eur : (p.price_per_100g ? p.price_per_100g / 1.95583 : null);
        const priceServingEur = p.price_per_serving_eur ? p.price_per_serving_eur : (p.price_per_serving ? p.price_per_serving / 1.95583 : null);

        const pricePer100gFormatted = price100gEur ? `€${price100gEur.toFixed(2)}` : "н/д";
        const pricePerServingFormatted = priceServingEur ? `€${priceServingEur.toFixed(2)}` : null;
        const discountBadge = p.discount_pct > 0 
            ? `<span class="bg-red-500 text-white font-extrabold text-[11px] px-2 py-0.5 rounded-full shadow-sm">-${p.discount_pct}%</span>` 
            : "";

        return `
            <div class="product-card-hover rounded-2xl bg-slate-900 border border-slate-800 p-4 flex flex-col justify-between relative overflow-hidden">
                <!-- Top Header: Store badge & Discount -->
                <div>
                    <div class="flex items-center justify-between gap-2 mb-3">
                        <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${meta.color}">
                            ${p.store_name}
                        </span>
                        ${discountBadge}
                    </div>

                    <!-- Brand & Clean Title -->
                    <div class="text-[11px] uppercase tracking-wider font-semibold text-emerald-400 mb-1">
                        ${p.brand} • <span class="text-slate-400 font-normal">${p.category}</span>
                    </div>
                    <h3 class="text-sm font-bold text-slate-100 line-clamp-2 leading-snug mb-3" title="${p.raw_title}">
                        ${p.clean_title}
                    </h3>

                    <!-- Specs Pills (Weight, Servings, Flavor) -->
                    <div class="flex flex-wrap gap-1.5 mb-4 text-[11px] text-slate-400">
                        ${p.weight_g ? `<span class="bg-slate-950 px-2 py-0.5 rounded border border-slate-800"><i class="fa-solid fa-weight-scale mr-1 text-slate-500"></i>${p.weight_g >= 1000 ? (p.weight_g/1000).toFixed(2) + ' кг' : p.weight_g + ' г'}</span>` : ''}
                        ${p.servings ? `<span class="bg-slate-950 px-2 py-0.5 rounded border border-slate-800"><i class="fa-solid fa-droplet mr-1 text-slate-500"></i>${p.servings} дози</span>` : ''}
                        ${p.flavor && p.flavor !== 'Неуточнен' ? `<span class="bg-slate-950 px-2 py-0.5 rounded border border-slate-800 text-slate-300 truncate max-w-[150px]"><i class="fa-solid fa-tag mr-1 text-slate-500"></i>${p.flavor}</span>` : ''}
                    </div>
                </div>

                <!-- Bottom Section: Normalized Value Metric & Final Price -->
                <div class="pt-3 border-t border-slate-800/80">
                    <!-- Key Normalized Value Highlight -->
                    <div class="bg-emerald-950/30 border border-emerald-500/20 rounded-xl p-2.5 mb-3 flex items-center justify-between">
                        <div>
                            <div class="text-[10px] uppercase font-bold text-emerald-400">Цена за 100g (€)</div>
                            <div class="text-base font-black text-emerald-300">${pricePer100gFormatted}</div>
                        </div>
                        ${pricePerServingFormatted ? `
                            <div class="text-right">
                                <div class="text-[10px] uppercase font-semibold text-slate-400">Цена за доза</div>
                                <div class="text-xs font-bold text-slate-200">${pricePerServingFormatted}</div>
                            </div>
                        ` : ''}
                    </div>

                    <!-- Final Sticker Price & Shop Link -->
                    <div class="flex items-center justify-between">
                        <div>
                            ${oldPriceEur ? `<span class="text-xs text-slate-500 line-through block">€${oldPriceEur.toFixed(2)}</span>` : ''}
                            <span class="text-xl font-extrabold text-white tracking-tight">€${priceEur.toFixed(2)} <span class="text-[11px] font-normal text-slate-400 block">${p.price_bgn.toFixed(2)} лв.</span></span>
                        </div>
                        <a href="${p.product_url}" target="_blank" rel="noopener noreferrer" 
                           class="px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-800 hover:bg-emerald-600 text-white transition flex items-center space-x-1.5 shadow-sm group">
                            <span>Виж в магазина</span>
                            <i class="fa-solid fa-arrow-up-right-from-square text-[10px] group-hover:translate-x-0.5 transition-transform"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

// ==================== STAGE 4: SMART STACK (BASKET) ====================

const AVAILABLE_STACK_CATEGORIES = [
    { id: "Суроватъчен изолат", label: "Суроватъчен изолат (Whey Isolate)" },
    { id: "Суроватъчен концентрат", label: "Суроватъчен концентрат (Whey Blend)" },
    { id: "Креатин", label: "Креатин монохидрат" },
    { id: "Предтренировъчни", label: "Предтренировъчен буустър (Pre-workout)" },
    { id: "Витамини и минерали", label: "Мултивитаминен комплекс" }
];

function renderStackItems() {
    const container = document.getElementById("stackItemsList");
    container.innerHTML = state.stackItems.map((item, idx) => `
        <div class="flex items-center gap-2 bg-slate-900 p-2.5 rounded-lg border border-slate-800">
            <span class="w-6 h-6 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center text-xs font-bold">${idx + 1}</span>
            <select onchange="updateStackItem(${idx}, this.value)" class="bg-slate-950 border border-slate-700 text-xs sm:text-sm text-slate-200 rounded-lg px-2.5 py-1.5 flex-1 focus:outline-none focus:border-indigo-500">
                ${AVAILABLE_STACK_CATEGORIES.map(cat => `
                    <option value="${cat.id}" ${cat.id === item.category ? 'selected' : ''}>${cat.label}</option>
                `).join("")}
            </select>
            <button onclick="removeStackItem(${idx})" class="text-slate-500 hover:text-red-400 px-2 py-1 text-xs transition">
                <i class="fa-solid fa-trash-can"></i>
            </button>
        </div>
    `).join("");
}

function addStackItem() {
    state.stackItems.push({ category: "Предтренировъчни", name: "Предтренировъчни" });
    renderStackItems();
}

function removeStackItem(idx) {
    if (state.stackItems.length > 1) {
        state.stackItems.splice(idx, 1);
        renderStackItems();
    }
}

function updateStackItem(idx, val) {
    state.stackItems[idx].category = val;
}

function loadStackPreset(type) {
    if (type === 'basic') {
        state.stackItems = [
            { category: "Суроватъчен концентрат" },
            { category: "Креатин" }
        ];
    } else if (type === 'full') {
        state.stackItems = [
            { category: "Суроватъчен изолат" },
            { category: "Креатин" },
            { category: "Предтренировъчни" }
        ];
    } else if (type === 'health') {
        state.stackItems = [
            { category: "Суроватъчен изолат" },
            { category: "Витамини и минерали" }
        ];
    }
    renderStackItems();
    executeBasketCompare();
}

async function executeBasketCompare() {
    const container = document.getElementById("basketResultsContainer");
    container.innerHTML = `
        <div class="py-12 text-center text-slate-500">
            <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-indigo-400"></i>
            <p class="text-xs">Изчисляване на цената на цялата кошница по магазини и прагове за доставка...</p>
        </div>
    `;

    try {
        const res = await fetch("/api/basket/compare", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ items: state.stackItems })
        });
        const data = await res.json();

        if (data.status === "success") {
            renderBasketResults(data.result);
        } else {
            container.innerHTML = `<div class="p-4 bg-red-900/20 text-red-400 text-xs rounded-xl">Грешка при сравнение на кошниците.</div>`;
        }
    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="p-4 bg-red-900/20 text-red-400 text-xs rounded-xl">Грешка при връзка със сървъра.</div>`;
    }
}

function renderBasketResults(result) {
    const container = document.getElementById("basketResultsContainer");
    const stores = result.store_comparisons;
    const bestSingle = result.best_single_store;
    const split = result.split_basket;

    let html = `
        <!-- Decision Support Banner -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Best Single Store -->
            <div class="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-950/40 border border-indigo-500/30">
                <div class="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-indigo-400 mb-1">
                    <i class="fa-solid fa-crown text-amber-400"></i>
                    <span>Най-евтина обща поръчка от един магазин:</span>
                </div>
                ${bestSingle ? `
                    <div class="text-2xl font-black text-white mb-1">${bestSingle.store_info.name}</div>
                    <div class="text-3xl font-extrabold text-emerald-400 mb-1">€${bestSingle.total_eur.toFixed(2)} <span class="text-xs font-normal text-slate-400">(${bestSingle.total.toFixed(2)} лв.)</span></div>
                    <div class="text-xs text-slate-300">
                        ${bestSingle.qualifies_free_shipping ? '✅ <strong>Безплатна доставка</strong> (надвишава прага от €' + (bestSingle.store_info.free_shipping_threshold_eur || 35.79).toFixed(2) + ')' : '⚠️ Доставка: €' + bestSingle.shipping_eur.toFixed(2) + ' (' + bestSingle.shipping.toFixed(2) + ' лв.)'}
                    </div>
                ` : `<p class="text-xs text-slate-400">Нито един магазин не предлага всички избрани продукти едновременно.</p>`}
            </div>

            <!-- Optimal Split Basket -->
            <div class="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-emerald-950/40 border border-emerald-500/30">
                <div class="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-emerald-400 mb-1">
                    <i class="fa-solid fa-shuffle text-emerald-400"></i>
                    <span>Оптимална разделена поръчка (Абсолютен минимум):</span>
                </div>
                <div class="text-2xl font-black text-white mb-1">Комбинирано пазаруване</div>
                <div class="text-3xl font-extrabold text-cyan-400 mb-1">€${split.subtotal_eur.toFixed(2)} <span class="text-xs font-normal text-slate-400">(${split.subtotal_bgn.toFixed(2)} лв.)</span></div>
                <div class="text-xs text-slate-300">
                    Купувайки всеки артикул от най-евтиния магазин в България, цената на продуктите пада с 
                    <strong class="text-emerald-400">€${bestSingle ? (bestSingle.subtotal_eur - split.subtotal_eur).toFixed(2) : 0}</strong>.
                </div>
            </div>
        </div>

        <!-- Store Comparison Cards Grid -->
        <div>
            <h3 class="text-base font-bold text-white mb-3">Подробно разпределение по магазини (в Евро €):</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                ${stores.map(s => {
                    const isWinner = bestSingle && bestSingle.store_info.code === s.store_info.code;
                    return `
                        <div class="p-4 rounded-xl bg-slate-900 border ${isWinner ? 'border-emerald-500 ring-1 ring-emerald-500/50 shadow-lg shadow-emerald-500/10' : 'border-slate-800'} flex flex-col justify-between">
                            <div>
                                <div class="flex items-center justify-between mb-2">
                                    <h4 class="text-sm font-bold text-white">${s.store_info.name}</h4>
                                    ${isWinner ? '<span class="bg-emerald-500 text-slate-950 text-[10px] font-black px-2 py-0.5 rounded-full uppercase">Победител</span>' : ''}
                                </div>

                                <!-- Items included -->
                                <div class="space-y-1.5 mb-3">
                                    ${s.items.map(it => `
                                        <div class="text-xs flex justify-between items-center text-slate-300 bg-slate-950 p-1.5 rounded border border-slate-800/80">
                                            <span class="truncate pr-2 font-medium">${it.clean_title}</span>
                                            <span class="font-bold whitespace-nowrap text-white">€${(it.price_eur || it.price_bgn/1.95583).toFixed(2)}</span>
                                        </div>
                                    `).join("")}
                                    ${s.missing_items.map(m => `
                                        <div class="text-xs flex justify-between items-center text-red-400/80 bg-red-950/20 p-1.5 rounded border border-red-900/30">
                                            <span>Няма наличност: ${m}</span>
                                            <span>—</span>
                                        </div>
                                    `).join("")}
                                </div>
                            </div>

                            <!-- Cost Breakdown -->
                            <div class="pt-3 border-t border-slate-800 text-xs space-y-1">
                                <div class="flex justify-between text-slate-400">
                                    <span>Стойност на продукти:</span>
                                    <span>€${s.subtotal_eur.toFixed(2)} <span class="text-[10px] text-slate-500">(${s.subtotal.toFixed(2)} лв)</span></span>
                                </div>
                                <div class="flex justify-between text-slate-400">
                                    <span>Доставка:</span>
                                    <span>${s.qualifies_free_shipping ? '<span class="text-emerald-400 font-bold">БЕЗПЛАТНА</span>' : '€' + s.shipping_eur.toFixed(2)}</span>
                                </div>
                                <div class="flex justify-between text-base font-black text-white pt-2 border-t border-slate-800/80">
                                    <span>Обща сума:</span>
                                    <span class="${isWinner ? 'text-emerald-400' : 'text-white'}">€${s.total_eur.toFixed(2)} <span class="text-xs font-normal text-slate-400">(${s.total.toFixed(2)} лв)</span></span>
                                </div>
                            </div>
                        </div>
                    `;
                }).join("")}
            </div>
        </div>
    `;

    container.innerHTML = html;
}

// ==================== STAGE 5: CONVERSATIONAL AI ADVISOR ====================

function askPreset(promptText) {
    document.getElementById("advisorInput").value = promptText;
    document.getElementById("advisorForm").dispatchEvent(new Event("submit"));
}

async function handleAdvisorSubmit(e) {
    e.preventDefault();
    const input = document.getElementById("advisorInput");
    const outputContainer = document.getElementById("advisorOutput");
    const query = input.value.trim();

    if (!query) return;

    outputContainer.classList.remove("hidden");
    outputContainer.innerHTML = `
        <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center">
            <i class="fa-solid fa-wand-magic-sparkles fa-spin text-2xl text-purple-400 mb-2"></i>
            <p class="text-xs text-slate-400">Анализиране на въпроса и търсене в базата данни...</p>
        </div>
    `;

    try {
        const res = await fetch("/api/advisor", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        const data = await res.json();

        if (data.status === "success") {
            const adv = data.result;
            outputContainer.innerHTML = `
                <div class="p-6 rounded-2xl bg-slate-900 border border-purple-500/30 space-y-4">
                    <div class="flex items-center space-x-2 text-xs font-bold uppercase text-purple-400">
                        <i class="fa-solid fa-robot"></i>
                        <span>Отговор на FitRadar AI:</span>
                    </div>
                    <p class="text-sm text-slate-200 leading-relaxed">${adv.summary}</p>
                    <div class="p-3.5 rounded-xl bg-purple-950/30 border border-purple-500/20 text-xs sm:text-sm text-purple-200">
                        ${adv.recommendation}
                    </div>

                    <div class="pt-2">
                        <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Подбрани продукти:</div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            ${adv.products.map(p => {
                                const pEur = p.price_eur ? p.price_eur : (p.price_bgn / 1.95583);
                                const p100gEur = p.price_per_100g_eur ? p.price_per_100g_eur : (p.price_per_100g ? p.price_per_100g / 1.95583 : null);
                                return `
                                    <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex justify-between items-center gap-2">
                                        <div>
                                            <span class="text-[10px] text-emerald-400 font-bold block">${p.store_name} • ${p.brand}</span>
                                            <span class="text-xs font-bold text-white line-clamp-1">${p.clean_title}</span>
                                            <span class="text-[11px] text-slate-400 block">${p100gEur ? '€' + p100gEur.toFixed(2) + ' / 100g' : ''}</span>
                                        </div>
                                        <div class="text-right">
                                            <span class="text-sm font-black text-white block">€${pEur.toFixed(2)}</span>
                                            <span class="text-[10px] text-slate-500 block">${p.price_bgn.toFixed(2)} лв</span>
                                            <a href="${p.product_url}" target="_blank" rel="noopener noreferrer" class="text-[10px] text-purple-400 hover:underline">Към магазина</a>
                                        </div>
                                    </div>
                                `;
                            }).join("")}
                        </div>
                    </div>
                </div>
            `;
        }
    } catch (err) {
        console.error(err);
        outputContainer.innerHTML = `<div class="p-4 bg-red-900/20 text-red-400 text-xs rounded-xl">Възникна грешка при обработка на въпроса.</div>`;
    }
}
