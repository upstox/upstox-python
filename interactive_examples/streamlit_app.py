"""
Upstox API Explorer — Streamlit web app.

All 38 examples from the CLI scripts wrapped in an interactive UI.
Paste your analytics (or daily access) token in the sidebar and explore.
"""

import math
import sys
import os
import time
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))
import upstox_client
from utils import (
    get_api_client,
    get_futures_sorted,
    get_full_quote,
    get_historical_candles,
    get_ltp,
    search_instrument,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Upstox API Explorer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📈 Upstox API Explorer")
    st.caption("Instrument Search + Analytics Token")

    token = st.text_input(
        "🔑 Token",
        type="password",
        placeholder="Paste analytics or access token…",
        help="Analytics token: 1-year validity, read-only. "
             "Get it from Upstox Developer Apps → Analytics tab.",
    )

    st.divider()

    CATEGORIES = {
        "🔍 Instrument Search": [
            "Search Equity",
            "Search Futures",
            "Search Options",
        ],
        "📈 Futures & Basis": [
            "NIFTY Futures Spread",
            "BankNifty Futures Spread",
            "Cash-Futures Basis",
            "Futures Roll Cost",
            "MCX Crude Spread",
        ],
        "🎯 Options Strategies": [
            "Straddle Pricer",
            "Strangle Pricer",
            "Bull Call Spread",
            "Iron Condor",
            "Butterfly Spread",
            "Calendar Spread",
            "Put-Call Parity",
        ],
        "📊 Options Analytics": [
            "Options Chain Builder",
            "Max Pain Calculator",
            "OI Skew",
            "Volatility Skew",
            "Gamma Exposure",
            "Option Chain (Native)",
            "Option Greeks",
        ],
        "⚖️ Arbitrage": [
            "NSE / BSE Arbitrage",
            "ETF vs Index",
            "Currency Futures Spread",
        ],
        "📉 Historical Analysis": [
            "Historical Candles",
            "Moving Average (SMA)",
            "Historical Volatility",
            "52-Week High / Low",
        ],
        "🗂️ Portfolio & Screening": [
            "Sector Index Comparison",
            "Top Volume Stocks",
            "Futures OI Buildup",
        ],
        "📡 Market Data": [
            "Market Status",
            "Market Holidays",
            "Market Timings",
            "Intraday Chart",
            "Live Depth (5-level)",
            "Live Depth MCX",
            "Live Depth USDINR",
        ],
    }

    category = st.selectbox("Category", list(CATEGORIES.keys()))
    example = st.selectbox("Example", CATEGORIES[category])

    st.divider()
    st.caption(
        "Built with [Streamlit](https://streamlit.io) · "
        "[Upstox API Docs](https://upstox.com/developer/api-documentation/)"
    )

# ── Shared helpers ────────────────────────────────────────────────────────────

def require_client():
    if not token:
        st.info("👈 Paste your Upstox token in the sidebar to get started.")
        st.stop()
    return get_api_client(token)


def lv(obj):
    """last_price from LTP or full-quote object."""
    if obj is None:
        return 0.0
    return obj.last_price if hasattr(obj, "last_price") else obj.get("last_price", 0.0)


def vv(obj):
    """volume."""
    if obj is None:
        return 0
    return obj.volume if hasattr(obj, "volume") else obj.get("volume", 0)


def cv(obj):
    """close / previous-close from LTP object (.cp)."""
    if obj is None:
        return 0.0
    return obj.cp if hasattr(obj, "cp") else obj.get("cp", 0.0)


def ov(obj):
    """open interest from full-quote object."""
    if obj is None:
        return 0
    return obj.oi if hasattr(obj, "oi") else obj.get("oi", 0)


def ohlc(obj):
    """Returns (open, high, low, close) from full-quote object."""
    if obj is None:
        return 0.0, 0.0, 0.0, 0.0
    o = obj.ohlc if hasattr(obj, "ohlc") else obj.get("ohlc", {})
    if hasattr(o, "open"):
        return o.open, o.high, o.low, o.close
    return o.get("open", 0.0), o.get("high", 0.0), o.get("low", 0.0), o.get("close", 0.0)


def dte(expiry_str: str) -> int:
    try:
        return max((datetime.strptime(expiry_str, "%Y-%m-%d").date() - date.today()).days, 1)
    except Exception:
        return 30


def fetch_one(client, query, expiry, itype, offset):
    resp = search_instrument(
        client, query,
        exchanges="NSE", segments="FO",
        instrument_types=itype, expiry=expiry,
        atm_offset=offset, records=1,
    )
    data = resp.data or []
    return data[0] if data else None


def fetch_options_range(client, query, expiry, itype, n, bar=None):
    """Fetch options instruments for offsets -n … +n, deduped by strike."""
    instruments, seen, unique = [], set(), []
    total = n * 2 + 1
    for i, offset in enumerate(range(-n, n + 1)):
        resp = search_instrument(
            client, query,
            exchanges="NSE", segments="FO",
            instrument_types=itype, expiry=expiry,
            atm_offset=offset, records=1,
        )
        data = resp.data or []
        if data:
            instruments.append(data[0])
        if bar:
            bar.progress((i + 1) / total)
    for inst in instruments:
        k = inst.get("strike_price", 0)
        if k not in seen:
            seen.add(k)
            unique.append(inst)
    return unique


def contango_label(spread):
    if spread > 0:
        return "🟢 **Contango** — far month at premium. Normal for index/equity futures."
    if spread < 0:
        return "🔴 **Backwardation** — far month at discount. Unusual — check news."
    return "⚪ Spread is zero — contracts at parity."


# ── Page header ───────────────────────────────────────────────────────────────
st.title(example)
st.caption(f"Category: {category}")
st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# 🔍 INSTRUMENT SEARCH
# ═════════════════════════════════════════════════════════════════════════════

if example == "Search Equity":
    client = require_client()
    c1, c2, c3 = st.columns([2, 1, 1])
    query   = c1.text_input("Search query", value="RELIANCE")
    exch    = c2.selectbox("Exchange", ["NSE", "BSE", "NSE,BSE"])
    records = c3.number_input("Max results", 1, 30, 10)

    if st.button("🔍 Search", type="primary"):
        with st.spinner("Searching…"):
            resp = search_instrument(client, query, exchanges=exch, segments="EQ", records=records)
        insts = resp.data or []
        if not insts:
            st.warning(f"No equity instruments found for '{query}' on {exch}.")
        else:
            df = pd.DataFrame([{
                "Instrument Key": i.get("instrument_key", ""),
                "Symbol":         i.get("trading_symbol", ""),
                "Name":           i.get("name", ""),
                "Exchange":       i.get("exchange", ""),
                "ISIN":           i.get("isin", ""),
                "Lot Size":       i.get("lot_size", 1),
                "Tick Size":      i.get("tick_size", 0.05),
            } for i in insts])
            st.success(f"Found {len(df)} result(s)")
            st.dataframe(df, use_container_width=True)


elif example == "Search Futures":
    client = require_client()
    c1, c2, c3 = st.columns([2, 1, 1])
    query = c1.text_input("Search query", value="NIFTY")
    exch  = c2.selectbox("Exchange", ["NSE", "BSE", "MCX"])
    exact = c3.checkbox("Exact underlying match", value=True,
                        help="Filter strictly by underlying_symbol to avoid e.g. NIFTYNXT50 when searching NIFTY")

    if st.button("🔍 Search", type="primary"):
        with st.spinner("Searching…"):
            futures = get_futures_sorted(client, query, exchange=exch, exact_symbol=exact)
        if not futures:
            st.warning(f"No futures found for '{query}'.")
        else:
            df = pd.DataFrame([{
                "Symbol":     i.get("trading_symbol", ""),
                "Underlying": i.get("underlying_symbol", ""),
                "Expiry":     i.get("expiry", ""),
                "Lot Size":   i.get("lot_size", ""),
                "Exchange":   i.get("exchange", ""),
                "Key":        i.get("instrument_key", ""),
            } for i in futures])
            st.success(f"Found {len(df)} contract(s)")
            st.dataframe(df, use_container_width=True)


elif example == "Search Options":
    client = require_client()
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    query        = c1.text_input("Underlying", value="NIFTY")
    expiry       = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    opt_type     = c3.selectbox("Option type", ["CE,PE", "CE", "PE"])
    strikes_each = c4.number_input("Strikes each side", 1, 15, 5)

    if st.button("🔍 Fetch Options", type="primary"):
        bar = st.progress(0)
        insts = fetch_options_range(client, query, expiry, opt_type, strikes_each, bar)
        bar.empty()
        if not insts:
            st.warning("No options found.")
        else:
            df = pd.DataFrame([{
                "Symbol": i.get("trading_symbol", ""),
                "Type":   i.get("instrument_type", ""),
                "Strike": i.get("strike_price", 0),
                "Expiry": i.get("expiry", ""),
                "Lot":    i.get("lot_size", ""),
                "Key":    i.get("instrument_key", ""),
            } for i in insts]).sort_values(["Strike", "Type"])
            st.success(f"Found {len(df)} option(s)")
            st.dataframe(df, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# 📈 FUTURES & BASIS
# ═════════════════════════════════════════════════════════════════════════════

elif example == "NIFTY Futures Spread":
    client = require_client()
    if st.button("▶ Run", type="primary"):
        with st.spinner("Fetching NIFTY futures…"):
            futures = get_futures_sorted(client, "NIFTY", exchange="NSE", exact_symbol=True)
        if len(futures) < 2:
            st.error("Need at least 2 NIFTY futures contracts.")
            st.stop()

        near, far  = futures[0], futures[1]
        ltp_data   = get_ltp(client, near["instrument_key"], far["instrument_key"])
        near_q     = ltp_data.get(near["instrument_key"])
        far_q      = ltp_data.get(far["instrument_key"])
        near_ltp   = lv(near_q); far_ltp = lv(far_q)
        spread     = far_ltp - near_ltp
        spread_pct = (spread / near_ltp * 100) if near_ltp else 0
        lot        = near.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("Near Month LTP",  f"₹{near_ltp:,.2f}", f"Close: {cv(near_q):,.2f}")
        c2.metric("Far Month LTP",   f"₹{far_ltp:,.2f}",  f"Close: {cv(far_q):,.2f}")
        c3.metric("Calendar Spread", f"₹{spread:+,.2f}",   f"{spread_pct:+.2f}%")

        st.divider()
        st.dataframe(pd.DataFrame([
            {"Contract": near["trading_symbol"], "Expiry": near["expiry"],
             "LTP": near_ltp, "Prev Close": cv(near_q), "Volume": vv(near_q)},
            {"Contract": far["trading_symbol"],  "Expiry": far["expiry"],
             "LTP": far_ltp,  "Prev Close": cv(far_q),  "Volume": vv(far_q)},
        ]), use_container_width=True)
        st.info(contango_label(spread))
        st.caption(f"Spread per lot ({lot} units): ₹{spread * lot:+,.2f}")
        st.caption("Arbitrage: Buy near + Sell far if spread > cost-of-carry. Spread collapses at near-month expiry.")


elif example == "BankNifty Futures Spread":
    client = require_client()
    if st.button("▶ Run", type="primary"):
        with st.spinner("Fetching BANKNIFTY futures…"):
            futures = get_futures_sorted(client, "BANKNIFTY", exchange="NSE", exact_symbol=True)
        if len(futures) < 2:
            st.error("Need at least 2 BANKNIFTY contracts.")
            st.stop()

        near, far  = futures[0], futures[1]
        ltp_data   = get_ltp(client, near["instrument_key"], far["instrument_key"])
        near_q     = ltp_data.get(near["instrument_key"])
        far_q      = ltp_data.get(far["instrument_key"])
        near_ltp   = lv(near_q); far_ltp = lv(far_q)
        spread     = far_ltp - near_ltp
        spread_pct = (spread / near_ltp * 100) if near_ltp else 0
        lot        = near.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("Near Contract LTP", f"₹{near_ltp:,.2f}", f"Close: {cv(near_q):,.2f}")
        c2.metric("Far Contract LTP",  f"₹{far_ltp:,.2f}",  f"Close: {cv(far_q):,.2f}")
        c3.metric("Calendar Spread",   f"₹{spread:+,.2f}",   f"{spread_pct:+.2f}%")

        st.divider()
        st.dataframe(pd.DataFrame([
            {"Contract": near["trading_symbol"], "Expiry": near["expiry"],
             "LTP": near_ltp, "Prev Close": cv(near_q), "Volume": vv(near_q)},
            {"Contract": far["trading_symbol"],  "Expiry": far["expiry"],
             "LTP": far_ltp,  "Prev Close": cv(far_q),  "Volume": vv(far_q)},
        ]), use_container_width=True)
        st.info(contango_label(spread))
        st.caption(f"Spread per lot ({lot} units): ₹{spread * lot:+,.2f}")
        st.caption("BankNifty has weekly expiries — near/far may both be in the current month.")


elif example == "Cash-Futures Basis":
    client = require_client()
    underlying = st.selectbox("Underlying", ["NIFTY 50", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"])

    if st.button("▶ Run", type="primary"):
        fut_q_map = {"NIFTY 50": "NIFTY", "BANKNIFTY": "BANKNIFTY",
                     "FINNIFTY": "FINNIFTY", "MIDCPNIFTY": "MIDCPNIFTY"}
        fut_sym = fut_q_map[underlying]

        with st.spinner("Fetching spot and futures…"):
            spot_resp = search_instrument(client, underlying, exchanges="NSE",
                                          segments="INDEX", instrument_types="INDEX", records=5)
            spot_insts = spot_resp.data or []
            spot_inst  = next(
                (i for i in spot_insts
                 if underlying.upper().replace(" ", "") in i.get("trading_symbol", "").upper().replace(" ", "")),
                spot_insts[0] if spot_insts else None,
            )
            futures = get_futures_sorted(client, fut_sym, exchange="NSE", exact_symbol=True)

        if not spot_inst:
            st.error(f"Could not find index for '{underlying}'.")
            st.stop()
        if not futures:
            st.error(f"No futures found for '{fut_sym}'.")
            st.stop()

        near    = futures[0]
        data    = get_ltp(client, spot_inst["instrument_key"], near["instrument_key"])
        spot_ltp = lv(data.get(spot_inst["instrument_key"]))
        fut_ltp  = lv(data.get(near["instrument_key"]))
        basis    = fut_ltp - spot_ltp
        basis_pct = (basis / spot_ltp * 100) if spot_ltp else 0
        d        = dte(near.get("expiry", ""))
        ann      = (basis_pct / d * 365) if d else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Spot (Index)",       f"₹{spot_ltp:,.2f}")
        c2.metric("Futures (Near)",     f"₹{fut_ltp:,.2f}")
        c3.metric("Basis (Fut − Spot)", f"₹{basis:+,.2f}", f"{basis_pct:+.2f}%")
        c4.metric("Annualised Carry",   f"{ann:+.2f}% p.a.", f"{d} DTE")

        st.divider()
        if basis > 0:
            st.success("🟢 Futures at premium — positive carry (interest rate > dividend yield).")
        else:
            st.warning("🔴 Futures at discount — dividend yield > cost of carry, or bearish sentiment.")


elif example == "Futures Roll Cost":
    client = require_client()
    c1, c2 = st.columns(2)
    query = c1.text_input("Underlying", value="NIFTY")
    side  = c2.selectbox("Position side", ["long", "short"])

    if st.button("▶ Run", type="primary"):
        with st.spinner("Fetching futures…"):
            futures = get_futures_sorted(client, query, exchange="NSE", exact_symbol=True)
        if len(futures) < 2:
            st.error("Need at least 2 contracts.")
            st.stop()

        near, far  = futures[0], futures[1]
        data       = get_ltp(client, near["instrument_key"], far["instrument_key"])
        near_ltp   = lv(data.get(near["instrument_key"]))
        far_ltp    = lv(data.get(far["instrument_key"]))
        roll       = (far_ltp - near_ltp) if side == "long" else (near_ltp - far_ltp)
        roll_pct   = (roll / near_ltp * 100) if near_ltp else 0
        lot        = near.get("lot_size", 1)

        try:
            d1       = datetime.strptime(near["expiry"], "%Y-%m-%d").date()
            d2       = datetime.strptime(far["expiry"], "%Y-%m-%d").date()
            gap      = abs((d2 - d1).days)
            dte_near = (d1 - date.today()).days
        except Exception:
            gap = 30; dte_near = 15

        ann = (roll_pct / gap * 365) if gap else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Roll Cost (pts)", f"{roll:+.2f}")
        c2.metric("Roll Cost (%)",   f"{roll_pct:+.2f}%")
        c3.metric("Annualised Rate", f"{ann:+.2f}% p.a.")

        st.divider()
        action_near = "Close" if side == "long" else "Open"
        action_far  = "Open"  if side == "long" else "Close"
        st.dataframe(pd.DataFrame([
            {"Action": action_near, "Contract": near["trading_symbol"], "Expiry": near["expiry"], "LTP": near_ltp},
            {"Action": action_far,  "Contract": far["trading_symbol"],  "Expiry": far["expiry"],  "LTP": far_ltp},
        ]), use_container_width=True)
        st.caption(f"Roll cost per lot: ₹{roll * lot:+,.2f} | Days between expiries: {gap} | DTE near: {dte_near}")


elif example == "MCX Crude Spread":
    client = require_client()
    query = st.text_input("Commodity symbol", value="CRUDEOIL",
                          help="e.g. CRUDEOIL, NATURALGAS, GOLD, SILVER")

    if st.button("▶ Run", type="primary"):
        with st.spinner("Fetching MCX futures…"):
            futures = get_futures_sorted(client, query, exchange="MCX", exact_symbol=False)
        if len(futures) < 2:
            st.error(f"Need at least 2 futures for '{query}'. Try CRUDEOIL or NATURALGAS.")
            st.stop()

        near, far  = futures[0], futures[1]
        data       = get_ltp(client, near["instrument_key"], far["instrument_key"])
        near_ltp   = lv(data.get(near["instrument_key"]))
        far_ltp    = lv(data.get(far["instrument_key"]))
        spread     = far_ltp - near_ltp
        spread_pct = (spread / near_ltp * 100) if near_ltp else 0
        lot        = near.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("Near LTP",  f"₹{near_ltp:,.2f}", f"Close: {cv(data.get(near['instrument_key'])):,.2f}")
        c2.metric("Far LTP",   f"₹{far_ltp:,.2f}",  f"Close: {cv(data.get(far['instrument_key'])):,.2f}")
        c3.metric("Spread",    f"₹{spread:+,.2f}",   f"{spread_pct:+.2f}%")

        st.divider()
        st.dataframe(pd.DataFrame([
            {"Contract": near["trading_symbol"], "Expiry": near["expiry"], "LTP": near_ltp},
            {"Contract": far["trading_symbol"],  "Expiry": far["expiry"],  "LTP": far_ltp},
        ]), use_container_width=True)
        st.info(contango_label(spread))
        st.caption(f"Spread per lot ({lot} units): ₹{spread * lot:+,.2f}")


# ═════════════════════════════════════════════════════════════════════════════
# 🎯 OPTIONS STRATEGIES
# ═════════════════════════════════════════════════════════════════════════════

elif example == "Straddle Pricer":
    client = require_client()
    c1, c2 = st.columns(2)
    query  = c1.text_input("Underlying", value="NIFTY")
    expiry = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])

    if st.button("▶ Price Straddle", type="primary"):
        with st.spinner("Fetching ATM options…"):
            ce = fetch_one(client, query, expiry, "CE", 0)
            pe = fetch_one(client, query, expiry, "PE", 0)
        if not ce or not pe:
            st.error("Could not find ATM options.")
            st.stop()

        data     = get_ltp(client, ce["instrument_key"], pe["instrument_key"])
        ce_ltp   = lv(data.get(ce["instrument_key"]))
        pe_ltp   = lv(data.get(pe["instrument_key"]))
        strike   = ce.get("strike_price", 0)
        premium  = ce_ltp + pe_ltp
        upper_be = strike + premium
        lower_be = strike - premium
        lot      = ce.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("ATM Strike",            f"₹{strike:,.0f}")
        c2.metric("Total Premium (CE+PE)", f"₹{premium:,.2f}")
        c3.metric("Max Profit (seller)",   f"₹{premium * lot:,.2f} / lot")

        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Upper Breakeven", f"₹{upper_be:,.2f}", f"+{premium:,.2f}")
        c2.metric("Lower Breakeven", f"₹{lower_be:,.2f}", f"-{premium:,.2f}")

        st.dataframe(pd.DataFrame([
            {"Leg": "Buy CE (ATM)", "Strike": strike, "Expiry": ce["expiry"], "LTP": ce_ltp, "Symbol": ce["trading_symbol"]},
            {"Leg": "Buy PE (ATM)", "Strike": strike, "Expiry": pe["expiry"], "LTP": pe_ltp, "Symbol": pe["trading_symbol"]},
        ]), use_container_width=True)
        st.caption(f"Buyer profits if underlying moves > ₹{premium:.2f} in either direction.")
        st.caption(f"Seller max profit ₹{premium * lot:,.2f}/lot if underlying stays within ₹{lower_be:,.2f}–₹{upper_be:,.2f}.")


elif example == "Strangle Pricer":
    client = require_client()
    c1, c2, c3 = st.columns(3)
    query      = c1.text_input("Underlying", value="NIFTY")
    expiry     = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    otm_offset = c3.number_input("OTM offset (strikes)", 1, 10, 2)

    if st.button("▶ Price Strangle", type="primary"):
        with st.spinner("Fetching OTM options…"):
            ce = fetch_one(client, query, expiry, "CE", +otm_offset)
            pe = fetch_one(client, query, expiry, "PE", -otm_offset)
        if not ce or not pe:
            st.error("Could not find OTM options.")
            st.stop()

        data      = get_ltp(client, ce["instrument_key"], pe["instrument_key"])
        ce_ltp    = lv(data.get(ce["instrument_key"]))
        pe_ltp    = lv(data.get(pe["instrument_key"]))
        ce_strike = ce.get("strike_price", 0)
        pe_strike = pe.get("strike_price", 0)
        premium   = ce_ltp + pe_ltp
        lot       = ce.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric(f"CE Strike (+{otm_offset})", f"₹{ce_strike:,.0f}", f"LTP: {ce_ltp:.2f}")
        c2.metric(f"PE Strike (-{otm_offset})", f"₹{pe_strike:,.0f}", f"LTP: {pe_ltp:.2f}")
        c3.metric("Total Premium",             f"₹{premium:,.2f}")

        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Upper Breakeven", f"₹{ce_strike + premium:,.2f}")
        c2.metric("Lower Breakeven", f"₹{pe_strike - premium:,.2f}")

        st.dataframe(pd.DataFrame([
            {"Leg": f"Buy CE +{otm_offset}", "Strike": ce_strike, "LTP": ce_ltp, "Symbol": ce["trading_symbol"]},
            {"Leg": f"Buy PE -{otm_offset}", "Strike": pe_strike, "LTP": pe_ltp, "Symbol": pe["trading_symbol"]},
        ]), use_container_width=True)
        st.caption(f"Max loss per lot: ₹{premium * lot:,.2f} (if underlying stays between strikes).")


elif example == "Bull Call Spread":
    client = require_client()
    c1, c2, c3    = st.columns(3)
    query         = c1.text_input("Underlying", value="NIFTY")
    expiry        = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    spread_width  = c3.number_input("Spread width (strikes)", 1, 10, 2)

    if st.button("▶ Price Bull Call Spread", type="primary"):
        with st.spinner("Fetching options…"):
            buy_ce  = fetch_one(client, query, expiry, "CE", 0)
            sell_ce = fetch_one(client, query, expiry, "CE", +spread_width)
        if not buy_ce or not sell_ce:
            st.error("Could not fetch options.")
            st.stop()

        data      = get_ltp(client, buy_ce["instrument_key"], sell_ce["instrument_key"])
        buy_ltp   = lv(data.get(buy_ce["instrument_key"]))
        sell_ltp  = lv(data.get(sell_ce["instrument_key"]))
        buy_k     = buy_ce.get("strike_price", 0)
        sell_k    = sell_ce.get("strike_price", 0)
        debit     = buy_ltp - sell_ltp
        max_prof  = (sell_k - buy_k) - debit
        lot       = buy_ce.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("Net Debit",  f"₹{debit:,.2f}", "Cost per unit")
        c2.metric("Max Profit", f"₹{max_prof:,.2f}", f"₹{max_prof * lot:,.2f}/lot")
        c3.metric("Breakeven",  f"₹{buy_k + debit:,.2f}")

        st.divider()
        st.dataframe(pd.DataFrame([
            {"Leg": "Buy CE (ATM)",         "Strike": buy_k,  "LTP": buy_ltp,  "Symbol": buy_ce["trading_symbol"]},
            {"Leg": f"Sell CE (+{spread_width})", "Strike": sell_k, "LTP": sell_ltp, "Symbol": sell_ce["trading_symbol"]},
        ]), use_container_width=True)
        st.caption(f"Max loss: ₹{debit:.2f}/unit if spot < {buy_k:,.0f} at expiry.")
        st.caption(f"Max profit: ₹{max_prof:.2f}/unit if spot > {sell_k:,.0f} at expiry.")


elif example == "Iron Condor":
    client = require_client()
    c1, c2, c3    = st.columns(3)
    query         = c1.text_input("Underlying", value="NIFTY")
    expiry        = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    short_offset  = c3.number_input("Short leg offset", 1, 10, 2,
                                    help="Strikes from ATM for the sold legs")
    long_offset   = short_offset + 2

    if st.button("▶ Price Iron Condor", type="primary"):
        with st.spinner("Fetching 4 legs…"):
            sell_ce = fetch_one(client, query, expiry, "CE", +short_offset)
            buy_ce  = fetch_one(client, query, expiry, "CE", +long_offset)
            sell_pe = fetch_one(client, query, expiry, "PE", -short_offset)
            buy_pe  = fetch_one(client, query, expiry, "PE", -long_offset)

        legs = [l for l in [sell_ce, buy_ce, sell_pe, buy_pe] if l]
        if len(legs) < 4:
            st.error("Could not fetch all 4 legs.")
            st.stop()

        data         = get_ltp(client, *[l["instrument_key"] for l in legs])
        sell_ce_ltp  = lv(data.get(sell_ce["instrument_key"]))
        buy_ce_ltp   = lv(data.get(buy_ce["instrument_key"]))
        sell_pe_ltp  = lv(data.get(sell_pe["instrument_key"]))
        buy_pe_ltp   = lv(data.get(buy_pe["instrument_key"]))
        net_credit   = (sell_ce_ltp + sell_pe_ltp) - (buy_ce_ltp + buy_pe_ltp)
        wing_width   = buy_ce["strike_price"] - sell_ce["strike_price"]
        max_loss     = wing_width - net_credit
        lot          = sell_ce.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("Net Credit", f"₹{net_credit:,.2f}", f"₹{net_credit * lot:,.2f}/lot")
        c2.metric("Max Loss",   f"₹{max_loss:,.2f}",   f"₹{max_loss * lot:,.2f}/lot")
        c3.metric("Upper / Lower BE",
                  f"{sell_ce['strike_price'] + net_credit:,.0f} / {sell_pe['strike_price'] - net_credit:,.0f}")

        st.divider()
        st.dataframe(pd.DataFrame([
            {"Leg": f"Sell CE +{short_offset}", "Strike": sell_ce["strike_price"], "LTP": sell_ce_ltp, "Symbol": sell_ce["trading_symbol"]},
            {"Leg": f"Buy CE  +{long_offset}",  "Strike": buy_ce["strike_price"],  "LTP": buy_ce_ltp,  "Symbol": buy_ce["trading_symbol"]},
            {"Leg": f"Sell PE -{short_offset}", "Strike": sell_pe["strike_price"], "LTP": sell_pe_ltp, "Symbol": sell_pe["trading_symbol"]},
            {"Leg": f"Buy PE  -{long_offset}",  "Strike": buy_pe["strike_price"],  "LTP": buy_pe_ltp,  "Symbol": buy_pe["trading_symbol"]},
        ]), use_container_width=True)


elif example == "Butterfly Spread":
    client = require_client()
    c1, c2 = st.columns(2)
    query  = c1.text_input("Underlying", value="NIFTY")
    expiry = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])

    if st.button("▶ Price Butterfly", type="primary"):
        with st.spinner("Fetching 3 legs…"):
            lower_ce = fetch_one(client, query, expiry, "CE", -1)
            atm_ce   = fetch_one(client, query, expiry, "CE",  0)
            upper_ce = fetch_one(client, query, expiry, "CE", +1)

        if not all([lower_ce, atm_ce, upper_ce]):
            st.error("Could not fetch all legs.")
            st.stop()

        data       = get_ltp(client, lower_ce["instrument_key"], atm_ce["instrument_key"], upper_ce["instrument_key"])
        lower_ltp  = lv(data.get(lower_ce["instrument_key"]))
        atm_ltp    = lv(data.get(atm_ce["instrument_key"]))
        upper_ltp  = lv(data.get(upper_ce["instrument_key"]))
        net_debit  = lower_ltp - 2 * atm_ltp + upper_ltp
        wing_width = atm_ce["strike_price"] - lower_ce["strike_price"]
        max_profit = wing_width - net_debit
        lot        = atm_ce.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("Net Debit",  f"₹{net_debit:,.2f}")
        c2.metric("Max Profit", f"₹{max_profit:,.2f}", f"at {atm_ce['strike_price']:,.0f}")
        c3.metric("Max Loss",   f"₹{net_debit:,.2f}",  "at both wings")

        st.divider()
        st.dataframe(pd.DataFrame([
            {"Leg": "Buy CE (-1)",  "Strike": lower_ce["strike_price"], "Qty": "+1", "LTP": lower_ltp},
            {"Leg": "Sell CE (ATM)","Strike": atm_ce["strike_price"],   "Qty": "-2", "LTP": atm_ltp},
            {"Leg": "Buy CE (+1)",  "Strike": upper_ce["strike_price"], "Qty": "+1", "LTP": upper_ltp},
        ]), use_container_width=True)
        st.caption(f"Max profit per lot: ₹{max_profit * lot:,.2f}. Max loss per lot: ₹{net_debit * lot:,.2f}.")


