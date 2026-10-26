\<\!DOCTYPE html\>  
\<html lang="en"\>  
\<head\>  
  \<meta charset="UTF-8"\>  
  \<meta name="viewport" content="width=device-width, initial-scale=1.0"\>  
  \<title\>ARINC812Forge Pro — Galley Insert Equipment (GAIN) & GNC Studio\</title\>  
  \<style\>  
    :root {  
      \--bg-dark: \#0a0f18;  
      \--card-bg: \#111927;  
      \--card-border: \#1e293b;  
      \--primary: \#38bdf8;  
      \--accent: \#0ea5e9;  
      \--success: \#10b981;  
      \--warning: \#f59e0b;  
      \--danger: \#ef4444;  
      \--text: \#f1f5f9;  
      \--text-muted: \#94a3b8;  
      \--font-mono: 'JetBrains Mono', 'Fira Code', monospace;  
    }  
    \* { box-sizing: border-box; margin: 0; padding: 0; }  
    body {  
      background: var(--bg-dark);  
      color: var(--text);  
      font-family: \-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;  
      padding: 1.5rem;  
      line-height: 1.5;  
    }  
    header {  
      display: flex;  
      justify-content: space-between;  
      align-items: center;  
      padding-bottom: 1.5rem;  
      border-bottom: 1px solid var(--card-border);  
      margin-bottom: 1.5rem;  
    }  
    .brand {  
      display: flex;  
      align-items: center;  
      gap: 1rem;  
    }  
    .logo-badge {  
      background: linear-gradient(135deg, \#0284c7, \#0369a1);  
      color: white;  
      padding: 0.5rem 0.8rem;  
      border-radius: 6px;  
      font-weight: 800;  
      font-size: 1.1rem;  
      letter-spacing: 1px;  
    }  
    .brand-title h1 {  
      font-size: 1.4rem;  
      font-weight: 700;  
      color: \#fff;  
    }  
    .brand-title p {  
      font-size: 0.85rem;  
      color: var(--text-muted);  
    }  
    .status-badge {  
      display: inline-flex;  
      align-items: center;  
      gap: 0.5rem;  
      padding: 0.4rem 0.8rem;  
      border-radius: 9999px;  
      font-size: 0.85rem;  
      font-weight: 600;  
      background: rgba(16, 185, 129, 0.15);  
      color: \#34d399;  
      border: 1px solid rgba(16, 185, 129, 0.3);  
    }  
    .status-badge.shedding {  
      background: rgba(245, 158, 11, 0.15);  
      color: \#fbbf24;  
      border: 1px solid rgba(245, 158, 11, 0.3);  
    }  
    .nav-tabs {  
      display: flex;  
      gap: 0.5rem;  
      margin-bottom: 1.5rem;  
      border-bottom: 1px solid var(--card-border);  
      padding-bottom: 0.5rem;  
    }  
    .tab-btn {  
      background: transparent;  
      border: none;  
      color: var(--text-muted);  
      padding: 0.6rem 1.2rem;  
      border-radius: 6px;  
      cursor: pointer;  
      font-weight: 600;  
      font-size: 0.9rem;  
      transition: all 0.2s;  
    }  
    .tab-btn:hover {  
      background: rgba(255, 255, 255, 0.05);  
      color: var(--text);  
    }  
    .tab-btn.active {  
      background: var(--card-bg);  
      color: var(--primary);  
      border: 1px solid var(--card-border);  
    }  
    .grid-2 {  
      display: grid;  
      grid-template-columns: 1fr 1fr;  
      gap: 1.5rem;  
    }  
    .grid-3 {  
      display: grid;  
      grid-template-columns: repeat(3, 1fr);  
      gap: 1.5rem;  
    }  
    .card {  
      background: var(--card-bg);  
      border: 1px solid var(--card-border);  
      border-radius: 8px;  
      padding: 1.25rem;  
      margin-bottom: 1.5rem;  
    }  
    .card-header {  
      display: flex;  
      justify-content: space-between;  
      align-items: center;  
      margin-bottom: 1rem;  
      padding-bottom: 0.5rem;  
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);  
    }  
    .card-title {  
      font-size: 1.05rem;  
      font-weight: 600;  
      color: var(--primary);  
      display: flex;  
      align-items: center;  
      gap: 0.5rem;  
    }  
    .data-row {  
      display: flex;  
      justify-content: space-between;  
      padding: 0.4rem 0;  
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);  
      font-size: 0.9rem;  
    }  
    .data-row .label { color: var(--text-muted); }  
    .data-row .val { font-weight: 500; font-family: var(--font-mono); }  
    table {  
      width: 100%;  
      border-collapse: collapse;  
      margin-top: 0.5rem;  
      font-size: 0.88rem;  
    }  
    th, td {  
      padding: 0.6rem;  
      text-align: left;  
      border-bottom: 1px solid var(--card-border);  
    }  
    th {  
      color: var(--text-muted);  
      font-weight: 600;  
      background: rgba(0, 0, 0, 0.2);  
    }  
    .badge {  
      display: inline-block;  
      padding: 0.2rem 0.5rem;  
      border-radius: 4px;  
      font-size: 0.75rem;  
      font-weight: 600;  
      font-family: var(--font-mono);  
    }  
    .badge-granted { background: rgba(16, 185, 129, 0.2); color: \#34d399; }  
    .badge-shedded { background: rgba(245, 158, 11, 0.2); color: \#fbbf24; }  
    .badge-fault { background: rgba(239, 68, 68, 0.2); color: \#f87171; }  
    .btn {  
      background: var(--accent);  
      color: white;  
      border: none;  
      padding: 0.5rem 1rem;  
      border-radius: 6px;  
      cursor: pointer;  
      font-weight: 600;  
      font-size: 0.85rem;  
      transition: background 0.2s;  
    }  
    .btn:hover { background: \#0284c7; }  
    .btn-outline {  
      background: transparent;  
      border: 1px solid var(--card-border);  
      color: var(--text);  
    }  
    .btn-outline:hover { background: rgba(255, 255, 255, 0.05); }  
    .code-block {  
      background: \#060910;  
      border: 1px solid var(--card-border);  
      border-radius: 6px;  
      padding: 1rem;  
      font-family: var(--font-mono);  
      font-size: 0.82rem;  
      color: \#38bdf8;  
      overflow-x: auto;  
    }  
    .tab-content { display: none; }  
    .tab-content.active { display: block; }  
    .progress-bar {  
      height: 8px;  
      background: rgba(255, 255, 255, 0.1);  
      border-radius: 4px;  
      overflow: hidden;  
      margin: 0.5rem 0;  
    }  
    .progress-fill {  
      height: 100%;  
      background: linear-gradient(90deg, \#0284c7, \#10b981);  
      width: 0%;  
      transition: width 0.3s ease;  
    }  
  \</style\>  
\</head\>  
\<body\>

  \<header\>  
    \<div class="brand"\>  
      \<div class="logo-badge"\>ARINC 812\</div\>  
      \<div class="brand-title"\>  
        \<h1\>ARINC812Forge Pro — Galley Insert \&amp; GNC Studio\</h1\>  
        \<p\>Commercial Aviation Galley Insert Equipment (GAIN) \&amp; CAN 2.0B Power Shedding Controller\</p\>  
      \</div\>  
    \</div\>  
    \<div style="display: flex; gap: 1rem; align-items: center;"\>  
      \<div class="status-badge" id="gnc-status-badge"\>  
        \<span\>●\</span\> GNC NORMAL — TOTAL LOAD: 10.1 kVA  
      \</div\>  
      \<button class="btn btn-outline" id="toggle-gen-btn" onclick="toggleSingleGenerator()"\>Toggle Single Gen Mode\</button\>  
      \<button class="btn" onclick="runNormativeAudit()"\>Run 10-Point Audit\</button\>  
    \</div\>  
  \</header\>

  \<nav class="nav-tabs"\>  
    \<button class="tab-btn active" onclick="switchTab('rack')"\>Galley Insert Rack\</button\>  
    \<button class="tab-btn" onclick="switchTab('feeders')"\>Power Feeders \&amp; Shedding\</button\>  
    \<button class="tab-btn" onclick="switchTab('canbus')"\>CAN 2.0B Bus Monitor\</button\>  
    \<button class="tab-btn" onclick="switchTab('arinc429')"\>ARINC 429 Telemetry\</button\>  
    \<button class="tab-btn" onclick="switchTab('auditor')"\>Compliance Auditor\</button\>  
  \</nav\>

  \<\!-- TAB: GALLEY INSERT RACK \--\>  
  \<div id="tab-rack" class="tab-content active"\>  
    \<div class="grid-3" id="gain-cards-container"\>  
      \<\!-- Injected by JS \--\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: POWER FEEDERS & SHEDDING \--\>  
  \<div id="tab-feeders" class="tab-content"\>  
    \<div class="grid-2"\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>Feeder A (115VAC 400Hz 3-Phase)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Feeder Rating:\</span\>\<span class="val"\>8.0 kVA\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Current Load:\</span\>\<span class="val" id="feeder-a-load"\>6.10 kVA (76.2%)\</span\>\</div\>  
        \<div class="progress-bar"\>\<div class="progress-fill" id="feeder-a-bar" style="width: 76.2%;"\>\</div\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Voltage / Frequency:\</span\>\<span class="val"\>115.0 VAC / 400.0 Hz\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Allocated Inserts:\</span\>\<span class="val"\>Oven 1 (3.1k), Oven 2 (3.0k)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Overload Status:\</span\>\<span class="val" style="color:\#34d399;"\>NORMAL\</span\>\</div\>  
      \</div\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>Feeder B (115VAC 400Hz 3-Phase)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Feeder Rating:\</span\>\<span class="val"\>6.0 kVA\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Current Load:\</span\>\<span class="val" id="feeder-b-load"\>4.00 kVA (66.7%)\</span\>\</div\>  
        \<div class="progress-bar"\>\<div class="progress-fill" id="feeder-b-bar" style="width: 66.7%;"\>\</div\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Voltage / Frequency:\</span\>\<span class="val"\>115.0 VAC / 400.0 Hz\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Allocated Inserts:\</span\>\<span class="val"\>Chiller (1.4k), Espresso (2.6k)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Overload Status:\</span\>\<span class="val" style="color:\#34d399;"\>NORMAL\</span\>\</div\>  
      \</div\>  
    \</div\>  
    \<div class="card"\>  
      \<div class="card-header"\>\<span class="card-title"\>Galley Network Controller (GNC) Dynamic Shedding Logic\</span\>\</div\>  
      \<p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;"\>  
        The GNC constantly evaluates feeder loads against primary generator limits. When shedding is triggered (e.g. single-generator de-rate or feeder overcurrent), loads are automatically shed in reverse priority order:  
      \</p\>  
      \<div class="data-row"\>\<span class="label"\>Priority 1 (Preserved):\</span\>\<span class="val" style="color:\#34d399;"\>Galley Air Chiller (Food safety 4°C rule)\</span\>\</div\>  
      \<div class="data-row"\>\<span class="label"\>Priority 2 \&amp; 3 (Heating):\</span\>\<span class="val"\>Convection Steam Ovens 1 \&amp; 2\</span\>\</div\>  
      \<div class="data-row"\>\<span class="label"\>Priority 4 (Beverage):\</span\>\<span class="val"\>Espresso / Hot Beverage Maker\</span\>\</div\>  
      \<div class="data-row"\>\<span class="label"\>Priority 5 (Water):\</span\>\<span class="val" style="color:\#fbbf24;"\>Rapid Water Boiler (First heating load to shed)\</span\>\</div\>  
      \<div class="data-row"\>\<span class="label"\>Priority 6 (Mechanical):\</span\>\<span class="val" style="color:\#f87171;"\>Trash Compactor (Lowest priority)\</span\>\</div\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: CAN BUS MONITOR \--\>  
  \<div id="tab-canbus" class="tab-content"\>  
    \<div class="card"\>  
      \<div class="card-header"\>  
        \<span class="card-title"\>ARINC 812 CAN 2.0B 29-Bit Extended Telemetry Frame Log\</span\>  
        \<span style="font-family:var(--font-mono); font-size:0.8rem; color:\#38bdf8;"\>BAUD: 125 KBPS / 250 KBPS (ISO 11898-1)\</span\>  
      \</div\>  
      \<table\>  
        \<thead\>  
          \<tr\>  
            \<th\>CAN ID (29-Bit)\</th\>  
            \<th\>Priority\</th\>  
            \<th\>PDU Type\</th\>  
            \<th\>Dest Addr\</th\>  
            \<th\>Source Addr\</th\>  
            \<th\>GAIN Device\</th\>  
            \<th\>Payload (Hex)\</th\>  
            \<th\>State\</th\>  
          \</tr\>  
        \</thead\>  
        \<tbody id="can-table-body"\>  
          \<\!-- Injected by JS \--\>  
        \</tbody\>  
      \</table\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: ARINC 429 \--\>  
  \<div id="tab-arinc429" class="tab-content"\>  
    \<div class="card"\>  
      \<div class="card-header"\>\<span class="card-title"\>Cabin Management System (CMS) ARINC 429 Discrete Bus Telemetry\</span\>\</div\>  
      \<div class="grid-2"\>  
        \<div\>  
          \<h4 style="color:\#38bdf8; margin-bottom:0.5rem;"\>Label 264 (Octal): Galley Feeder Load \&amp; Shedding Status\</h4\>  
          \<div class="code-block" id="label264-display"\>  
Hex:     0x300230B4  
Binary:  0011 0000 0000 0010 0011 0000 1011 0100  
Label:   0xB4 (Octal 264\)  
Bits 11-14 (Feeder A): 12 (6.0 kVA)  
Bits 15-18 (Feeder B): 8 (4.0 kVA)  
Bit 19 (Shedding):     0 (Normal)  
Bit 32 (Parity):       0 (Odd Parity Valid)  
          \</div\>  
        \</div\>  
        \<div\>  
          \<h4 style="color:\#38bdf8; margin-bottom:0.5rem;"\>Label 265 (Octal): GAIN Device Health \&amp; Bus Mode\</h4\>  
          \<div class="code-block" id="label265-display"\>  
Hex:     0x300018B5  
Binary:  0011 0000 0000 0000 0001 1000 1011 0101  
Label:   0xB5 (Octal 265\)  
Bits 11-16 (Online):   6 Inserts Online  
Bits 17-22 (Faulted):  0 Faulted  
Bits 23-24 (Gen Mode): 0 (Dual Gen Normal)  
Bit 32 (Parity):       0 (Odd Parity Valid)  
          \</div\>  
        \</div\>  
      \</div\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: AUDITOR \--\>  
  \<div id="tab-auditor" class="tab-content"\>  
    \<div class="card"\>  
      \<div class="card-header"\>  
        \<span class="card-title"\>Normative Galley Insert Regulatory Compliance Audit\</span\>  
        \<span id="audit-score" style="font-family:var(--font-mono); color:\#34d399; font-weight:700;"\>10 / 10 CHECKS PASSED (100.0%)\</span\>  
      \</div\>  
      \<div id="audit-results-list"\>  
        \<\!-- Rendered by JS \--\>  
      \</div\>  
    \</div\>  
  \</div\>

  \<script src="arinc812-engine.js"\>\</script\>  
  \<script src="arinc812-auditor.js"\>\</script\>  
  \<script\>  
    const engine \= new ARINC812Engine();

    function switchTab(tabId) {  
      document.querySelectorAll('.tab-btn').forEach(b \=\> b.classList.remove('active'));  
      document.querySelectorAll('.tab-content').forEach(c \=\> c.classList.remove('active'));  
      event.target.classList.add('active');  
      document.getElementById('tab-' \+ tabId).classList.add('active');  
    }

    function renderRack() {  
      const container \= document.getElementById('gain-cards-container');  
      container.innerHTML \= engine.gainDevices.map(g \=\> \`  
        \<div class="card"\>  
          \<div class="card-header"\>  
            \<span class="card-title"\>\${g.name}\</span\>  
            \<span class="badge \${g.powerGranted ? 'badge-granted' : (g.biteStatus==='FAULT'?'badge-fault':'badge-shedded')}"\>  
              \${g.powerGranted ? 'POWER GRANTED' : (g.biteStatus==='FAULT'?'BITE FAULT':'SHEDDED')}  
            \</span\>  
          \</div\>  
          \<div class="data-row"\>\<span class="label"\>ID / ATA:\</span\>\<span class="val"\>\${g.id} (\${g.ataChapter})\</span\>\</div\>  
          \<div class="data-row"\>\<span class="label"\>CAN Address:\</span\>\<span class="val"\>0x\${g.canAddress.toString(16).toUpperCase()}\</span\>\</div\>  
          \<div class="data-row"\>\<span class="label"\>Power Feeder:\</span\>\<span class="val"\>\${g.feeder} (\${g.actualKva} kVA)\</span\>\</div\>  
          \<div class="data-row"\>\<span class="label"\>Priority:\</span\>\<span class="val"\>Priority \${g.priority}\</span\>\</div\>  
          \<div class="data-row"\>\<span class="label"\>Temperature:\</span\>\<span class="val"\>\${g.temperatureC}°C (Target: \${g.targetTempC}°C)\</span\>\</div\>  
          \<div class="data-row"\>\<span class="label"\>BITE Health:\</span\>\<span class="val" style="color:\${g.biteStatus==='NORMAL'?'\#34d399':'\#f87171'}"\>\${g.biteStatus}\</span\>\</div\>  
        \</div\>  
      \`).join('');  
    }

    function renderCanBus() {  
      const tbody \= document.getElementById('can-table-body');  
      tbody.innerHTML \= engine.gainDevices.map(g \=\> {  
        const canId \= engine.encodeCan29BitId(g.priority, 0x05, 0x01, g.canAddress);  
        return \`  
          \<tr\>  
            \<td style="font-family:var(--font-mono); color:var(--primary);"\>0x\${canId.toString(16).toUpperCase().padStart(8, '0')}\</td\>  
            \<td\>Priority \${g.priority}\</td\>  
            \<td\>0x05 (Telemetry)\</td\>  
            \<td\>0x01 (GNC)\</td\>  
            \<td style="font-family:var(--font-mono);"\>0x\${g.canAddress.toString(16).toUpperCase()}\</td\>  
            \<td\>\${g.name}\</td\>  
            \<td style="font-family:var(--font-mono);"\>\${g.actualKva \> 0 ? '05 ' \+ Math.round(g.temperatureC).toString(16).padStart(2,'0') \+ ' 00 00' : '00 00 00 00'}\</td\>  
            \<td\>\<span class="badge \${g.powerGranted ? 'badge-granted' : 'badge-shedded'}"\>\${g.state}\</span\>\</td\>  
          \</tr\>  
        \`;  
      }).join('');  
    }

    function toggleSingleGenerator() {  
      const current \= engine.powerFeeders.singleGeneratorMode;  
      engine.setSingleGeneratorMode(\!current);  
        
      const badge \= document.getElementById('gnc-status-badge');  
      const btn \= document.getElementById('toggle-gen-btn');

      if (\!current) {  
        badge.className \= 'status-badge shedding';  
        badge.innerHTML \= '\<span\>●\</span\> SINGLE GEN DE-RATE — SHEDDING ENGAGED';  
        btn.innerText \= 'Restore Dual Gen Mode';  
      } else {  
        badge.className \= 'status-badge';  
        badge.innerHTML \= '\<span\>●\</span\> GNC NORMAL — DUAL GEN ONLINE';  
        btn.innerText \= 'Toggle Single Gen Mode';  
      }

      renderRack();  
      renderCanBus();  
      runNormativeAudit();  
    }

    function runNormativeAudit() {  
      const auditor \= new ARINC812Auditor(engine);  
      const res \= auditor.audit();

      document.getElementById('audit-score').innerText \= \`\${res.passedCount} / \${res.totalTests} CHECKS PASSED (\${res.scorePct}%)\`;

      const container \= document.getElementById('audit-results-list');  
      container.innerHTML \= res.results.map(r \=\> \`  
        \<div style="padding: 0.8rem; margin-bottom: 0.5rem; background: rgba(255,255,255,0.02); border-left: 4px solid \${r.passed ? '\#10b981' : '\#ef4444'}; border-radius: 4px;"\>  
          \<div style="display:flex; justify-content:space-between; align-items:center;"\>  
            \<strong style="color:\${r.passed ? '\#34d399' : '\#f87171'}"\>\${r.id}: \${r.rule}\</strong\>  
            \<span class="badge \${r.passed ? 'badge-granted' : 'badge-fault'}"\>\${r.passed ? 'PASS' : 'FAIL'}\</span\>  
          \</div\>  
          \<div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;"\>Standard: \${r.standard}\</div\>  
          \<div style="font-size:0.85rem; color:\#cbd5e1; margin-top:0.2rem;"\>\${r.details}\</div\>  
        \</div\>  
      \`).join('');  
    }

    window.onload \= function() {  
      renderRack();  
      renderCanBus();  
      runNormativeAudit();  
    };  
  \</script\>  
\</body\>  
\</html\>  
