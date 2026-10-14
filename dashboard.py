"""
dashboard.py - Clean, Modern Web Dashboard UI for Py12 Telegram Bot.
Runs locally without requiring any third-party web frameworks.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import os
import json
import threading
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import database

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Py12 Bot - Admin Analytics & Query Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .badge-command { background-color: #E0F2FE; color: #0369A1; }
    .badge-button { background-color: #ECFDF5; color: #047857; }
    .badge-question { background-color: #FDF2F8; color: #BE185D; }
    .badge-menu { background-color: #FEF3C7; color: #B45309; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen">
  <!-- Top Navigation Bar -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold text-xl shadow-md shadow-indigo-100">
          🤖
        </div>
        <div>
          <h1 class="font-bold text-lg text-slate-900 leading-tight">Py12 Bot Analytics & Queries</h1>
          <p class="text-xs text-slate-500 font-medium">Live Visitor Activity & Lead Stream</p>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <div class="flex items-center space-x-2 text-xs font-semibold px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Live Tracking Active</span>
        </div>
        
        <a href="/export.csv" download="users.csv" class="inline-flex items-center px-3.5 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-300 rounded-lg shadow-sm hover:bg-slate-50 transition">
          📥 Download CSV
        </a>

        <button onclick="fetchData()" id="refreshBtn" class="inline-flex items-center px-3.5 py-1.5 text-xs font-semibold text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700 transition">
          🔄 Refresh
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
    <!-- Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center text-2xl font-bold">
          👥
        </div>
        <div>
          <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Unique Visitors</p>
          <h3 id="statTotalUsers" class="text-2xl font-extrabold text-slate-900 mt-0.5">--</h3>
          <p class="text-xs text-slate-400 mt-0.5">Individual Telegram accounts</p>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-2xl font-bold">
          ⚡
        </div>
        <div>
          <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Interactions</p>
          <h3 id="statTotalInteractions" class="text-2xl font-extrabold text-slate-900 mt-0.5">--</h3>
          <p class="text-xs text-slate-400 mt-0.5">Button clicks & navigations</p>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center text-2xl font-bold">
          💬
        </div>
        <div>
          <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Recorded Actions / Log</p>
          <h3 id="statTotalQueries" class="text-2xl font-extrabold text-slate-900 mt-0.5">--</h3>
          <p class="text-xs text-slate-400 mt-0.5">Full audit trail entries</p>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-pink-50 text-pink-600 flex items-center justify-center text-2xl font-bold">
          📩
        </div>
        <div>
          <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Custom Questions</p>
          <h3 id="statCustomQuestions" class="text-2xl font-extrabold text-slate-900 mt-0.5">--</h3>
          <p class="text-xs text-slate-400 mt-0.5">Direct student questions/leads</p>
        </div>
      </div>
    </div>

    <!-- Tab Buttons -->
    <div class="flex items-center space-x-2 border-b border-slate-200 pb-2">
      <button onclick="switchTab('queries')" id="tabQueriesBtn" class="px-4 py-2 font-semibold text-sm rounded-lg bg-indigo-50 text-indigo-700 transition">
        📜 Live Queries & Activity Stream
      </button>
      <button onclick="switchTab('users')" id="tabUsersBtn" class="px-4 py-2 font-medium text-sm rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition">
        👥 Registered Visitors Directory
      </button>
    </div>

    <!-- Section 1: User Queries & Activity Stream -->
    <section id="sectionQueries" class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
      <!-- Table Filters -->
      <div class="p-4 border-b border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
        <div class="flex items-center space-x-3 w-full sm:w-auto">
          <input 
            type="text" 
            id="searchInput" 
            onkeyup="debouncedSearch()" 
            placeholder="🔍 Search student name, @username, or query text..." 
            class="w-full sm:w-80 px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
          >
          <select 
            id="typeFilter" 
            onchange="fetchQueries()" 
            class="px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white font-medium text-slate-700"
          >
            <option value="all">All Query Types</option>
            <option value="button">Button Clicks</option>
            <option value="question">User Questions</option>
            <option value="command">Bot Commands</option>
            <option value="menu">Bottom Menu</option>
          </select>
        </div>

        <div class="flex items-center space-x-2">
          <label class="text-xs font-semibold text-slate-500 flex items-center space-x-1.5 cursor-pointer">
            <input type="checkbox" id="autoRefreshCheck" checked onchange="toggleAutoRefresh()" class="rounded text-indigo-600 focus:ring-indigo-500">
            <span>Auto-refresh (every 5s)</span>
          </label>
        </div>
      </div>

      <!-- Table Content -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead class="bg-slate-50 text-slate-500 font-semibold text-xs uppercase tracking-wider">
            <tr>
              <th scope="col" class="px-5 py-3.5">Time</th>
              <th scope="col" class="px-5 py-3.5">Student / Visitor</th>
              <th scope="col" class="px-5 py-3.5">Type</th>
              <th scope="col" class="px-5 py-3.5">Query / Action Detail</th>
            </tr>
          </thead>
          <tbody id="queriesTableBody" class="divide-y divide-slate-100 bg-white font-medium">
            <tr>
              <td colspan="4" class="px-5 py-10 text-center text-slate-400">Loading student queries...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Section 2: Visitors Directory -->
    <section id="sectionUsers" class="hidden bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
      <div class="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/50">
        <div>
          <h3 class="font-bold text-slate-900 text-sm">All Unique Visitors</h3>
          <p class="text-xs text-slate-500">Ranked by latest activity timestamp</p>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead class="bg-slate-50 text-slate-500 font-semibold text-xs uppercase tracking-wider">
            <tr>
              <th scope="col" class="px-5 py-3.5">User</th>
              <th scope="col" class="px-5 py-3.5">Telegram ID</th>
              <th scope="col" class="px-5 py-3.5">First Seen</th>
              <th scope="col" class="px-5 py-3.5">Last Active</th>
              <th scope="col" class="px-5 py-3.5">Interactions</th>
              <th scope="col" class="px-5 py-3.5">Last Action</th>
            </tr>
          </thead>
          <tbody id="usersTableBody" class="divide-y divide-slate-100 bg-white font-medium">
            <tr>
              <td colspan="6" class="px-5 py-10 text-center text-slate-400">Loading visitor directory...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>

  <script>
    let autoRefreshTimer = null;

    function switchTab(tab) {
      const qSec = document.getElementById('sectionQueries');
      const uSec = document.getElementById('sectionUsers');
      const qBtn = document.getElementById('tabQueriesBtn');
      const uBtn = document.getElementById('tabUsersBtn');

      if (tab === 'queries') {
        qSec.classList.remove('hidden');
        uSec.classList.add('hidden');
        qBtn.className = 'px-4 py-2 font-semibold text-sm rounded-lg bg-indigo-50 text-indigo-700 transition';
        uBtn.className = 'px-4 py-2 font-medium text-sm rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition';
      } else {
        qSec.classList.add('hidden');
        uSec.classList.remove('hidden');
        uBtn.className = 'px-4 py-2 font-semibold text-sm rounded-lg bg-indigo-50 text-indigo-700 transition';
        qBtn.className = 'px-4 py-2 font-medium text-sm rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition';
        fetchUsers();
      }
    }

    function formatActionText(text) {
      if (!text) return '—';
      if (text.startsWith('button:modules_')) {
        return '📖 Checked Modules: <b>' + text.replace('button:modules_', '').replace('_', ' ') + '</b>';
      }
      if (text.startsWith('button:price_')) {
        return '💵 Checked Price: <b>' + text.replace('button:price_', '').replace('_', ' ') + '</b>';
      }
      if (text.startsWith('button:duration_')) {
        return '⏳ Checked Duration: <b>' + text.replace('button:duration_', '').replace('_', ' ') + '</b>';
      }
      if (text.startsWith('button:course_')) {
        return '🎓 Opened Course: <b>' + text.replace('button:course_', '').replace('_', ' ') + '</b>';
      }
      if (text.startsWith('button:enroll_')) {
        return '📝 Clicked Register: <b>' + text.replace('button:enroll_', '').replace('_', ' ') + '</b>';
      }
      if (text.startsWith('button:')) {
        return '🔘 Clicked ' + text.replace('button:', '');
      }
      return text;
    }

    async function fetchStats() {
      try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        document.getElementById('statTotalUsers').innerText = data.total_users || 0;
        document.getElementById('statTotalInteractions').innerText = data.total_interactions || 0;
        document.getElementById('statTotalQueries').innerText = data.total_queries || 0;
        document.getElementById('statCustomQuestions').innerText = data.custom_questions || 0;
      } catch (err) {
        console.error('Error fetching stats:', err);
      }
    }

    async function fetchQueries() {
      const type = document.getElementById('typeFilter').value;
      const search = document.getElementById('searchInput').value.trim();
      const tbody = document.getElementById('queriesTableBody');

      try {
        const url = `/api/queries?type=${encodeURIComponent(type)}&search=${encodeURIComponent(search)}`;
        const res = await fetch(url);
        const queries = await res.json();

        if (queries.length === 0) {
          tbody.innerHTML = `<tr><td colspan="4" class="px-5 py-8 text-center text-slate-400">No queries match your search or filter.</td></tr>`;
          return;
        }

        tbody.innerHTML = queries.map(q => {
          let badgeClass = 'badge-button';
          let badgeLabel = 'Button Click';
          if (q.query_type === 'question') {
            badgeClass = 'badge-question';
            badgeLabel = 'Question';
          } else if (q.query_type === 'command') {
            badgeClass = 'badge-command';
            badgeLabel = 'Command';
          } else if (q.query_type === 'menu') {
            badgeClass = 'badge-menu';
            badgeLabel = 'Menu';
          }

          const usernameDisplay = q.username && q.username !== 'N/A' 
            ? `<a href="https://t.me/${q.username.replace('@','')}" target="_blank" class="text-indigo-600 hover:underline text-xs">${q.username}</a>` 
            : `<span class="text-xs text-slate-400">No @handle</span>`;

          return `
            <tr class="hover:bg-slate-50/80 transition">
              <td class="px-5 py-3.5 whitespace-nowrap text-xs text-slate-500 font-mono">${q.created_at || '—'}</td>
              <td class="px-5 py-3.5">
                <div class="font-semibold text-slate-900">${q.full_name || 'Anonymous User'}</div>
                <div class="flex items-center space-x-1.5 mt-0.5">
                  ${usernameDisplay}
                  <span class="text-slate-300">•</span>
                  <span class="text-slate-400 text-xs font-mono">ID: ${q.user_id}</span>
                </div>
              </td>
              <td class="px-5 py-3.5 whitespace-nowrap">
                <span class="px-2.5 py-1 rounded-md text-xs font-semibold ${badgeClass}">
                  ${badgeLabel}
                </span>
              </td>
              <td class="px-5 py-3.5 text-slate-700">
                <div class="break-words">${formatActionText(q.query_text)}</div>
              </td>
            </tr>
          `;
        }).join('');
      } catch (err) {
        tbody.innerHTML = `<tr><td colspan="4" class="px-5 py-8 text-center text-rose-500 font-semibold">Error loading queries: ${err}</td></tr>`;
      }
    }

    async function fetchUsers() {
      const tbody = document.getElementById('usersTableBody');
      try {
        const res = await fetch('/api/users');
        const users = await res.json();

        if (users.length === 0) {
          tbody.innerHTML = `<tr><td colspan="6" class="px-5 py-8 text-center text-slate-400">No visitors recorded yet.</td></tr>`;
          return;
        }

        tbody.innerHTML = users.map(u => {
          const usernameDisplay = u.username && u.username !== 'N/A'
            ? `<a href="https://t.me/${u.username.replace('@','')}" target="_blank" class="text-indigo-600 hover:underline">${u.username}</a>`
            : `<span class="text-slate-400">N/A</span>`;

          const fullName = [u.first_name, u.last_name].filter(Boolean).join(' ') || 'Anonymous';

          return `
            <tr class="hover:bg-slate-50/80 transition">
              <td class="px-5 py-3.5">
                <div class="font-semibold text-slate-900">${fullName}</div>
                <div class="text-xs">${usernameDisplay}</div>
              </td>
              <td class="px-5 py-3.5 text-xs font-mono text-slate-500">${u.user_id}</td>
              <td class="px-5 py-3.5 text-xs text-slate-500 whitespace-nowrap font-mono">${u.first_seen}</td>
              <td class="px-5 py-3.5 text-xs text-slate-500 whitespace-nowrap font-mono">${u.last_active}</td>
              <td class="px-5 py-3.5">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-indigo-50 text-indigo-700">
                  ${u.interaction_count} clicks
                </span>
              </td>
              <td class="px-5 py-3.5 text-xs text-slate-600">
                ${formatActionText(u.last_action)}
              </td>
            </tr>
          `;
        }).join('');
      } catch (err) {
        tbody.innerHTML = `<tr><td colspan="6" class="px-5 py-8 text-center text-rose-500">Failed to load users: ${err}</td></tr>`;
      }
    }

    let searchTimeout = null;
    function debouncedSearch() {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(fetchQueries, 250);
    }

    function toggleAutoRefresh() {
      const isChecked = document.getElementById('autoRefreshCheck').checked;
      if (isChecked) {
        if (!autoRefreshTimer) {
          autoRefreshTimer = setInterval(() => {
            fetchStats();
            fetchQueries();
          }, 5000);
        }
      } else {
        if (autoRefreshTimer) {
          clearInterval(autoRefreshTimer);
          autoRefreshTimer = null;
        }
      }
    }

    function fetchData() {
      fetchStats();
      fetchQueries();
    }

    // Initial Load
    fetchData();
    toggleAutoRefresh();
  </script>
</body>
</html>
"""


class DashboardRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for serving dashboard UI and REST endpoints."""

    def log_message(self, format, *args):
        # Silence routine HTTP access logs to keep console clean
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
            return

        if path == "/api/stats":
            stats = database.get_analytics_summary()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode("utf-8"))
            return

        if path == "/api/queries":
            q_type = params.get("type", ["all"])[0]
            search = params.get("search", [""])[0]
            queries = database.get_all_queries(limit=250, query_type=q_type, search=search)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(queries).encode("utf-8"))
            return

        if path == "/api/users":
            users = database.get_all_users()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(users).encode("utf-8"))
            return

        if path == "/export.csv":
            count, file_path = database.export_users_to_csv("users.csv")
            try:
                with open(file_path, "rb") as f:
                    csv_data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="users.csv"')
                self.end_headers()
                self.wfile.write(csv_data)
                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode("utf-8"))
                return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 Not Found")


def run_dashboard_server(host: str = "127.0.0.1", port: int = 5000):
    """Runs dashboard HTTP server."""
    database.init_db()
    for p in [port, 5001, 8080, 8081]:
        try:
            server = HTTPServer((host, p), DashboardRequestHandler)
            print("=" * 65)
            print(f"📊 PY12 DASHBOARD UI IS LIVE!")
            print(f"👉 Open in your browser: http://localhost:{p}")
            print("=" * 65)
            server.serve_forever()
            return
        except OSError:
            continue


def start_dashboard_in_background(host: str = "127.0.0.1", port: int = 5000):
    """Starts the dashboard HTTP server in a separate background daemon thread."""
    t = threading.Thread(target=run_dashboard_server, args=(host, port), daemon=True)
    t.start()
    return t


if __name__ == "__main__":
    run_dashboard_server()