elif example == "Calendar Spread":
    client = require_client()
    c1, c2   = st.columns(2)
    query    = c1.text_input("Underlying", value="NIFTY")
    opt_type = c2.selectbox("Option type", ["CE", "PE"])

    if st.button("▶ Price Calendar Spread", type="primary"):
        with st.spinner("Fetching near + far month options…"):
            near_opt = fetch_one(client, query, "current_month", opt_type, 0)
            far_opt  = fetch_one(client, query, "next_month",    opt_type, 0)
        if not near_opt or not far_opt:
            st.error("Could not find options for both expiries.")
            st.stop()

        data      = get_ltp(client, near_opt["instrument_key"], far_opt["instrument_key"])
        near_ltp  = lv(data.get(near_opt["instrument_key"]))
        far_ltp   = lv(data.get(far_opt["instrument_key"]))
        net_debit = far_ltp - near_ltp
        lot       = near_opt.get("lot_size", 1)

        c1, c2, c3 = st.columns(3)
        c1.metric(f"Near {opt_type}", f"₹{near_ltp:,.2f}", near_opt["expiry"])
        c2.metric(f"Far {opt_type}",  f"₹{far_ltp:,.2f}",  far_opt["expiry"])
        c3.metric("Net Debit",        f"₹{net_debit:,.2f}", f"₹{net_debit * lot:,.2f}/lot")

        st.divider()
        st.dataframe(pd.DataFrame([
            {"Leg": f"Sell {opt_type} (Near)", "Strike": near_opt["strike_price"],
             "Expiry": near_opt["expiry"], "LTP": near_ltp, "Symbol": near_opt["trading_symbol"]},
            {"Leg": f"Buy {opt_type} (Far)",   "Strike": far_opt["strike_price"],
             "Expiry": far_opt["expiry"],  "LTP": far_ltp,  "Symbol": far_opt["trading_symbol"]},
        ]), use_container_width=True)
        st.caption("Strategy profits from faster time-decay of the near-month leg.")


