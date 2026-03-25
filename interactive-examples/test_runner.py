#!/usr/bin/env python3
"""
Test runner for all Upstox API examples.

Usage:
    python test_runner.py
"""

import subprocess
import sys
import os

def validate_token(token):
    """Make a lightweight API call to confirm the token works. Returns (ok, message)."""
    here = os.path.dirname(os.path.abspath(__file__))
    script = "\n".join([
        "import sys",
        "sys.path.insert(0, '.')",
        "from utils import get_api_client, search_instrument",
        f"client = get_api_client({token!r})",
        "resp = search_instrument(client, 'NIFTY', exchanges='NSE', segments='EQ', records=1)",
        "sys.exit(0 if resp and resp.data is not None else 1)",
    ])
    result = subprocess.run(
        [PYTHON, "-c", script],
        cwd=here,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        return True, "Token valid."
    stderr = result.stderr
    if "401" in stderr or "Unauthorized" in stderr or "UDAPI100068" in stderr:
        return False, "Token rejected (401 Unauthorized)."
    if "403" in stderr:
        return False, "Token rejected (403 Forbidden)."
    if stderr.strip():
        return False, stderr.strip().splitlines()[-1]
    return False, "Token validation failed."

def _find_python():
    """Use venv Python if one exists in the project root, else fall back to current interpreter."""
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (
        os.path.join(here, "bin", "python3"),
        os.path.join(here, "bin", "python"),
        os.path.join(here, ".venv", "bin", "python3"),
        os.path.join(here, "venv", "bin", "python3"),
    ):
        if os.path.isfile(candidate):
            return candidate
    return sys.executable

PYTHON = _find_python()

# ── All examples in order ────────────────────────────────────────────────────

EXAMPLES = [
    # (category, script, extra_args)
    ("Instrument Search",   "instrument_search/search_equity.py",              ["--query", "RELIANCE"]),
    ("Instrument Search",   "instrument_search/search_futures.py",             ["--query", "NIFTY"]),
    ("Instrument Search",   "instrument_search/search_options.py",             ["--query", "NIFTY"]),

    ("Futures & Basis",     "futures_basis/nifty_futures_spread.py",           []),
    ("Futures & Basis",     "futures_basis/banknifty_futures_spread.py",       []),
    ("Futures & Basis",     "futures_basis/cash_futures_basis.py",             []),
    ("Futures & Basis",     "futures_basis/futures_roll_cost.py",              []),
    ("Futures & Basis",     "futures_basis/mcx_crude_spread.py",               []),

    ("Options Strategies",  "options_strategies/straddle_pricer.py",           ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/strangle_pricer.py",           ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/bull_call_spread.py",          ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/iron_condor_setup.py",         ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/butterfly_spread.py",          ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/calendar_spread_options.py",   ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/put_call_parity.py",           ["--query", "NIFTY"]),

    ("Options Analytics",   "options_analytics/options_chain_builder.py",      ["--query", "NIFTY", "--strikes", "3"]),
    ("Options Analytics",   "options_analytics/max_pain_calculator.py",        ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/oi_skew.py",                    ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/volatility_skew.py",            ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/gamma_exposure.py",             ["--query", "NIFTY"]),

    ("Arbitrage",           "arbitrage/nse_bse_arbitrage.py",                  ["--query", "RELIANCE"]),
    ("Arbitrage",           "arbitrage/etf_vs_index.py",                       []),
    ("Arbitrage",           "arbitrage/currency_futures_spread.py",            []),

    ("Historical Analysis", "historical_analysis/historical_candle.py",        ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/moving_average.py",           ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/historical_volatility.py",    ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/week_52_high_low.py",         ["--query", "RELIANCE"]),

    ("Portfolio Screening", "portfolio_screening/sector_index_comparison.py",  []),
    ("Portfolio Screening", "portfolio_screening/top_volume_stocks.py",        []),
    ("Portfolio Screening", "portfolio_screening/futures_oi_buildup.py",       []),

    ("Market Data",         "market_data/intraday_chart.py",                   ["--query", "SENSEX"]),
    ("Market Data",         "market_data/market_status.py",                    []),
    ("Market Data",         "market_data/market_holidays.py",                  []),
    ("Market Data",         "market_data/market_timings.py",                   []),
    ("Market Data",         "market_data/live_depth.py",                       []),      # streaming — auto-aborted after 5s
    ("Market Data",         "market_data/live_depth_d30.py",                   []),      # streaming — auto-aborted after 5s (Plus Pack)
    ("Market Data",         "market_data/live_depth_mcx.py",                   []),      # streaming — auto-aborted after 5s
    ("Market Data",         "market_data/live_depth_usdinr.py",                []),      # streaming — auto-aborted after 5s

    ("Options Analytics",   "options_analytics/option_chain_native.py",        ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/option_greeks.py",              ["--query", "NIFTY", "--strikes", "3"]),
    ("Options Analytics",   "options_analytics/pcr_trend.py",                  ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/iv_percentile.py",              ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/implied_move.py",               ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/expiry_decay.py",               ["--query", "NIFTY", "--strikes", "3"]),

    ("Historical Analysis", "historical_analysis/vwap.py",                     ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/beta_calculator.py",          ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/stock_correlation.py",        ["--queries", "RELIANCE,TCS,INFY"]),
]

# Scripts that run indefinitely — killed after this many seconds and counted as PASS
STREAMING_SCRIPTS = {
    "market_data/live_depth.py",
    "market_data/live_depth_d30.py",
    "market_data/live_depth_mcx.py",
    "market_data/live_depth_usdinr.py",
}
STREAMING_TIMEOUT = 5

# ── Helpers ───────────────────────────────────────────────────────────────────

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"

def hr(char="─", width=70):
    print(char * width)

def run_example(script, token, extra_args):
    """Run a single example script and stream output live."""
    cmd = [PYTHON, script, "--token", token] + extra_args
    is_streaming = script in STREAMING_SCRIPTS
    try:
        timeout = STREAMING_TIMEOUT if is_streaming else None
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__), timeout=timeout)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        # Streaming script ran for the full timeout window — counts as pass
        print(f"\n{DIM}  (streaming script auto-stopped after {STREAMING_TIMEOUT}s){RESET}")
        return True

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    hr("═")
    print(f"{BOLD}  Upstox API Examples — Test Runner{RESET}")
    print(f"  {len(EXAMPLES)} examples across 8 categories (including 7 new analytics scripts)")
    hr("═")
    print()

    # Ask for token
    try:
        token = input("  Paste your Upstox analytics or access token: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(0)

    if not token:
        print(f"{RED}  No token provided. Exiting.{RESET}")
        sys.exit(1)

    print(f"  Validating token...", end=" ", flush=True)
    ok, msg = validate_token(token)
    if ok:
        print(f"{GREEN}✓ {msg}{RESET}")
    else:
        print(f"{RED}✗ {msg}{RESET}")
        sys.exit(1)

    print()

    passed = []
    failed = []
    current_category = None

    for i, (category, script, extra_args) in enumerate(EXAMPLES, start=1):
        # Print category header when it changes
        if category != current_category:
            current_category = category
            print()
            print(f"{CYAN}{BOLD}  ── {category} {'─' * (50 - len(category))}{RESET}")

        # Print test header
        print()
        print(f"{BOLD}  [{i}/{len(EXAMPLES)}] {script}{RESET}")
        if extra_args:
            print(f"{DIM}  args: {' '.join(extra_args)}{RESET}")
        hr()

        # Run it
        ok = run_example(script, token, extra_args)

        if ok:
            print(f"\n{GREEN}  ✓ PASSED{RESET}")
            passed.append(script)
        else:
            print(f"\n{RED}  ✗ FAILED (exit code non-zero){RESET}")
            failed.append(script)

    # Summary
    print()
    hr("═")
    print(f"{BOLD}  Results: {GREEN}{len(passed)} passed{RESET}  {RED}{len(failed)} failed{RESET}  out of {len(passed)+len(failed)} run")
    hr("═")

    if failed:
        print(f"\n{RED}  Failed scripts:{RESET}")
        for s in failed:
            print(f"    • {s}")
        print()

if __name__ == "__main__":
    main()
