<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>شركة سما كربلاء - التقرير التنفيذي</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* ================= الستايلات الأساسية ================= */
        body { font-family: 'Cairo', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; transition: background-color 0.3s, color 0.3s; }
        ::-webkit-scrollbar { height: 8px; width: 8px; }
        ::-webkit-scrollbar-track { background: #1e293b; border-radius: 4px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }
        
        /* ================= أزرار الفلاتر والإكسل ================= */
        .filter-btn { background-color: transparent; border: 1px solid #475569; color: #cbd5e1; padding: 4px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; transition: all 0.2s; }
        .filter-btn:hover { background-color: #334155; border-color: #64748b; }
        .filter-btn.active { background-color: #0f766e; border-color: #14b8a6; color: #ffffff; }
        .metric-btn { background-color: transparent; border: 1px solid #475569; color: #94a3b8; padding: 6px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; transition: all 0.2s; display: flex; align-items: center; gap: 6px; }
        .metric-btn.active { background-color: #334155; border-color: #cca344; color: #cca344; }
        .btn-excel { border: 1px solid #059669; color: #34d399; background-color: transparent; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; display: flex; align-items: center; gap: 4px; transition: all 0.2s; cursor: pointer; }
        .btn-excel:hover { background-color: #059669; color: #ffffff; }
        .report-select { background-color: #0f172a; border: 1px solid #334155; color: #94a3b8; font-size: 0.75rem; padding: 4px 8px; border-radius: 4px; outline: none; }
        .report-select:focus { border-color: #cca344; }

        /* ================= ستايل الجداول ================= */
        .advanced-table th { background-color: #1e293b; position: sticky; top: 0; z-index: 10; font-size: 0.75rem; border-bottom: 2px solid #334155; padding: 12px 8px;}
        .advanced-table td { padding: 10px 8px; font-size: 0.8rem; border-bottom: 1px solid #1e293b; }
        .advanced-table tr:hover { background-color: #1e293b80; }
        .heatmap-table th { background-color: #1e293b; border: 1px solid #334155; padding: 12px; font-size: 0.85rem; font-weight: 700; }
        .heatmap-table td { border: 1px solid #334155; padding: 8px; font-size: 0.85rem; transition: all 0.2s; }
        .heatmap-table td:hover { filter: brightness(1.2); }
        .badge-A { background: #22c55e30; color: #4ade80; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
        .badge-B { background: #eab30830; color: #fde047; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
        .badge-C { background: #ef444430; color: #f87171; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
        .text-up { color: #4ade80; font-weight: bold; }
        .text-down { color: #f87171; font-weight: bold; }

        /* ================= شاشة الدخول ================= */
        #loginOverlay { position: fixed; inset: 0; background-color: #18202f; z-index: 50; display: flex; align-items: center; justify-content: center; background-image: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%); transition: background 0.3s; }
        .login-box { background-color: #1b2431; padding: 2.5rem; border: 1px solid #334155; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); width: 100%; max-width: 360px; border-radius: 12px; position: relative; transition: all 0.3s;}
        .login-top-bar { position: absolute; top: 1rem; right: 1rem; display: flex; gap: 8px; }
        .login-icon-btn { background: transparent; border: 1px solid #334155; color: #cbd5e1; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; cursor: pointer; transition: 0.2s;}
        .login-icon-btn:hover { background: #334155; }
        .login-input { width: 100%; padding: 12px 16px; margin-bottom: 14px; background-color: #111827; border: 1px solid #334155; color: white; border-radius: 8px; font-size: 0.9rem; transition: all 0.2s;}
        .login-input:focus { border-color: #cca344; outline: none; }
        .btn-login { width: 100%; background-color: #cca344; color: #ffffff; font-weight: bold; font-size: 1.1rem; padding: 12px; border-radius: 8px; margin-top: 10px; transition: all 0.2s; border: none; cursor: pointer;}
        .btn-login:hover { background-color: #b38b34; }
        .checkbox-custom { width: 1.1rem; height: 1.1rem; accent-color: #cca344; cursor: pointer; }

        /* ================= الوضع النهاري (Light Mode) ================= */
        body.light-theme { background-color: #f8fafc; color: #0f172a; }
        body.light-theme .bg-slate-800 { background-color: #ffffff; border-color: #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        body.light-theme .bg-\[\#1a2332\], body.light-theme .bg-\[\#111827\] { background-color: #f1f5f9; border-color: #e2e8f0;}
        body.light-theme .text-white { color: #0f172a; }
        body.light-theme .text-slate-400 { color: #64748b; }
        body.light-theme .text-slate-300 { color: #475569; }
        body.light-theme .text-slate-200 { color: #334155; }
        body.light-theme .border-slate-700 { border-color: #e2e8f0; }
        body.light-theme .border-slate-600 { border-color: #cbd5e1; }
        body.light-theme .bg-slate-900 { background-color: #ffffff; color: #0f172a; border-color: #cbd5e1;}
        body.light-theme .advanced-table th { background-color: #e2e8f0; color:#0f172a; border-bottom: 2px solid #cbd5e1; }
        body.light-theme .advanced-table td { border-bottom: 1px solid #e2e8f0; }
        body.light-theme .advanced-table tr:hover { background-color: #f8fafc; }
        body.light-theme .heatmap-table th { background-color: #e2e8f0; color:#0f172a; border-color: #cbd5e1; }
        body.light-theme .heatmap-table td { border-color: #cbd5e1; }
        body.light-theme .report-select { background-color: #ffffff; border-color: #cbd5e1; color: #0f172a; }
        body.light-theme #loginOverlay { background: #f8fafc; }
        body.light-theme .login-box { background-color: #ffffff; border-color: #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); }
        body.light-theme .login-input { background-color: #f1f5f9; border-color: #cbd5e1; color: #0f172a; }
        body.light-theme .login-icon-btn { color: #0f172a; border-color: #cbd5e1; }
        body.light-theme .login-icon-btn:hover { background: #e2e8f0; }
    </style>
</head>
<body class="w-full min-h-screen">

    <!-- ================= شاشة تسجيل الدخول ================= -->
    <div id="loginOverlay">
        <div class="login-box">
            <div class="login-top-bar" dir="ltr">
                <button onclick="toggleLang()" class="login-icon-btn">EN / ع</button>
                <button onclick="toggleTheme()" id="themeBtnLogin" class="login-icon-btn">☀️</button>
            </div>
            
            <h2 class="text-2xl font-bold text-white text-center mb-1 mt-10" data-ar="تسجيل الدخول" data-en="Login">تسجيل الدخول</h2>
            <p class="text-slate-400 text-[11px] text-center mb-6" data-ar="شركة سما كربلاء — التقرير التنفيذي" data-en="Sama Karbala — Executive Report">شركة سما كربلاء — التقرير التنفيذي</p>
            
            <input type="text" id="usernameInput" data-ar-ph="اسم المستخدم" data-en-ph="Username" placeholder="اسم المستخدم" class="login-input" dir="auto">
            <input type="password" id="passwordInput" data-ar-ph="كلمة المرور" data-en-ph="Password" placeholder="كلمة المرور" class="login-input" dir="auto" onkeypress="if(event.key === 'Enter') checkLogin()">
            
            <div class="flex items-center justify-start gap-2 mb-2 pr-1">
                <input type="checkbox" id="rememberMe" class="checkbox-custom">
                <label for="rememberMe" class="text-sm text-slate-300 cursor-pointer select-none" data-ar="تذكّرني" data-en="Remember Me">تذكّرني</label>
            </div>
            
            <button onclick="checkLogin()" class="btn-login" data-ar="دخول" data-en="Sign In">دخول</button>
            <p id="loginError" class="text-rose-500 text-sm mt-4 text-center hidden" data-ar="البيانات غير صحيحة" data-en="Invalid Credentials">البيانات غير صحيحة</p>
        </div>
    </div>

    <!-- ================= الداشبورد الرئيسي ================= -->
    <div id="mainDashboard" class="w-full max-w-[1800px] mx-auto p-3 md:p-5 hidden">
        
        <!-- الهيدر -->
        <header class="flex flex-col md:flex-row justify-between items-center gap-4 mb-4 bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl">
            <div class="flex items-center gap-4">
                <div>
                    <h1 class="text-2xl font-bold text-[#cca344]" data-ar="لوحة المبيعات والتحليل الشامل" data-en="Sales & Analytics Dashboard">لوحة المبيعات والتحليل الشامل</h1>
                    <p id="welcomeMessage" class="text-sm text-slate-400"></p>
                </div>
            </div>
            <div class="flex items-center gap-4">
                <button onclick="toggleLang()" class="login-icon-btn hidden md:block">EN / ع</button>
                <button onclick="toggleTheme()" id="themeBtnMain" class="login-icon-btn hidden md:block">☀️</button>
                <div id="status" class="bg-amber-500/10 text-amber-400 px-3 py-1.5 rounded-full text-xs font-semibold border border-amber-500/20" data-ar="جاري التحقق..." data-en="Checking...">جاري التحقق...</div>
                <button onclick="logout()" class="text-slate-400 hover:text-rose-500 text-xs font-bold underline" data-ar="تسجيل خروج" data-en="Logout">تسجيل خروج</button>
            </div>
        </header>

        <!-- نظام إدارة المستخدمين (للمدير فقط) -->
        <div id="userManagementPanel" class="bg-slate-800 p-4 rounded-xl border border-slate-700 mb-4 shadow-xl hidden">
            <h3 class="text-lg font-bold text-teal-400 mb-3" data-ar="إدارة المستخدمين للنظام" data-en="User Management">إدارة المستخدمين للنظام</h3>
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3 mb-4">
                <input type="text" id="newUsername" data-ar-ph="اسم المستخدم (إنجليزي)" data-en-ph="Username" placeholder="اسم المستخدم (إنجليزي)" class="login-input m-0">
                <input type="text" id="newName" data-ar-ph="الاسم الكامل" data-en-ph="Full Name" placeholder="الاسم الكامل" class="login-input m-0">
                <input type="password" id="newPassword" data-ar-ph="كلمة المرور" data-en-ph="Password" placeholder="كلمة المرور" class="login-input m-0">
                <select id="newRole" class="report-select w-full m-0 p-3 text-sm">
                    <option value="viewer" data-ar="مشاهد (قراءة فقط)" data-en="Viewer (Read Only)">مشاهد (قراءة فقط)</option>
                    <option value="admin" data-ar="مدير النظام (أدمن)" data-en="System Admin">مدير النظام (أدمن)</option>
                </select>
                <button onclick="addUser()" class="btn-excel bg-teal-900/30 justify-center h-full" data-ar="➕ إضافة مستخدم" data-en="➕ Add User">➕ إضافة مستخدم</button>
            </div>
            <div class="overflow-x-auto max-h-[200px] overflow-y-auto">
                <table class="w-full text-center advanced-table text-slate-300">
                    <thead><tr><th data-ar="اسم المستخدم" data-en="Username">اسم المستخدم</th><th data-ar="الاسم" data-en="Name">الاسم</th><th data-ar="الصلاحية" data-en="Role">الصلاحية</th><th data-ar="إجراء" data-en="Action">إجراء</th></tr></thead>
                    <tbody id="usersTableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- لوحة الربط (للمدير فقط) -->
        <div id="adminPanel" class="bg-slate-800 p-4 rounded-xl border border-slate-700 mb-4 shadow-xl grid-cols-1 md:grid-cols-3 gap-4 items-end hidden">
            <div>
                <button id="pickFileBtn" class="w-full bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 px-4 rounded-lg transition-all border border-slate-600 flex items-center justify-center gap-2 text-sm">
                    <span id="fileNameDisplay" class="truncate max-w-[200px]" data-ar="1. ربط ملف الإكسل المحلي (للمدير)" data-en="1. Link Local Excel (Admin)">1. ربط ملف الإكسل المحلي (للمدير)</span>
                </button>
            </div>
            <div>
                <select id="sheetSelect" onchange="parseExcelData()" class="w-full bg-slate-900 text-white text-sm p-2 rounded-lg border border-slate-700 focus:outline-none focus:border-[#cca344]">
                    <option value="" data-ar="2. اختر شيت الداتا..." data-en="2. Select Sheet...">2. اختر شيت الداتا...</option>
                </select>
            </div>
            <div>
                <button onclick="refreshData()" class="w-full bg-[#cca344] hover:bg-[#b38b34] text-white font-semibold py-2 px-4 rounded-lg transition-all shadow-lg flex items-center justify-center gap-2 text-sm" data-ar="تحديث التعديلات 🔄" data-en="Refresh Data 🔄">تحديث التعديلات 🔄</button>
            </div>
        </div>

        <!-- شريط الفلاتر الذكي -->
        <div class="bg-[#1a2332] p-4 rounded-xl border border-slate-700 mb-4 shadow-xl flex flex-col lg:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-2 order-2 lg:order-1">
                <button id="btnMetricCount" onclick="setMetric('count')" class="metric-btn"><span data-ar="صناديق" data-en="Boxes">صناديق</span> 📦</button>
                <button id="btnMetricTons" onclick="setMetric('tons')" class="metric-btn active"><span data-ar="طن" data-en="Tons">طن</span> ⚖️</button>
            </div>
            <div class="flex flex-wrap items-center justify-end gap-2 order-1 lg:order-2 flex-row-reverse w-full lg:w-auto">
                <input type="date" id="dateFrom" onchange="applyFiltersAndRender()" class="bg-slate-900 border border-slate-600 rounded px-2 py-1 text-slate-300 text-xs">
                <span class="text-slate-400 text-xs" data-ar="إلى" data-en="To">إلى</span>
                <input type="date" id="dateTo" onchange="applyFiltersAndRender()" class="bg-slate-900 border border-slate-600 rounded px-2 py-1 text-slate-300 text-xs">
                <button onclick="setDateFilter('last7', this)" class="filter-btn date-btn" data-ar="آخر 7" data-en="Last 7">آخر 7</button>
                <button onclick="setDateFilter('last30', this)" class="filter-btn date-btn" data-ar="آخر 30" data-en="Last 30">آخر 30</button>
                <button onclick="setDateFilter('thisMonth', this)" class="filter-btn date-btn" data-ar="هذا الشهر" data-en="This Month">هذا الشهر</button>
                <button onclick="setDateFilter('all', this)" class="filter-btn date-btn active" data-ar="كل الفترة" data-en="All Time">كل الفترة</button>
            </div>
        </div>

        <!-- البطاقات الإحصائية -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div class="bg-slate-800 p-4 rounded-xl border-t-4 border-t-teal-500 shadow"><p class="text-slate-400 text-xs font-semibold" data-ar="إجمالي الكمية (طن)" data-en="Total Quantity (Tons)">إجمالي الكمية (طن)</p><h3 id="totalTons" class="text-2xl font-bold text-white mt-1">0</h3></div>
            <div class="bg-slate-800 p-4 rounded-xl border-t-4 border-t-amber-500 shadow"><p class="text-slate-400 text-xs font-semibold" data-ar="إجمالي العدد (صندوق)" data-en="Total Count (Boxes)">إجمالي العدد (صندوق)</p><h3 id="totalCount" class="text-2xl font-bold text-white mt-1">0</h3></div>
            <div class="bg-slate-800 p-4 rounded-xl border-t-4 border-t-blue-500 shadow"><p class="text-slate-400 text-xs font-semibold" data-ar="عدد الحركات" data-en="Transactions">عدد الحركات</p><h3 id="totalDocs" class="text-2xl font-bold text-white mt-1">0</h3></div>
            <div class="bg-slate-800 p-4 rounded-xl border-t-4 border-t-[#cca344] shadow"><p class="text-slate-400 text-xs font-semibold" data-ar="المعدل اليومي الشامل" data-en="Daily Avg">المعدل اليومي الشامل</p><h3 id="dailyAvgTotal" class="text-2xl font-bold text-white mt-1">0</h3></div>
        </div>

        <!-- المصفوفة الحرارية -->
        <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 mb-4 shadow-xl">
            <div class="flex justify-between items-center mb-3">
                <h3 id="heatmapTitle" class="text-sm font-bold text-slate-300" data-ar="🔥 المصفوفة الحرارية" data-en="🔥 Heatmap Matrix">🔥 المصفوفة الحرارية</h3>
                <button onclick="exportTableToExcel('heatmapTableFull', 'المصفوفة_الحرارية')" class="btn-excel" data-ar="إكسل" data-en="Excel">إكسل</button>
            </div>
            <div class="overflow-x-auto max-h-[500px] overflow-y-auto rounded-lg">
                <table id="heatmapTableFull" class="w-full text-center text-slate-300 whitespace-nowrap text-sm border-collapse heatmap-table"><thead id="heatmapHead" class="sticky top-0 z-10 shadow-md"></thead><tbody id="heatmapBody"></tbody></table>
            </div>
        </div>

        <!-- الجارتات العلوية -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 class="text-sm font-bold text-slate-300 mb-2" data-ar="نمو المحافظات" data-en="Growth">نمو المحافظات <span id="growthPeriodLabel" class="text-xs font-normal text-slate-500"></span></h3><div class="w-full h-[300px] relative"><canvas id="growthChart"></canvas></div></div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 class="text-sm font-bold text-slate-300 mb-2" id="paretoTitle" data-ar="باريتو الوكلاء 80/20" data-en="Pareto 80/20">باريتو الوكلاء 80/20</h3><div class="w-full h-[300px] relative"><canvas id="paretoChart"></canvas></div><p id="paretoSummary" class="text-xs text-slate-400 mt-2 text-center"></p></div>
        </div>

        <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 mb-4 shadow-xl"><h3 class="text-sm font-bold text-slate-300 mb-2" data-ar="اتجاه حصص المحافظات الأسبوعي" data-en="Weekly Share Trend">اتجاه حصص المحافظات الأسبوعي</h3><div class="w-full h-[250px] relative"><canvas id="weeklyShareChart"></canvas></div></div>

        <!-- الجارتات الوسطى -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 id="rankingTitle" class="text-sm font-bold text-slate-300 mb-2" data-ar="ترتيب المحافظات" data-en="Gov Ranking">ترتيب المحافظات</h3><div class="w-full h-[250px] relative"><canvas id="rankingChart"></canvas></div></div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 class="text-sm font-bold text-slate-300 mb-2 text-center" data-ar="حصة المحافظات %" data-en="Gov Share %">حصة المحافظات %</h3><div class="w-full h-[250px] relative flex justify-center"><canvas id="shareChart"></canvas></div></div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 class="text-sm font-bold text-slate-300 mb-2 text-center" data-ar="فريش مقابل مجمد - الإجمالي" data-en="Fresh vs Frozen - Total">فريش مقابل مجمد - الإجمالي</h3><div class="w-full h-[250px] relative flex justify-center"><canvas id="ffTotalChart"></canvas></div></div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 class="text-sm font-bold text-slate-300 mb-2" data-ar="فريش مقابل مجمد (محافظات)" data-en="Fresh/Frozen by Gov">فريش مقابل مجمد (محافظات)</h3><div class="w-full h-[250px] relative"><canvas id="ffGovChart"></canvas></div></div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 id="dailyAvgTitle" class="text-sm font-bold text-slate-300 mb-2" data-ar="المعدل اليومي" data-en="Daily Average">المعدل اليومي</h3><div class="w-full h-[250px] relative"><canvas id="dailyAvgChart"></canvas></div></div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl"><h3 class="text-sm font-bold text-slate-300 mb-2" data-ar="الاتجاه اليومي" data-en="Daily Trend">الاتجاه اليومي</h3><div class="w-full h-[250px] relative"><canvas id="trendChart"></canvas></div></div>
        </div>

        <!-- جدول التفاصيل العملاق -->
        <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 mb-4 shadow-xl">
            <div class="flex justify-between items-center mb-3">
                <h3 class="text-sm font-bold text-teal-400" data-ar="تفاصيل المحافظات – أداء شامل" data-en="Gov Details - Overview">تفاصيل المحافظات – أداء شامل</h3>
                <button onclick="exportTableToExcel('govDetailsTableFull', 'تفاصيل_المحافظات')" class="btn-excel" data-ar="إكسل" data-en="Excel">إكسل</button>
            </div>
            <div class="overflow-x-auto max-h-[400px] overflow-y-auto">
                <table id="govDetailsTableFull" class="w-full text-center advanced-table text-slate-300 whitespace-nowrap">
                    <thead><tr><th data-ar="المحافظة" data-en="Gov">المحافظة</th><th data-ar="صندوق" data-en="Boxes">صندوق</th><th>%</th><th data-ar="طن" data-en="Tons">طن</th><th>%</th><th data-ar="معدل (صندوق)" data-en="Avg (Box)">معدل (صندوق)</th><th data-ar="معدل (طن)" data-en="Avg (Ton)">معدل (طن)</th><th data-ar="وكلاء" data-en="Agents">وكلاء</th><th data-ar="منتجات" data-en="Products">منتجات</th><th data-ar="أيام نشطة" data-en="Active Days">أيام نشطة</th><th data-ar="أقوى وكيل" data-en="Top Agent">أقوى وكيل</th><th data-ar="أقوى منتج" data-en="Top Product">أقوى منتج</th></tr></thead>
                    <tbody id="govDetailsTable"></tbody>
                </table>
            </div>
        </div>

        <!-- الصعود والهبوط + ترتيب الوكلاء -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl">
                <div class="flex justify-between items-center mb-3"><h3 class="text-sm font-bold text-emerald-400" data-ar="صعود وهبوط الوكلاء" data-en="Agents Rise & Fall">صعود وهبوط الوكلاء</h3><button onclick="exportTableToExcel('agentRiseFallTableFull', 'صعود_وهبوط_الوكلاء')" class="btn-excel" data-ar="إكسل" data-en="Excel">إكسل</button></div>
                <div class="overflow-x-auto max-h-[400px] overflow-y-auto"><table id="agentRiseFallTableFull" class="w-full text-center advanced-table text-slate-300 whitespace-nowrap"><thead><tr><th data-ar="الوكيل" data-en="Agent">الوكيل</th><th data-ar="المحافظة" data-en="Gov">المحافظة</th><th data-ar="الحالية" data-en="Current">الحالية</th><th data-ar="السابقة" data-en="Previous">السابقة</th><th data-ar="الفرق" data-en="Diff">الفرق</th><th>%</th></tr></thead><tbody id="agentRiseFallTable"></tbody></table></div>
            </div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-xl">
                <div class="flex justify-between items-center mb-3"><h3 class="text-sm font-bold text-[#cca344]" data-ar="ترتيب الوكلاء الشامل" data-en="Agents Ranking">ترتيب الوكلاء الشامل</h3><button onclick="exportTableToExcel('agentRankingTableFull', 'ترتيب_الوكلاء')" class="btn-excel" data-ar="إكسل" data-en="Excel">إكسل</button></div>
                <div class="overflow-x-auto max-h-[400px] overflow-y-auto"><table id="agentRankingTableFull" class="w-full text-center advanced-table text-slate-300 whitespace-nowrap"><thead><tr><th>#</th><th data-ar="صنف" data-en="Class">صنف</th><th data-ar="الوكيل" data-en="Agent">الوكيل</th><th data-ar="المحافظة" data-en="Gov">المحافظة</th><th data-ar="صندوق" data-en="Boxes">صندوق</th><th data-ar="طن" data-en="Tons">طن</th><th data-ar="التراكمي" data-en="Cum %">التراكمي</th><th data-ar="معدل يومي" data-en="Daily Avg">معدل يومي</th></tr></thead><tbody id="agentRankingTable"></tbody></table></div>
            </div>
        </div>

        <!-- تقرير المنتجات -->
        <div class="bg-[#111827] rounded-xl border border-slate-700 overflow-hidden shadow-2xl mb-4">
            <div class="p-4 border-b border-slate-700 flex flex-col md:flex-row justify-between items-center gap-4 bg-[#1a2332]">
                <div class="flex items-center gap-4"><h2 class="text-lg font-bold text-slate-200" data-ar="سحوبات المنتجات" data-en="Products Report">سحوبات المنتجات</h2><button onclick="exportTableToExcel('productReportTableFull', 'تقرير_المنتجات')" class="btn-excel" data-ar="إكسل" data-en="Excel">إكسل</button></div>
                <div class="flex items-center gap-3 flex-wrap justify-end">
                    <span class="text-xs text-slate-400" data-ar="المحافظة:" data-en="Gov:">المحافظة:</span><select id="reportGovFilter" onchange="updateReportAgentDropdown(); renderProductReport()" class="report-select w-32"><option value="">الكل</option></select>
                    <span class="text-xs text-slate-400" data-ar="الوكيل:" data-en="Agent:">الوكيل:</span><select id="reportAgentFilter" onchange="renderProductReport()" class="report-select w-40"><option value="">الكل</option></select>
                    <button onclick="clearReportFilters()" class="text-xs text-slate-300 hover:text-white border border-slate-600 hover:bg-slate-700 px-3 py-1.5 rounded transition-all" data-ar="مسح ↺" data-en="Clear ↺">مسح ↺</button>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 bg-[#0f172a]">
                <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 text-center"><p class="text-slate-400 text-xs mb-1" data-ar="أقوى منتج" data-en="Top Product">أقوى منتج</p><h4 id="repTopProdName" class="font-bold text-sm text-teal-400 truncate max-w-full">-</h4><p id="repTopProdStats" class="text-[10px] text-slate-400 mt-1">-</p></div>
                <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 text-center"><p class="text-slate-400 text-xs mb-1" data-ar="النطاق" data-en="Scope">النطاق</p><h4 id="repScopeAgents" class="font-bold text-xl text-white mt-1">0</h4><p id="repScopeDetails" class="text-[10px] text-slate-400 mt-1">-</p></div>
                <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 text-center"><p id="repDaysTitle" class="text-slate-400 text-xs mb-1">المعدل اليومي</p><h4 id="repDailyBox" class="font-bold text-2xl text-amber-400 mt-1">0</h4><p id="repDailyTon" class="text-[10px] text-slate-400 mt-1">0</p></div>
                <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 text-center"><p class="text-slate-400 text-xs mb-1" data-ar="إجمالي السحوبات" data-en="Total Withdrawals">إجمالي السحوبات</p><h4 id="repTotalBox" class="font-bold text-2xl text-white mt-1">0</h4><p id="repTotalTon" class="text-[10px] text-slate-400 mt-1">0</p></div>
            </div>
            <div class="overflow-x-auto max-h-[500px] overflow-y-auto">
                <table id="productReportTableFull" class="w-full text-center advanced-table text-slate-300 whitespace-nowrap"><thead><tr><th class="w-10">#</th><th class="text-right" data-ar="المنتج" data-en="Product">المنتج</th><th data-ar="الفئة" data-en="Category">الفئة</th><th data-ar="أقوى محافظة" data-en="Top Gov">أقوى محافظة</th><th data-ar="صندوق" data-en="Boxes">صندوق</th><th>%</th><th data-ar="طن" data-en="Tons">طن</th><th>%</th><th data-ar="تراكمي %" data-en="Cum %">تراكمي %</th></tr></thead><tbody id="productReportTable"><tr><td colspan="9" class="p-4 text-center">بانتظار البيانات...</td></tr></tbody></table>
            </div>
        </div>

        <!-- جدول البيانات الأساسي -->
        <div class="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden shadow-2xl pb-2">
            <div class="p-3 bg-slate-850 border-b border-slate-700 flex justify-between items-center">
                <div class="flex flex-col"><span class="font-bold text-sm text-teal-300" data-ar="سجل العمليات الأساسي (19 عمود)" data-en="Main Data Log">سجل العمليات الأساسي</span><span id="filteredRowsCount" class="font-normal text-xs text-slate-400 mt-1"></span></div>
                <button onclick="exportRawDataToExcel()" class="btn-excel bg-emerald-900/30" data-ar="سحب كل البيانات" data-en="Export All Data">سحب كل البيانات</button>
            </div>
            <div class="overflow-x-auto w-full max-h-[400px] overflow-y-auto">
                <table class="w-full text-center text-xs advanced-table text-slate-300 whitespace-nowrap">
                    <thead><tr><th class="border-r border-slate-600/50">تصنيف</th><th class="border-r border-slate-600/50">الملاحظات</th><th class="border-r border-slate-600/50">رقم السيارة</th><th class="border-r border-slate-600/50">السائق</th><th class="border-r border-slate-600/50">الكمية طن</th><th class="border-r border-slate-600/50">الكمية عدد</th><th class="border-r border-slate-600/50">الفرع</th><th class="border-r border-slate-600/50">الوكيل</th><th class="border-r border-slate-600/50">المادة</th><th class="border-r border-slate-600/50">النوع</th><th class="border-r border-slate-600/50 text-emerald-400">التاريخ</th><th class="border-r border-slate-600/50">رقم المستند</th><th class="text-amber-400 border-r border-slate-600/50">Governorates</th><th class="border-r border-slate-600/50">Item Type</th><th class="border-r border-slate-600/50">Week No</th><th class="border-r border-slate-600/50">Destributor NAME en</th><th class="border-r border-slate-600/50">Brand</th><th class="border-r border-slate-600/50">Own Category</th><th class="border-r border-slate-600/50">Category</th><th>Product Name EN</th></tr></thead>
                    <tbody id="dataTable"><tr><td colspan="20" class="p-6 text-center text-slate-500">يرجى ربط ملف الإكسل...</td></tr></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // ======================= المتغيرات العامة =======================
        let USERS = JSON.parse(localStorage.getItem('sysUsers')) || { 'admin': { pass: '1234', role: 'admin', name: 'المدير العام' } };
        let currentUser = null;
        let fileHandle = null; let globalWorkbook = null; let allRawData = [];
        let currentFilteredData = []; let currentMetric = 'tons'; let chartInstances = {};
        const govColors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f43f5e', '#f97316', '#eab308', '#22c55e', '#14b8a6', '#0ea5e9', '#6366f1', '#a855f7', '#d946ef', '#f43f5e', '#f97316'];
        
        Chart.defaults.color = '#94a3b8'; 
        Chart.defaults.font.family = 'Cairo';

        let isLightMode = false;
        let currentLang = 'ar';

        // ======================= إدارة المستخدمين =======================
        function saveUsers() { localStorage.setItem('sysUsers', JSON.stringify(USERS)); }
        
        function renderUsersTable() {
            let html = '';
            for (let u in USERS) {
                html += `<tr><td>${u}</td><td>${USERS[u].name}</td><td>${USERS[u].role === 'admin' ? 'مدير' : 'مشاهد'}</td><td>${u !== 'admin' ? `<button onclick="deleteUser('${u}')" class="text-rose-500 text-xs bg-rose-500/10 px-2 py-1 rounded">حذف</button>` : '-'}</td></tr>`;
            }
            document.getElementById('usersTableBody').innerHTML = html;
        }

        function addUser() {
            let u = document.getElementById('newUsername').value.trim().toLowerCase();
            let n = document.getElementById('newName').value.trim();
            let p = document.getElementById('newPassword').value.trim();
            let r = document.getElementById('newRole').value;
            if(!u || !p || !n) { alert('يرجى تعبئة كافة الحقول'); return; }
            if(USERS[u]) { alert('اسم المستخدم موجود مسبقاً!'); return; }
            USERS[u] = { pass: p, name: n, role: r };
            saveUsers(); renderUsersTable();
            document.getElementById('newUsername').value = ''; document.getElementById('newName').value = ''; document.getElementById('newPassword').value = '';
        }

        function deleteUser(u) {
            if(confirm(`هل أنت متأكد من حذف المستخدم ${u}؟`)) { delete USERS[u]; saveUsers(); renderUsersTable(); }
        }

        // ======================= تسجيل الدخول والمظهر =======================
        function checkLogin() {
            const user = document.getElementById('usernameInput').value.trim().toLowerCase();
            const pass = document.getElementById('passwordInput').value.trim();
            const errorMsg = document.getElementById('loginError');

            if (USERS[user] && USERS[user].pass === pass) {
                currentUser = USERS[user];
                document.getElementById('loginOverlay').style.display = 'none';
                document.getElementById('mainDashboard').style.display = 'block';
                document.getElementById('welcomeMessage').innerText = currentLang === 'ar' ? `مرحباً بك، ${currentUser.name}` : `Welcome, ${currentUser.name}`;
                
                if (currentUser.role === 'admin') {
                    document.getElementById('adminPanel').style.display = 'grid';
                    document.getElementById('userManagementPanel').style.display = 'block';
                    renderUsersTable();
                    document.getElementById('status').innerText = currentLang === 'ar' ? 'وضع الإدارة مفعل' : 'Admin Mode Active';
                } else {
                    document.getElementById('adminPanel').style.display = 'none';
                    document.getElementById('userManagementPanel').style.display = 'none';
                    fetchServerExcel();
                }
            } else { errorMsg.style.display = 'block'; }
        }

        function logout() {
            currentUser = null; document.getElementById('loginOverlay').style.display = 'flex';
            document.getElementById('mainDashboard').style.display = 'none';
            document.getElementById('usernameInput').value = ''; document.getElementById('passwordInput').value = '';
            document.getElementById('loginError').style.display = 'none';
        }

        function toggleTheme() {
            isLightMode = !isLightMode;
            if(isLightMode) {
                document.body.classList.add('light-theme');
                document.getElementById('themeBtnLogin').innerText = '🌙'; document.getElementById('themeBtnMain').innerText = '🌙';
                Chart.defaults.color = '#334155';
            } else {
                document.body.classList.remove('light-theme');
                document.getElementById('themeBtnLogin').innerText = '☀️'; document.getElementById('themeBtnMain').innerText = '☀️';
                Chart.defaults.color = '#94a3b8';
            }
            if(allRawData.length > 0) applyFiltersAndRender();
        }

        function toggleLang() {
            currentLang = currentLang === 'ar' ? 'en' : 'ar';
            document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
            document.querySelectorAll('[data-ar]').forEach(el => { el.innerText = el.getAttribute(`data-${currentLang}`); });
            document.querySelectorAll('input[data-ar-ph]').forEach(el => { el.placeholder = el.getAttribute(`data-${currentLang}-ph`); });
        }

        // ======================= قراءة الملفات (التحديث السحابي) =======================
        // 🌟 الرابط المباشر إلى Google Sheets
        const GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS1j77BhqHnxfiA0jHEPMMnGV78JWe6ufnnj5vuG4LIIbwrrrzNMJxeMEgmSrg-bktmrvah6IBxH1TP/pub?output=csv';

        async function fetchServerExcel(isAutoRefresh = false) {
            if (!isAutoRefresh) {
                document.getElementById('status').innerText = currentLang === 'ar' ? 'جاري الاتصال بالسيرفر...' : 'Connecting...';
                document.getElementById('status').className = 'bg-blue-500/10 text-blue-400 px-3 py-1.5 rounded-full text-xs font-semibold border border-blue-500/20';
            }
            
            try {
                // منع التخزين المؤقت (Cache Busting)
                const finalUrl = GOOGLE_SHEET_CSV_URL.includes('?') ? GOOGLE_SHEET_CSV_URL + '&t=' + new Date().getTime() : GOOGLE_SHEET_CSV_URL + '?t=' + new Date().getTime();
                const response = await fetch(finalUrl); 
                
                if (!response.ok) throw new Error('Network response was not ok');
                
                const csvText = await response.text();
                globalWorkbook = XLSX.read(csvText, { type: 'string' });
                
                let targetSheet = globalWorkbook.SheetNames[0]; 
                document.getElementById('sheetSelect').innerHTML = `<option value="${targetSheet}">${targetSheet}</option>`;
                
                parseExcelData(targetSheet);
                
                document.getElementById('status').innerText = currentLang === 'ar' ? 'أونلاين (تحديث تلقائي) 🟢' : 'Online (Auto) 🟢';
                document.getElementById('status').className = 'bg-emerald-500/10 text-emerald-400 px-3 py-1.5 rounded-full text-xs font-semibold border border-emerald-500/20';
            } catch (error) {
                console.error("Fetch error: ", error);
                document.getElementById('status').innerText = currentLang === 'ar' ? 'انقطع الاتصال 🔴' : 'Offline 🔴';
                document.getElementById('status').className = 'bg-rose-500/10 text-rose-400 px-3 py-1.5 rounded-full text-xs font-semibold border border-rose-500/20';
            }
        }

        // التحديث التلقائي كل 5 دقائق
        setInterval(() => {
            if (currentUser && currentUser.role === 'viewer') {
                fetchServerExcel(true);
            }
        }, 300000);

        function exportTableToExcel(tableId, filename) {
            let table = document.getElementById(tableId); if(!table) return;
            let wb = XLSX.utils.table_to_book(table, {sheet: "Data"}); XLSX.writeFile(wb, filename + ".xlsx");
        }

        function exportRawDataToExcel() {
            if (!currentFilteredData || currentFilteredData.length === 0) { alert('لا توجد بيانات!'); return; }
            let exportData = currentFilteredData.map(r => ({
                "تصنيف": r.ffClass, "الملاحظات": r.c0, "رقم السيارة": r.c1, "السائق": r.c2, "الكمية طن": r.c3_tons, "الكمية عدد": r.c4_count, "الفرع": r.c5, "الوكيل": r.c6, "المادة": r.c7, "النوع": r.c8, "التاريخ": r.dateStr, "رقم المستند": r.c10, "Governorates": r.c11, "Item Type": r.c12, "Week No": r.c13, "Destributor NAME en": r.c14, "Brand": r.c15, "Own Category": r.c16, "Category": r.c17, "Product Name EN": r.c18
            }));
            let ws = XLSX.utils.json_to_sheet(exportData); let wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "البيانات"); XLSX.writeFile(wb, "البيانات_الكاملة.xlsx");
        }

        document.getElementById('pickFileBtn').addEventListener('click', async () => {
            if(currentUser.role !== 'admin') return;
            try { [fileHandle] = await window.showOpenFilePicker({ types: [{ accept: {'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'], 'text/csv': ['.csv']} }] });
                document.getElementById('fileNameDisplay').innerText = fileHandle.name; await processFile(false); } catch (e) {}
        });

        async function refreshData() { if (currentUser.role === 'viewer') { fetchServerExcel(); return; } if (fileHandle) await processFile(true); else fetchServerExcel(); }

        async function processFile(isRefresh) {
            try { const file = await fileHandle.getFile(); const arrayBuffer = await file.arrayBuffer();
                globalWorkbook = XLSX.read(arrayBuffer, { type: 'array' });
                if (!isRefresh) { const select = document.getElementById('sheetSelect'); select.innerHTML = ''; globalWorkbook.SheetNames.forEach(name => select.appendChild(new Option(name, name))); }
                parseExcelData(); document.getElementById('status').innerText = 'متصل';
            } catch (e) { document.getElementById('status').innerText = 'خطأ'; }
        }

        function getWeekNumber(d) {
            d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())); d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
            var yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1)); return Math.ceil((((d - yearStart) / 86400000) + 1)/7);
        }

        function parseExcelData(sheetOverride) {
            if (!globalWorkbook) return;
            let sheetName = sheetOverride || document.getElementById('sheetSelect').value;
            const worksheet = globalWorkbook.Sheets[sheetName];
            const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: "" });
            allRawData = []; let uniqueAllGovs = new Set(); 

            for (let i = 1; i < rows.length; i++) {
                const c = rows[i]; if (!c[1] && !c[2] && !parseFloat(c[3]) && !parseFloat(c[4])) continue;
                let rawDate = c[9]; let dateStr = ""; let parsedDateObj = null;
                if (typeof rawDate === 'number' && rawDate > 20000) {
                    const d = new Date(Math.floor(rawDate - 25569) * 86400 * 1000); dateStr = `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}-${String(d.getUTCDate()).padStart(2, '0')}`; parsedDateObj = d;
                } else { dateStr = String(rawDate).trim(); if(dateStr) parsedDateObj = new Date(dateStr); }

                let typeCol = String(c[8]).trim(); let prodCol = String(c[7]).trim() + " " + String(c[18]).trim(); let itemType = String(c[12]).trim();
                let isFresh = typeCol.includes('فريش') || typeCol.includes('مبرد') || prodCol.includes('فريش') || itemType.toLowerCase().includes('fresh');
                let isFrozen = typeCol.includes('مجمد') || prodCol.includes('مجمد') || itemType.toLowerCase().includes('frozen');
                let catClass = isFresh ? 'فريش' : (isFrozen ? 'مجمد' : 'أخرى');
                let weekStr = parsedDateObj ? `${parsedDateObj.getFullYear()}-W${String(getWeekNumber(parsedDateObj)).padStart(2,'0')}` : 'Unknown';
                let gov = String(c[11]).trim() || 'غير محدد'; let agent = String(c[6]).trim() || 'غير معروف';
                uniqueAllGovs.add(gov);

                allRawData.push({
                    c0: String(c[0]).trim(), c1: String(c[1]).trim(), c2: String(c[2]).trim(), c3_tons: parseFloat(c[3]) || 0, c4_count: parseFloat(c[4]) || 0, c5: String(c[5]).trim(), c6: agent, c7: String(c[7]).trim(), c8: String(c[8]).trim(), dateStr: dateStr, dateObj: isNaN(parsedDateObj) ? null : parsedDateObj, weekStr: weekStr, c10: String(c[10]).trim(), c11: gov, c12: String(c[12]).trim(), c13: String(c[13]).trim(), c14: String(c[14]).trim(), c15: String(c[15]).trim(), c16: String(c[16]).trim(), c17: String(c[17]).trim(), c18: String(c[18]).trim(), ffClass: catClass, fullProdName: prodCol
                });
            }
            let repGovSel = document.getElementById('reportGovFilter'); repGovSel.innerHTML = '<option value="">الكل</option>';
            Array.from(uniqueAllGovs).sort().forEach(g => repGovSel.innerHTML += `<option value="${g}">${g}</option>`);
            updateReportAgentDropdown(); applyFiltersAndRender();
        }

        function updateReportAgentDropdown() {
            let selectedGov = document.getElementById('reportGovFilter').value; let repAgentSel = document.getElementById('reportAgentFilter');
            let agentsInGov = new Set(); allRawData.forEach(r => { if (!selectedGov || r.c11 === selectedGov) { agentsInGov.add(r.c6); } });
            repAgentSel.innerHTML = '<option value="">الكل</option>'; Array.from(agentsInGov).sort().forEach(a => { repAgentSel.innerHTML += `<option value="${a}">${a}</option>`; });
        }

        function clearReportFilters() { document.getElementById('reportGovFilter').value = ''; updateReportAgentDropdown(); document.getElementById('reportAgentFilter').value = ''; renderProductReport(); }
        function setMetric(metric) { currentMetric = metric; document.getElementById('btnMetricTons').className = metric === 'tons' ? 'metric-btn active' : 'metric-btn'; document.getElementById('btnMetricCount').className = metric === 'count' ? 'metric-btn active' : 'metric-btn'; applyFiltersAndRender(); }
        function setDateFilter(type, btn) {
            document.querySelectorAll('.date-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active');
            const today = new Date(); let dFrom = null; let dTo = new Date();
            if (type === 'last7') { dFrom = new Date(); dFrom.setDate(today.getDate() - 7); } else if (type === 'last30') { dFrom = new Date(); dFrom.setDate(today.getDate() - 30); } else if (type === 'thisMonth') { dFrom = new Date(today.getFullYear(), today.getMonth(), 1); } else if (type === 'all') { dFrom = null; dTo = null; }
            document.getElementById('dateFrom').value = dFrom ? dFrom.toISOString().split('T')[0] : ''; document.getElementById('dateTo').value = dTo ? dTo.toISOString().split('T')[0] : ''; applyFiltersAndRender();
        }

        // ======================= التحليل والفلاتر =======================
        function applyFiltersAndRender() {
            const dFrom = document.getElementById('dateFrom').value ? new Date(document.getElementById('dateFrom').value) : null;
            const dTo = document.getElementById('dateTo').value ? new Date(document.getElementById('dateTo').value) : null;
            if(dFrom) dFrom.setHours(0,0,0,0); if(dTo) dTo.setHours(23,59,59,999);

            let prevDFrom = null; let prevDTo = null; let timeDiff = 0;
            if (dFrom && dTo) { timeDiff = dTo.getTime() - dFrom.getTime(); prevDTo = new Date(dFrom.getTime() - 86400000); prevDFrom = new Date(prevDTo.getTime() - timeDiff); }

            let totalTons = 0; let totalCount = 0; let filteredRows = 0;
            let govTotals = {}; let prevGovTotals = {}; let agentTotals = {}; let prevAgentTotals = {}; let agentGovs = {};
            let dailyTrend = {}; let ffTotal = { 'فريش': 0, 'مجمد': 0, 'أخرى': 0 }; let ffGovs = {}; let uniqueDates = new Set(); let weeklyShare = {}; 
            let heatmapData = {}; let uniqueCats = new Set(); let govDetails = {};
            currentFilteredData = []; let tableHTML = '';

            allRawData.forEach(r => {
                let isCurrent = false; let isPrev = false;
                if (!dFrom && !dTo) { isCurrent = true; }
                else if (r.dateObj) { if (dFrom && dTo && r.dateObj >= dFrom && r.dateObj <= dTo) isCurrent = true; if (prevDFrom && prevDTo && r.dateObj >= prevDFrom && r.dateObj <= prevDTo) isPrev = true; }
                let val = currentMetric === 'tons' ? r.c3_tons : r.c4_count;

                if (isPrev && val > 0) { prevGovTotals[r.c11] = (prevGovTotals[r.c11] || 0) + val; prevAgentTotals[r.c6] = (prevAgentTotals[r.c6] || 0) + val; }
                
                if (isCurrent) {
                    currentFilteredData.push(r); totalTons += r.c3_tons; totalCount += r.c4_count; filteredRows++;
                    if (val > 0) {
                        govTotals[r.c11] = (govTotals[r.c11] || 0) + val; agentTotals[r.c6] = (agentTotals[r.c6] || 0) + val; agentGovs[r.c6] = r.c11; 
                        ffTotal[r.ffClass] += val; if(!ffGovs[r.c11]) ffGovs[r.c11] = { 'فريش': 0, 'مجمد': 0, 'أخرى': 0 }; ffGovs[r.c11][r.ffClass] += val;
                        
                        if(!govDetails[r.c11]) govDetails[r.c11] = { tons:0, count:0, agents:new Set(), prods:new Set(), dates:new Set(), agentSales:{}, prodSales:{} };
                        govDetails[r.c11].tons += r.c3_tons; govDetails[r.c11].count += r.c4_count; govDetails[r.c11].agents.add(r.c6); govDetails[r.c11].prods.add(r.fullProdName);
                        if(r.dateStr) govDetails[r.c11].dates.add(r.dateStr); govDetails[r.c11].agentSales[r.c6] = (govDetails[r.c11].agentSales[r.c6] || 0) + val; govDetails[r.c11].prodSales[r.fullProdName] = (govDetails[r.c11].prodSales[r.fullProdName] || 0) + val;

                        if(r.dateStr) { uniqueDates.add(r.dateStr); if(!dailyTrend[r.dateStr]) dailyTrend[r.dateStr] = {}; dailyTrend[r.dateStr][r.c11] = (dailyTrend[r.dateStr][r.c11] || 0) + val; }
                        if(r.weekStr) { if(!weeklyShare[r.weekStr]) weeklyShare[r.weekStr] = { total: 0, govs: {} }; weeklyShare[r.weekStr].total += val; weeklyShare[r.weekStr].govs[r.c11] = (weeklyShare[r.weekStr].govs[r.c11] || 0) + val; }
                        let cat = r.c17 || r.c16 || 'أخرى'; if (!heatmapData[r.c11]) heatmapData[r.c11] = { total: 0, cats: {} }; heatmapData[r.c11].cats[cat] = (heatmapData[r.c11].cats[cat] || 0) + val; heatmapData[r.c11].total += val; uniqueCats.add(cat);
                    }

                    if (filteredRows <= 150) {
                        let badgeColor = r.ffClass === 'فريش' ? 'bg-green-500/20 text-green-400' : (r.ffClass === 'مجمد' ? 'bg-blue-500/20 text-blue-400' : 'bg-slate-500/20 text-slate-400');
                        tableHTML += `<tr><td><span class="px-2 py-1 rounded ${badgeColor}">${r.ffClass}</span></td><td class="truncate max-w-[100px]" title="${r.c0}">${r.c0}</td><td>${r.c1}</td><td>${r.c2}</td><td class="text-teal-400">${r.c3_tons.toFixed(2)}</td><td class="text-amber-400">${r.c4_count}</td><td>${r.c5}</td><td class="truncate max-w-[100px]">${r.c6}</td><td class="truncate max-w-[100px]">${r.c7}</td><td>${r.c8}</td><td class="text-emerald-400">${r.dateStr}</td><td>${r.c10}</td><td>${r.c11}</td><td>${r.c12}</td><td>${r.c13}</td><td class="truncate max-w-[100px]">${r.c14}</td><td>${r.c15}</td><td>${r.c16}</td><td>${r.c17}</td><td class="truncate max-w-[100px]" title="${r.c18}">${r.c18}</td></tr>`;
                    }
                }
            });

            if (filteredRows > 150) tableHTML += `<tr><td colspan="20" class="p-2 text-center text-slate-400 bg-slate-800/50">تم عرض أحدث 150...</td></tr>`;
            
            let daysCount = Math.max(1, uniqueDates.size); let totalValActive = currentMetric === 'tons' ? totalTons : totalCount; let dailyAvgAll = totalValActive / daysCount;
            document.getElementById('totalTons').innerText = totalTons.toLocaleString(undefined, {minimumFractionDigits: 2}); document.getElementById('totalCount').innerText = totalCount.toLocaleString(); document.getElementById('totalDocs').innerText = filteredRows.toLocaleString(); document.getElementById('dailyAvgTotal').innerText = dailyAvgAll.toLocaleString(undefined, {maximumFractionDigits: 1});
            
            let agentArr = Object.keys(agentTotals).map(a => ({ name: a, val: agentTotals[a], gov: agentGovs[a] })).sort((a,b) => b.val - a.val);
            let runTotal = 0; let classACount = 0; let classBCount = 0;
            agentArr.forEach(a => { runTotal += a.val; a.cumPct = (runTotal / totalValActive) * 100; if(a.cumPct <= 80) { a.class = 'A'; classACount++; } else if(a.cumPct <= 95) { a.class = 'B'; classBCount++; } else a.class = 'C'; });
            document.getElementById('paretoSummary').innerText = `${classACount} وكلاء يمثلون 80% (فئة A)`;

            buildHeatmapTable(heatmapData, uniqueCats); 
            buildGovDetailsTable(govDetails, totalTons, totalCount); 
            buildAgentTables(agentArr, prevAgentTotals, daysCount, govDetails);
            document.getElementById('dataTable').innerHTML = tableHTML || `<tr><td colspan="20">لا توجد بيانات!</td></tr>`;

            const sortedGovs = Object.keys(govTotals).sort((a,b) => govTotals[b] - govTotals[a]); const sortedVals = sortedGovs.map(g => govTotals[g]); const colorMap = {}; sortedGovs.forEach((g, i) => colorMap[g] = govColors[i % govColors.length]);
            let growthData = []; let growthColors = []; sortedGovs.forEach(g => { let curr = govTotals[g] || 0; let prev = prevGovTotals[g] || 0; let pct = prev > 0 ? ((curr - prev) / prev) * 100 : (curr > 0 ? 100 : 0); growthData.push(pct); growthColors.push(pct >= 0 ? '#22c55e' : '#ef4444'); });

            renderCharts(sortedGovs, sortedVals, colorMap, dailyTrend, ffTotal, ffGovs, sortedGovs.map(g => govTotals[g] / daysCount), agentArr.slice(0,40), growthData, growthColors, weeklyShare, sortedGovs.slice(0,6));
            renderProductReport();
        }

        // ======================= تقرير المنتجات وبناء الجداول =======================
        function renderProductReport() {
            let govFilter = document.getElementById('reportGovFilter').value; let agentFilter = document.getElementById('reportAgentFilter').value;
            let reportData = {}; let repTotalTons = 0; let repTotalCount = 0; let repActiveDays = new Set();
            currentFilteredData.forEach(r => {
                if (govFilter && r.c11 !== govFilter) return; if (agentFilter && r.c6 !== agentFilter) return;
                if (r.c3_tons > 0 || r.c4_count > 0) {
                    repTotalTons += r.c3_tons; repTotalCount += r.c4_count; if(r.dateStr) repActiveDays.add(r.dateStr);
                    let pName = r.fullProdName || 'غير محدد'; if (!reportData[pName]) { reportData[pName] = { tons: 0, count: 0, category: r.c17 || r.c16 || r.ffClass, govs: {} }; }
                    reportData[pName].tons += r.c3_tons; reportData[pName].count += r.c4_count; reportData[pName].govs[r.c11] = (reportData[pName].govs[r.c11] || 0) + (currentMetric === 'tons' ? r.c3_tons : r.c4_count);
                }
            });
            let prodArr = Object.keys(reportData).map(p => ({ name: p, tons: reportData[p].tons, count: reportData[p].count, cat: reportData[p].category, govs: reportData[p].govs, val: currentMetric === 'tons' ? reportData[p].tons : reportData[p].count })).sort((a,b) => b.val - a.val);
            
            let days = Math.max(1, repActiveDays.size);
            document.getElementById('repTotalBox').innerText = repTotalCount.toLocaleString(); document.getElementById('repTotalTon').innerText = repTotalTons.toLocaleString(undefined,{maximumFractionDigits:1});
            document.getElementById('repDaysTitle').innerText = `المعدل اليومي (${days} أيام)`; document.getElementById('repDailyBox').innerText = (repTotalCount/days).toLocaleString(undefined,{maximumFractionDigits:0}); document.getElementById('repDailyTon').innerText = (repTotalTons/days).toFixed(1);
            if (prodArr.length > 0) { let topP = prodArr[0]; document.getElementById('repTopProdName').innerText = topP.name; } else { document.getElementById('repTopProdName').innerText = '-'; }

            let tbodyHtml = ''; let runPct = 0; let actTotalCount = repTotalCount > 0 ? repTotalCount : 1; let actTotalTons = repTotalTons > 0 ? repTotalTons : 1;
            prodArr.forEach((p, index) => {
                let pCountPct = (p.count / actTotalCount) * 100; let pTonsPct = (p.tons / actTotalTons) * 100; runPct += (currentMetric === 'tons' ? pTonsPct : pCountPct);
                let sortedPgovs = Object.keys(p.govs).sort((a,b) => p.govs[b] - p.govs[a]); let bestGovStr = sortedPgovs.length > 0 ? sortedPgovs[0] : '-';
                tbodyHtml += `<tr><td>${index + 1}</td><td class="text-right truncate max-w-[250px] font-bold">${p.name}</td><td>${p.cat}</td><td>${bestGovStr}</td><td class="text-amber-400 font-bold">${p.count.toLocaleString()}</td><td class="text-teal-400 font-bold">${p.tons.toFixed(1)}</td><td class="text-emerald-400 font-bold">${runPct.toFixed(1)}%</td></tr>`;
            });
            document.getElementById('productReportTable').innerHTML = tbodyHtml || `<tr><td colspan="7">لا توجد بيانات</td></tr>`;
        }

        function buildHeatmapTable(heatmapData, uniqueCats) {
            let catsArr = Array.from(uniqueCats); let govsArr = Object.keys(heatmapData).sort((a,b) => heatmapData[b].total - heatmapData[a].total); let catTotals = {}; govsArr.forEach(g => { catsArr.forEach(c => { catTotals[c] = (catTotals[c] || 0) + (heatmapData[g].cats[c] || 0); }); }); catsArr.sort((a,b) => catTotals[b] - catTotals[a]);
            let thead = `<tr><th class="text-right" data-ar="المحافظة" data-en="Gov">المحافظة</th>`; catsArr.forEach(c => { thead += `<th>${c}</th>`; }); thead += `<th class="text-left" data-ar="الإجمالي" data-en="Total">الإجمالي</th></tr>`;
            let tbody = ''; govsArr.forEach(g => {
                let rowTotal = heatmapData[g].total; tbody += `<tr><td class="font-bold text-right">${g}</td>`;
                catsArr.forEach(c => {
                    let val = heatmapData[g].cats[c] || 0;
                    if (val === 0) tbody += `<td>-</td>`; else { let pct = val / rowTotal; let opacity = Math.max(0.15, Math.min(0.9, 0.15 + (pct * 0.8))); let bgColor = `rgba(37, 99, 235, ${opacity})`; let valStr = val >= 1000 ? (val/1000).toFixed(val % 1000 === 0 ? 0 : 1).replace('.0', '') + 'K' : Math.round(val).toLocaleString(); tbody += `<td style="background-color: ${bgColor};"><div class="font-bold text-white">${valStr}</div><div class="text-[10px] text-slate-300 mt-1">${(pct*100).toFixed(0)}%</div></td>`; }
                });
                tbody += `<td class="font-bold text-amber-400 text-left">${rowTotal.toLocaleString(undefined, {maximumFractionDigits:0})}</td></tr>`;
            });
            document.getElementById('heatmapHead').innerHTML = thead; document.getElementById('heatmapBody').innerHTML = tbody;
        }

        function buildGovDetailsTable(govDetails, totalTons, totalCount) {
            let html = ''; let sortedGovs = Object.keys(govDetails).sort((a,b) => govDetails[b][currentMetric] - govDetails[a][currentMetric]);
            sortedGovs.forEach(gov => { let d = govDetails[gov]; let days = Math.max(1, d.dates.size); let topAgent = Object.keys(d.agentSales).sort((a,b)=>d.agentSales[b]-d.agentSales[a])[0] || '-'; let topProd = Object.keys(d.prodSales).sort((a,b)=>d.prodSales[b]-d.prodSales[a])[0] || '-'; html += `<tr><td class="font-bold">${gov}</td><td class="text-amber-400">${d.count.toLocaleString()}</td><td>${(totalCount > 0 ? (d.count/totalCount)*100 : 0).toFixed(1)}%</td><td class="text-teal-400">${d.tons.toFixed(2)}</td><td>${(totalTons > 0 ? (d.tons/totalTons)*100 : 0).toFixed(1)}%</td><td>${(d.count/days).toLocaleString(undefined,{maximumFractionDigits:0})}</td><td>${(d.tons/days).toFixed(1)}</td><td>${d.agents.size}</td><td>${d.prods.size}</td><td>${days}</td><td class="truncate max-w-[120px]">${topAgent}</td><td class="truncate max-w-[150px] text-xs">${topProd}</td></tr>`; });
            document.getElementById('govDetailsTable').innerHTML = html;
        }

        function buildAgentTables(agentArr, prevAgentTotals, daysCount, govDetails) {
            let rankHtml = ''; agentArr.forEach((a, i) => { let t_tons = 0; let t_count = 0; allRawData.forEach(r => { if(r.c6 === a.name && r.c3_tons > 0 || r.c4_count > 0) { t_tons += r.c3_tons; t_count += r.c4_count; } }); rankHtml += `<tr><td>${i+1}</td><td><span class="badge-${a.class}">${a.class}</span></td><td class="truncate max-w-[120px]">${a.name}</td><td>${a.gov}</td><td class="text-amber-400">${t_count.toLocaleString()}</td><td class="text-teal-400">${t_tons.toFixed(1)}</td><td>${a.cumPct.toFixed(1)}%</td><td>${(a.val/daysCount).toLocaleString(undefined,{maximumFractionDigits:0})}</td></tr>`; });
            document.getElementById('agentRankingTable').innerHTML = rankHtml;
            let riseFall = []; agentArr.forEach(a => { let prev = prevAgentTotals[a.name] || 0; let diff = a.val - prev; let pct = prev > 0 ? (diff / prev) * 100 : (a.val > 0 ? 100 : 0); if(prev > 0 || a.val > 0) riseFall.push({ name: a.name, gov: a.gov, curr: a.val, prev: prev, diff: diff, pct: pct }); }); riseFall.sort((a,b) => b.diff - a.diff);
            let rfHtml = ''; riseFall.slice(0, 10).forEach(r => { if(r.diff > 0) rfHtml += `<tr><td class="truncate max-w-[120px]">${r.name}</td><td>${r.gov}</td><td>${r.curr.toLocaleString()}</td><td>${r.prev.toLocaleString()}</td><td class="text-up">▲ ${Math.abs(r.diff).toLocaleString()}</td><td class="text-up">+${r.pct.toFixed(1)}%</td></tr>`; }); riseFall.slice(-10).reverse().forEach(r => { if(r.diff < 0) rfHtml += `<tr><td class="truncate max-w-[120px]">${r.name}</td><td>${r.gov}</td><td>${r.curr.toLocaleString()}</td><td>${r.prev.toLocaleString()}</td><td class="text-down">▼ ${Math.abs(r.diff).toLocaleString()}</td><td class="text-down">${r.pct.toFixed(1)}%</td></tr>`; });
            document.getElementById('agentRiseFallTable').innerHTML = rfHtml || `<tr><td colspan="6">لا توجد بيانات</td></tr>`;
        }

        // ======================= رسم الجارتات =======================
        function destroyChart(id) { if (chartInstances[id]) chartInstances[id].destroy(); }
        
        function renderCharts(govs, vals, colorMap, dailyTrend, ffTotal, ffGovs, dailyAvgGovVals, top40Agents, growthData, growthColors, weeklyShare, top6Govs) {
            ['ranking', 'share', 'trend', 'ffGov', 'ffTotal', 'dailyAvg', 'growth', 'pareto', 'weeklyShare'].forEach(id => destroyChart(id));
            
            // تهيئة إعدادات الألوان حسب الوضع الحالي (ليلي/نهاري)
            const gridColor = isLightMode ? '#e2e8f0' : '#334155';
            
            chartInstances['ranking'] = new Chart(document.getElementById('rankingChart').getContext('2d'), { type: 'bar', data: { labels: govs, datasets: [{ data: vals, backgroundColor: '#cca344', borderRadius: 4, barThickness: 15 }] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: gridColor } }, y: { grid: { display: false } } } } });
            chartInstances['share'] = new Chart(document.getElementById('shareChart').getContext('2d'), { type: 'doughnut', data: { labels: govs, datasets: [{ data: vals, backgroundColor: govs.map(g => colorMap[g]), borderWidth: 0 }] }, options: { responsive: true, maintainAspectRatio: false, cutout: '65%', plugins: { legend: { position: 'left', labels: { boxWidth: 10, font: { size: 10 } } } } } });
            
            const sortedDates = Object.keys(dailyTrend).sort(); 
            chartInstances['trend'] = new Chart(document.getElementById('trendChart').getContext('2d'), { type: 'line', data: { labels: sortedDates, datasets: govs.map(g => ({ label: g, data: sortedDates.map(d => dailyTrend[d][g] || 0), borderColor: colorMap[g], tension: 0.4, pointRadius: 0 })) }, options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false }, scales: { x: { grid: { display: false } }, y: { grid: { color: gridColor } } } } });
            
            chartInstances['ffTotal'] = new Chart(document.getElementById('ffTotalChart').getContext('2d'), { type: 'doughnut', data: { labels: ['مجمد', 'فريش', 'أخرى'], datasets: [{ data: [ffTotal['مجمد'], ffTotal['فريش'], ffTotal['أخرى']], backgroundColor: ['#3b82f6', '#22c55e', '#cca344'], borderWidth: 0 }] }, options: { responsive: true, maintainAspectRatio: false, cutout: '50%', plugins: { legend: { position: 'right' } } } });
            chartInstances['ffGov'] = new Chart(document.getElementById('ffGovChart').getContext('2d'), { type: 'bar', data: { labels: govs, datasets: [ { label: 'مجمد', data: govs.map(g => ffGovs[g] ? ffGovs[g]['مجمد'] : 0), backgroundColor: '#3b82f6', barThickness: 10 }, { label: 'فريش', data: govs.map(g => ffGovs[g] ? ffGovs[g]['فريش'] : 0), backgroundColor: '#22c55e', barThickness: 10 } ] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } }, scales: { x: { stacked: true, grid: { color: gridColor } }, y: { stacked: true, grid: { display: false } } } } });
            chartInstances['dailyAvg'] = new Chart(document.getElementById('dailyAvgChart').getContext('2d'), { type: 'bar', data: { labels: govs, datasets: [{ data: dailyAvgGovVals, backgroundColor: '#cca344', borderRadius: 4, barThickness: 15 }] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: gridColor } }, y: { grid: { display: false } } } } });
            chartInstances['growth'] = new Chart(document.getElementById('growthChart').getContext('2d'), { type: 'bar', data: { labels: govs, datasets: [{ data: growthData, backgroundColor: growthColors, borderRadius: 4, barThickness: 12 }] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => c.raw.toFixed(1) + '%' } } }, scales: { x: { grid: { color: gridColor }, ticks: { callback: v => v + '%' } }, y: { grid: { display: false } } } } });
            
            chartInstances['pareto'] = new Chart(document.getElementById('paretoChart').getContext('2d'), { type: 'bar', data: { labels: top40Agents.map(a => a.name.split(' ')[0] + ' ' + (a.name.split(' ')[1]||'')), datasets: [ { type: 'line', label: 'التراكمي %', data: top40Agents.map(a => a.cumPct), borderColor: '#cca344', backgroundColor: '#cca344', borderWidth: 2, tension: 0.3, pointRadius: 2, yAxisID: 'y1' }, { type: 'bar', label: currentMetric === 'tons' ? 'طن' : 'صندوق', data: top40Agents.map(a => a.val), backgroundColor: top40Agents.map(a => a.class==='A'?'#22c55e':(a.class==='B'?'#eab308':'#ef4444')), borderRadius: 2, yAxisID: 'y' } ] }, options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index' }, plugins: { legend: { position: 'top' } }, scales: { x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 90, minRotation: 90 } }, y: { type: 'linear', position: 'left', grid: { color: gridColor }, display: false }, y1: { type: 'linear', position: 'right', grid: { display: false }, ticks: { callback: v => v + '%' }, max: 100 } } } });
            
            const sortedWeeks = Object.keys(weeklyShare).sort();
            chartInstances['weeklyShare'] = new Chart(document.getElementById('weeklyShareChart').getContext('2d'), { type: 'line', data: { labels: sortedWeeks, datasets: top6Govs.map(g => ({ label: g, data: sortedWeeks.map(w => { let total = weeklyShare[w].total; return total > 0 ? (weeklyShare[w].govs[g]||0)/total * 100 : 0; }), borderColor: colorMap[g], backgroundColor: colorMap[g], tension: 0.3, pointRadius: 3 })) }, options: { responsive: true, maintainAspectRatio: false, plugins: { tooltip: { callbacks: { label: c => c.dataset.label + ': ' + c.raw.toFixed(1) + '%' } } }, scales: { x: { grid: { display: false } }, y: { grid: { color: gridColor }, ticks: { callback: v => v + '%' } } } } });
        }
    </script>
</body>
</html>