elif example == "Put-Call Parity":
    client = require_client()
    c1, c2 = st.columns(2)
    query  = c1.text_input("Underlying", value="NIFTY")
    expiry = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])

    if st.button("▶ Check Parity", type="primary"):
        with st.spinner("Fetching options + futures…"):
            ce      = fetch_one(client, query, expiry, "CE", 0)
            pe      = fetch_one(client, query, expiry, "PE", 0)
            futures = get_futures_sorted(client, query, exchange="NSE", exact_symbol=True)
        if not ce or not pe:
            st.error("Could not find ATM options.")
            st.stop()
        if not futures:
            st.error("Could not find futures.")
            st.stop()

        data    = get_ltp(client, ce["instrument_key"], pe["instrument_key"], futures[0]["instrument_key"])
        ce_ltp  = lv(data.get(ce["instrument_key"]))
        pe_ltp  = lv(data.get(pe["instrument_key"]))
        fut_ltp = lv(data.get(futures[0]["instrument_key"]))
        strike  = ce.get("strike_price", 0)
        lhs     = ce_ltp - pe_ltp           # C − P
        rhs     = fut_ltp - strike          # F − K
        dev     = lhs - rhs
        dev_pct = (dev / strike * 100) if strike else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("CE − PE (LHS)",             f"₹{lhs:+.2f}")
        c2.metric("Futures − Strike (RHS)",    f"₹{rhs:+.2f}")
        c3.metric("Parity Deviation",          f"₹{dev:+.2f}", f"{dev_pct:+.4f}%")

        st.divider()
        if abs(dev) < 2:
            st.success("✅ Parity holds — no actionable arbitrage after transaction costs.")
        else:
            st.warning(f"⚠️ Deviation of ₹{dev:+.2f} detected. May be arbitrageable if spread > transaction costs.")

        st.dataframe(pd.DataFrame([
            {"Item": "CE (ATM)", "Strike": strike, "LTP": ce_ltp, "Symbol": ce["trading_symbol"]},
            {"Item": "PE (ATM)", "Strike": strike, "LTP": pe_ltp, "Symbol": pe["trading_symbol"]},
            {"Item": "Futures (Near)", "Strike": "—", "LTP": fut_ltp, "Symbol": futures[0]["trading_symbol"]},
        ]), use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# 📊 OPTIONS ANALYTICS
# ═════════════════════════════════════════════════════════════════════════════

elif example == "Options Chain Builder":
    client = require_client()
    c1, c2, c3   = st.columns(3)
    query        = c1.text_input("Underlying", value="NIFTY")
    expiry       = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    strikes_each = c3.number_input("Strikes each side of ATM", 1, 15, 5)

    if st.button("▶ Build Chain", type="primary"):
        bar     = st.progress(0, text="Fetching chain…")
        offsets = list(range(-strikes_each, strikes_each + 1))
        ce_map, pe_map = {}, {}

        for i, offset in enumerate(offsets):
            for itype, store in [("CE", ce_map), ("PE", pe_map)]:
                resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                         instrument_types=itype, expiry=expiry,
                                         atm_offset=offset, records=1)
                data = resp.data or []
                if data:
                    inst = data[0]
                    store[inst.get("strike_price", 0)] = inst
            bar.progress((i + 1) / len(offsets), text=f"Offset {offset}…")
        bar.empty()

        all_strikes = sorted(set(list(ce_map.keys()) + list(pe_map.keys())))
        all_keys    = []
        for k in all_strikes:
            if k in ce_map: all_keys.append(ce_map[k]["instrument_key"])
            if k in pe_map: all_keys.append(pe_map[k]["instrument_key"])

        ltp_data   = get_ltp(client, *all_keys)
        atm_resp   = search_instrument(client, query, exchanges="NSE", segments="FO",
                                       instrument_types="CE", expiry=expiry, atm_offset=0, records=1)
        atm_strike = (atm_resp.data or [{}])[0].get("strike_price", 0)

        rows = []
        for strike in reversed(all_strikes):
            ce_inst = ce_map.get(strike)
            pe_inst = pe_map.get(strike)
            rows.append({
                "CE LTP": lv(ltp_data.get(ce_inst["instrument_key"])) if ce_inst else "—",
                "Strike": strike,
                "PE LTP": lv(ltp_data.get(pe_inst["instrument_key"])) if pe_inst else "—",
                "ATM":    "◀ ATM" if strike == atm_strike else "",
            })

        df = pd.DataFrame(rows)

        def highlight_atm(row):
            return (["background-color: #fff3cd"] * len(row)
                    if row["ATM"] == "◀ ATM" else [""] * len(row))

        st.dataframe(df.style.apply(highlight_atm, axis=1), use_container_width=True)


