"""Compatibility rules. Pure functions, no Flask, so they are easy to unit test."""

from .catalog import CATALOG, CATEGORY_ORDER, find

BASE_SYSTEM_DRAW = 50      # W for motherboard, fans, USB, RGB
PSU_HEADROOM = 1.3         # recommended PSU = estimated draw x 1.3
GPU_TIGHT_MARGIN = 15      # mm of clearance below which we warn


def evaluate(selection):
    """selection: {category: part_id}. Returns issues, power estimate and total price."""
    parts = {}
    issues = []

    for category, part_id in (selection or {}).items():
        if category not in CATALOG or not part_id:
            continue
        part = find(category, part_id)
        if part is None:
            issues.append(_issue("error", category, f"Unknown {category} '{part_id}'."))
        else:
            parts[category] = part

    cpu, board, ram = parts.get("cpu"), parts.get("motherboard"), parts.get("memory")
    gpu, cooler, case, psu = parts.get("gpu"), parts.get("cooler"), parts.get("case"), parts.get("psu")

    if cpu and board and cpu["socket"] != board["socket"]:
        issues.append(_issue("error", "motherboard",
                             f"{cpu['name']} needs an {cpu['socket']} board, but {board['name']} is {board['socket']}."))

    if board and ram and ram["type"] != board["memory"]:
        issues.append(_issue("error", "memory",
                             f"{board['name']} takes {board['memory']}, but the selected kit is {ram['type']}."))
    elif cpu and ram and ram["type"] not in cpu["memory"]:
        issues.append(_issue("error", "memory",
                             f"{cpu['name']} does not support {ram['type']}."))

    if board and case and board["form"] not in case["forms"]:
        issues.append(_issue("error", "case",
                             f"{case['name']} fits {', '.join(case['forms'])} boards, not {board['form']}."))

    if gpu and case:
        margin = case["max_gpu"] - gpu["length"]
        if margin < 0:
            issues.append(_issue("error", "gpu",
                                 f"GPU is {gpu['length']} mm long; {case['name']} only fits {case['max_gpu']} mm."))
        elif margin < GPU_TIGHT_MARGIN:
            issues.append(_issue("warning", "gpu",
                                 f"Only {margin} mm of GPU clearance left; check cable routing and front fans."))

    if cooler:
        if cpu and cpu["socket"] not in cooler["sockets"]:
            issues.append(_issue("error", "cooler",
                                 f"{cooler['name']} has no mounting kit for {cpu['socket']}."))
        if case:
            if cooler["kind"] == "air" and cooler["height"] > case["max_cooler"]:
                issues.append(_issue("error", "cooler",
                                     f"Cooler is {cooler['height']} mm tall; {case['name']} allows {case['max_cooler']} mm."))
            if cooler["kind"] == "aio" and cooler["radiator"] > case["max_radiator"]:
                issues.append(_issue("error", "cooler",
                                     f"{cooler['radiator']} mm radiator will not fit; {case['name']} takes up to {case['max_radiator']} mm."))
        if cpu and cooler["rated"] < cpu["power"]:
            issues.append(_issue("warning", "cooler",
                                 f"{cooler['name']} is rated ~{cooler['rated']} W but {cpu['name']} can pull {cpu['power']} W; expect throttling."))

    estimated = BASE_SYSTEM_DRAW + sum(p.get("power", 0) for p in parts.values())
    recommended = _round_up(estimated * PSU_HEADROOM, 50)

    if psu:
        if case and psu["form"] not in case["psu"]:
            issues.append(_issue("error", "psu",
                                 f"{case['name']} needs an {'/'.join(case['psu'])} PSU, not {psu['form']}."))
        if psu["watts"] < estimated:
            issues.append(_issue("error", "psu",
                                 f"{psu['watts']} W is below the estimated {estimated} W peak draw."))
        elif psu["watts"] < recommended:
            issues.append(_issue("warning", "psu",
                                 f"{psu['watts']} W works, but {recommended} W is recommended for transient spikes."))

    missing = [c for c in CATEGORY_ORDER if c not in parts]
    errors = sum(1 for i in issues if i["level"] == "error")

    return {
        "status": "incompatible" if errors else ("incomplete" if missing else "ok"),
        "issues": issues,
        "missing": missing,
        "power": {"estimated": estimated, "recommended_psu": recommended,
                  "psu": psu["watts"] if psu else None},
        "total_price": sum(p["price"] for p in parts.values()),
    }


def _issue(level, category, message):
    return {"level": level, "category": category, "message": message}


def _round_up(value, step):
    return int(-(-value // step) * step)
