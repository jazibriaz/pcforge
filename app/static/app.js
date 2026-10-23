(() => {
  const LABELS = {
    cpu: "CPU", motherboard: "Motherboard", memory: "Memory", gpu: "Graphics",
    cooler: "Cooler", case: "Case", psu: "Power supply", storage: "Storage",
  };

  const state = { order: [], catalog: {}, presets: {}, selection: {}, timer: null };
  const $ = (id) => document.getElementById(id);
  const euro = (n) => "€" + Number(n).toLocaleString("en-IE");

  function specsFor(cat, p) {
    if (!p) return [];
    switch (cat) {
      case "cpu": return [p.socket, `${p.cores} cores`, `${p.power} W peak`, p.memory.join("/")];
      case "motherboard": return [p.socket, p.form, p.memory];
      case "memory": return [p.type];
      case "gpu": return [`${p.length} mm`, `${p.power} W`];
      case "cooler": return p.kind === "air"
        ? ["Air", `${p.height} mm tall`, `~${p.rated} W`]
        : ["AIO", `${p.radiator} mm radiator`, `~${p.rated} W`];
      case "case": return [p.forms.join(" / "), `GPU ≤ ${p.max_gpu} mm`, `Cooler ≤ ${p.max_cooler} mm`, `${p.psu.join("/")} PSU`];
      case "psu": return [`${p.watts} W`, p.form];
      case "storage": return ["NVMe"];
      default: return [];
    }
  }

  function el(tag, attrs = {}, children = []) {
    const node = document.createElement(tag);
    Object.entries(attrs).forEach(([k, v]) => (k === "text" ? (node.textContent = v) : node.setAttribute(k, v)));
    children.forEach((c) => node.appendChild(c));
    return node;
  }

  function renderRows() {
    const list = $("part-rows");
    list.innerHTML = "";
    state.order.forEach((cat) => {
      const select = el("select", { id: `sel-${cat}`, "aria-label": LABELS[cat] });
      select.appendChild(el("option", { value: "", text: `Choose ${LABELS[cat].toLowerCase()}…` }));
      state.catalog[cat].forEach((p) => select.appendChild(el("option", { value: p.id, text: p.name })));
      select.value = state.selection[cat] || "";
      select.addEventListener("change", () => {
        if (select.value) state.selection[cat] = select.value; else delete state.selection[cat];
        renderSpecs(cat);
        scheduleCheck();
      });
      const row = el("li", { class: "part-row", id: `row-${cat}` }, [
        el("div", { class: "part-cat" }, [el("span", { class: "label", text: LABELS[cat] })]),
        el("div", { class: "part-body" }, [select, el("div", { class: "specs", id: `specs-${cat}` })]),
      ]);
      list.appendChild(row);
      renderSpecs(cat);
    });
  }

  function renderSpecs(cat) {
    const box = $(`specs-${cat}`);
    const part = state.catalog[cat].find((p) => p.id === state.selection[cat]);
    box.innerHTML = "";
    specsFor(cat, part).forEach((s) => box.appendChild(el("span", { class: "spec", text: s })));
    if (part) box.appendChild(el("span", { class: "spec price", text: euro(part.price) }));
  }

  function renderPresets() {
    const box = $("presets");
    Object.entries(state.presets).forEach(([key, preset]) => {
      const btn = el("button", { type: "button", text: preset.label });
      if (key === "broken") btn.classList.add("danger");
      btn.addEventListener("click", () => {
        state.selection = { ...preset.parts };
        state.order.forEach((cat) => { $(`sel-${cat}`).value = state.selection[cat] || ""; renderSpecs(cat); });
        check();
      });
      box.appendChild(btn);
    });
  }

  function scheduleCheck() {
    clearTimeout(state.timer);
    state.timer = setTimeout(check, 120);
  }

  async function check() {
    const res = await fetch("/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ parts: state.selection }),
    });
    if (!res.ok) return;
    renderSummary(await res.json());
  }

  function renderSummary(r) {
    const chosen = state.order.length - r.missing.length;
    const statusText = { ok: "Compatible", incomplete: "Incomplete", incompatible: "Incompatible" }[r.status];
    $("status").className = `status status-${r.status}`;
    $("status").textContent = statusText;
    $("count").textContent = `${chosen} / ${state.order.length} parts`;
    $("total").textContent = euro(r.total_price);

    const { estimated, recommended_psu: rec, psu } = r.power;
    $("power-text").textContent = `${estimated} W est.`;
    const scale = Math.max(psu || 0, rec, estimated) * 1.05;
    const fill = $("meter-fill");
    fill.style.width = `${Math.min(100, (estimated / scale) * 100)}%`;
    fill.className = "meter-fill" + (psu && psu < estimated ? " err" : psu && psu < rec ? " warn" : "");
    const marker = $("meter-rec");
    marker.style.left = `${(rec / scale) * 100}%`;
    marker.style.opacity = chosen ? 1 : 0;
    $("psu-text").textContent = psu ? `PSU ${psu} W` : "No PSU selected";
    $("rec-text").textContent = chosen ? `${rec} W recommended` : "";

    document.querySelectorAll(".part-row").forEach((row) => row.classList.remove("has-error", "has-warning"));
    r.issues.forEach((i) => {
      const row = $(`row-${i.category}`);
      if (row && !row.classList.contains("has-error")) row.classList.add(i.level === "error" ? "has-error" : "has-warning");
    });

    const list = $("issues");
    list.innerHTML = "";
    if (!chosen) {
      list.appendChild(el("li", { class: "issue-empty", text: "Select parts to start checking." }));
      return;
    }
    const sorted = [...r.issues].sort((a, b) => (a.level === "error" ? -1 : 1) - (b.level === "error" ? -1 : 1));
    sorted.forEach((i) => {
      const li = el("li", { class: i.level }, [el("span", { class: "tag", text: i.level === "error" ? "Error" : "Check" })]);
      li.appendChild(document.createTextNode(i.message));
      list.appendChild(li);
    });
    if (!r.issues.length) {
      const msg = r.missing.length
        ? `No conflicts so far. Still to choose: ${r.missing.map((c) => LABELS[c].toLowerCase()).join(", ")}.`
        : "Everything fits. Sockets, memory, clearances and power all check out.";
      list.appendChild(el("li", { class: "ok" }, [el("span", { class: "tag", text: "OK" }), document.createTextNode(msg)]));
    }
  }

  async function init() {
    const res = await fetch("/api/parts");
    const data = await res.json();
    Object.assign(state, { order: data.order, catalog: data.catalog, presets: data.presets });
    renderRows();
    renderPresets();
    check();
  }

  init();
})();