elif example == "Max Pain Calculator":
    client = require_client()
    c1, c2, c3   = st.columns(3)
    query        = c1.text_input("Underlying", value="NIFTY")
    expiry       = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    strikes_each = c3.number_input("Strikes each side", 3, 15, 8)

    if st.button("▶ Calculate Max Pain", type="primary"):
        bar = st.progress(0, text="Fetching OI data…")
        ce_insts, pe_insts = [], []
        total = strikes_each * 2 + 1

        for i, offset in enumerate(range(-strikes_each, strikes_each + 1)):
            for itype, store in [("CE", ce_insts), ("PE", pe_insts)]:
                resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                         instrument_types=itype, expiry=expiry,
                                         atm_offset=offset, records=1)
                d = resp.data or []
                if d: store.append(d[0])
            bar.progress((i + 1) / total)

        def dedup(insts):
            seen, unique = set(), []
            for inst in insts:
                k = inst.get("strike_price", 0)
                if k not in seen: seen.add(k); unique.append(inst)
            return unique

        ce_insts = dedup(ce_insts)
        pe_insts = dedup(pe_insts)
        all_keys = [i["instrument_key"] for i in ce_insts + pe_insts]
        quotes   = get_full_quote(client, *all_keys)
        bar.empty()

        ce_oi = {i["strike_price"]: ov(quotes.get(i["instrument_key"])) for i in ce_insts}
        pe_oi = {i["strike_price"]: ov(quotes.get(i["instrument_key"])) for i in pe_insts}
        all_s  = sorted(set(list(ce_oi) + list(pe_oi)))

        pain = {}
        for candidate in all_s:
            pain[candidate] = (
                sum(max(0, candidate - s) * (o or 0) for s, o in ce_oi.items()) +
                sum(max(0, s - candidate) * (o or 0) for s, o in pe_oi.items())
            )

        max_pain_strike = min(pain, key=pain.get)
        st.metric("🎯 Max Pain Strike", f"₹{max_pain_strike:,.0f}")

        df = pd.DataFrame([{
            "Strike":     s,
            "CE OI":      ce_oi.get(s, 0),
            "PE OI":      pe_oi.get(s, 0),
            "Pain Value": pain.get(s, 0),
            "":           "🎯 MAX PAIN" if s == max_pain_strike else "",
        } for s in reversed(all_s)])

        fig = px.bar(df.sort_values("Strike"), x="Strike", y="Pain Value",
                     title="Pain Value by Strike (lower = max pain)",
                     color="Pain Value", color_continuous_scale="RdYlGn_r")
        fig.add_vline(x=max_pain_strike, line_dash="dash", line_color="red",
                      annotation_text="Max Pain")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)
        st.caption("Interpretation: underlying tends to gravitate toward max pain at expiry.")


elif example == "OI Skew":
    client = require_client()
    c1, c2, c3   = st.columns(3)
    query        = c1.text_input("Underlying", value="NIFTY")
    expiry       = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    strikes_each = c3.number_input("Strikes each side", 3, 12, 7)

    if st.button("▶ Analyse OI Skew", type="primary"):
        bar = st.progress(0)
        ce_insts, pe_insts = [], []
        total = strikes_each * 2 + 1

        for i, offset in enumerate(range(-strikes_each, strikes_each + 1)):
            for itype, store in [("CE", ce_insts), ("PE", pe_insts)]:
                resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                         instrument_types=itype, expiry=expiry,
                                         atm_offset=offset, records=1)
                d = resp.data or []
                if d: store.append(d[0])
            bar.progress((i + 1) / total)

        def dedup(insts):
            seen, unique = set(), []
            for inst in insts:
                k = inst.get("strike_price", 0)
                if k not in seen: seen.add(k); unique.append(inst)
            return unique

        ce_insts = dedup(ce_insts); pe_insts = dedup(pe_insts)
        all_keys = [i["instrument_key"] for i in ce_insts + pe_insts]
        quotes   = get_full_quote(client, *all_keys)
        bar.empty()

        ce_oi = {i["strike_price"]: ov(quotes.get(i["instrument_key"])) for i in ce_insts}
        pe_oi = {i["strike_price"]: ov(quotes.get(i["instrument_key"])) for i in pe_insts}
        all_s  = sorted(set(list(ce_oi) + list(pe_oi)))

        total_ce = sum(ce_oi.values()); total_pe = sum(pe_oi.values())
        pcr      = total_pe / total_ce if total_ce else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total CE OI", f"{total_ce:,.0f}")
        c2.metric("Total PE OI", f"{total_pe:,.0f}")
        c3.metric("Overall PCR", f"{pcr:.2f}", ">1.2 bullish | <0.8 bearish")

        df = pd.DataFrame([{
            "Strike": s,
            "CE OI":  ce_oi.get(s, 0),
            "PE OI":  pe_oi.get(s, 0),
            "PCR":    round(pe_oi.get(s, 0) / ce_oi.get(s, 1), 2) if ce_oi.get(s) else 0,
        } for s in all_s])

        fig = go.Figure()
        fig.add_trace(go.Bar(name="CE OI", x=df["Strike"].astype(str), y=df["CE OI"], marker_color="#e74c3c"))
        fig.add_trace(go.Bar(name="PE OI", x=df["Strike"].astype(str), y=df["PE OI"], marker_color="#27ae60"))
        fig.update_layout(barmode="group", title="CE vs PE Open Interest by Strike")
        st.plotly_chart(fig, use_container_width=True)

        max_ce = max(ce_oi, key=ce_oi.get) if ce_oi else 0
        max_pe = max(pe_oi, key=pe_oi.get) if pe_oi else 0
        c1, c2 = st.columns(2)
        c1.error(f"🔴 Key Resistance (max CE OI): **{max_ce:,.0f}**")
        c2.success(f"🟢 Key Support (max PE OI): **{max_pe:,.0f}**")

        if pcr > 1.2:
            st.success("📈 Heavy put writing — bullish bias.")
        elif pcr < 0.8:
            st.error("📉 Heavy call writing — bearish bias.")
        else:
            st.info("⚖️ Balanced OI — no strong directional bias.")

        st.dataframe(df, use_container_width=True)


elif example == "Volatility Skew":
    client = require_client()
    c1, c2, c3 = st.columns(3)
    query  = c1.text_input("Underlying", value="NIFTY")
    expiry = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    depth  = c3.number_input("OTM depth (strikes)", 1, 10, 4)

    if st.button("▶ Analyse Skew", type="primary"):
        with st.spinner("Fetching options…"):
            atm_ce = fetch_one(client, query, expiry, "CE", 0)
            atm_pe = fetch_one(client, query, expiry, "PE", 0)
            rows, all_keys = [], []
            if atm_ce: all_keys.append(atm_ce["instrument_key"])
            if atm_pe: all_keys.append(atm_pe["instrument_key"])
            for offset in range(1, depth + 1):
                ce = fetch_one(client, query, expiry, "CE", +offset)
                pe = fetch_one(client, query, expiry, "PE", -offset)
                if ce and pe:
                    rows.append((offset, ce, pe))
                    all_keys += [ce["instrument_key"], pe["instrument_key"]]

        if not all_keys:
            st.error("No data found.")
            st.stop()

        data = get_ltp(client, *all_keys)

        def price(inst):
            return lv(data.get(inst["instrument_key"])) if inst else 0.0

        atm_ce_p  = price(atm_ce)
        atm_pe_p  = price(atm_pe)
        atm_strike = atm_ce.get("strike_price", 0) if atm_ce else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("ATM Strike", f"₹{atm_strike:,.0f}")
        c2.metric("ATM CE",     f"₹{atm_ce_p:.2f}")
        c3.metric("ATM Skew (PE/CE)", f"{atm_pe_p/atm_ce_p:.3f}" if atm_ce_p else "N/A")

        chart = []
        for offset, ce, pe in rows:
            ce_p  = price(ce); pe_p = price(pe)
            ratio = pe_p / ce_p if ce_p else 0
            chart.append({
                "OTM Offset": f"+{offset}/-{offset}",
                "CE Strike":  ce.get("strike_price", 0),
                "CE LTP":     ce_p,
                "PE Strike":  pe.get("strike_price", 0),
                "PE LTP":     pe_p,
                "PE/CE Ratio": ratio,
            })

        if chart:
            cdf = pd.DataFrame(chart)
            fig = px.line(cdf, x="OTM Offset", y="PE/CE Ratio", markers=True,
                          title="Volatility Skew — PE/CE ratio at equal OTM distance")
            fig.add_hline(y=1.0, line_dash="dash", annotation_text="Parity (ratio = 1)")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(cdf, use_container_width=True)
            st.caption("Ratio > 1 → OTM puts premium over equidistant calls. Normal for equity/index (negative skew).")


