// Shared Qwen-style zoomable slider chart, version 01.
// Ports the Quen (Qwen) spend tracker chart to the Codex, Claude, and
// DeepSeek tracker pages. Each page supplies its own time series through
// getSeries, so every tracker keeps its own data source and this one file
// holds the shared graphing principle (smooth log-scale time zoom slider
// from 1 hour to full history with no jumps, auto-fit value axis, date ticks,
// and per-zoom spend report).
(function () {
  "use strict";
  var SVG = "http://www.w3.org/2000/svg";

  function fmtDur(sec) {
    if (sec < 3600) return Math.round(sec / 60) + " min";
    if (sec < 86400) return (sec / 3600).toFixed(1) + " hours";
    return (sec / 86400).toFixed(1) + " days";
  }

  function fmtTick(ts) {
    var x = new Date(ts * 1000);
    var h = x.getHours(), ampm = h >= 12 ? "PM" : "AM";
    h = h % 12 || 12;
    return (x.getMonth() + 1) + "/" + x.getDate() + " " + h + ":" + String(x.getMinutes()).padStart(2, "0") + " " + ampm;
  }

  function fmtValue(cfg, v) {
    if (cfg.unit === "%") return v.toFixed(1) + "%";
    return "$" + v.toFixed(2);
  }

  function mount(cfg) {
    var host = document.getElementById(cfg.mountId);
    if (!host || host.dataset.qslMounted) return;
    host.dataset.qslMounted = "1";

    var accent = cfg.accent || "#6f42c1";
    var style = document.createElement("style");
    style.textContent = [
      ".qsl-card{background:var(--paper,#fff);border:1px solid var(--line,#dce3e8);border-radius:18px;box-shadow:0 3px 14px #1825360a;padding:24px;margin-bottom:16px}",
      ".qsl-head{display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:16px}",
      ".qsl-head h2{margin:0;font-size:22px}",
      ".qsl-sub{color:var(--muted,#65717d)}",
      ".qsl-delta{margin-top:6px;color:var(--muted,#65717d);font-size:13px}",
      ".qsl-zoom{display:flex;align-items:center;gap:14px;margin:14px 0 2px;color:var(--muted,#65717d);font-size:14px}",
      ".qsl-zoom input{flex:1;accent-color:" + accent + "}",
      ".qsl-zoom .qsl-zoomValue{font-weight:700;color:var(--ink,#17202a);white-space:nowrap}",
      ".qsl-wrap{position:relative;width:min(100%,760px);margin:auto;aspect-ratio:100/60;border-left:2px solid var(--ink,#17202a);border-bottom:2px solid var(--ink,#17202a);background:linear-gradient(to right,transparent 24.8%,var(--line,#dce3e8) 25%,transparent 25.2%,transparent 49.8%,var(--line,#dce3e8) 50%,transparent 50.2%,transparent 74.8%,var(--line,#dce3e8) 75%,transparent 75.2%),linear-gradient(to top,transparent 24.8%,var(--line,#dce3e8) 25%,transparent 25.2%,transparent 49.8%,var(--line,#dce3e8) 50%,transparent 50.2%,transparent 74.8%,var(--line,#dce3e8) 75%,transparent 75.2%)}",
      ".qsl-wrap svg{display:block;width:100%;height:100%;overflow:visible}",
      ".qsl-line{stroke:" + accent + ";stroke-width:.7;fill:none;stroke-linecap:round;stroke-linejoin:round}",
      ".qsl-dot{fill:var(--paper,#fff);stroke:" + accent + ";stroke-width:.45}",
      ".qsl-now{stroke:var(--amber,#b36500);stroke-width:.7;stroke-dasharray:1.2 1.2;opacity:.8}",
      ".qsl-ygrid line{stroke:var(--line,#dce3e8);stroke-width:.3}",
      ".qsl-ygrid text{fill:var(--muted,#65717d);font-size:2.6px}",
      ".qsl-datetick line{stroke:var(--ink,#17202a);stroke-width:.5}",
      ".qsl-datetick text{fill:var(--muted,#65717d);font-size:2.8px}",
      ".qsl-axis{position:absolute;color:var(--muted,#65717d);font-size:11px}",
      ".qsl-axisTop{top:0;left:-8px;transform:translate(-100%,-50%)}",
      ".qsl-axisBottom{left:-8px;bottom:0;transform:translate(-100%,50%)}"
    ].join("");
    document.head.appendChild(style);

    var section = document.createElement("section");
    section.className = "qsl-card";
    section.innerHTML =
      '<div class="qsl-head"><div><h2></h2><div class="qsl-sub"></div><div class="qsl-delta"></div></div><div class="qsl-sub qsl-status"></div></div>' +
      '<div class="qsl-zoom"><label for="qsl-zoom">Zoom time scale</label><span class="qsl-zoomValue"></span><input type="range" id="qsl-zoom" min="1" max="40" step="1" value="40" aria-label="How far back the time axis extends"></div>' +
      '<div class="qsl-wrap"><span class="qsl-axis qsl-axisTop"></span><span class="qsl-axis qsl-axisBottom"></span>' +
      '<svg viewBox="0 0 100 60" role="img" aria-label="' + (cfg.ariaLabel || "Value over time") + '">' +
      '<line class="qsl-now" x1="0" y1="0" x2="0" y2="60"></line>' +
      '<g class="qsl-ytickg"></g>' +
      '<polyline class="qsl-line"></polyline>' +
      '<g class="qsl-dotg"></g>' +
      '<g class="qsl-datetickg"></g></svg></div>';
    host.appendChild(section);

    section.querySelector("h2").textContent = cfg.title;
    section.querySelector(".qsl-sub").textContent = cfg.subtitle || "";

    var zoomRange = section.querySelector("#qsl-zoom");
    var zoomLabel = section.querySelector(".qsl-zoomValue");
    var actualLine = section.querySelector(".qsl-line");
    var dotsGroup = section.querySelector(".qsl-dotg");
    var dateTicksGroup = section.querySelector(".qsl-datetickg");
    var yTicksGroup = section.querySelector(".qsl-ytickg");
    var nowLine = section.querySelector(".qsl-now");
    var axisTop = section.querySelector(".qsl-axisTop");
    var axisBottom = section.querySelector(".qsl-axisBottom");
    var deltaReport = section.querySelector(".qsl-delta");
    var sampleStatus = section.querySelector(".qsl-status");
    var L = 4, R = 98, T = 2, B = 58, W = R - L, H = B - T;
    var retryTimer = null;

    function series() {
      try { return cfg.getSeries() || []; } catch (e) { return []; }
    }

    function render() {
      var data = series().filter(function (p) {
        return p && typeof p[0] === "number" && typeof p[1] === "number";
      });
      if (data.length < 2) {
        deltaReport.textContent = cfg.emptyMessage || "Waiting for data. The collector adds points on its schedule.";
        sampleStatus.textContent = "0 points";
        actualLine.setAttribute("points", "");
        dotsGroup.innerHTML = "";
        dateTicksGroup.innerHTML = "";
        yTicksGroup.innerHTML = "";
        if (!retryTimer) {
          retryTimer = setTimeout(function () {
            retryTimer = null;
            render();
          }, 2000);
        }
        return;
      }

      var zoomValue = parseInt(zoomRange.value, 10);
      var maxZoom = 40;
      var now = Math.floor(Date.now() / 1000);
      var dataSpan = Math.max(now - data[0][0], 3600);
      var minWindow = 3600;
      var ratio = Math.pow(dataSpan / minWindow, (zoomValue - 1) / (maxZoom - 1));
      var timeRange = minWindow * ratio;
      var visible = data.filter(function (p) { return p[0] >= now - timeRange; });
      if (visible.length < 2) visible = data.slice(-2);
      zoomLabel.textContent = zoomValue >= maxZoom ? "Full history" : fmtDur(Math.min(timeRange, dataSpan));
      if (visible.length < 2) return;

      var tMin = visible[0][0], tMax = visible[visible.length - 1][0];
      var tRange = Math.max(tMax - tMin, 1);
      var vals = visible.map(function (p) { return p[1]; });
      var yMin = Math.min.apply(null, vals), yMax = Math.max.apply(null, vals);
      var yPad = Math.max(yMax - yMin, 0.01) * 0.08;
      var yLow = Math.max(yMin - yPad, 0), yHigh = yMax + yPad, ySpan = yHigh - yLow;
      axisTop.textContent = fmtValue(cfg, yHigh);
      axisBottom.textContent = fmtValue(cfg, yLow);

      function sx(t) { return L + ((t - tMin) / tRange) * W; }
      function sy(v) { return B - ((v - yLow) / ySpan) * H; }

      actualLine.setAttribute("points", visible.map(function (p) {
        return sx(p[0]).toFixed(2) + "," + sy(p[1]).toFixed(2);
      }).join(" "));
      nowLine.setAttribute("x1", sx(tMax).toFixed(2));
      nowLine.setAttribute("x2", sx(tMax).toFixed(2));

      dotsGroup.innerHTML = "";
      if (visible.length <= 160) {
        visible.forEach(function (p) {
          var c = document.createElementNS(SVG, "circle");
          c.setAttribute("class", "qsl-dot");
          c.setAttribute("cx", sx(p[0]).toFixed(2));
          c.setAttribute("cy", sy(p[1]).toFixed(2));
          c.setAttribute("r", "0.6");
          dotsGroup.appendChild(c);
        });
      }

      yTicksGroup.innerHTML = "";
      for (var i = 0; i <= 5; i++) {
        var val = yLow + i * (ySpan / 5);
        var y = sy(val);
        var grid = document.createElementNS(SVG, "line");
        grid.setAttribute("class", "qsl-ygrid");
        grid.setAttribute("x1", L); grid.setAttribute("x2", R);
        grid.setAttribute("y1", y.toFixed(2)); grid.setAttribute("y2", y.toFixed(2));
        yTicksGroup.appendChild(grid);
        var lab = document.createElementNS(SVG, "text");
        lab.setAttribute("class", "qsl-ygrid");
        lab.setAttribute("font-size", "2.6");
        lab.setAttribute("x", L - 1); lab.setAttribute("y", y.toFixed(2));
        lab.setAttribute("text-anchor", "end");
        lab.setAttribute("dominant-baseline", "middle");
        lab.textContent = fmtValue(cfg, val);
        yTicksGroup.appendChild(lab);
      }

      dateTicksGroup.innerHTML = "";
      var tickCount = 6;
      for (var j = 0; j < tickCount; j++) {
        var t = tMin + (j / (tickCount - 1)) * tRange;
        var x = sx(t);
        var tick = document.createElementNS(SVG, "g");
        tick.setAttribute("class", "qsl-datetick");
        var tl = document.createElementNS(SVG, "line");
        tl.setAttribute("x1", x.toFixed(2)); tl.setAttribute("x2", x.toFixed(2));
        tl.setAttribute("y1", B); tl.setAttribute("y2", B + 1.5);
        tick.appendChild(tl);
        var tt = document.createElementNS(SVG, "text");
        tt.setAttribute("font-size", "2.8");
        tt.setAttribute("x", x.toFixed(2)); tt.setAttribute("y", B + 4);
        tt.setAttribute("text-anchor", "middle");
        tt.textContent = fmtTick(t);
        tick.appendChild(tt);
        dateTicksGroup.appendChild(tick);
      }

      var spendDelta = visible[visible.length - 1][1] - visible[0][1];
      var timeDelta = tMax - tMin;
      var perHour = timeDelta > 0 ? spendDelta / (timeDelta / 3600) : 0;
      deltaReport.textContent = cfg.unit === "%"
        ? "This zoom: " + spendDelta.toFixed(1) + " pp over " + fmtDur(timeDelta) +
          " (" + perHour.toFixed(2) + " pp/hr, " + (perHour * 24).toFixed(1) + " pp/day)"
        : "This zoom: $" + spendDelta.toFixed(4) + " over " + fmtDur(timeDelta) +
          " ($" + perHour.toFixed(4) + "/hr, $" + (perHour * 24).toFixed(2) + "/day)";
      sampleStatus.textContent = visible.length + " points";
    }

    zoomRange.addEventListener("input", render);
    render();
    setInterval(render, 60000);
  }

  window.ExpenseSliderChart = { mount: mount };
})();
