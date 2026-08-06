// Shared expense summary component, version 03.
// Injects the tracker data files as <script> tags (script tags work on
// file:// where fetch/XHR do not), then renders one snapshot table on every
// tracker page: DeepSeek, Claude, Codex, WAN video, Qwen text.
//
// Version 03 (2026-08-06): Alibaba is now TWO rows, not one. WAN video
// generation and Qwen text share one Alibaba account and one bill, but they
// are different beasts and are never summed together here. Both come from
// alibaba_spend.js, which reads the real bill instead of estimating.

(function() {
  "use strict";

  var DATA_FILES = [
    "../deepseek_cost_projector/deepseek_balance.js",
    "../claude_cost_projector/claude_readings.js",
    "../codex_cost_projector/allowance_history.js",
    "../quen_cost_projector/alibaba_spend.js"
  ];

  function money(v) {
    if (v === null || v === undefined || isNaN(v)) return "-";
    return "$" + Number(v).toFixed(2);
  }

  function sameLocalDay(epochSec, nowMs) {
    var a = new Date(epochSec * 1000), b = new Date(nowMs);
    return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
  }

  function deepseekRow() {
    var d = window.DEEPSEEK_BALANCE;
    if (!d || !d.snapshots || !d.snapshots.length) return null;
    var nowMs = Date.now();
    var weekCut = nowMs / 1000 - 7 * 86400;
    var lifetime = 0, today = 0, week = 0;
    d.snapshots.forEach(function(s) {
      lifetime += s.spend || 0;
      if (s.t >= weekCut) week += s.spend || 0;
      if (sameLocalDay(s.t, nowMs)) today += s.spend || 0;
    });
    var balance = d.snapshots[d.snapshots.length - 1].balance;
    return {
      name: "DeepSeek", link: "../deepseek_cost_projector/deepseek_tracker.html",
      lifetime: lifetime, today: today, week: week,
      status: "prepaid, " + money(balance) + " left"
    };
  }

  function claudeRow() {
    var r = window.CLAUDE_READINGS;
    if (!r || !r.length) return null;
    var latest = r[r.length - 1];
    var pct = latest.used <= 1 ? latest.used * 100 : latest.used;
    return {
      name: "Claude", link: "../claude_cost_projector/tracker.html",
      lifetime: null, today: null, week: null,
      status: Math.round(pct) + "% used, resets " + latest.resetDate + " " + latest.resetTime
    };
  }

  function codexRow() {
    var h = window.CODEX_ALLOWANCE_HISTORY;
    if (!h || !h.latest) return null;
    return {
      name: "Codex", link: "../codex_cost_projector/projector.html",
      lifetime: null, today: null, week: null,
      status: h.latest.usedPercent + "% used (" + h.latest.leftPercent + "% left)"
    };
  }

  function alibabaRow(bucketKey, label) {
    var a = window.ALIBABA_SPEND;
    var b = a && a[bucketKey];
    if (!b) return null;
    return {
      name: label, link: "../quen_cost_projector/quen_tracker.html",
      lifetime: b.lifetime_usd, today: b.today_usd, week: b.last_7_days_usd,
      status: a.live ? "real Alibaba bill" : "real bill, last read " +
        new Date((a.updated || 0) * 1000).toLocaleDateString()
    };
  }

  function wanRow() { return alibabaRow("video", "WAN video (Alibaba)"); }
  function qwenRow() { return alibabaRow("qwen", "Qwen text (Alibaba)"); }

  function render() {
    var tbody = document.getElementById("summaryBody");
    if (!tbody) return;
    var rows = [deepseekRow(), claudeRow(), codexRow(), wanRow(), qwenRow()].filter(Boolean);
    if (!rows.length) {
      tbody.innerHTML = "<tr><td colspan='5'>No data available</td></tr>";
      return;
    }
    tbody.innerHTML = rows.map(function(row) {
      return "<tr><td><a href='" + row.link + "'>" + row.name + "</a></td><td>" +
        money(row.lifetime) + "</td><td>" + money(row.today) + "</td><td>" +
        money(row.week) + "</td><td>" + row.status + "</td></tr>";
    }).join("");
  }

  function mount() {
    if (document.getElementById("expenseSummaryBox")) { render(); return; }
    var style = document.createElement("style");
    style.textContent = ".expense-summary{background:var(--paper,#fff);border:1px solid var(--line,#dce3e8);border-radius:18px;padding:20px;margin:0 0 16px}" +
      ".expense-summary h3{margin:0 0 16px;font-size:20px}" +
      ".summary-table{width:100%;border-collapse:collapse;font-size:14px}" +
      ".summary-table th{text-align:left;padding:10px 8px;border-bottom:2px solid var(--line,#dce3e8);color:var(--muted,#65717d);font-weight:650;font-size:13px;text-transform:uppercase;letter-spacing:.04em}" +
      ".summary-table td{padding:10px 8px;border-bottom:1px solid var(--line,#dce3e8)}" +
      ".summary-table tr:last-child td{border-bottom:none}" +
      ".summary-table a{color:var(--blue,#1769e0);text-decoration:none;font-weight:600}" +
      ".summary-table a:hover{text-decoration:underline}";
    document.head.appendChild(style);

    var box = document.createElement("div");
    box.className = "expense-summary";
    box.id = "expenseSummaryBox";
    box.innerHTML = "<h3>All expenses snapshot</h3><table class='summary-table'><thead><tr><th>Source</th><th>Lifetime</th><th>Today</th><th>7 days</th><th>Status</th></tr></thead><tbody id='summaryBody'><tr><td colspan='5'>Loading…</td></tr></tbody></table>";
    var nav = document.querySelector(".monitors");
    var anchor = nav && nav.closest("header") ? nav.closest("header") : nav;
    if (anchor && anchor.parentNode) {
      anchor.parentNode.insertBefore(box, anchor.nextSibling);
    } else if (document.querySelector("main")) {
      document.querySelector("main").insertBefore(box, document.querySelector("main").children[1] || null);
    } else {
      document.body.appendChild(box);
    }

    var pending = DATA_FILES.length;
    var done = false;
    function finish() {
      if (done) return;
      done = true;
      render();
    }
    DATA_FILES.forEach(function(src) {
      var s = document.createElement("script");
      s.src = src;
      s.async = false;
      s.onload = function() { pending -= 1; if (pending <= 0) finish(); };
      s.onerror = function() { pending -= 1; if (pending <= 0) finish(); };
      document.head.appendChild(s);
    });
    setTimeout(finish, 2500);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