elif example == "Gamma Exposure":
    client = require_client()
    c1, c2, c3, c4 = st.columns(4)
    query        = c1.text_input("Underlying", value="NIFTY")
    expiry       = c2.selectbox("Expiry", ["current_month", "current_week", "next_month"])
    strikes_each = c3.number_input("Strikes each side", 3, 12, 8)
    dte_est      = c4.number_input("Est. DTE for gamma calc", 1, 60, 15)

    if st.button("▶ Estimate GEX", type="primary"):
        bar = st.progress(0)
        ce_insts, pe_insts = [], []
        total = strikes_each * 2 + 1

        for i, offset in enumerate(range(-strikes_each, strikes_each + 1)):
            for itype, store in [("CE", ce_insts), ("PE", pe_insts)]:
                resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                         instrument_types=itype, expiry=expiry,
                                         atm_offset=offset, records=1)
                d = resp.data or []
                if d: store.append(d[0])
            bar.progress((i + 1) / total)

        def dedup(insts):
            seen, unique = set(), []
            for inst in insts:
                k = inst.get("strike_price", 0)
                if k not in seen: seen.add(k); unique.append(inst)
            return unique

        ce_insts = dedup(ce_insts); pe_insts = dedup(pe_insts)
        all_keys = [i["instrument_key"] for i in ce_insts + pe_insts]
        quotes   = get_full_quote(client, *all_keys)
        bar.empty()

        atm_resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                     instrument_types="CE", expiry=expiry, atm_offset=0, records=1)
        spot     = (atm_resp.data or [{}])[0].get("strike_price", 22000)
        lot      = ce_insts[0].get("lot_size", 50) if ce_insts else 50
        t        = max(dte_est / 365, 0.001)
        iv       = 0.15

        ce_oi = {i["strike_price"]: ov(quotes.get(i["instrument_key"])) for i in ce_insts}
        pe_oi = {i["strike_price"]: ov(quotes.get(i["instrument_key"])) for i in pe_insts}

        gex_rows = []
        for strike in sorted(set(list(ce_oi) + list(pe_oi))):
            c_oi  = ce_oi.get(strike, 0) or 0
            p_oi  = pe_oi.get(strike, 0) or 0
            d1    = (math.log(spot / strike) + 0.5 * iv**2 * t) / (iv * math.sqrt(t)) if strike > 0 else 0
            gamma = (math.exp(-0.5 * d1**2) / (math.sqrt(2 * math.pi) * spot * iv * math.sqrt(t))
                     if (spot > 0 and t > 0) else 0)
            gex   = (c_oi - p_oi) * lot * spot * gamma
            gex_rows.append({"Strike": strike, "CE OI": c_oi, "PE OI": p_oi, "GEX": gex})

        df        = pd.DataFrame(gex_rows)
        total_gex = df["GEX"].sum()

        label = "🟢 Positive — dealers dampen volatility" if total_gex > 0 else "🔴 Negative — dealers may amplify moves"
        st.metric("Net Dealer GEX (proxy)", f"{total_gex:+,.0f}", label)

        colors = ["#27ae60" if v > 0 else "#e74c3c" for v in df["GEX"]]
        fig = go.Figure(go.Bar(x=df["Strike"].astype(str), y=df["GEX"],
                               marker_color=colors, name="GEX"))
        fig.update_layout(title="Estimated Dealer Gamma Exposure by Strike",
                          xaxis_title="Strike", yaxis_title="GEX (proxy)")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)
        st.caption("GEX uses simplified Black-Scholes gamma with IV=15%. For approximate direction only.")


# ═════════════════════════════════════════════════════════════════════════════
# ⚖️ ARBITRAGE
# ═════════════════════════════════════════════════════════════════════════════

elif example == "NSE / BSE Arbitrage":
    client = require_client()
    query = st.text_input("Stock symbol", value="RELIANCE")

    if st.button("▶ Check Arbitrage", type="primary"):
        def find_eq(exchange):
            resp  = search_instrument(client, query, exchanges=exchange, segments="EQ", records=5)
            insts = resp.data or []
            for i in insts:
                sym = i.get("trading_symbol", "")
                if query.upper() == sym.upper() or query.upper() == sym.upper().split("-")[0]:
                    return i
            return insts[0] if insts else None

        with st.spinner("Scanning NSE and BSE…"):
            nse = find_eq("NSE")
            bse = find_eq("BSE")

        if not nse: st.error(f"'{query}' not found on NSE."); st.stop()
        if not bse: st.error(f"'{query}' not found on BSE."); st.stop()

        data    = get_ltp(client, nse["instrument_key"], bse["instrument_key"])
        nse_ltp = lv(data.get(nse["instrument_key"]))
        bse_ltp = lv(data.get(bse["instrument_key"]))
        nse_vol = vv(data.get(nse["instrument_key"]))
        bse_vol = vv(data.get(bse["instrument_key"]))
        spread  = nse_ltp - bse_ltp
        spr_pct = (spread / bse_ltp * 100) if bse_ltp else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("NSE LTP", f"₹{nse_ltp:,.2f}", f"Vol: {nse_vol:,}")
        c2.metric("BSE LTP", f"₹{bse_ltp:,.2f}", f"Vol: {bse_vol:,}")
        c3.metric("Spread (NSE−BSE)", f"₹{spread:+.2f}", f"{spr_pct:+.4f}%")

        st.divider()
        if abs(spread) < 0.05:
            st.success("✅ Prices at parity — no arbitrage opportunity.")
        elif spread > 0:
            st.warning(f"⚠️ NSE at premium. Theoretical: Buy BSE, Sell NSE. Verify spread > transaction costs.")
        else:
            st.warning(f"⚠️ BSE at premium. Theoretical: Buy NSE, Sell BSE. Verify spread > transaction costs.")

        st.dataframe(pd.DataFrame([
            {"Exchange": "NSE", "Symbol": nse.get("trading_symbol"), "LTP": nse_ltp, "Volume": nse_vol},
            {"Exchange": "BSE", "Symbol": bse.get("trading_symbol"), "LTP": bse_ltp, "Volume": bse_vol},
        ]), use_container_width=True)


elif example == "ETF vs Index":
    client = require_client()
    ETFs = {
        "NIFTY BeES (NIFTYBEES)":  ("NIFTYBEES", "NIFTY 50"),
        "BankBees (BANKBEES)":     ("BANKBEES",  "NIFTY BANK"),
        "JuniorBees (JUNIORBEES)": ("JUNIORBEES","NIFTY NEXT 50"),
    }
    choice           = st.selectbox("ETF", list(ETFs.keys()))
    etf_sym, idx_q   = ETFs[choice]

    if st.button("▶ Compare", type="primary"):
        with st.spinner("Fetching ETF and index prices…"):
            etf_resp  = search_instrument(client, etf_sym,  exchanges="NSE", segments="EQ",    records=3)
            idx_resp  = search_instrument(client, idx_q,    exchanges="NSE", segments="INDEX",
                                          instrument_types="INDEX", records=3)
            etf_inst  = (etf_resp.data or [None])[0]
            idx_inst  = (idx_resp.data or [None])[0]

        if not etf_inst: st.error(f"ETF '{etf_sym}' not found."); st.stop()
        if not idx_inst: st.error(f"Index '{idx_q}' not found."); st.stop()

        data     = get_ltp(client, etf_inst["instrument_key"], idx_inst["instrument_key"])
        etf_ltp  = lv(data.get(etf_inst["instrument_key"]))
        idx_ltp  = lv(data.get(idx_inst["instrument_key"]))
        nav_prx  = idx_ltp / 100          # most NSE ETFs track 1/100 of the index
        premium  = etf_ltp - nav_prx
        prm_pct  = (premium / nav_prx * 100) if nav_prx else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("ETF LTP",       f"₹{etf_ltp:,.2f}")
        c2.metric("NAV Proxy",     f"₹{nav_prx:,.2f}", f"Index: {idx_ltp:,.2f}")
        c3.metric("Premium/Disc.", f"₹{premium:+.2f}", f"{prm_pct:+.4f}%")

        st.divider()
        if abs(prm_pct) < 0.1:
            st.success("✅ ETF trading near NAV — no significant arbitrage.")
        elif premium > 0:
            st.warning(f"⚠️ ETF at premium ({prm_pct:+.2f}%). Arb: Short ETF + Buy index basket.")
        else:
            st.info(f"📉 ETF at discount ({prm_pct:+.2f}%). Arb: Buy ETF + Short index futures.")
        st.caption("NAV proxy = Index / 100. Actual intraday NAV from AMC may differ slightly.")


elif example == "Currency Futures Spread":
    client = require_client()
    pair = st.selectbox("Currency pair", ["USDINR", "EURINR", "GBPINR", "JPYINR"])

    if st.button("▶ Run", type="primary"):
        with st.spinner("Fetching currency futures…"):
            futures = get_futures_sorted(client, pair, exchange="NSE", exact_symbol=True)
            if not futures:
                futures = get_futures_sorted(client, pair, exchange="BSE", exact_symbol=True)

        if len(futures) < 2:
            st.error(f"Need at least 2 contracts for '{pair}'.")
            st.stop()

        near, far  = futures[0], futures[1]
        data       = get_ltp(client, near["instrument_key"], far["instrument_key"])
        near_ltp   = lv(data.get(near["instrument_key"]))
        far_ltp    = lv(data.get(far["instrument_key"]))
        spread     = far_ltp - near_ltp

        c1, c2, c3 = st.columns(3)
        c1.metric("Near Month", f"₹{near_ltp:.4f}", near["expiry"])
        c2.metric("Far Month",  f"₹{far_ltp:.4f}",  far["expiry"])
        c3.metric("Spread",     f"₹{spread:+.4f}")

        st.dataframe(pd.DataFrame([
            {"Contract": near["trading_symbol"], "Expiry": near["expiry"], "LTP": near_ltp},
            {"Contract": far["trading_symbol"],  "Expiry": far["expiry"],  "LTP": far_ltp},
        ]), use_container_width=True)
        st.caption("Currency spread reflects interest rate differential (covered interest parity).")


# ═════════════════════════════════════════════════════════════════════════════
# 📉 HISTORICAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════

elif example == "Historical Candles":
    client = require_client()
    c1, c2 = st.columns(2)
    instr_key = c1.text_input("Instrument Key", value="NSE_EQ|INE002A01018",
                               help="e.g. NSE_EQ|INE002A01018 (RELIANCE)")
    interval  = c2.selectbox("Interval", ["1day", "1week", "1month",
                                          "30minute", "15minute", "5minute", "1minute"])
    unit_map  = {"1day": ("days", 1), "1week": ("weeks", 1), "1month": ("months", 1),
                 "30minute": ("minutes", 30), "15minute": ("minutes", 15),
                 "5minute": ("minutes", 5),   "1minute":  ("minutes", 1)}
    unit, num = unit_map[interval]

    today     = date.today()
    c1, c2    = st.columns(2)
    from_date = c1.date_input("From", value=today - timedelta(days=365))
    to_date   = c2.date_input("To",   value=today)

    if st.button("▶ Fetch Candles", type="primary"):
        with st.spinner("Fetching historical data…"):
            candles = get_historical_candles(client, instr_key, unit, num, str(to_date), str(from_date))
        if not candles:
            st.warning("No candles returned.")
            st.stop()

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume", "oi"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        st.success(f"Fetched {len(df)} candles")
        fig = go.Figure(go.Candlestick(
            x=df["timestamp"], open=df["open"], high=df["high"],
            low=df["low"],     close=df["close"],
        ))
        fig.update_layout(title=f"OHLC — {instr_key}", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)


elif example == "Moving Average (SMA)":
    client = require_client()
    c1, c2, c3 = st.columns(3)
    instr_key  = c1.text_input("Instrument Key", value="NSE_EQ|INE002A01018")
    sma_fast   = c2.number_input("Fast SMA (days)", 5, 100, 20)
    sma_slow   = c3.number_input("Slow SMA (days)", 10, 200, 50)

    today     = date.today()
    from_date = today - timedelta(days=400)

    if st.button("▶ Plot Moving Averages", type="primary"):
        with st.spinner("Fetching data…"):
            candles = get_historical_candles(client, instr_key, "days", 1, str(today), str(from_date))
        if not candles:
            st.warning("No data."); st.stop()

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume", "oi"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        df[f"SMA{sma_fast}"] = df["close"].rolling(sma_fast).mean()
        df[f"SMA{sma_slow}"] = df["close"].rolling(sma_slow).mean()
        df["signal"]    = np.where(df[f"SMA{sma_fast}"] > df[f"SMA{sma_slow}"], 1, 0)
        df["crossover"] = df["signal"].diff()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["close"],
                                  name="Close", line=dict(color="grey", width=1)))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df[f"SMA{sma_fast}"],
                                  name=f"SMA{sma_fast}", line=dict(color="#3498db")))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df[f"SMA{sma_slow}"],
                                  name=f"SMA{sma_slow}", line=dict(color="#e67e22")))

        buys  = df[df["crossover"] == 1]
        sells = df[df["crossover"] == -1]
        fig.add_trace(go.Scatter(x=buys["timestamp"],  y=buys[f"SMA{sma_fast}"],
                                  mode="markers", name="Bullish Cross",
                                  marker=dict(symbol="triangle-up", size=12, color="green")))
        fig.add_trace(go.Scatter(x=sells["timestamp"], y=sells[f"SMA{sma_fast}"],
                                  mode="markers", name="Bearish Cross",
                                  marker=dict(symbol="triangle-down", size=12, color="red")))
        fig.update_layout(title=f"SMA Crossover — {instr_key}")
        st.plotly_chart(fig, use_container_width=True)

        signal_now = "📈 Bullish (fast > slow)" if df["signal"].iloc[-1] == 1 else "📉 Bearish (fast < slow)"
        st.info(f"Current signal: {signal_now}")
        c1, c2 = st.columns(2)
        c1.metric(f"SMA{sma_fast}", f"₹{df[f'SMA{sma_fast}'].iloc[-1]:,.2f}")
        c2.metric(f"SMA{sma_slow}", f"₹{df[f'SMA{sma_slow}'].iloc[-1]:,.2f}")


elif example == "Historical Volatility":
    client = require_client()
    c1, c2    = st.columns(2)
    instr_key = c1.text_input("Instrument Key", value="NSE_EQ|INE002A01018")
    window    = c2.number_input("Rolling window (days)", 5, 90, 30)

    today     = date.today()
    from_date = today - timedelta(days=400)

    if st.button("▶ Calculate HV", type="primary"):
        with st.spinner("Fetching data…"):
            candles = get_historical_candles(client, instr_key, "days", 1, str(today), str(from_date))
        if not candles:
            st.warning("No data."); st.stop()

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume", "oi"])
        df["timestamp"]  = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        df["log_return"] = np.log(df["close"] / df["close"].shift(1))
        df["hv"]         = df["log_return"].rolling(window).std() * math.sqrt(252) * 100

        cur = df["hv"].iloc[-1]; avg = df["hv"].mean()
        mx  = df["hv"].max();    mn  = df["hv"].dropna().min()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"{window}D HV (now)", f"{cur:.1f}%")
        c2.metric("1Y Average HV",       f"{avg:.1f}%")
        c3.metric("1Y High HV",          f"{mx:.1f}%")
        c4.metric("1Y Low HV",           f"{mn:.1f}%")

        fig = go.Figure(go.Scatter(x=df["timestamp"], y=df["hv"],
                                    name=f"{window}D HV", fill="tozeroy",
                                    line=dict(color="#9b59b6")))
        fig.add_hline(y=avg, line_dash="dash", line_color="orange",
                      annotation_text=f"Avg {avg:.1f}%")
        fig.update_layout(title=f"{window}-Day Historical Volatility (Annualised) — {instr_key}",
                          yaxis_title="HV (%)")
        st.plotly_chart(fig, use_container_width=True)


elif example == "52-Week High / Low":
    client    = require_client()
    instr_key = st.text_input("Instrument Key", value="NSE_EQ|INE002A01018")

    if st.button("▶ Fetch 52-Week Range", type="primary"):
        today     = date.today()
        from_date = today - timedelta(days=365)

        with st.spinner("Fetching data…"):
            candles  = get_historical_candles(client, instr_key, "days", 1, str(today), str(from_date))
            ltp_data = get_ltp(client, instr_key)

        if not candles:
            st.warning("No data."); st.stop()

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume", "oi"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        high_52 = df["high"].max()
        low_52  = df["low"].min()
        cur     = lv(ltp_data.get(instr_key)) or df["close"].iloc[-1]
        pct_h   = (cur - high_52) / high_52 * 100
        pct_l   = (cur - low_52)  / low_52  * 100
        rng_pct = (cur - low_52) / (high_52 - low_52) * 100 if high_52 != low_52 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Current LTP",   f"₹{cur:,.2f}")
        c2.metric("52-Week High",  f"₹{high_52:,.2f}", f"{pct_h:+.1f}% from high")
        c3.metric("52-Week Low",   f"₹{low_52:,.2f}",  f"{pct_l:+.1f}% from low")

        st.progress(rng_pct / 100, text=f"Position in 52W range: {rng_pct:.1f}%")

        fig = go.Figure(go.Candlestick(
            x=df["timestamp"], open=df["open"], high=df["high"],
            low=df["low"],     close=df["close"],
        ))
        fig.add_hline(y=high_52, line_dash="dot", line_color="green",
                      annotation_text=f"52W High ₹{high_52:,.2f}")
        fig.add_hline(y=low_52,  line_dash="dot", line_color="red",
                      annotation_text=f"52W Low ₹{low_52:,.2f}")
        fig.update_layout(title=f"52-Week Range — {instr_key}")
        st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# 🗂️ PORTFOLIO & SCREENING
# ═════════════════════════════════════════════════════════════════════════════

elif example == "Sector Index Comparison":
    client = require_client()
    INDICES = {
        "Nifty 50":      "NSE_INDEX|Nifty 50",
        "Nifty Bank":    "NSE_INDEX|Nifty Bank",
        "Nifty IT":      "NSE_INDEX|Nifty IT",
        "Nifty Pharma":  "NSE_INDEX|Nifty Pharma",
        "Nifty Auto":    "NSE_INDEX|Nifty Auto",
        "Nifty FMCG":    "NSE_INDEX|Nifty FMCG",
        "Nifty Metal":   "NSE_INDEX|Nifty Metal",
        "Nifty Realty":  "NSE_INDEX|Nifty Realty",
        "Nifty Energy":  "NSE_INDEX|Nifty Energy",
        "Nifty Infra":   "NSE_INDEX|Nifty Infra",
    }
    selected = st.multiselect(
        "Select indices", list(INDICES.keys()),
        default=["Nifty 50", "Nifty Bank", "Nifty IT", "Nifty Pharma", "Nifty Auto"],
    )

    if st.button("▶ Compare Sectors", type="primary"):
        keys = [INDICES[s] for s in selected]
        with st.spinner("Fetching index prices…"):
            data = get_ltp(client, *keys)

        rows = []
        for name in selected:
            key = INDICES[name]
            q   = data.get(key)
            if q:
                ltp_price = lv(q); cp_price = cv(q)
                chg     = ltp_price - cp_price
                chg_pct = (chg / cp_price * 100) if cp_price else 0
                rows.append({"Index": name, "LTP": ltp_price, "Prev Close": cp_price,
                              "Change": chg, "Change %": chg_pct})

        df = pd.DataFrame(rows).sort_values("Change %", ascending=False)

        fig = px.bar(df, x="Index", y="Change %", color="Change %",
                     color_continuous_scale=["#e74c3c", "#f9f0a0", "#27ae60"],
                     title="Sector Performance — Day Change %")
        fig.add_hline(y=0, line_color="black", line_width=1)
        st.plotly_chart(fig, use_container_width=True)

        def color_chg(val):
            c = "green" if val > 0 else ("red" if val < 0 else "grey")
            return f"color: {c}; font-weight: bold"

        st.dataframe(df.style.applymap(color_chg, subset=["Change", "Change %"]),
                     use_container_width=True)


elif example == "Top Volume Stocks":
    client = require_client()
    c1, c2 = st.columns(2)
    query  = c1.text_input("Search query", value="NIFTY",
                            help="Pulls matching equity instruments and ranks by volume")
    exch   = c2.selectbox("Exchange", ["NSE", "BSE"])

    if st.button("▶ Screen by Volume", type="primary"):
        with st.spinner("Searching…"):
            resp  = search_instrument(client, query, exchanges=exch, segments="EQ", records=20)
        insts = resp.data or []
        if not insts:
            st.warning(f"No instruments found for '{query}'."); st.stop()

        keys = [i["instrument_key"] for i in insts]
        with st.spinner("Fetching market data…"):
            data = get_ltp(client, *keys)

        rows = []
        for inst in insts:
            key = inst["instrument_key"]
            q   = data.get(key)
            if q:
                ltp_price = lv(q); cp_price = cv(q)
                rows.append({
                    "Symbol":   inst.get("trading_symbol", ""),
                    "Name":     inst.get("name", ""),
                    "LTP":      ltp_price,
                    "Prev Close": cp_price,
                    "Volume":   vv(q),
                    "Change %": (ltp_price - cp_price) / cp_price * 100 if cp_price else 0,
                })

        df = pd.DataFrame(rows).sort_values("Volume", ascending=False)
        fig = px.bar(df.head(10), x="Symbol", y="Volume", color="Change %",
                     color_continuous_scale=["#e74c3c", "#f9f0a0", "#27ae60"],
                     title="Top 10 by Volume")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)


elif example == "Futures OI Buildup":
    client = require_client()
    c1, c2 = st.columns(2)
    query  = c1.text_input("Search query", value="NIFTY")
    exch   = c2.selectbox("Exchange", ["NSE", "BSE", "MCX"])

    if st.button("▶ Analyse OI Buildup", type="primary"):
        with st.spinner("Searching futures…"):
            futures = get_futures_sorted(client, query, exchange=exch, exact_symbol=False)
        if not futures:
            st.warning(f"No futures found for '{query}'."); st.stop()

        keys = [f["instrument_key"] for f in futures]
        with st.spinner("Fetching full quotes…"):
            quotes = get_full_quote(client, *keys)

        rows = []
        for fut in futures:
            key = fut["instrument_key"]
            q   = quotes.get(key)
            if q:
                _, _, _, close_p = ohlc(q)
                rows.append({
                    "Symbol":    fut.get("trading_symbol", ""),
                    "Expiry":    fut.get("expiry", ""),
                    "LTP":       lv(q),
                    "Prev Close": close_p,
                    "OI":        ov(q),
                    "Volume":    vv(q),
                    "Lot Size":  fut.get("lot_size", 1),
                    "OI × Lot":  ov(q) * fut.get("lot_size", 1),
                })

        df = pd.DataFrame(rows).sort_values("OI", ascending=False)

        fig = px.bar(df, x="Symbol", y="OI", color="Volume",
                     title="Futures Open Interest Buildup",
                     labels={"OI": "Open Interest"})
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)
        st.caption("High OI + high volume → trend confirmation. High OI + low volume → unwinding signal.")

# ═════════════════════════════════════════════════════════════════════════════
# 📊 OPTIONS ANALYTICS (new)
# ═════════════════════════════════════════════════════════════════════════════

elif example == "Option Chain (Native)":
    client = require_client()

    INDEX_KEYS_OC = {
        "NIFTY":     "NSE_INDEX|Nifty 50",
        "BANKNIFTY": "NSE_INDEX|Nifty Bank",
        "FINNIFTY":  "NSE_INDEX|Nifty Fin Service",
        "SENSEX":    "BSE_INDEX|SENSEX",
        "BANKEX":    "BSE_INDEX|BANKEX",
    }

    c1, c2 = st.columns(2)
    underlying = c1.selectbox("Underlying", list(INDEX_KEYS_OC.keys()))
    expiry_input = c2.text_input("Expiry date (YYYY-MM-DD)", value="",
                                  placeholder="leave blank for nearest")

    if st.button("▶ Fetch Chain", type="primary"):
        und_key = INDEX_KEYS_OC[underlying]

        # Resolve nearest expiry if not specified
        expiry_date = expiry_input.strip()
        if not expiry_date:
            with st.spinner("Finding nearest expiry…"):
                exch = "BSE" if underlying in ("SENSEX", "BANKEX") else "NSE"
                resp = search_instrument(client, underlying,
                                         exchanges=exch, segments="FO",
                                         instrument_types="CE",
                                         expiry="current_month", records=1)
                data = resp.data or []
                expiry_date = data[0].get("expiry", "") if data else ""

        if not expiry_date:
            st.error("Could not determine expiry date."); st.stop()

        with st.spinner(f"Fetching option chain for {underlying} exp {expiry_date}…"):
            api  = upstox_client.OptionsApi(client)
            resp = api.get_put_call_option_chain(und_key, expiry_date)

        chain = resp.data or []
        if not chain:
            st.warning("No chain data returned."); st.stop()

        def _get(obj, *keys, default=0):
            for k in keys:
                if obj is None: return default
                obj = getattr(obj, k, None) if hasattr(obj, k) else (obj.get(k) if isinstance(obj, dict) else None)
            return obj if obj is not None else default

        rows = []
        for entry in chain:
            strike = _get(entry, "strike_price")
            ce = _get(entry, "call_options"); pe = _get(entry, "put_options")
            rows.append({
                "Strike":  strike,
                "CE OI":   _get(ce, "market_data", "oi"),
                "CE LTP":  _get(ce, "market_data", "ltp"),
                "CE IV":   round(_get(ce, "option_greeks", "iv") * 100, 1),
                "PE LTP":  _get(pe, "market_data", "ltp"),
                "PE OI":   _get(pe, "market_data", "oi"),
                "PE IV":   round(_get(pe, "option_greeks", "iv") * 100, 1),
            })

        df = pd.DataFrame(rows).sort_values("Strike")

        # Find ATM (closest to index LTP)
        ltp_resp = get_ltp(client, und_key)
        spot = lv(ltp_resp.get(und_key)) if ltp_resp else 0
        if spot:
            atm_strike = df.iloc[(df["Strike"] - spot).abs().argsort()[:1]]["Strike"].values[0]
        else:
            atm_strike = None

        total_ce_oi = df["CE OI"].sum(); total_pe_oi = df["PE OI"].sum()
        pcr = total_pe_oi / total_ce_oi if total_ce_oi else 0

        c1, c2, c3 = st.columns(3)
        if spot: c1.metric("Spot", f"₹{spot:,.2f}")
        if atm_strike: c2.metric("ATM Strike", f"₹{atm_strike:,.0f}")
        c3.metric("PCR", f"{pcr:.2f}", "≥1.2 bullish | ≤0.8 bearish")

        def highlight_atm(row):
            if atm_strike and row["Strike"] == atm_strike:
                return ["background-color: #1a3a2a"] * len(row)
            return [""] * len(row)

        st.dataframe(df.style.apply(highlight_atm, axis=1).format({
            "CE OI": "{:,.0f}", "CE LTP": "{:.2f}", "CE IV": "{:.1f}%",
            "PE LTP": "{:.2f}", "PE OI": "{:,.0f}", "PE IV": "{:.1f}%",
        }), use_container_width=True)

        sentiment = "📈 Bullish bias" if pcr >= 1.2 else ("📉 Bearish bias" if pcr <= 0.8 else "⚖️ Neutral")
        st.info(f"{sentiment} — PCR {pcr:.2f} | Expiry: {expiry_date}")


elif example == "Option Greeks":
    client = require_client()

    c1, c2, c3 = st.columns(3)
    query  = c1.text_input("Underlying", value="NIFTY")
    strikes = c2.slider("Strikes each side", 1, 8, 4)
    expiry = c3.selectbox("Expiry", ["current_month", "current_week", "next_month"])

    if st.button("▶ Fetch Greeks", type="primary"):
        bar = st.progress(0)
        ce_insts, pe_insts = [], []
        total = strikes * 2 + 1

        for i, offset in enumerate(range(-strikes, strikes + 1)):
            for itype, store in [("CE", ce_insts), ("PE", pe_insts)]:
                resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                         instrument_types=itype, expiry=expiry,
                                         atm_offset=offset, records=1)
                d = resp.data or []
                if d: store.append(d[0])
            bar.progress((i + 1) / total)
        bar.empty()

        def dedup(insts):
            seen, unique = set(), []
            for inst in insts:
                k = inst.get("strike_price", 0)
                if k not in seen: seen.add(k); unique.append(inst)
            return unique

        ce_insts = dedup(ce_insts); pe_insts = dedup(pe_insts)
        all_keys = [i["instrument_key"] for i in ce_insts + pe_insts]

        if not all_keys:
            st.error("No options found."); st.stop()

        with st.spinner("Fetching greeks…"):
            api   = upstox_client.MarketQuoteV3Api(client)
            gresp = api.get_market_quote_option_greek(instrument_key=",".join(all_keys))

        gdata = {}
        if gresp and gresp.data:
            for key, val in gresp.data.items():
                gdata[key] = val

        atm_resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                     instrument_types="CE", expiry=expiry, atm_offset=0, records=1)
        atm_strike = (atm_resp.data or [{}])[0].get("strike_price", 0)

        rows = []
        for inst in sorted(ce_insts + pe_insts, key=lambda x: (x.get("strike_price", 0), x.get("instrument_type", ""))):
            key = inst["instrument_key"]
            g   = gdata.get(key)
            def gv(attr):
                if g is None: return 0.0
                return getattr(g, attr, 0.0) or 0.0
            rows.append({
                "Strike": inst.get("strike_price", 0),
                "Type":   inst.get("instrument_type", ""),
                "LTP":    round(gv("last_price"), 2),
                "IV %":   round(gv("iv") * 100, 1),
                "Delta":  round(gv("delta"), 4),
                "Gamma":  round(gv("gamma"), 6),
                "Theta":  round(gv("theta"), 4),
                "Vega":   round(gv("vega"), 4),
                "OI":     int(gv("oi")),
            })

        df = pd.DataFrame(rows)

        def highlight_greeks(row):
            if row["Strike"] == atm_strike:
                return ["background-color: #1a2a3a"] * len(row)
            if row["Type"] == "CE":
                return ["color: #27ae60"] * len(row)
            return ["color: #e74c3c"] * len(row)

        st.dataframe(df.style.apply(highlight_greeks, axis=1).format({
            "LTP": "{:.2f}", "IV %": "{:.1f}", "Delta": "{:.4f}",
            "Gamma": "{:.6f}", "Theta": "{:.4f}", "Vega": "{:.4f}", "OI": "{:,.0f}",
        }), use_container_width=True)
        st.caption("ATM row highlighted blue · CE green · PE red")


# ═════════════════════════════════════════════════════════════════════════════
# 📡 MARKET DATA
# ═════════════════════════════════════════════════════════════════════════════

elif example == "Market Status":
    client = require_client()
    if st.button("▶ Fetch Status", type="primary"):
        api = upstox_client.MarketHolidaysAndTimingsApi(client)
        EXCHANGES = ["NSE", "BSE", "MCX", "NFO", "BFO", "CDS"]
        rows = []
        for exch in EXCHANGES:
            try:
                resp = api.get_market_status(exch)
                d    = resp.data
                rows.append({
                    "Exchange": getattr(d, "exchange", exch),
                    "Status":   getattr(d, "status", "—"),
                    "Updated":  str(getattr(d, "last_updated", "—")),
                })
            except Exception:
                rows.append({"Exchange": exch, "Status": "ERROR", "Updated": "—"})

        df = pd.DataFrame(rows)

        def colour_status(val):
            if "OPEN" in str(val).upper():   return "color: #27ae60; font-weight: bold"
            if "CLOSED" in str(val).upper(): return "color: #e74c3c; font-weight: bold"
            if "PRE" in str(val).upper():    return "color: #f39c12; font-weight: bold"
            return ""

        st.dataframe(df.style.applymap(colour_status, subset=["Status"]),
                     use_container_width=True)


elif example == "Market Holidays":
    client = require_client()
    if st.button("▶ Fetch Holidays", type="primary"):
        with st.spinner("Fetching holiday calendar…"):
            api  = upstox_client.MarketHolidaysAndTimingsApi(client)
            resp = api.get_holidays()

        holidays = resp.data or []
        today    = date.today()

        IST = timezone(timedelta(hours=5, minutes=30))

        ALL_EXCHANGES = {"NSE", "BSE", "MCX", "NFO", "BFO", "CDS", "BCD", "NSCOM"}

        def session_label(exch, start_ms, end_ms):
            try:
                end_hm = datetime.fromtimestamp(end_ms / 1000, tz=IST).strftime("%H:%M")
                start_hm = datetime.fromtimestamp(start_ms / 1000, tz=IST).strftime("%H:%M")
                if exch in ("MCX", "NSCOM"):
                    if end_hm <= "17:00": return "morning only"
                    if start_hm >= "17:00": return "evening only"
                return f"{start_hm}–{end_hm}"
            except Exception:
                return "partial"

        rows_upcoming, rows_past = [], []
        for h in holidays:
            raw_date = getattr(h, "_date", None)
            if raw_date is None: continue
            hdate  = raw_date.date() if hasattr(raw_date, "date") else raw_date
            desc   = getattr(h, "_description", "") or ""
            closed = set(getattr(h, "_closed_exchanges", None) or [])
            open_e = getattr(h, "_open_exchanges", None) or []

            partial_notes = []
            fully_open    = set()
            for e in open_e:
                exch      = getattr(e, "exchange", e.get("exchange", "")) if not isinstance(e, str) else e
                start_ms  = getattr(e, "start_time", e.get("start_time", 0)) if not isinstance(e, str) else 0
                end_ms    = getattr(e, "end_time",   e.get("end_time",   0)) if not isinstance(e, str) else 0
                label     = session_label(exch, start_ms, end_ms)
                if "only" in label or "Muhurat" in label or "muhurat" in label:
                    partial_notes.append(f"{exch}: {label}")
                else:
                    fully_open.add(exch)

            open_str    = ", ".join(sorted(fully_open)) if fully_open else "—"
            closed_str  = ", ".join(sorted(closed))     if closed     else "—"
            partial_str = " | ".join(partial_notes)     if partial_notes else ""

            delta = (hdate - today).days
            if delta < 0:
                when = f"{-delta}d ago"
            elif delta == 0:
                when = "today"
            elif delta == 1:
                when = "tomorrow"
            else:
                when = f"{delta}d ahead"

            row = {
                "Date":    str(hdate),
                "Day":     hdate.strftime("%a"),
                "Holiday": desc,
                "Open":    open_str,
                "Closed":  closed_str,
                "Partial": partial_str,
                "When":    when,
            }
            if delta >= 0:
                rows_upcoming.append(row)
            else:
                rows_past.append(row)

        tab1, tab2 = st.tabs([f"Upcoming ({len(rows_upcoming)})", f"Past ({len(rows_past)})"])
        for tab, rows in [(tab1, rows_upcoming), (tab2, sorted(rows_past, key=lambda r: r["Date"], reverse=True))]:
            with tab:
                if not rows:
                    st.info("No holidays in this period.")
                else:
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True)


elif example == "Market Timings":
    client = require_client()
    sel_date = st.date_input("Date", value=date.today())

    if st.button("▶ Fetch Timings", type="primary"):
        with st.spinner("Fetching exchange timings…"):
            api  = upstox_client.MarketHolidaysAndTimingsApi(client)
            resp = api.get_exchange_timings(str(sel_date))

        sessions = resp.data or []
        IST      = timezone(timedelta(hours=5, minutes=30))
        now_ist  = datetime.now(IST)

        rows = []
        for s in sessions:
            exch  = getattr(s, "exchange", "—")
            s_ms  = getattr(s, "start_time", 0) or 0
            e_ms  = getattr(s, "end_time",   0) or 0
            start = datetime.fromtimestamp(s_ms / 1000, tz=IST) if s_ms else None
            end   = datetime.fromtimestamp(e_ms / 1000, tz=IST) if e_ms else None

            if start and end:
                if start <= now_ist <= end:
                    status = "🟢 ACTIVE"
                elif now_ist < start:
                    status = "🔵 Upcoming"
                else:
                    status = "⚫ Closed"
                start_str = start.strftime("%H:%M")
                end_str   = end.strftime("%H:%M")
            else:
                status, start_str, end_str = "—", "—", "—"

            rows.append({
                "Exchange": exch,
                "Start":    start_str,
                "End":      end_str,
                "Status":   status,
            })

        if not rows:
            st.warning("No timing data returned for this date.")
        else:
            df = pd.DataFrame(rows).sort_values("Exchange")
            st.dataframe(df, use_container_width=True)


elif example == "Intraday Chart":
    client = require_client()

    INDEX_KEYS_IC = {
        "SENSEX":    "BSE_INDEX|SENSEX",
        "NIFTY":     "NSE_INDEX|Nifty 50",
        "BANKNIFTY": "NSE_INDEX|Nifty Bank",
        "FINNIFTY":  "NSE_INDEX|Nifty Fin Service",
        "MIDCPNIFTY":"NSE_INDEX|NIFTY MID SELECT",
    }

    c1, c2 = st.columns(2)
    query    = c1.selectbox("Instrument", list(INDEX_KEYS_IC.keys()))
    interval = c2.selectbox("Interval (minutes)", [1, 5, 15, 30, 60], index=1)

    if st.button("▶ Load Chart", type="primary"):
        inst_key = INDEX_KEYS_IC[query]
        with st.spinner(f"Fetching {interval}-min intraday candles for {query}…"):
            api  = upstox_client.HistoryV3Api(client)
            resp = api.get_intra_day_candle_data(inst_key, "minutes", interval)

        candles = resp.data.candles if resp.data else []
        if not candles:
            st.warning("No intraday candle data returned."); st.stop()

        times  = [c[0][11:16] for c in candles]  # "HH:MM"
        opens  = [float(c[1]) for c in candles]
        highs  = [float(c[2]) for c in candles]
        lows   = [float(c[3]) for c in candles]
        closes = [float(c[4]) for c in candles]
        vols   = [int(c[5])   for c in candles]
        colors = ["#27ae60" if closes[i] >= opens[i] else "#e74c3c" for i in range(len(candles))]

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=times, open=opens, high=highs, low=lows, close=closes,
            increasing_line_color="#27ae60", decreasing_line_color="#e74c3c",
            name="Price",
        ))
        fig.update_layout(
            title=f"{query} — {interval}-min intraday ({date.today()})",
            xaxis_title="Time (IST)", yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            height=450,
        )
        st.plotly_chart(fig, use_container_width=True)

        vol_fig = go.Figure()
        vol_fig.add_trace(go.Bar(x=times, y=vols, marker_color=colors, name="Volume"))
        vol_fig.update_layout(
            title="Volume", xaxis_title="Time", yaxis_title="Volume",
            template="plotly_dark", height=200,
        )
        st.plotly_chart(vol_fig, use_container_width=True)

        st.caption(f"{len(candles)} candles · {times[0]} → {times[-1]} IST")


elif example == "Live Depth (5-level)":
    client = require_client()

    st.info("WebSocket streaming is not available in the web UI. This view polls the REST API instead.")

    SENSEX_IDX    = "BSE_INDEX|SENSEX"
    NIFTY_IDX     = "NSE_INDEX|Nifty 50"
    NIFTYBANK_IDX = "NSE_INDEX|Nifty Bank"
    REL_NSE       = "NSE_EQ|INE002A01018"
    REL_BSE       = "BSE_EQ|INE002A01018"

    c1, c2 = st.columns(2)
    future     = c1.selectbox("Index future", ["NIFTY", "BANKNIFTY"])
    auto_refresh = c2.checkbox("Auto-refresh (every 3s)", value=False)

    @st.cache_data(ttl=3, show_spinner=False)
    def _resolve_futures(tok, fut_sym):
        cl = get_api_client(tok)
        nf = get_futures_sorted(cl, fut_sym, exchange="NSE", exact_symbol=True)
        sf = get_futures_sorted(cl, "SENSEX", exchange="BSE", exact_symbol=True)
        return (nf[0] if nf else None), (sf[0] if sf else None)

    nf, sf = _resolve_futures(token, future)
    if not nf or not sf:
        st.error("Could not resolve futures."); st.stop()

    def render_depth(col, label, quote):
        col.markdown(f"**{label}**")
        if quote is None:
            col.write("No data"); return
        ltp_v = lv(quote)
        cp_v  = cv(quote)
        chg   = ltp_v - cp_v
        col.metric("LTP", f"₹{ltp_v:,.2f}", f"{chg:+.2f}")
        depth = getattr(quote, "depth", None)
        if depth:
            bids = getattr(depth, "buy",  []) or []
            asks = getattr(depth, "sell", []) or []
            rows = []
            for i in range(max(len(bids), len(asks))):
                b = bids[i] if i < len(bids) else None
                a = asks[i] if i < len(asks) else None
                rows.append({
                    "Bid Qty": getattr(b, "quantity", 0) if b else 0,
                    "Bid":     getattr(b, "price",    0) if b else 0,
                    "Ask":     getattr(a, "price",    0) if a else 0,
                    "Ask Qty": getattr(a, "quantity", 0) if a else 0,
                })
            col.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            col.write("Depth not available")

    all_keys = [nf["instrument_key"], sf["instrument_key"], REL_NSE, REL_BSE]
    with st.spinner("Fetching quotes…"):
        quotes = get_full_quote(client, *all_keys)

    st.subheader("Index Futures")
    c1, c2 = st.columns(2)
    render_depth(c1, nf["trading_symbol"],  quotes.get(nf["instrument_key"]))
    render_depth(c2, sf["trading_symbol"],  quotes.get(sf["instrument_key"]))

    st.divider()
    st.subheader("RELIANCE")
    c3, c4 = st.columns(2)
    render_depth(c3, "RELIANCE NSE", quotes.get(REL_NSE))
    render_depth(c4, "RELIANCE BSE", quotes.get(REL_BSE))

    st.caption("Index banner (SENSEX / NIFTY / NIFTY BANK):")
    idx_quotes = get_ltp(client, SENSEX_IDX, NIFTY_IDX, NIFTYBANK_IDX)
    ci1, ci2, ci3 = st.columns(3)
    for col, key, name in [(ci1, SENSEX_IDX, "SENSEX"), (ci2, NIFTY_IDX, "NIFTY 50"), (ci3, NIFTYBANK_IDX, "NIFTY BANK")]:
        q = idx_quotes.get(key)
        col.metric(name, f"₹{lv(q):,.2f}", f"{lv(q) - cv(q):+.2f}" if q else "—")

    if auto_refresh:
        time.sleep(3)
        st.rerun()


elif example == "Live Depth MCX":
    client = require_client()

    st.info("WebSocket streaming is not available in the web UI. This view polls the REST API instead.")

    MCX_QUERIES = [("GOLD", "MCX_FO"), ("SILVER", "MCX_FO"), ("CRUDEOIL", "MCX_FO"), ("NATURALGAS", "MCX_FO")]

    auto_refresh = st.checkbox("Auto-refresh (every 3s)", value=False)

    @st.cache_data(ttl=60, show_spinner=False)
    def _resolve_mcx(tok):
        cl   = get_api_client(tok)
        keys, labels = [], []
        for sym, _ in MCX_QUERIES:
            resp = search_instrument(cl, sym, exchanges="MCX_FO", segments="COMM",
                                     instrument_types="FUT", expiry="current_month", records=1)
            d = resp.data or []
            if d:
                keys.append(d[0]["instrument_key"])
                labels.append(d[0].get("trading_symbol", sym))
        return keys, labels

    keys, labels = _resolve_mcx(token)
    if not keys:
        st.error("Could not resolve MCX instruments."); st.stop()

    with st.spinner("Fetching MCX quotes…"):
        quotes = get_full_quote(client, *keys)

    cols = st.columns(min(len(keys), 4))
    for i, (key, label) in enumerate(zip(keys, labels)):
        col = cols[i % 4]
        q   = quotes.get(key)
        col.markdown(f"**{label}**")
        if q:
            ltp_v = lv(q); cp_v = cv(q)
            col.metric("LTP", f"₹{ltp_v:,.2f}", f"{ltp_v - cp_v:+.2f}")
            depth = getattr(q, "depth", None)
            if depth:
                bids = getattr(depth, "buy",  []) or []
                asks = getattr(depth, "sell", []) or []
                rows = []
                for j in range(min(5, max(len(bids), len(asks)))):
                    b = bids[j] if j < len(bids) else None
                    a = asks[j] if j < len(asks) else None
                    rows.append({
                        "Bid Qty": getattr(b, "quantity", 0) if b else 0,
                        "Bid":     getattr(b, "price",    0) if b else 0,
                        "Ask":     getattr(a, "price",    0) if a else 0,
                        "Ask Qty": getattr(a, "quantity", 0) if a else 0,
                    })
                col.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            col.write("No data")

    if auto_refresh:
        time.sleep(3)
        st.rerun()


elif example == "Live Depth USDINR":
    client = require_client()

    st.info("WebSocket streaming is not available in the web UI. This view polls the REST API instead.")

    auto_refresh = st.checkbox("Auto-refresh (every 3s)", value=False)

    @st.cache_data(ttl=60, show_spinner=False)
    def _resolve_usdinr(tok):
        cl = get_api_client(tok)
        nse_resp = search_instrument(cl, "USDINR", exchanges="CDS", segments="CURR",
                                      instrument_types="FUT", expiry="current_month", records=1)
        bse_resp = search_instrument(cl, "USDINR", exchanges="BCD", segments="CURR",
                                      instrument_types="FUT", expiry="current_month", records=1)
        nse_d = (nse_resp.data or [{}])[0]
        bse_d = (bse_resp.data or [{}])[0]
        return nse_d, bse_d

    nse_inst, bse_inst = _resolve_usdinr(token)

    def render_usdinr(col, inst, exchange):
        col.markdown(f"**{inst.get('trading_symbol', 'USDINR')} ({exchange})**")
        key = inst.get("instrument_key", "")
        if not key:
            col.write("Instrument not found"); return
        q = get_full_quote(client, key).get(key)
        if q:
            ltp_v = lv(q); cp_v = cv(q)
            col.metric("LTP", f"₹{ltp_v:.4f}", f"{ltp_v - cp_v:+.4f}")
            depth = getattr(q, "depth", None)
            if depth:
                bids = getattr(depth, "buy",  []) or []
                asks = getattr(depth, "sell", []) or []
                rows = []
                for j in range(min(5, max(len(bids), len(asks)))):
                    b = bids[j] if j < len(bids) else None
                    a = asks[j] if j < len(asks) else None
                    rows.append({
                        "Bid Qty": getattr(b, "quantity", 0) if b else 0,
                        "Bid":     getattr(b, "price",    0) if b else 0,
                        "Ask":     getattr(a, "price",    0) if a else 0,
                        "Ask Qty": getattr(a, "quantity", 0) if a else 0,
                    })
                col.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            col.write("No data")

    c1, c2 = st.columns(2)
    render_usdinr(c1, nse_inst, "NSE CDS")
    render_usdinr(c2, bse_inst, "BSE BCD")

    if auto_refresh:
        time.sleep(3)
        st.rerun()


else:
    st.info(f"Example **{example}** — coming soon.")